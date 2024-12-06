"""
Callbacks to save the model both locally and to upload them to huggingface_hub.
"""

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Dict, Any
from urllib.error import HTTPError

import lightning as pl
import torch
from huggingface_hub import HfApi, CommitInfo
from huggingface_hub.utils import (
    RepositoryNotFoundError,
    RevisionNotFoundError,
    HfHubHTTPError,
)
from lightning.pytorch.utilities.rank_zero import rank_zero_only
from lightning.pytorch.utilities.types import STEP_OUTPUT

from anhaltai_commons_pl_hyper.dataclasses.callback import SavePaths, SaveModelConfig


def extract_retry_time_from_message(message: str) -> int:
    """
    Read retry time from a str message.
    Args:
        message (str): Message of a request response message or error message

    Returns:
        int: seconds

    """
    # Define regex patterns to match hours, minutes, and seconds
    hours_pattern = r"(\d+)\s*hours?"
    minutes_pattern = r"(\d+)\s*minutes?"
    seconds_pattern = r"(\d+)\s*seconds?"

    # Search for patterns in the message
    hours_match = re.search(hours_pattern, message, re.IGNORECASE)
    minutes_match = re.search(minutes_pattern, message, re.IGNORECASE)
    seconds_match = re.search(seconds_pattern, message, re.IGNORECASE)

    # Initialize time in seconds
    total_seconds = 0

    # Convert matched time to seconds
    if hours_match:
        total_seconds += int(hours_match.group(1)) * 3600
    if minutes_match:
        total_seconds += int(minutes_match.group(1)) * 60
    if seconds_match:
        total_seconds += int(seconds_match.group(1))

    return total_seconds


