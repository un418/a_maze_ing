
from config_parser import config_importer, ConfigData
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing configuration file. \
Usage: poetry run python3 <PROGRAM.py> <config.txt>")

    val_data: ConfigData = config_importer(sys.argv[1])
