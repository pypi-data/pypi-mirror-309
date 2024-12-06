"""
Provides a server that creates a wandb sweep and provides the sweep ID to the agent.

The sweep ID is made available to the agent through a REST API with the endpoint
/api/get_sweep_id.
"""

import logging
import os
from copy import copy
from datetime import datetime
from pathlib import Path

import uvicorn
import wandb
import yaml
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from yaml import SafeLoader

from anhaltai_commons_pl_hyper.config_validation import shallow_validate_every_config
from anhaltai_commons_pl_hyper.constants import DataSplittingMode


class SweepServer:
    """
    The SweepServer creates a wandb sweep and provides the sweep ID to the agent
    through an API.

    Attributes:
        router: FastAPI router to add the API endpoints
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._sweep_id: str = ""
        self._api_prefix = "/api"
        self.router = APIRouter()

        wandb.login()
        sweep_config: dict = self.get_sweep_config()

        # resume sweep if sweep id is provided inside the sweep_config
        if "sweep_id" in sweep_config and sweep_config["sweep_id"]:
            self.resume_sweep(sweep_config)
        else:
            self.start_sweep(sweep_config)

        self.define_router_endpoints()

    def define_router_endpoints(self):
        """
        Set rest api endpoints for the FastAPI router
        """

        @self.router.get(
            self._api_prefix + "/get_sweep_id", response_class=PlainTextResponse
        )
        def get_sweep_id():
            return self._sweep_id

    def start_sweep(self, sweep_config: dict):
        """
        Start a new wandb sweep
        Args:
            sweep_config (dict): wandb sweep config
        """
        # sweep id is technically not an allowed parameter for wandb.sweep
        # so we remove it from the sweep config
        if "sweep_id" in sweep_config:
            del sweep_config["sweep_id"]
        # create a new sweep if sweep id is not given (sweep id is generated)
        self._sweep_id = wandb.sweep(sweep=sweep_config)

    def resume_sweep(self, sweep_config: dict) -> bool:
        """
        Resume an existing wandb sweep
        Args:
            sweep_config (dict): wandb sweep config

        Returns:
            bool: if the sweep was resumed
        """
        self.logger.warning(
            "WARNING: sweep_id is provided in the sweep_config. The sweep will "
            "be resumed. If you want to create a new sweep, please remove the "
            "sweep_id from the sweep_config."
        )
        self._sweep_id = sweep_config["sweep_id"]
        wandb_entity = os.getenv("WANDB_ENTITY")
        wandb_project = os.getenv("WANDB_PROJECT")
        if not wandb_entity:
            raise ValueError("WANDB_ENTITY must be set in the .env file.")
        if not wandb_project:
            raise ValueError("WANDB_PROJECT must be set in the .env file.")

        # Apparently wandb.sweep does not support the resume option
        # As a workaround, we use the wandb CLI to resume the sweep
        command = (
            f"wandb sweep --resume {wandb_entity}/{wandb_project}/{self._sweep_id}"
        )
        self.logger.info("Execute command: %s", command)
        exit_code = os.system(command)
        if exit_code == 0:
            self.logger.info("Command executed successfully:  %s", command)
            return True

        raise RuntimeError(
            f"Error {exit_code} while executing command: {command}. "
            "Please check if wandb is installed on your system interpreter and "
            "the sweep_id in your config is correct."
        )

    @staticmethod
    def add_elements_to_dict(base_dict: dict, additional_dict: dict) -> dict:
        """
        Add elements from an additional dictionary to a base dictionary

        Args:
            base_dict: Dictionary to which the elements are added
            additional_dict: Dictionary from which the elements are added

        Returns: The base dictionary with the added elements
        """
        for key in additional_dict:
            base_dict[key] = additional_dict[key]
        return base_dict

    def get_config_files(self, sweep_directory: Path) -> list[str]:
        """
        Get all yaml files in the sweep directory.

        Args:
            sweep_directory: Path to the sweep directory

        Returns: List of yaml files in the sweep directory

        """

        files = []
        for file in sweep_directory.iterdir():
            if file.is_dir():
                files.extend(self.get_config_files(file))
            elif file.name != "sweep.yaml":
                files.append(file.as_posix())

        return files

    def get_sweep_config(self) -> dict:
        """
        Get the sweep configuration from the yaml files in the sweep directory. The
        sweep configuration is created by combining the model, logging, dataset and
        sweep configuration files.

        Returns: The combined sweep configuration

        """
        sweep_directory = Path(os.getenv("SWEEP_DIRECTORY", default="configs/sweep"))
        sweep_config_path = sweep_directory / "sweep.yaml"

        config_file_names = self.get_config_files(sweep_directory)

        with open(sweep_config_path.as_posix(), encoding="utf-8") as config_file:
            sweep_config = yaml.load(config_file, Loader=SafeLoader)

        sweep_parameters: dict = {}

        for file_name in config_file_names:
            with open(file_name, encoding="utf-8") as config_file:
                sweep_parameters = self.add_elements_to_dict(
                    sweep_parameters, yaml.load(config_file, Loader=SafeLoader)
                )

        # Add the metric and start_time to the sweep parameters
        # The metric for the sweep gets the cross_validation_ prefix if cross
        # validation is active which is not necessary for the run metric since this
        # metric is for each fold.
        auto_filled_parameters = {
            "metric": {"value": copy(sweep_config["metric"])},
            "start_time": {"value": datetime.now().timestamp()},
        }

        sweep_parameters = self.add_elements_to_dict(
            sweep_parameters, auto_filled_parameters
        )

        if (
            "data_splitting_mode" in sweep_parameters
            and sweep_parameters["data_splitting_mode"]["value"]
            == DataSplittingMode.CROSS_VALIDATION
        ):
            sweep_config["metric"]["name"] = (
                "cross_validation_" + sweep_config["metric"]["name"]
            )
        sweep_config["parameters"] = sweep_parameters
        shallow_validate_every_config(sweep_config)
        return sweep_config

    def main(self, port: int = 5001):
        """
        Start sweep server
        Args:
            port (int): server port (default=5001)
        """

        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_headers=["*"],
            allow_methods=["*"],
        )

        app.include_router(self.router)
        uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    SweepServer().main()
