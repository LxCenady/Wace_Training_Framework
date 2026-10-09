"""Get the SCSA past papers. One job: put every file listed in sources.tsv into */papers/.

The papers are © School Curriculum and Standards Authority and are not redistributed in this repo.
  python tools/fetch.py                 download what can be downloaded (2016-2019 come from the Wayback Machine)
  python tools/fetch.py --from DIR      import PDFs you saved in a browser — any file names: matched by the
                                        official file name, else recognised from the first page (paperid.py)
The SCSA site sits behind bot protection, so direct downloads of 2020+ papers are usually refused (HTTP 403);
open the printed URLs in a normal browser, save the PDFs, then import them with --from.
"""
import os, re, shutil, sys, time, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperid import identify  # noqa: E402

WAYBACK = "https://web.archive.org/web/2020id_/"
ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sources(root=None):
    """-> list of (relative path, download URL, official URL, archived?)."""
    out = []
    for line in open(os.path.join(root or ROOT, "sources.tsv"), encoding="utf-8"):
        if line.strip():
            path, url = line.rstrip("\n").split("\t")
            archived = url.endswith(" (wayback)")
            official = url[: -len(" (wayback)")] if archived else url
            out.append((path, WAYBACK + official if archived else official, official, archived))
    return out


def is_pdf(path):
    try:
        with open(path, "rb") as f:
            return f.read(5) == b"%PDF-"
    except OSError:
        return False


def missing(root=None):
    root = root or ROOT
    return [s for s in sources(root) if not is_pdf(os.path.join(root, s[0]))]


def download(rel, url, root=None, timeout=60, tries=5, wait=lambda s: time.sleep(s)):
    """Fetch one file, retrying dropped connections, timeouts and 429/5xx with growing pauses
    (Retry-After honoured). Raises on a final failure, on 4xx refusals (e.g. 403) and on a non-PDF reply."""
    dest = os.path.join(root or ROOT, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for attempt in range(1, tries + 1):
        try:
            req = urllib.request.Request(url, headers={"user-agent": "Mozilla/5.0 (WTF fetch.py)"})
            with urllib.request.urlopen(req, timeout=timeout) as r, open(dest + ".part", "wb") as f:
                shutil.copyfileobj(r, f)
            break
        except urllib.error.HTTPError as e:
            if e.code not in (408, 429, 500, 502, 503, 504) or attempt == tries:
                raise
            pause = float(e.headers.get("Retry-After") or 0) or 2 ** attempt
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            if attempt == tries:
                raise
            pause = 2 ** attempt
        wait(min(pause, 60))
    if not is_pdf(dest + ".part"):
        os.remove(dest + ".part")
        raise ValueError("reply was not a PDF")
    os.replace(dest + ".part", dest)


def official_name(url):
    return urllib.parse.unquote(url.rsplit("/", 1)[-1]).lower()


def match(path, root=None):
    """Which listed paper is this PDF? Official file name first (ignoring case and ' (1)'), then its content."""
    if not is_pdf(path):
        return None
    name = re.sub(r" \(\d+\)(?=\.pdf$)", "", os.path.basename(path).lower())
    listed = sources(root)
    for rel, _, official, _ in listed:
        if name == official_name(official):
            return rel
    rel = identify(path)
    return rel if rel in {s[0] for s in listed} else None


def import_file(path, root=None):
    """Copy one PDF into place if it is a listed, still-missing paper. Returns its relative path or None."""
    root = root or ROOT
    rel = match(path, root)
    if not rel:
        return None
    dest = os.path.join(root, rel)
    if is_pdf(dest):
        return None
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(path, dest)
    return rel


def import_dir(folder, root=None):
    got = []
    for name in sorted(os.listdir(folder)):
        if name.lower().endswith(".pdf"):
            rel = import_file(os.path.join(folder, name), root)
            if rel:
                got.append(rel)
    return got


def main(args):
    if len(args) > 1 and args[0] == "--from":
        for rel in import_dir(args[1]):
            print("ok  ", rel)
    else:
        for rel, url, _, _ in missing():
            try:
                download(rel, url)
                print("ok  ", rel)
            except Exception as e:
                print("MISS", rel, f"({type(e).__name__}: {e})")
    left = missing()
    print(f"\n{len(left)} file(s) missing")
    for _, _, official, _ in left:
        print(official)
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
