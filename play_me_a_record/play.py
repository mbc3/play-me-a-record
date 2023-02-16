import shelve
from pathlib import Path
from mpd import MPDClient

FILE_EXTENSIONS = (".mp3", ".flac", ".m4a", ".opus", ".wav")


def build_shelf(filename: str, music):
    """create a shelf from parameter

    Args:
        filename (str): full path of shelf as string
        music (dict): a dictionary of Artists and their Albums
    """
    with shelve.open(filename) as f:
        f["music"] = music
        f.close()


def build_database(location: str) -> dict:
    """builds and returns a dictionary of artists and their albums,
    using LOCATION as a root directory"""

    path = Path(location)
    database = {}

    for artists in path.iterdir():
        artist_name = artists.name
        albums = []

        for album in artists.iterdir():
            albums.append(album.name)

        database.update({artist_name: albums})

    return database


def get_songs_in_directory(directory) -> list:
    """return a sorted list of PosixPath for all the songs in a directory"""
    album = []

    if Path(directory).exists():
        for song in directory.iterdir():
            if song.suffix in FILE_EXTENSIONS:
                album.append(song)

        album.sort()
        return album

    else:
        raise FileNotFoundError("cannot open directory to find songs!")


def play(songs):
    """add and play a list of songs to MPD"""

    client = MPDClient()
    client.timeout = 10  # network timeout in seconds
    client.idletimeout = None  # timeout for fetching the result of the idle
    client.connect(
        "/run/user/1000/mpd/socket", 6600
    )  # has to be socket instead of localhost so absolute paths can resolve

    client.clear()  # clear playlist

    for song in songs:
        try:
            client.add(song)
        except Exception as e:
            print(type(e))
            raise FileNotFoundError(f"cannot add song {song}!")

    client.play(0)
    song_info = client.currentsong()
    print("Artist:", end="\t")
    print(song_info["artist"])
    print("Album:", end="\t")
    print(song_info["album"])
    client.close()
    client.disconnect()
