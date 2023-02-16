from pathlib import Path
import shelve
from play_me_a_record import play


def test_build_shelf():
    """tests build_shelf function"""
    filename = Path.cwd().joinpath("tests/test_shelf")
    play.build_shelf(str(filename), "test")
    t = shelve.open(str(filename))
    assert t["music"] == "test"
    t.close()
