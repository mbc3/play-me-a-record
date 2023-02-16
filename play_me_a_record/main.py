from pathlib import Path
import random
import shelve
import argparse
from play_me_a_record import play
from play_me_a_record import config as toml

# hardcoded config files path
CONFIG_DIR = Path("~/.config/PlayMeARecord/").expanduser()

# ARGUMENT PARSER

parser = argparse.ArgumentParser(description="play a random record")
parser.add_argument("-u", help="update database", action="store_true")
parser.add_argument(
    "-d",
    "--db-file",
    help="path where database is located (defaults to 'CONFIG_DIR/db')",
    default=CONFIG_DIR.joinpath("db"),
    action="store",
)
parser.add_argument(
    "-m",
    "--music-directory",
    help="path to directory where albums are located",
    default=Path("~/Music/Albums/").expanduser(),
    action="store",
)
parser.add_argument(
    "-g",
    "--generate-config",
    help="generate a new TOML config file at LOCATION",
    action="store",
)

args = parser.parse_args()

# READING CONFIG AND SETTING GLOBAL VARIABLES

CONFIG_FILE = CONFIG_DIR.joinpath("playmearecord.toml")

if CONFIG_FILE.exists():
    MUSIC_DIR, DATABASE = toml.read_config(CONFIG_FILE)
else:
    MUSIC_DIR = args.music_directory
    DATABASE = args.db_file


def build_path(artist, album) -> Path:
    """builds and returns a path from artist and album paramaters"""
    path = Path(MUSIC_DIR).joinpath(Path(artist)).joinpath(Path(album))
    return path


def main():
    """Main program

    Raises:
        Exception: error if database can't be loaded
    """

    if args.u:  # update database if requested
        database = play.build_database(str(MUSIC_DIR))
        play.build_shelf(str(DATABASE), database)

    if args.generate_config:
        toml.create_config(
            Path(args.generate_config).expanduser(), str(MUSIC_DIR), str(DATABASE)
        )

    try:
        f = shelve.open(str(DATABASE))
    except Exception as e:
        print(type(e))
        raise FileNotFoundError("cannot find database!")
    else:
        artist = random.choice(list(f["music"]))
        album = random.choice(f["music"][artist])
        songs = play.get_songs_in_directory(build_path(artist, album))
        play.play(songs)
        f.close()
