"""Get the SCSA past papers. One job: sources.tsv -> MAM/papers, MAS/papers.

The papers are © School Curriculum and Standards Authority and are not redistributed in this repo.
  python tools/fetch.py                 try to download every missing file from its official URL
  python tools/fetch.py --from DIR      copy files you downloaded yourself in a browser (matched by URL file name)
The SCSA site sits behind bot protection, so direct downloads may be refused (HTTP 403); then open the
printed URLs in a browser, save them into one folder, and run --from on that folder.
"""
import os, shutil, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sources():
    for line in open(os.path.join(ROOT, "sources.tsv"), encoding="utf-8"):
        if line.strip():
            path, url = line.rstrip("\n").split("\t")
            yield path, url


def is_pdf(path):
    with open(path, "rb") as f:
        return f.read(5) == b"%PDF-"


def main(args):
    local = args[1] if len(args) > 1 and args[0] == "--from" else None
    missing = []
    for path, url in sources():
        dest = os.path.join(ROOT, path)
        if os.path.exists(dest) and is_pdf(dest):
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            if local:
                name = urllib.parse.unquote(url.rsplit("/", 1)[-1])
                src = next((os.path.join(local, f) for f in os.listdir(local) if f.lower() == name.lower()), None)
                if not src:
                    raise FileNotFoundError(name)
                shutil.copyfile(src, dest)
            else:
                req = urllib.request.Request(url, headers={"user-agent": "Mozilla/5.0 (WTF fetch.py)"})
                with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
                    shutil.copyfileobj(r, f)
            if not is_pdf(dest):
                os.remove(dest)
                raise ValueError("not a PDF")
            print("ok  ", path)
        except Exception as e:
            missing.append((path, url))
            print("MISS", path, f"({type(e).__name__}: {e})")
    print(f"\n{len(missing)} file(s) missing")
    for path, url in missing:
        print(url)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
