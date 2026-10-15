"""WTF Hub client. One job: the Hub's pack index -> a verified .wtfpack file on this computer.

The Hub is an index (JSON, a few kB) of subject packs; the packs themselves are files anywhere on HTTPS (GitHub
releases or raw files today). Every entry names its download URL, size and SHA-256: a download that does not match
is deleted, never installed. Installing is the app's ordinary pack import (tools/pack.py for data packs,
wtf_compiler for recipe packs); the Hub adds nothing a local .wtfpack file does not have.

  index = load(url)                       {"hub": 1, "packs": [entry, ...]}
  path = download(entry, folder)          the verified file
"""
import hashlib, json, os, re, tempfile, urllib.request
from pathlib import Path

DEFAULT = "https://raw.githubusercontent.com/LxCenady/worldwide-teachers-friend/main/hub/index.json"
AGENT = "WTF-Hub (+https://wtf-academy.org)"  # a named client (Cloudflare turns away anonymous scripts)
MAX_INDEX = 2 * 1024 * 1024
MAX_PACK = 256 * 1024 * 1024
FIELDS = ("id", "kind", "name", "version", "url", "sha256", "size")


class HubError(RuntimeError):
    pass


def check(entry):
    """An index entry -> itself, or HubError when it is malformed or unsafe."""
    if not isinstance(entry, dict) or any(f not in entry for f in FIELDS):
        raise HubError("index entry is missing fields")
    if entry["kind"] not in ("data", "recipe") or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", str(entry["id"])):
        raise HubError(f"bad pack id or kind: {entry.get('id')}")
    if not str(entry["url"]).startswith("https://") or not re.fullmatch(r"[0-9a-f]{64}", str(entry["sha256"])):
        raise HubError(f"{entry['id']}: the download must be HTTPS with a SHA-256")
    if type(entry["size"]) is not int or not 0 < entry["size"] <= MAX_PACK:
        raise HubError(f"{entry['id']}: bad size")
    if not isinstance(entry["name"], dict) or not entry["name"]:
        raise HubError(f"{entry['id']}: bad name")
    return entry


def get(url, limit, timeout=30):
    if not url.startswith("https://") and not url.startswith("file:"):
        raise HubError("the Hub is only read over HTTPS")
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read(limit + 1)
    if len(data) > limit:
        raise HubError("download larger than allowed")
    return data


def load(url=None):
    """The Hub index -> {"hub": 1, "packs": [checked entries]}."""
    try:
        index = json.loads(get(url or DEFAULT, MAX_INDEX).decode("utf-8"))
    except (OSError, ValueError) as e:
        raise HubError(f"cannot read the Hub index: {e}") from None
    if not isinstance(index, dict) or index.get("hub") != 1 or not isinstance(index.get("packs"), list):
        raise HubError("not a WTF Hub index")
    index["packs"] = [check(e) for e in index["packs"]]
    return index


def download(entry, folder):
    """Download one pack into `folder`, verify its size and SHA-256 -> the file's path."""
    entry = check(entry)
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    data = get(entry["url"], entry["size"], timeout=120)
    if len(data) != entry["size"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise HubError(f"{entry['id']}: the downloaded file does not match the Hub's SHA-256 (not installed)")
    target = folder / f"{entry['id']}-{entry['version']}.wtfpack"
    fd, tmp = tempfile.mkstemp(dir=folder, suffix=".part")
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    os.replace(tmp, target)
    return target


def entry_for(path, url, tier="official"):
    """A Hub index entry for a local .wtfpack (used by tools/hub_index.py)."""
    import zipfile
    data = Path(path).read_bytes()
    with zipfile.ZipFile(path) as z:
        manifest = json.loads(z.read("pack.json"))
    recipe = manifest.get("wtf_pack") == 2
    course = manifest["course"] if recipe else None
    entry = {"id": course["id"] if recipe else manifest["subject"], "kind": "recipe" if recipe else "data",
             "name": course["name"] if recipe else manifest["name"], "version": manifest["version"],
             "requires_wtf": manifest.get("requires_wtf", ">=2.1.0" if recipe else ">=2.0.0"),
             "board": "" if recipe else manifest.get("board", ""), "exam": "" if recipe else manifest.get("exam", ""),
             "url": url, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data), "tier": tier}
    return check(entry)
