"""
Dataclasses for the configuration of the training pipeline.
"""

from dataclasses import dataclass

from anhaltai_commons_pl_hyper.constants import DataSplittingMode


@dataclass
class RunMetadata:
    """
    Metadata for the run to be used for the logging and saving of the model.

    Attributes:
        run_id: Unique wandb id for the run.
        start_time: Start time of the wandb run.
        identifier: Identifier for the model. Consists of the start time and wandb
          run id
        metric_postfix: Postfix for the metric name. "_fold_{fold_id}" when
          cross validation is enabled else empty string.
    """

    run_id: str
    start_time: float
    identifier: str
    metric_postfix: str


@dataclass
class PreprocessorConfig:
    """
    Preprocessor configuration describing the preprocessor to be used for the data.

    Attributes:
        enabled: Flag to enable the preprocessor
        name: Name of the preprocessor e.g. "microsoft/resnet-50"
        type: Type of the preprocessor e.g. "huggingface"
        parameters: Additional arguments, set by "preprocessor_parameters" in the
          config
    """

    enabled: bool
    name: str | None
    type: str | None
    parameters: dict | None


@dataclass
class DataLoaderConfig:
    """
    DataLoader configuration describing the DataLoader to be used for the data.

    Attributes:
        batch_size: Batch size used for training
        num_workers: Number of workers(threads) to load data
        persistent_workers: Flag to enable persistent workers. If set to False, the
          workers are deleted and recreated after each epoch.
        pin_memory: Flag to enable pin memory. If set to True, the copying to the GPU
          memory is sped up. If your data is already in the GPU memory, you can set
          this to False.
    """

    batch_size: int
    num_workers: int
    persistent_workers: bool
    pin_memory: bool


@dataclass
class DatasetConfig:
    """
    Dataset configuration describing the dataset to be used for the training.

    Attributes:
        origin (str): Name of the origin e.g. "minio"
        path (str): Path to the dataset inside the `origin`
        data_splitting_mode (DataSplittingMode): Split mode
          (see data-splitting-documentation.md for details)
        validation_split_ratio (float): Split ratio for the validation data if no
        validation dataset
        is provided
        test_split_ratio (float): Split ratio for the test data if no test dataset
        is provided
    """

    origin: str | None
    path: str | None
    data_splitting_mode: DataSplittingMode
    validation_split_ratio: float
    test_split_ratio: float


@dataclass
class CrossValidationConfig:
    """
    CrossValidation configuration describing the cross validation to be used for the
    training.

    Attributes:
        enabled: Flag to enable cross validation
        num_folds: Number of folds
        seed: Seed for the random state of Fold splitting
        fold_id: ID of the current fold to use for the cross validation
    """

    enabled: bool
    num_folds: int
    seed: int
    fold_id: int


@dataclass
class DataIndices:
    """
    Data indices for the train and validation data.

    Attributes:
        train: Indices for the training data
        val: Indices for the validation data
    """

    train: list[int]
    val: list[int]


@dataclass
class DataModuleConfig:
    """
    DataModule configuration describing the data to be used for the training.

    Attributes:
        dataset_config: Dataset configuration to describe the dataset
        data_loader_config: DataLoader configuration to describe the DataLoader
        preprocessor_config: Preprocessor configuration to describe the preprocessor
        cross_validation_config: cross validation configuration to describe the cross
          validation
    """

    dataset_config: DatasetConfig
    data_loader_config: DataLoaderConfig
    preprocessor_config: PreprocessorConfig
    cross_validation_config: CrossValidationConfig


@dataclass
class ModelConfig:
    """
    Model configuration describing the model to be trained.

    Attributes:
        name: Name of the model e.g. "microsoft/resnet-50"
        type: Type of the model e.g. "huggingface"
        parameters: Additional arguments, set by "model_parameters" in the
          config
    """

    name: str
    type: str | None
    parameters: dict | None


@dataclass
class OptimizerConfig:
    """
    Optimizer configuration describing the optimizer to be used for the training.

    Attributes:
        name: Name of the optimizer e.g. "adam"
        parameters: Additional arguments, set by "optimizer_parameters" in the
          config
    """

    name: str | None
    parameters: dict | None


@dataclass
class LoggingConfig:
    """
    Logging configuration describing the logging to be used for the training.

    Attributes:
        save_every_n_steps: Number of steps between saving the model
        log_every_n_steps: Number of steps between logging the model during training.
          Validation and test data are logged after each epoch.
    """

    save_every_n_steps: int
    log_every_n_steps: int


@dataclass
class TrainingModuleConfig:
    """
    TrainingModule configuration describing the training module which implements the
    training logic.

    Attributes:
        model_config: Model configuration to describe the model
        optimizer_config: Optimizer configuration to describe the optimizer
        preprocessor_config: Preprocessor configuration to describe the preprocessor
        logging_config: Logging configuration to describe the logging
        run_metadata_config: RunMetadata to describe the run
    """

    model_config: ModelConfig
    optimizer_config: OptimizerConfig
    preprocessor_config: PreprocessorConfig
    logging_config: LoggingConfig
    run_metadata_config: RunMetadata


@dataclass
class TrainerConfig:
    """
    Trainer configuration describing the trainer which initializes the training.

    Attributes:
        max_epochs: Maximum number of epochs to train
        accumulate_grad_batches: Number of batches to accumulate the gradients before
          updating the weights
        accelerator: Type of the device to be used for training e.g. "gpu"
        devices: Number of devices to be used for training. If gpu is selected,
          it is ignored and all available GPUs are used.
        check_val_every_n_epoch: Number of epochs between validation checks
        checkpoint_path: Model checkpoint path to continue training from a checkpoint.
          If empty, training starts from scratch
        logging_config: Logging configuration to describe the logging
    """

    max_epochs: int
    accumulate_grad_batches: int
    accelerator: str
    devices: int
    check_val_every_n_epoch: int
    checkpoint_path: str
    logging_config: LoggingConfig
