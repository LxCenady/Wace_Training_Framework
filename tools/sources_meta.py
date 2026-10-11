"""Fill in a subject's paper manifest from the papers on this computer. One job: <S>/sources.tsv -> the same file
with method, Wayback capture, sha256, size, pages and need filled in (the columns are described in fetch.py).

  python tools/sources_meta.py MAM MAS MAA      (needs every listed paper on disk; asks the Wayback Machine for
                                                the capture whose content digest equals the local file)
"""
import base64, hashlib, json, os, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch  # noqa: E402
import pymupdf  # noqa: E402

CDX = "https://web.archive.org/cdx/search/cdx?output=json&fl=timestamp,digest,statuscode&url="


def capture(url, sha1):
    """The Wayback timestamp whose stored content is exactly this file (Wayback digests are base32 SHA-1)."""
    for attempt in range(5):  # the CDX server times out now and then (504)
        try:
            with urllib.request.urlopen(CDX + urllib.parse.quote(url, safe=""), timeout=120) as r:
                rows = json.load(r)[1:]
            break
        except OSError:
            if attempt == 4:
                raise
            time.sleep(3 * (attempt + 1))
    for ts, digest, status in rows:
        if status == "200" and digest == sha1:
            return ts
    raise ValueError(f"no Wayback capture has the local file's content: {url}")


def need(rel):
    """Papers the bank is built from are required; sample papers and examination reports are not."""
    name = os.path.basename(rel)
    return "optional" if "Sample" in name or "ExamReport" in name else "required"


def row(src, root):
    path = os.path.join(root, src["path"])
    data = open(path, "rb").read()
    with pymupdf.open(path) as doc:
        pages = doc.page_count
    method = src["method"]
    ts = src["capture"]
    if method == "wayback" and not ts:
        ts = capture(src["url"], base64.b32encode(hashlib.sha1(data).digest()).decode())
    return [src["path"], src["url"], method, ts, hashlib.sha256(data).hexdigest(), str(len(data)),
            str(pages), need(src["path"])]


def fill(subject, root=fetch.ROOT):
    with ThreadPoolExecutor(8) as pool:  # one CDX query per archived paper, a few at a time
        rows = list(pool.map(lambda s: row(s, root), fetch.entries(root, [subject])))
    out = os.path.join(root, subject, "sources.tsv")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("#" + "\t".join(fetch.COLUMNS) + "\n")
        f.writelines("\t".join(r) + "\n" for r in rows)
    return out


if __name__ == "__main__":
    for s in sys.argv[1:]:
        print(fill(s))
