"""
Create a wandb agent to run the sweep.
"""

import logging
import os
import subprocess
import sys
import time

import requests
import wandb

logger = logging.getLogger(__name__.rsplit(".", maxsplit=1)[-1])


def create_agent(timeout: int = 10, retry_time: int = 10) -> None:
    """
    Create a wandb agent to start a run from the sweep. Through recursion the agent
    runs multiple available runs of the sweep one after another.
    If there are no more planned runs in the sweep then the agent stops.
    Multiple agents can run in parallel to balance the load. The sweep ID is retrieved
    from the sweep server.
    The agent runs the spawn_training_process function for each run.

    Args:
        timeout (int): timeout for requesting the sweep ID
        retry_time (int): amount of seconds the agent waits before retry the request

    """
    logger.info("initialize sweep agent")
    wandb.login()
    try:
        get_sweep_id_url = (
            os.getenv("SWEEP_SERVER_ADDRESS", default="http://localhost:5001")
            + "/api/get_sweep_id"
        )
        response: requests.Response = requests.get(get_sweep_id_url, timeout=timeout)
        sweep_id = response.text
    except requests.exceptions.RequestException as e:
        logger.error(e)
        logger.info(
            "Unable to get sweep ID. Run sweep_server.py first to create the "
            "SweepServer"
        )
        logger.info("Retry in %d seconds", retry_time)
        time.sleep(retry_time)
        create_agent()
        return

    wandb.agent(sweep_id, function=spawn_training_process, count=2)


def spawn_training_process() -> None:
    """
    Spawn the training process for the sweep run. The trainer path is retrieved from
    the environment variables. The trainer is run with the wandb run ID and project
    name as arguments.
    """

    trainer_path = os.getenv("TRAINER_PATH", default=None)
    if trainer_path is None:
        raise ValueError("TRAINER_PATH not set in .env file")

    # use the same python executable as used for this file (else it failed for my
    # Windows implementation)
    try:
        subprocess.run(
            args=[sys.executable, "-u", "-m", trainer_path, str(0)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(e)
        logger.error("Error while running the trainer")
        raise e  # Let program crash if the trainer fails


if __name__ == "__main__":
    create_agent()