# It is possible to remove _huggingface_config attribute, but it would make the code
# less readable. Else logging could be removed, but it is useful for debugging.
# pylint: disable=too-many-instance-attributes
class SaveModelCallback(pl.Callback):
    """
    Callback to save the model locally and to huggingface after every n training
    steps. Set by config through save_every_n_steps.

    Attributes:
        save_every_n_steps: Number of steps to save the model
        save_paths: Paths to save the model checkpoint and meta file
        new_best_model: Flag to indicate if a new best model was found
    """

    def __init__(
        self,
        config: SaveModelConfig,
        callback_name: str,
    ):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("initialize callback")
        self._run_config = config.run_config
        self._huggingface_config = config.huggingface_config
        self.save_every_n_steps = config.save_every_n_steps

        self._wait_seconds: int = 0  # seconds to wait unit next checkpoint upload
        self._timestamp_upload: float = time.time()  # timestamp last upload try

        checkpoint_dir = (
            os.getenv("CHECKPOINT_DIRECTORY", default="models")
            + "/"
            + callback_name
            + "/"
            + config.identifier
        )
        self._create_directory(checkpoint_dir)

        checkpoint_path = checkpoint_dir + "/" + "model.ckpt"
        meta_file_path = checkpoint_dir + "/" + "meta.json"
        self.save_paths = SavePaths(checkpoint_path, meta_file_path)

        self.new_best_model = False
        self.best_model_uploaded_to_hf = False
        self.force_push_to_hf = False
        self.created_hf_repo: bool | None = False
        self.created_hf_branch: bool | None = False
        self.run_step = 0

        if self._huggingface_config.save_enabled:
            self._huggingface_config.branch_name = (
                callback_name + "-" + config.identifier.replace("/", "-")
            )

            self.created_hf_repo = self._create_hf_repo()
            # upload after wait time
            if time.time() - self._timestamp_upload >= self._wait_seconds:
                self.created_hf_branch = self._create_hf_branch()

    def _handle_upload_not_possible_exception(self, e: HfHubHTTPError):
        self.logger.error(e)
        self._wait_seconds = extract_retry_time_from_message(e.response.text)
        self.logger.error("Next upload possible in %s seconds", self._wait_seconds)

    @rank_zero_only
    def _create_hf_repo(self) -> bool:
        self._hf_api = HfApi()
        try:
            self._huggingface_config.repo_id = self._hf_api.create_repo(
                self._huggingface_config.username
                + "/"
                + self._huggingface_config.repo_name.replace("/", "-"),
                exist_ok=True,
            ).repo_id
            return True
        except HfHubHTTPError as e:
            if e.response.status_code == 429:
                self.logger.error(
                    "Failed to create a repo to upload the model "
                    "to huggingface. Too "
                    "many requests for uploading the checkpoint to "
                    "Hugging Face"
                )
                self._handle_upload_not_possible_exception(e)
            return False
        except Exception as e:
            # We decided to continue with the training in this case and can use the
            # local checkpoints after training if there are errors with Hugging Face.
            self.logger.error(
                "Unexpected Error. Failed to create a repo to upload the model to "
                "huggingface"
            )
            self.logger.error(e)
            return False

    @rank_zero_only
    def _create_hf_branch(self) -> bool:
        """
        Create branch on Hugging Face.

        Update wait time for next upload on fail due given limits.
        """
        try:
            self._hf_api.create_branch(
                repo_id=self._huggingface_config.repo_id,
                repo_type="model",
                branch=self._huggingface_config.branch_name,
                exist_ok=True,
            )
            logging.info("created HF branch %s", self._huggingface_config.branch_name)
        except HfHubHTTPError as e:
            if e.response.status_code == 429:
                self.logger.error(
                    "Failed to create a branch to upload the model "
                    "to huggingface. Too "
                    "many requests for uploading the checkpoint to "
                    "Hugging Face"
                )
                self._handle_upload_not_possible_exception(e)
                return False
        except Exception as e:
            # We decided to continue with the training in this case and can use the
            # local checkpoints after training if there are errors with Hugging Face.
            self.logger.error(
                "Unexpected Error. Failed to create a branch to upload the model to "
                "huggingface"
            )
            self.logger.error(e)
            return False
        return True

    def on_save_checkpoint(
        self,
        trainer: "pl.Trainer",
        pl_module: "pl.LightningModule",
        checkpoint: Dict[str, Any],
    ) -> None:
        """
        Save the model to the local directory and upload it to huggingface if a new best
        model was found. This method is called by every callback with each checkpoint.

        Args:
            trainer: The trainer object running the training
            pl_module: LightningModule which contains the model
            checkpoint: Describes the current state of the model

        """
        if self.new_best_model:
            self._save_model(trainer, checkpoint)
            self.best_model_uploaded_to_hf = False

        if not self.best_model_uploaded_to_hf and self._huggingface_config.save_enabled:
            # upload after wait time
            if self.force_push_to_hf:
                self._force_push_to_hub()

            # We do not wait for the time to finish since during training some time
            # passes
            elif time.time() - self._timestamp_upload >= self._wait_seconds:
                success: bool | None = self._push_to_hub()  # tries again later if it
                # fails
                if success:
                    self._timestamp_upload = time.time()
                    self._wait_seconds = 0

    def _force_push_to_hub(self):
        time_to_wait = self._wait_seconds - time.time() - self._timestamp_upload
        time.sleep(time_to_wait + 1)  # just to be sure
        success = self._push_to_hub()
        if not success:
            self._force_push_to_hub()
        self._timestamp_upload = time.time()
        self._wait_seconds = 0
        self.force_push_to_hf = False

    @rank_zero_only
    def _save_model(self, trainer: "pl.Trainer", checkpoint: Dict[str, Any]):
        """
        Save the model to the local directory and upload it to huggingface if enabled
        Args:
            trainer: The trainer object running the training
            checkpoint: Describes the current state of the model

        """
        self.new_best_model = False
        torch.save(checkpoint, self.save_paths.checkpoint_path)
        with open(self.save_paths.meta_file_path, "w", encoding="utf-8") as meta_file:
            json.dump(
                {
                    "step": trainer.global_step,
                    "epoch": trainer.current_epoch,
                    "run_config": self._run_config,
                },
                meta_file,
                indent=4,
            )

    @rank_zero_only
    def _create_directory(self, directory: str) -> None:
        """
        Create a directory if it does not exist

        Args:
            directory: Path of the directory to create
        """
        Path(directory).mkdir(parents=True, exist_ok=True)

    @rank_zero_only
    def _push_to_hub(self) -> bool:
        """
        Push the model to huggingface in the specified repository and branch of this
        callback.

        Update wait time for next upload on fail due given limits.

        Returns:
            bool: True if the model was uploaded successfully, False otherwise
        """
        self.logger.info("Uploading model to huggingface")
        model_ckpt_path: str = "model.ckpt"

        if not self.created_hf_repo:
            self.created_hf_repo = self._create_hf_repo()
            if not self.created_hf_repo:
                return False

        if not self.created_hf_branch:
            self.created_hf_branch = self._create_hf_branch()
            if not self.created_hf_branch:
                return False

        try:
            response_ckpt: CommitInfo = self._hf_api.upload_file(
                repo_id=self._huggingface_config.repo_id,
                path_in_repo=model_ckpt_path,
                revision=self._huggingface_config.branch_name,
                repo_type="model",
                path_or_fileobj=self.save_paths.checkpoint_path,
            )
            self.logger.info("uploaded %s", str(response_ckpt))

            response_meta: CommitInfo = self._hf_api.upload_file(
                repo_id=self._huggingface_config.repo_id,
                path_in_repo="meta.json",
                revision=self._huggingface_config.branch_name,
                repo_type="model",
                path_or_fileobj=self.save_paths.meta_file_path,
            )
            self.logger.info("uploaded %s", str(response_meta))
            self.best_model_uploaded_to_hf = True
        except (
            HTTPError,
            ValueError,
            RepositoryNotFoundError,
            RevisionNotFoundError,
        ) as e:
            self.logger.error("Failed to upload model to huggingface")
            self.logger.error(e)
            return False
        except HfHubHTTPError as e:
            if e.response.status_code == 429:
                self.logger.error(
                    "Failed to upload model to huggingface. Too "
                    "many requests for uploading the checkpoint to "
                    "Hugging Face"
                )
                self._handle_upload_not_possible_exception(e)
                return False
        except Exception as e:
            # We decided to continue with the training in this case and can use the
            # local checkpoints after training if there are errors with Hugging Face.
            self.logger.error(
                "Unexpected Error. Failed to upload model to huggingface."
            )
            self.logger.error(e)
            return False
        return True

    def save_checkpoint(self, trainer: "pl.Trainer") -> None:
        """
        Save the model checkpoint and meta file to the local directory and upload it to
        huggingface if enabled.
        Args:
            trainer: The trainer object running the training

        """
        self.new_best_model = True
        trainer.save_checkpoint(self.save_paths.checkpoint_path)

    def on_save_model(
        self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"
    ) -> None:
        """
        Hook to implement custom saving behavior. Use self.save_checkpoint(trainer) to
        save the model when your condition to save is met. Can be extended by
        the user.
        Args:
            trainer: The trainer object running the training
            pl_module: LightningModule which contains the model

        Returns:

        """
        self.save_checkpoint(trainer)

    # Inherited from Callback, as such we can't change the signature
    # pylint: disable=too-many-arguments
    def on_train_batch_end(
        self,
        trainer: "pl.Trainer",
        pl_module: "pl.LightningModule",
        outputs: STEP_OUTPUT,
        batch: Any,
        batch_idx: int,
    ) -> None:
        """
        Increases the run_step by one and saves the model if run_step is a multiple of
        save_every_n_steps.

        Args:
            trainer: The trainer object running the training
            pl_module: LightningModule which contains the model
            outputs: Values returned by the training step
            batch: Current batch
            batch_idx: Current batch index
        """
        self.run_step += 1
        if self.run_step % self.save_every_n_steps != 0:
            self.on_save_model(trainer, pl_module)

    def on_train_end(
        self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"
    ) -> None:
        """
        Save the model at the end of the training, if the condition to save is met.
        Args:
            trainer:
            pl_module:

        Returns:

        """
        self.force_push_to_hf = True
        self.on_save_model(trainer, pl_module)


