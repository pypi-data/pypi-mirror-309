"""
DataModule class for the Trainer for model training.

The DataModule class is used to load the dataset, split it into train, validation
and test data and create the dataloaders. The class needs to be extended to implement
the loading of the dataset and the preprocessing of the data. The DataModule class is an
extension of the PyTorch Lightning DataModule class.
"""

import logging
from typing import Callable

import lightning as pl
import torch
from datasets import DatasetDict
from datasets import Split
from sklearn.model_selection import KFold
from torch.utils.data import Dataset, DataLoader, random_split
from torch.utils.data import default_collate
from typing_extensions import override

from anhaltai_commons_pl_hyper.constants import DataSplittingMode
from anhaltai_commons_pl_hyper.dataclasses.config import (
    PreprocessorConfig,
    DataModuleConfig,
    DataIndices,
    DatasetConfig,
)


class DataModule(pl.LightningDataModule):
    """
    The data module loads the dataset, splits it into train, validation and test data
    and creates the dataloaders.

    Args:
        config: DataModuleConfig object containing the configuration for the datamodule
    """

    def __init__(self, config: DataModuleConfig):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("Initialize DataModule")
        self._dataset_config = config.dataset_config
        self._data_loader_config = config.data_loader_config
        self._cross_validation_config = config.cross_validation_config

        if (
            self._dataset_config.validation_split_ratio is not None
            and self._dataset_config.test_split_ratio is not None
        ):
            if (
                self._dataset_config.validation_split_ratio
                + self._dataset_config.test_split_ratio
                >= 1.0
            ):
                raise ValueError(
                    "Validation and test split combined need to be smaller than 1.0"
                )

        self._datasets: DatasetDict = DatasetDict()

        self._dataset_indices = DataIndices(train=[], val=[])

        self._preprocessor: Callable | None = None

        self._preprocessor_config = config.preprocessor_config
        if self._preprocessor_config.enabled:
            self._preprocessor = self.load_preprocessor(self._preprocessor_config)

    def load_preprocessor(self, config: PreprocessorConfig) -> Callable:
        """
        Load the preprocessor for the data. The preprocessor is a function that
        transforms the data from the dataset to the input format of the model. Needs
        to be implemented in the extension class.

        Args:
            config: PreprocessorConfig object containing the configuration for the
              preprocessor

        Returns: Callable to preprocess data.
        """
        raise NotImplementedError("Preprocessor loading needs to be implemented")

    def load_dataset(self, config: DatasetConfig) -> DatasetDict:
        """
        Load the dataset from the given path. Needs to be implemented in the extension
        class

        Args:
            config: DatasetConfig object containing the configuration for the dataset

        Returns: DatasetDict with the loaded dataset
        """

        raise NotImplementedError(
            "Dataset loading needs to be implemented in the extension class"
        )

    def get_dataset_metadata(self, dataset_config: DatasetConfig) -> dict:
        """
        Get the metadata of the dataset. This method is called once on the main process
        and the return is saved to a file. It can also be used to download and cache
        the dataset similar to the prepare_data method. Can be overwritten in the
        extension class

        Args:
            dataset_config: DatasetConfig object containing the configuration for the
              dataset

        Returns: Dictionary with the metadata of the dataset
        """
        return {}

    @staticmethod
    def get_split_seed(seed: int):
        """
        Get the seed for the split based on the seed given by the run config.
        """
        return torch.Generator().manual_seed(seed)

    def setup(self, stage: str) -> None:
        """
        Set up the datamodule. This includes loading the dataset and splitting it into
        train, validation and test data.

        Args:
            stage: Current stage of the training (e.g. fit, test)
        """
        self._logger.info("SETUP STAGE: %s", stage)
        dataset: DatasetDict = self.load_dataset(self._dataset_config)

        self.validate_given_data_split(dataset)

        (
            self._datasets[Split.TRAIN],
            self._datasets[Split.VALIDATION],
            self._datasets[Split.TEST],
        ) = DataModule.get_initial_split(
            dataset=dataset,
            val_split_ratio=self._dataset_config.validation_split_ratio,
            test_split_ratio=self._dataset_config.test_split_ratio,
            seed=self._cross_validation_config.seed,
        )

        # preprocess given split
        self._datasets[Split.TRAIN] = self.transform_dataset(
            self._datasets[Split.TRAIN], self._preprocessor, self._preprocessor_config
        )
        self._datasets[Split.VALIDATION] = self.transform_dataset(
            self._datasets[Split.VALIDATION],
            self._preprocessor,
            self._preprocessor_config,
        )
        self._datasets[Split.TEST] = self.transform_dataset(
            self._datasets[Split.TEST], self._preprocessor, self._preprocessor_config
        )
        # count samples for logging
        train_count: int = len(self._datasets[Split.TRAIN])
        validation_count: int = len(self._datasets[Split.VALIDATION])
        test_count: int = len(self._datasets[Split.TEST])

        # further splitting configured with data_splitting_mode

        if (
            self._dataset_config.data_splitting_mode
            == DataSplittingMode.CROSS_VALIDATION
            and self._cross_validation_config.enabled
        ):

            # combine train and validation to train
            self._datasets[Split.TRAIN] = torch.utils.data.ConcatDataset(
                [self._datasets[Split.TRAIN], self._datasets[Split.VALIDATION]]
            )
            kf = KFold(
                n_splits=self._cross_validation_config.num_folds,
                shuffle=True,
                random_state=self._cross_validation_config.seed,
            )
            all_data_splits = kf.split(self._datasets[Split.TRAIN])
            for _ in range(self._cross_validation_config.fold_id + 1):
                # Numpy list with int32 can cause problems, as such we convert to int
                # list
                fold_train_indices, fold_val_indices = next(all_data_splits)
                self._dataset_indices.train, self._dataset_indices.val = (
                    fold_train_indices.tolist(),
                    fold_val_indices.tolist(),
                )
                # update counters
                train_count = len(fold_train_indices)
                validation_count = len(fold_val_indices)
        elif self._dataset_config.data_splitting_mode == DataSplittingMode.FINAL:
            self._datasets[Split.TRAIN] = torch.utils.data.ConcatDataset(
                [self._datasets[Split.TRAIN], self._datasets[Split.VALIDATION]]
            )

        if self._cross_validation_config.enabled:
            self._logger.info(
                "Cross-validation with %s folds and fold id %s",
                self._cross_validation_config.num_folds,
                self._cross_validation_config.fold_id,
            )

        self._logger.info(
            "Split data instances: train: %d, validation: %d, test: %d",
            train_count,
            validation_count,
            test_count,
        )

    @staticmethod
    def get_initial_split(
        dataset: DatasetDict, val_split_ratio: float, test_split_ratio: float, seed: int
    ):
        """
        Do initial data split to train, validation and test sets.
        Raise ValueError if a set is empty.
        Args:
            dataset (DatasetDict): given dataset to split
            val_split_ratio (float): given validation split ratio to split the train set
            test_split_ratio (float): given test split ratio to split the train set
            seed (int): random seed for splitting

        Returns:
            tuple(Subset): dataset subsets train, validation and test
        """
        seed_gen: torch.Generator = DataModule.get_split_seed(seed)
        train_set = dataset[Split.TRAIN]  # train set is mandatory
        if Split.TEST not in dataset:
            # only train given
            ratios = [
                1 - test_split_ratio - val_split_ratio,
                test_split_ratio,
                val_split_ratio,
            ]
            train_set, test_set, val_set = random_split(train_set, ratios, seed_gen)
        elif Split.VALIDATION not in dataset:
            # only train and test given
            adjusted_val_split_ratio = val_split_ratio / (1 - test_split_ratio)
            ratios = [1 - adjusted_val_split_ratio, adjusted_val_split_ratio]
            train_set, val_set = random_split(train_set, ratios, seed_gen)
            test_set = dataset[Split.TEST]
        else:
            # train, validation and test given
            train_set = dataset[Split.TRAIN]
            val_set = dataset[Split.VALIDATION]
            test_set = dataset[Split.TEST]

        if len(train_set) <= 0:
            raise ValueError("Length of the train set would be 0 after splitting.")
        if len(val_set) <= 0:
            raise ValueError("Length of the validation set would be 0 after splitting.")
        if len(test_set) <= 0:
            raise ValueError("Length of the test set would be 0 after splitting.")

        return train_set, val_set, test_set

    def validate_given_data_split(self, dataset: DatasetDict):
        """
        Validate if one of three supported data split cases is given.
        Raises ValueError if not.
        Args:
            dataset (DatasetDict): Dataset to be checked
        """
        valid: bool = False
        if (
            (
                Split.TRAIN in dataset
                and Split.TEST not in dataset
                and Split.VALIDATION not in dataset
            )
            or (
                Split.TRAIN in dataset
                and Split.TEST in dataset
                and Split.VALIDATION not in dataset
            )
            or (
                Split.TRAIN in dataset
                and Split.VALIDATION in dataset
                and Split.TEST in dataset
            )
        ):
            valid = True

        if not valid:
            raise ValueError(
                f"Invalid data split:\n"
                f"'{Split.TRAIN}': {Split.TRAIN in dataset}\n"
                f"'{Split.VALIDATION}': {Split.VALIDATION in dataset}\n"
                f"'{Split.TEST}': {Split.TEST in dataset}\n"
                f"Please check your self.load_dataset() method of your DataModule "
                f"subclass.\n"
                f"Keys must be specified in the DatasetDict in one of the following "
                f"options:\n"
                f"1) '{Split.TRAIN}'\n"
                f"2) '{Split.TRAIN}' + '{Split.TEST}'\n"
                f"3) '{Split.TRAIN}' + '{Split.VALIDATION}' + '{Split.TEST}'\n"
            )

        if len(dataset[Split.TRAIN]) == 0:
            raise ValueError("Train set is given but it is empty.")
        if Split.TEST not in dataset:
            self._logger.warning(
                "No test dataset found, splitting train dataset to create one"
            )
        else:
            if len(dataset[Split.TEST]) == 0:
                raise ValueError("Test set is given but it is empty.")
        if Split.VALIDATION not in dataset:
            self._logger.warning(
                "No validation dataset found, splitting train dataset to create one"
            )
        else:
            if len(dataset[Split.VALIDATION]) == 0:
                raise ValueError("Validation set is given but it is empty.")

    def transform_dataset(
        self,
        dataset: Dataset,
        preprocessor: Callable | None,
        preprocess_config: PreprocessorConfig,
    ) -> Dataset:
        """
        Transform the dataset from torch.utils.data to custom Dataset class. The
        Dataset class needs to inherit from torch.utils.data.Dataset. To extend the
        Dataset class implement the __getitem__ and __len__ functions.
        Needs to be implemented in the extension class

        Args:
            dataset: Dataset to be transformed
            preprocessor: Preprocessor to transform the data. Return from
              load_preprocessor or None if preprocess_dataset is False
            preprocess_config: PreprocessorConfig object containing the configuration
              for the preprocessor
        """

        raise NotImplementedError("Transforming the dataset needs to be implemented")

    def get_collate_function(self) -> Callable:
        """
        Get collate function for the dataloader. Returns default_collate on default.
        Needs to
        return a callable which needs to be pickable (atleast) for windows systems.
        This means
        the resulting function can not stem from the data_module class since the self
        variable makes the function unpickable on windows (on linux it does work).
        Can be overwritten in the extension class

        Returns: Function to preprocess the batch
        """

        return default_collate

    @override
    def train_dataloader(self) -> DataLoader:
        """
        Get the dataloader for train data
        """
        return DataLoader(
            self._datasets[Split.TRAIN],
            shuffle=not self._cross_validation_config.enabled,
            batch_size=self._data_loader_config.batch_size,
            num_workers=self._data_loader_config.num_workers,
            persistent_workers=self._data_loader_config.persistent_workers,
            pin_memory=self._data_loader_config.pin_memory,
            collate_fn=self.get_collate_function(),
            sampler=(
                torch.utils.data.SubsetRandomSampler(self._dataset_indices.train)
                if self._cross_validation_config.enabled
                else None
            ),
        )

    @override
    def val_dataloader(self) -> DataLoader:
        """
        Get the dataloader for validation data
        """
        return DataLoader(
            (
                self._datasets[Split.VALIDATION]
                if not self._cross_validation_config.enabled
                else self._datasets[Split.TRAIN]  # using sampler
            ),
            batch_size=self._data_loader_config.batch_size,
            num_workers=self._data_loader_config.num_workers,
            persistent_workers=self._data_loader_config.persistent_workers,
            pin_memory=self._data_loader_config.pin_memory,
            collate_fn=self.get_collate_function(),
            sampler=(
                torch.utils.data.SubsetRandomSampler(self._dataset_indices.val)
                if self._cross_validation_config.enabled
                else None
            ),
        )

    @override
    def test_dataloader(self) -> DataLoader:
        """
        Get the dataloader for test data
        """
        return DataLoader(
            self._datasets[Split.TEST],
            batch_size=self._data_loader_config.batch_size,
            num_workers=self._data_loader_config.num_workers,
            persistent_workers=self._data_loader_config.persistent_workers,
            pin_memory=self._data_loader_config.pin_memory,
            collate_fn=self.get_collate_function(),
            sampler=None,
        )
