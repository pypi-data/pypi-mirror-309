"""
Functions to validate the run configuration file used for the training for a better
control.
"""

import logging

from anhaltai_commons_pl_hyper.constants import DataSplittingMode

logger = logging.getLogger(__name__.rsplit(".", maxsplit=1)[-1])


def _get_config_combination(sweep_config: dict, combi_index) -> tuple[dict, bool]:
    """
    Get the configuration for the given combination index. The combinations are shallow
    and each parameter is validated individually instead of all combinations.

    Args:
        sweep_config: Sweep configuration with multiple combinations.
        combi_index: Index of the combination to extract.

    Returns: configuration for the given combination index and a flag if a new
      combination was found.

    """
    config_combination = {}
    curr_combi_index = 0
    new_combi = False
    for key, value in sweep_config["parameters"].items():
        if "value" in value:
            config_combination[key] = value["value"]
        elif "values" in value:
            relative_index = combi_index - curr_combi_index
            if len(value["values"]) > relative_index > 0:
                config_combination[key] = value["values"][relative_index]
                new_combi = True
            else:
                config_combination[key] = value["values"][0]
            curr_combi_index += len(value["values"]) - 1
    return config_combination, new_combi


def shallow_validate_every_config(sweep_config: dict) -> None:
    """
    Check every configuration combination of a sweep configuration. The function
    validates the conditionally must-have values for every combination and the
    unconditionally must-have values for the last combination.

    Args:
        sweep_config: Configuration with multiple combinations to validate.

    Raises: ValueError if the configuration is invalid.

    """

    logger.info("Check every config combination conditional values")
    combi_index = 1
    new_combi = True
    all_combi_valid = True
    config_combination: dict = {}

    while new_combi:
        config_combination, new_combi = _get_config_combination(
            sweep_config, combi_index
        )
        if new_combi:
            try:
                # Only the conditionally must-have values are validated here since the
                # must-have values are the same for all combinations.
                validate_configuration(config_combination, True)
            except ValueError:
                all_combi_valid = False
        combi_index += 1

    try:
        logger.info("----------------------------------------")
        logger.info("Check config unconditionally must-have values")
        validate_configuration(config_combination, False)
    except ValueError:
        all_combi_valid = False

    if not all_combi_valid:
        raise ValueError("Invalid configuration file")

    logger.info("----------------------------------------")
    logger.info("All configurations are valid")


def validate_configuration(config: dict, conditionally_only: bool = False) -> None:
    """
    Check a single configuration file. The function validates the conditionally
    must-have values if conditionally_only is set to True. Otherwise, it validates all
    values.

    Args:
        config: Configuration to be validated.
        conditionally_only: Flag to validate only the conditionally must-have values.

    Raises: ValueError if the configuration is invalid.

    """

    if "checkpoint_path" in config and config["checkpoint_path"]:
        return  # Config will be loaded from checkpoint

    valid_run_config = _validate_conditionally_must_have_values(config)
    if not conditionally_only:
        valid_run_config = (
            _validate_must_have_values(config)
            and _validate_metric(config)
            and valid_run_config
        )

    _validate_optional_values(config)

    if (
        "num_workers" in config
        and config["num_workers"] == 0
        and "persistent_workers" in config
        and config["persistent_workers"]
    ):
        logger.error(
            "persistent_workers is set to True but num_workers is set "
            "to 0. persistent_workers need num_workers > 0."
        )
        valid_run_config = False

    if not valid_run_config:
        raise ValueError("Invalid configuration file. See error messages above.")


def _validate_optional_values(run_config: dict) -> None:
    """
    Check the optional values of the configuration file. Throws a warning if a value
    is missing.

    Args:
        run_config: Configuration file to be validated.

    Returns:

    """

    optional_keys = ["validation_split_ratio", "test_split_ratio"]

    for key in optional_keys:
        if key not in run_config:
            logger.warning(
                "%s is missing in the configuration file. The run will "
                "continue but might crash if your dataset is missing the %s.",
                key,
                key,
            )


def _validate_metric(config: dict) -> bool:
    """
    Check the metric field of the configuration file.

    Args:
        config: Configuration file to be validated.

    Returns: True if the metric field is valid, False otherwise.

    """

    if "metric" not in config:
        logger.warning("metric is missing in the configuration file.")
        return False

    valid_run_config = True
    metric: dict = config["metric"]
    if "name" not in metric:
        logger.error("The name of the metric is missing in the configuration file.")
        valid_run_config = False
    if "goal" not in metric:
        logger.error("The goal of the metric is missing in the configuration file.")
        valid_run_config = False

    return valid_run_config


def _validate_conditionally_must_have_values(config: dict) -> bool:
    """
    Check the conditionally must-have values of the configuration file. Logs an error
    if a value is missing.

    Args:
        config: Configuration file to be validated.

    Returns: True if the conditionally must-have values are valid, False otherwise.

    """

    valid_run_config: bool = True

    # use str for logging to be more readable for the user instead of enum values
    data_splitting_mode_values: list[str] = [
        str(DataSplittingMode.NORMAL),
        str(DataSplittingMode.FINAL),
        str(DataSplittingMode.CROSS_VALIDATION),
    ]

    # special cases:

    if (
        "data_splitting_mode" not in config
        or config["data_splitting_mode"] not in data_splitting_mode_values
    ):
        logger.error(
            "data_splitting_mode missing or not among the supported values of %s",
            data_splitting_mode_values,
        )
        return False

    if config["data_splitting_mode"] == DataSplittingMode.CROSS_VALIDATION:
        n_splits_value: int | None = config.get("n_splits", None)
        if not n_splits_value or n_splits_value < 2:
            logger.error(
                "n_splits >= 2 is missing in the configuration file when "
                " data_splitting_mode==%s. Current value is: %s.",
                DataSplittingMode.CROSS_VALIDATION,
                n_splits_value,
            )
            valid_run_config = False

    if (
        "early_stopping" in config
        and config["data_splitting_mode"] == DataSplittingMode.FINAL
    ):
        logger.error(
            "early_stopping is not supported when data_splitting_mode==%s.",
            DataSplittingMode.FINAL,
        )
        valid_run_config = False

    if "early_stopping" in config and config["data_splitting_mode"]:
        early_stopping = config["early_stopping"]
        if "patience" not in early_stopping:
            logger.error("patience is missing in the early_stopping configuration.")
            valid_run_config = False
        if "monitor" not in early_stopping:
            logger.error("monitor is missing in the early_stopping configuration.")
            valid_run_config = False
        if "mode" not in early_stopping:
            logger.error("mode is missing in the early_stopping configuration.")
            valid_run_config = False
    return valid_run_config


def _validate_must_have_values(config: dict) -> bool:
    """
    Check the must-have values of the configuration file. Logs an error if a value is
    missing.

    Args:
        config: Configuration file to be validated.

    Returns: True if the must-have values are valid, False otherwise.

    """

    valid_run_config: bool = True
    must_have_keys: list[str] = [
        "data_splitting_mode",
        "accelerator",
        "max_epochs",
        "check_val_every_n_epoch",
        "accumulate_grad_batches",
        "metric",
        "batch_size",
        "num_workers",
        "persistent_workers",
        "pin_memory",
        "random_seed",
        "log_every_n_steps",
        "enable_checkpointing",
    ]
    for key in must_have_keys:
        if key not in config:
            logger.error("%s is missing in the configuration file.", key)
            valid_run_config = False

    return valid_run_config