class SaveNewestModelCallback(SaveModelCallback):
    """
    Callback to save the model to huggingface after save_every_n_steps (set by
    config) training steps

    Attributes:
        global_step: Number of the current training step
        run_step: Number of the current training step
    """

    def __init__(
        self,
        config: SaveModelConfig,
        callback_name: str,
    ):
        """
        Callback to save the model to huggingface after save_every_n_steps (set by
        config) training steps
        """
        super().__init__(config, callback_name)
        self.global_step = 0

    def on_save_model(
        self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"
    ) -> None:
        """
        Save the model if the global step is smaller than the trainer's global step.
        Args:
            trainer: The trainer object running the training
            pl_module: LightningModule which contains the model

        """

        if self.global_step < trainer.global_step:
            self.global_step = trainer.global_step
            self.save_checkpoint(trainer)


class SaveBestModelCallback(SaveModelCallback):
    """
    Saves the best model to the local directory and uploads it to huggingface.

    Attributes:
        monitor: Name of the metric to monitor
        mode: Goal of the metric (min or max)
        best_score: Best score of the model
        run_step: Number of the current training step
    """

    def __init__(
        self,
        config: SaveModelConfig,
        callback_name: str,
        monitor: str,
        mode: str,
    ):
        super().__init__(config, callback_name)

        self.monitor: str = monitor
        self.mode: str = mode

        if self.mode.startswith("min"):
            self.best_score = float("inf")
        else:
            self.best_score = -float("inf")

    def on_save_model(
        self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"
    ) -> None:

        # If the metric is not logged yet
        if self.monitor not in trainer.callback_metrics:
            return

        new_score = trainer.callback_metrics[self.monitor].item()

        if self.mode.startswith("max"):
            is_better_score = self.best_score < new_score
        else:
            is_better_score = self.best_score > new_score

        if is_better_score:
            self.best_score = trainer.callback_metrics[self.monitor].item()
            self.save_checkpoint(trainer)
