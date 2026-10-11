"""Redirect user databases before plugin setup, not after Store has already opened them."""
from pathlib import Path
import sqlite3
import tempfile

_temp = None


def isolate():
    global _temp
    if _temp is not None:
        return
    import plugins.config as config
    _temp = tempfile.TemporaryDirectory(prefix="wtf-test-settings-")
    config.PATH = str(Path(_temp.name) / "config.json")
    original = sqlite3.connect
    live_past = Path(__file__).resolve().parents[2] / "wace.db"

    def connect(database, *args, **kwargs):
        path = Path(str(database))
        if path.name in ("generated.db", "external.db"):
            database = ":memory:"
        elif path.resolve() == live_past:
            database = live_past.as_uri() + "?mode=ro"
            kwargs["uri"] = True
        return original(database, *args, **kwargs)

    sqlite3.connect = connect
