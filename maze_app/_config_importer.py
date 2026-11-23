from config_parser import ConfigData, config_validator


class ImporterError(Exception):
    """
    Indicate that the command expects exactly one config file argument.
    """
    def __str__(self) -> str:
        """
        Return the usage message for an incorrect argument count.
        """
        return "Missing configuration file. \
Usage: poetry run python3 <PROGRAM.py> <config.txt>"


def config_importer(cl_arguments: list[str]) -> ConfigData:
    """Load and validate the config file passed on the command line.

    Returns:
        The validated maze configuration.

    Raises:
        ImporterError: If the command does not receive exactly one argument.
        OSError: If the config file cannot be opened or read.
        ValueError: If the file contains malformed or duplicate entries.
        ValidationError: If the config values fail validation.
    """
    if len(cl_arguments) != 2:
        raise ImporterError
    val_data: ConfigData = config_validator(cl_arguments[1])
    return val_data
