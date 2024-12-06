""" Quran CLI, A tool to generate the most sophisticated Quran data. """

from enum import Enum


class DataFormat(str, Enum):
    """Export formats"""

    CSV = "csv"
    XML = "xml"
    JSON = "json"
