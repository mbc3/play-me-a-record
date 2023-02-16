from tomlkit import document
from tomlkit import comment
from tomlkit import nl
from tomlkit import dump
from tomlkit import parse
from pathlib import Path


def create_config(config_file_location, music_dir, db_location):
    """Saves a config file in TOML format

    Args:
        config_file_location (str): location to save file
        music_dir (str): location of music directory
        db_location (str): location of database file
    """
    config = document()
    config.add(comment("Play Me A Record config file"))
    config.add(nl())
    config.add(comment("path to your albums' directory"))
    config.add(nl())
    config.add("music", music_dir)
    config.add(nl())
    config.add(comment("path to database file"))
    config.add("db", db_location)
    with open(config_file_location, "w") as f:
        dump(config, f)
        f.close()


def is_valid_config(config_file):
    """checks if config file is a valid config

    Args:
        config_file (str): configuration file
    """
    with open(config_file, "r") as f:
        config = parse(f.read())
        if "music" in config and "db" in config:
            if (
                Path(config["music"]).expanduser().exists()
                and Path(config["db"]).expanduser().exists()
            ):
                return True
            else:
                return False
        else:
            return False


def read_config(config_file) -> tuple:
    """Reads a config_file TOML format

    Args:
        config_file (str): location of config file
    """
    with open(config_file, "r") as f:
        config = parse(f.read())
        if is_valid_config(config_file):
            return (
                Path(str(config["music"])).expanduser(),
                Path(str(config["db"])).expanduser(),
            )
        else:
            raise Exception("invalid TOML file!")
