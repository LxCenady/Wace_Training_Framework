"""Get the SCSA past papers. One job: put every file listed in sources.tsv into */papers/.

The papers are © School Curriculum and Standards Authority and are not redistributed in this repo.
  python tools/fetch.py                 download what can be downloaded (2016-2019 come from the Wayback Machine)
  python tools/fetch.py --from DIR      import PDFs you saved in a browser — any file names: matched by the
                                        official file name, else recognised from the first page (paperid.py)
The SCSA site sits behind bot protection, so direct downloads of 2020+ papers are usually refused (HTTP 403);
open the printed URLs in a normal browser, save the PDFs, then import them with --from.
"""
import hashlib, os, re, shutil, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperid import identify  # noqa: E402
import subjects as subject_registry

WAYBACK = "https://web.archive.org/web/{}id_/"
ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# <S>/sources.tsv, one paper per line (a first line starting with "#" names the columns):
#   path     where the paper goes, e.g. MAA/papers/2016_MAA_Exam_CalcFree.pdf
#   url      the official SCSA address
#   method   wayback: downloaded from the Wayback Machine | browser: the student saves it from the official site
#            (scripts get HTTP 403 there) | direct: plain download
#   capture  Wayback timestamp of the exact copy the tags were made on (wayback only)
#   sha256   of that exact copy: a different version would put every crop in the wrong place, so it is refused
#   bytes pages   for progress and to spot truncated archive copies
#   need     required: the bank is built from it | optional: sample papers, examination reports
# Old two-column lines ("path<TAB>url[ (wayback)]") still read, without the checks.
COLUMNS = ("path", "url", "method", "capture", "sha256", "bytes", "pages", "need")


def entries(root=None, subjects=None):
    """-> [{path, url, method, capture, sha256, bytes, pages, need}] from <S>/sources.tsv (and a legacy root
    sources.tsv, which a subject's own manifest supersedes); only `subjects` when given."""
    data_root = Path(root or ROOT)
    merged = {}
    for manifest in [data_root / "sources.tsv", *sorted(data_root.glob("*/sources.tsv"))]:
        if not manifest.exists():
            continue
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            row = dict(zip(COLUMNS, line.split("\t")))
            if manifest.parent != data_root and row["path"].split("/", 1)[0] != manifest.parent.name:
                raise ValueError(f"Source belongs to another subject: {manifest}")
            if not row.get("method"):  # legacy line
                archived = row["url"].endswith(" (wayback)")
                row["url"] = row["url"].removesuffix(" (wayback)")
                row["method"] = "wayback" if archived else "browser"
            if row["method"] not in ("wayback", "browser", "direct"):
                raise ValueError(f"Unknown download method in {manifest}: {row['method']}")
            row.setdefault("need", "required")
            row["need"] = row["need"] or "required"
            merged[row["path"]] = {c: row.get(c, "") for c in COLUMNS}
    return [r for p, r in merged.items() if subjects is None or p.split("/", 1)[0] in subjects]


def download_url(entry):
    if entry["method"] == "wayback":
        return WAYBACK.format(entry["capture"] or "2020") + entry["url"]
    return entry["url"]


def sources(root=None, subjects=None, optional=True):
    """-> list of (relative path, download URL, official URL, archived?); only `subjects` when given."""
    return [(e["path"], download_url(e), e["url"], e["method"] == "wayback") for e in entries(root, subjects)
            if optional or e["need"] == "required"]


def verify(path, rel, root=None):
    """None when the PDF at `path` is the copy `rel` lists (or the manifest has no hash), else why not."""
    want = next((e for e in entries(root) if e["path"] == rel), {}).get("sha256")
    if not want:
        return None
    with open(path, "rb") as f:
        got = hashlib.sha256(f.read()).hexdigest()
    return None if got == want else f"{os.path.basename(rel)}：不是题库标注所用的那一版 PDF（内容不同），已跳过"


def subjects(root=None):
    """Registered subjects with manifest entries, in profile order."""
    available = {s[0].split("/", 1)[0] for s in sources(root)}
    return [s for s in subject_registry.names(root) if s in available]


