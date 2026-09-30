
from ._validator import ConfigData


def dict_builder(config_name: str) -> dict[str, str]:
    """
    Builds a dictionary from the 'config.txt'

    Raises:
        ValueError: key/value unpacking fails.
        OSError: If the configuration file cannot be opened or read.
    """
    config_data: dict[str, str] = {}
    with open(config_name, "r") as config:
        for line in config:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if '=' not in line:
                raise ValueError(f"{line} doesn't follow the 'KEY=VALUE' format")

            key, value = line.split('=', maxsplit=1) # Only splits first '='. Value can have a '='
            key = key.strip()
            value = value.strip()

            if key in config_data:
                raise ValueError(f"{key} is duplicate")

            config_data[key] = value

    return config_data


def config_importer(filepath: str) -> ConfigData:
    """
    Handles the config import and validation.
    Returns object with validated data.

    Raises:
        ValidationError: If the parsed data violates 'ConfigData' constraints.
        ValueError: key/value unpacking fails or there's no 'config.txt'
        OSError: If the configuration file cannot be opened or read.
    """

    config_data: dict[str, str] = dict_builder(filepath)
    return ConfigData(**config_data) # type: ignore
