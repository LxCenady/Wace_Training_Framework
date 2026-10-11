"""Fetch/import MAA PDFs from its independent manifest; never build the live database."""
import argparse
from pathlib import Path
import re
import sys

import pymupdf
import fetch

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "tools/sources_MAA.tsv"


def sources():
    rows = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        rel, url = line.split("\t")
        archived = url.endswith(" (wayback)")
        official = url.removesuffix(" (wayback)")
        if not re.fullmatch(r"MAA/papers/20\d\d_MAA_(?:ExamReport|(?:Exam|MarkingKey)_Calc(?:Free|Assumed))\.pdf", rel):
            raise ValueError(f"Unexpected destination: {rel}")
        rows.append((rel, fetch.WAYBACK + official if archived else official, official))
    if len({row[0] for row in rows}) != len(rows):
        raise ValueError("Duplicate manifest destination")
    return rows


def validate(path, rel):
    """Check content identity, not merely a PDF header or a downloaded filename."""
    with open(path, "rb") as stream:
        stream.seek(max(0, Path(path).stat().st_size - 1024))
        if b"%%EOF" not in stream.read():
            raise ValueError(f"Truncated PDF (no end marker): {rel}")
    with pymupdf.open(path) as doc:
        if not len(doc):
            raise ValueError(f"Empty PDF: {rel}")
        text = " ".join(doc[i].get_text() for i in range(min(2, len(doc))))
    text = " ".join(text.lower().split())
    year = Path(rel).name[:4]
    if "mathematics applications" not in text:
        raise ValueError(f"Subject mismatch: {rel}")
    if "ExamReport" in rel:
        found = re.search(r"(20\d\d)\s+atar course examination report", text)
        if not found or found.group(1) != year:
            raise ValueError(f"Report year/type mismatch: {rel}")
    else:
        found = re.search(r"(?:atar course |wace )?examination,?\s+(20\d\d)", text)
        if not found or found.group(1) != year:
            raise ValueError(f"Examination year/type mismatch: {rel}")
        section = "calculator-free" if "CalcFree" in rel else "calculator-assumed"
        if section not in text:
            raise ValueError(f"Section mismatch: {rel}")
        is_key = bool(re.search(r"marking\s*key", text))
        if is_key != ("MarkingKey" in rel) or "sample" in text:
            raise ValueError(f"Exam/key/sample mismatch: {rel}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from", dest="folder", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--years", nargs="+", type=int)
    parser.add_argument("--archive-year", type=int, help="Use a Wayback snapshot selector instead of the current official site")
    args = parser.parse_args()
    rows = [row for row in sources() if not args.years or int(Path(row[0]).name[:4]) in args.years]
    missed = []
    for rel, url, official in rows:
        dest = ROOT / rel
        try:
            valid = False
            if dest.exists():
                try:
                    validate(dest, rel)
                    valid = True
                except (ValueError, RuntimeError):
                    pass
            if not valid and args.folder:
                for candidate in sorted(args.folder.glob("*")):
                    if candidate.suffix.lower() != ".pdf":
                        continue
                    try:
                        validate(candidate, rel)
                    except (ValueError, RuntimeError):
                        continue
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    import shutil
                    shutil.copyfile(candidate, dest)
                    break
            elif not valid and not args.check:
                if args.archive_year:
                    url = f"https://web.archive.org/web/{args.archive_year}id_/" + official
                staging = rel + ".incoming"
                try:
                    fetch.download(staging, url, root=str(ROOT), tries=2, timeout=25)
                    validate(ROOT / staging, rel)
                    (ROOT / staging).replace(dest)
                finally:
                    (ROOT / staging).unlink(missing_ok=True)
                    (ROOT / (staging + ".part")).unlink(missing_ok=True)
            if not dest.exists():
                raise FileNotFoundError("Not imported")
            validate(dest, rel)
            print("OK", rel)
        except Exception as exc:
            missed.append(rel)
            print("MISS", rel, str(exc), "\n ", official)
    print(f"Validated {len(rows) - len(missed)}/{len(rows)} PDFs; missing/invalid {len(missed)}")
    return bool(missed)


if __name__ == "__main__":
    sys.exit(main())
