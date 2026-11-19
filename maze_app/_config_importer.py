import sys

from config_parser import ConfigData, config_validator


class ImporterError(Exception):
    def __str__(self) -> str:
        return "Missing configuration file. \
Usage: poetry run python3 <PROGRAM.py> <config.txt>"


def config_importer() -> ConfigData:

    if len(sys.argv) != 2:
        raise ImporterError
    val_data: ConfigData = config_validator(sys.argv[1])
    return val_data