def is_pdf(path):
    try:
        with open(path, "rb") as f:
            return f.read(5) == b"%PDF-"
    except OSError:
        return False


def missing(root=None, subjects=None, optional=False):
    """Listed papers not on disk yet; the bank needs only the required ones (optional=True adds the rest)."""
    root = root or ROOT
    return [s for s in sources(root, subjects, optional) if not is_pdf(os.path.join(root, s[0]))]


def hint(error):
    """(kind, what to do) for a download error a student can act on, else (None, "")."""
    text = f"{type(error).__name__} {error}"
    if "CERTIFICATE_VERIFY_FAILED" in text or "certificate verify failed" in text:
        return "cert", ("网络在中间替换了 HTTPS 证书（学校 / 公司网络、VPN、代理或杀毒软件的网络防护都会这样），"
                        "而这台电脑不信任它。可以：换一个网络（例如手机热点）再点「开始下载」；或暂时关掉 VPN / "
                        "代理 / 杀毒软件的 HTTPS 检查；若是学校网络，请向老师或 IT 要学校的根证书并装进系统。")
    if any(s in text for s in ("Errno 61", "Errno 111", "WinError 10061", "Connection refused")):
        return "refused", ("连接被拒绝：常见原因是系统里设置了代理但代理软件没在运行（检查 VPN / 代理软件，或在"
                           "系统网络设置里关掉代理），也可能是所在网络屏蔽了 web.archive.org。换个网络再试最快。")
    if any(s in text for s in ("timed out", "Errno 60", "WinError 10060", "getaddrinfo failed", "nodename nor servname")):
        return "network", "连不上网络或 web.archive.org 响应太慢：检查网络连接，稍后会自动再试。"
    return None, ""


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
    wrong = verify(dest + ".part", rel, root)
    if wrong:
        os.remove(dest + ".part")
        raise ValueError(wrong)
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


def import_file(path, root=None, rejected=None):
    """Copy one PDF into place if it is a listed, still-missing paper. Returns its relative path or None;
    a listed paper in a different version than the manifest's goes to `rejected` (a list) with the reason."""
    root = root or ROOT
    rel = match(path, root)
    if not rel:
        return None
    dest = os.path.join(root, rel)
    if is_pdf(dest):
        return None
    wrong = verify(path, rel, root)
    if wrong:
        if rejected is not None:
            rejected.append(wrong)
        return None
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(path, dest)
    return rel


def why_not(path, root=None):
    """Why a file was not imported, as a code the wizard words: 'missing', 'not-pdf' (a saved web or verification
    page), 'not-listed' (some other PDF); None when it is a listed paper that is already in place."""
    if not os.path.isfile(path):
        return "missing"
    if not is_pdf(path):
        return "not-pdf"
    return None if match(path, root) else "not-listed"


def import_files(paths, root=None, rejected=None, skipped=None):
    """Import the given files (e.g. picked in a file dialog). `skipped` collects (file name, why_not code)."""
    got = []
    for path in paths:
        rel = import_file(path, root, rejected) if is_pdf(path) else None
        if rel:
            got.append(rel)
        elif skipped is not None and (reason := why_not(path, root)):
            skipped.append((os.path.basename(path), reason))
    return got


def import_dir(folder, root=None, rejected=None, skipped=None):
    """Import every .pdf in `folder` (not its subfolders). Raises OSError when the folder cannot be read
    (macOS: the app was not allowed into Downloads)."""
    names = [n for n in sorted(os.listdir(folder)) if n.lower().endswith(".pdf")]
    return import_files([os.path.join(folder, n) for n in names], root, rejected, skipped)


def main(args):
    if len(args) > 1 and args[0] == "--from":
        for rel in import_dir(args[1]):
            print("ok  ", rel)
    else:
        for rel, url, _, _ in missing(optional=True):
            try:
                download(rel, url)
                print("ok  ", rel)
            except Exception as e:
                print("MISS", rel, f"({type(e).__name__}: {e})")
    left = missing(optional=True)
    print(f"\n{len(left)} file(s) missing")
    for _, _, official, _ in left:
        print(official)
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
