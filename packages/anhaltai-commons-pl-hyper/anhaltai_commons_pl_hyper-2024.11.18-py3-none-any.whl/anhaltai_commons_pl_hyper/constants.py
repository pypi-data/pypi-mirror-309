"""
Classes to provide frequently used constants
"""

# TODO: for py >=3.11: from enum import StrEnum
from strenum import StrEnum


class DataSplittingMode(StrEnum):
    """
    Data splitting modes. Please refer to the data splitting documentation for details.
    """

    NORMAL: str = "normal"
    CROSS_VALIDATION: str = "cross-validation"
    FINAL: str = "final"
