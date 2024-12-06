"""
Dataclasses for Callbacks used in the training process.
"""

from dataclasses import dataclass


@dataclass
class HuggingfaceConfig:
    """
    Huggingface configuration for the saving of the model to huggingface.

    Attributes:
        username: Username for huggingface account
        save_enabled: Flag to enable the saving of the model to huggingface
        repo_name: Name of the repository
        branch_name: Name of the branch
        repo_id: Id of the repository
    """

    username: str
    save_enabled: bool
    repo_name: str
    branch_name: str = ""
    repo_id: str = ""


@dataclass
class MetricConfig:
    """
    Metric used for the evaluation of the model.

    Attributes:
        mode: Mode of the metric (max or min)
        monitor: Monitor of the metric e.g. val_loss
    """

    mode: str
    monitor: str


@dataclass
class SaveModelConfig:
    """
    Configuration for the SaveModelCallback.

    Attributes:
        run_config: Run configuration
        huggingface_config: Huggingface configuration
        save_every_n_steps: Number of steps to save the model
        identifier: Identifier for the model
    """

    run_config: dict
    huggingface_config: HuggingfaceConfig
    save_every_n_steps: int

    identifier: str


@dataclass
class SavePaths:
    """
    Paths to save the model checkpoint and meta file.

    Attributes:
        checkpoint_path: Path to the model checkpoint
        meta_file_path: Path to the meta file. Includes the run configuration.
    """

    checkpoint_path: str
    meta_file_path: str
