"""
Training module for the pytorch lightning trainer. The module is used for training,
validation and testing of the model.
"""

import logging
from dataclasses import dataclass
from typing import Any

import lightning as pl
import torch
from lightning.pytorch.utilities.enums import LightningEnum
from lightning.pytorch.utilities.types import _METRIC
from typing_extensions import override

from anhaltai_commons_pl_hyper.dataclasses.config import (
    TrainingModuleConfig,
    ModelConfig,
    OptimizerConfig,
)


class TrainingPrefix(LightningEnum):
    """
    Enum class for the training prefix.

    Attributes:
        TRAIN: Training prefix
        VALIDATION: Validation prefix
        TEST: Test prefix
    """

    TRAIN = "train"
    VALIDATION = "val"
    TEST = "test"


@dataclass
class TrainLogger:
    """
    Class for logging the training values.

    Attributes:
        train_values: Dictionary with the training values
        step_counter: Counter for the steps
        train_samples: Number of samples used for training
        sample_count: Number of samples used for the current batch
    """

    train_values: dict
    step_counter: int = 0
    train_samples: int = 0

    batch_sample_count: int = 0
    log_sample_count: int = 0


class TrainingModule(pl.LightningModule):
    """
    Creates a pytorch LightningModule. The module is used for training, validation and
    testing of the model.

    Args:
        config: Configuration for the training module
        run_config: Configuration for the run
        dataset_metadata: Metadata for the dataset

    Attributes:
        model: Model used for training
    """

    def __init__(
        self,
        config: TrainingModuleConfig,
        run_config: dict,
        dataset_metadata: dict,
    ):
        super().__init__()
        self.run_config = run_config

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("Initialize TrainingModule")
        self._dataset_metadata = dataset_metadata
        self._config = config
        self._current_training_prefix = TrainingPrefix.TRAIN

        self._metric_postfix = config.run_metadata_config.metric_postfix

        if self._config.logging_config.log_every_n_steps <= 0:
            raise ValueError("log_every_n_steps needs to be >1")

        if self._config.logging_config.log_every_n_steps == 1:
            self._logger.warning(
                "log_every_n_steps is set to only 1. Be careful since the last batch "
                "can be as small as a single sample making it hard to evaluate the "
                "model"
            )

        self._train_logger = TrainLogger(train_values={})
        self.model: torch.nn.Module = self.load_model(
            self._dataset_metadata, self._config.model_config
        )

        self.save_hyperparameters()

    def load_model(
        self, dataset_metadata: dict, config: ModelConfig
    ) -> torch.nn.Module:
        """
        Load the model for training. Model_type is the type set in the configuration
        file e.g. huggingface. Needs to be implemented in an extension class.

        Args:
            dataset_metadata: Metadata for the dataset
            config: Configuration for the model

        Returns: Model used for training
        """

        raise NotImplementedError(
            "This method needs to be implemented in an extension class"
        )

    # The inherited method uses *args, **kwargs as argument but usually the forward
    # function uses the input x. This is why we disable the arguments-differ check
    # pylint: disable=arguments-differ
    def forward(self, x: Any) -> torch.Tensor:
        """
        Alias for the forward function of the model. The forward function is used to
        predict the output of the model.

        :param x: Input of the model
        :return: Output of the model
        """
        return self.model.forward(x)

    @override
    def log(
        self,
        name: str,
        value: _METRIC,
        prog_bar: bool = False,
        logger: bool | None = None,
        on_step: bool | None = None,
        on_epoch: bool | None = None,
        reduce_fx: str | Any = "mean",
        enable_graph: bool = False,
        sync_dist: bool = False,
        sync_dist_group: Any | None = None,
        add_dataloader_idx: bool = True,
        batch_size: int | None = None,
        metric_attribute: str | None = None,
        rank_zero_only: bool = False,
    ) -> None:
        """
        Log the value of the metric. The name has as prefix the current training
        stage (train, val, test) and as postfix with the fold_id, if cross validation is
        enabled.

        During training the values are logged and averaged over n batches set in the
        configuration file with log_every_n_steps. During validation and testing the
        values are logged after each epoch.

        Args:
            name: Name of the metric
            value: Value of the metric
            prog_bar: Flag to show the metric in the progress bar
        """

        name = self._current_training_prefix + "_" + name + self._metric_postfix
        if self._current_training_prefix != TrainingPrefix.TRAIN:
            super().log(
                name,
                value,
                prog_bar=prog_bar,
                on_epoch=True,
                sync_dist=True,
            )

        elif name not in self._train_logger.train_values.keys():
            self._train_logger.train_values[name] = {
                "value": value * self._train_logger.batch_sample_count,
                "prog_bar": prog_bar,
            }

        else:
            self._train_logger.train_values[name]["value"] += (
                value * self._train_logger.batch_sample_count
            )

    def _log_values(self) -> None:
        """
        Log the values of the training step. The values are averaged over the number of
        samples in the batch
        """
        if self._current_training_prefix != TrainingPrefix.TRAIN:
            return

        sample_count = self._train_logger.log_sample_count
        for key in self._train_logger.train_values:
            value = self._train_logger.train_values[key]["value"]
            super().log(
                key,
                value / sample_count,
                prog_bar=self._train_logger.train_values[key]["prog_bar"],
                sync_dist=True,
                on_step=True,
            )

        super().log("train_samples", self._train_logger.train_samples, sync_dist=True)
        super().log("step_counter", self._train_logger.step_counter, sync_dist=True)

        # empty the train_logging_values to start collecting the new values
        self._train_logger.train_values = {}
        self._train_logger.log_sample_count = 0

    def step(
        self, batch: dict, prefix: TrainingPrefix = TrainingPrefix.TRAIN
    ) -> torch.Tensor:
        """
        Step function for the training. Is called for every batch during training,
        validation and testing. Needs to be implemented in an extension class.

        Args:
            batch: Current batch
            prefix: Prefix of the training step (train, validation, test)

        Returns: Loss tensor used to train the model
        """
        raise NotImplementedError(
            "This method needs to be implemented in an extension class"
        )

    def _step(
        self, batch: dict, prefix: TrainingPrefix = TrainingPrefix.TRAIN
    ) -> torch.Tensor:
        """
        Step function for the training. It checks if the batch has the same number of
        samples and then calls the step function implemented in the extension class.

        Args:
            batch (dict): Current batch
            prefix: Prefix of the training step (train, validation, test)

        Returns: Loss tensor used to train the model
        """
        self._current_training_prefix = prefix
        self._train_logger.batch_sample_count = -1
        for key in batch:
            if (
                self._train_logger.batch_sample_count != -1
                and len(batch[key]) != self._train_logger.batch_sample_count
            ):
                raise ValueError(
                    "Batches with different feature count are not supported"
                )
            self._train_logger.batch_sample_count = len(batch[key])

        loss = self.step(batch, prefix=prefix)
        return loss

    # pylint: disable=arguments-differ
    @override
    def training_step(self, batch: dict) -> torch.Tensor:
        """
        Run lightning training step.
        The inherited method uses *args, **kwargs as argument, but use the
        batch specifically for the training step.
        Args:
            batch (dict): current batch as dict

        Returns:
            torch.Tensor: loss tensor
        """
        self._current_training_prefix = TrainingPrefix.TRAIN
        self._train_logger.step_counter += 1
        loss = self._step(batch, prefix=TrainingPrefix.TRAIN)

        # self._train_logger.sample_count is set in the _step function
        self._train_logger.train_samples += self._train_logger.batch_sample_count
        self._train_logger.log_sample_count += self._train_logger.batch_sample_count

        if (
            self._train_logger.step_counter
            % self._config.logging_config.log_every_n_steps
            == 0
        ):
            self._log_values()
        return loss

    @override
    def validation_step(self, batch: dict) -> torch.Tensor:
        """
        Run lightning validation step
        Args:
            batch (dict): current batch as dict

        Returns:
            torch.Tensor: loss tensor
        """
        return self._step(batch, prefix=TrainingPrefix.VALIDATION)

    @override
    def test_step(self, batch: dict) -> torch.Tensor:
        """
        Run lightning test step
        Args:
            batch (dict): current batch as dict

        Returns:
            torch.Tensor: loss tensor
        """
        return self._step(batch, prefix=TrainingPrefix.TEST)

    def get_optimizers(self, config: OptimizerConfig) -> torch.optim.Optimizer:
        """
        Get the optimizer for the training. Needs to be implemented in an extension
        class

        Args:
            config: Configuration for the optimizer

        Returns: Optimizer for the training
        """
        raise NotImplementedError(
            "This method needs to be implemented in an extension class"
        )

    @override
    def configure_optimizers(self) -> torch.optim.Optimizer:
        """
        Get the optimizer for the training. Calls extendable function
        self.get_optimizers().
        Returns:
            torch.optim.Optimizer: optimizer for training
        """
        return self.get_optimizers(self._config.optimizer_config)
