"""Audit MAA source pairs, segmentation and reviewed labels without writing any database."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

import fetch_maa
import partmarks
import segment

ROOT = fetch_maa.ROOT


def audit(labels=None, years=None):
    errors, missing, invalid, valid = [], [], [], set()
    scope = set(years or range(2016, 2026))
    if not scope or not scope <= set(range(2016, 2026)):
        raise ValueError("Years must be within 2016–2025")
    sources = [row for row in fetch_maa.sources() if int(Path(row[0]).name[:4]) in scope]
    expected_core = {f"MAA/papers/{year}_MAA_{kind}_{section}.pdf"
                     for year in scope for kind in ("Exam", "MarkingKey")
                     for section in ("CalcFree", "CalcAssumed")}
    if not expected_core <= {row[0] for row in sources}:
        errors.append("Manifest does not cover all core PDFs in scope")
    for rel, _, _ in sources:
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        try:
            fetch_maa.validate(path, rel)
            valid.add(rel)
        except Exception as exc:
            invalid.append({"path": rel, "error": str(exc)})
    qpath = ROOT / "MAA/questions.json"
    records = json.loads(qpath.read_text(encoding="utf-8")) if qpath.exists() else []
    records = [q for q in records if int(q["year"]) in scope]
    catalogue = json.loads((ROOT / "tools/catalogue_MAA.json").read_text(encoding="utf-8"))
    patterns = {p["id"] for p in catalogue["patterns"]}
    topics = set(catalogue["topic_codes"])
    by_id, groups, part_conflicts = {}, defaultdict(list), []
    for record in records:
        ident = (str(record["year"]), record["section"], record["q"])
        if ident in by_id:
            errors.append(f"Duplicate question {ident}")
        by_id[ident] = record
        groups[ident[:2]].append(record)
        if record["subject"] != "MAA" or record["exam"] not in valid or record["key"] not in valid:
            errors.append(f"Invalid source identity/pair {ident}")
        if not record["exam_regions"] or not record["key_regions"]:
            errors.append(f"Missing regions {ident}")
        if not isinstance(record["marks"], int) or record["marks"] <= 0:
            errors.append(f"Invalid marks {ident}")
        found = partmarks.split(record["text"], record["marks"])
        if found is None:
            part_conflicts.append(list(ident))
    totals = []
    for rel in valid:
        if "_Exam_" in rel and rel.replace("_Exam_", "_MarkingKey_") in valid:
            year, _, _, section = Path(rel).stem.split("_")
            if (year, section) not in groups:
                errors.append(f"Validated paper omitted from segmentation {year} {section}")
    for (year, section), questions in sorted(groups.items()):
        numbers = sorted(q["q"] for q in questions)
        if numbers != list(range(numbers[0], numbers[-1] + 1)):
            errors.append(f"Question sequence gap {year} {section}")
        exam = ROOT / questions[0]["exam"]
        key = ROOT / questions[0]["key"]
        edoc, heads, _, _ = segment.scan(str(exam))
        kdoc, kheads, _, _ = segment.scan(str(key))
        try:
            expected = {h[0]: h[3] for h in heads}
            keymarks = {h[0]: h[3] for h in kheads}
            if set(numbers) != set(expected) or set(expected) != set(keymarks):
                errors.append(f"Exam/key question coverage differs {year} {section}")
            for question in questions:
                if question["marks"] != keymarks.get(question["q"]):
                    errors.append(f"Exam/key marks differ {year} {section} q{question['q']}")
            totals.append({"year": year, "section": section, "questions": len(questions),
                           "exam_marks": sum(q["marks"] or 0 for q in questions),
                           "key_marks": sum(m or 0 for m in keymarks.values())})
        finally:
            edoc.close()
            kdoc.close()
    labelled, reviewed, pending = set(), set(), []
    manual_checks = []
    part_count = 0
    for label in labels or []:
        if int(label["year"]) not in scope:
            continue
        ident = (str(label["year"]), label["section"], label["q"])
        if ident in labelled:
            errors.append(f"Duplicate label {ident}")
        labelled.add(ident)
        question = by_id.get(ident)
        if not question:
            errors.append(f"Unknown labelled question {ident}")
            continue
        if not set(label.get("topics", [])) <= topics or not label.get("topics"):
            errors.append(f"Invalid/empty topics {ident}")
        parts = label.get("parts", [])
        names = [p["label"] for p in parts]
        if len(names) != len(set(names)) or sum(p.get("marks", 0) for p in parts) != question["marks"]:
            errors.append(f"Part labels/marks conflict {ident}")
        found = partmarks.split(question["text"], question["marks"])
        if found is not None:
            actual = {p["label"].replace("-", ""): p["marks"] for p in parts}
            if partmarks.for_tags(found, actual) != actual:
                if (label.get("primary_reviewed") and label.get("manual_part_marks") == actual
                        and label.get("manual_part_marks_reason")
                        and label.get("key_total") == question["marks"]):
                    manual_checks.append({"question": list(ident), "parser_marks": found,
                                          "verified_marks": actual, "reason": label["manual_part_marks_reason"]})
                else:
                    errors.append(f"Printed part coverage/marks conflict {ident}")
        for part in parts:
            tags = part.get("tags", [])
            if not tags or not set(tags) <= patterns or len(tags) != len(set(tags)) or not part.get("reason"):
                errors.append(f"Invalid tags/reason {ident} {part.get('label')}")
        part_count += len(parts)
        if label.get("needs_review") or label.get("flags") or any(p.get("confidence") == "pending" for p in parts):
            pending.append(list(ident))
        if label.get("primary_reviewed"):
            reviewed.add(ident)
    review_coverage = []
    for group, questions in sorted(groups.items()):
        count = sum((str(q["year"]), q["section"], q["q"]) in reviewed for q in questions)
        required = (len(questions) + 4) // 5
        review_coverage.append({"year": group[0], "section": group[1], "reviewed": count, "required": required})
    review_ok = all(row["reviewed"] >= row["required"] for row in review_coverage)
    return {"years": sorted(scope), "expected_core_pdfs": len(expected_core), "valid_pdfs": len(valid), "missing": missing, "invalid": invalid,
            "questions": len(records), "labelled_questions": len(labelled & by_id.keys()), "labelled_parts": part_count,
            "unlabelled": [list(i) for i in sorted(by_id.keys() - labelled)], "pending": pending,
            "primary_reviewed": len(reviewed), "part_mark_conflicts": part_conflicts,
            "manual_part_mark_checks": manual_checks,
            "review_coverage": review_coverage,
            "paper_totals": totals, "errors": errors,
            "complete": not (missing or invalid or errors or pending or part_conflicts or by_id.keys() - labelled)
                        and bool(records) and review_ok}


def export_tags(labels, report):
    """Export original annotations only. Explicitly partial; no question text or answer content."""
    if report["errors"]:
        raise ValueError("Fix audit errors before exporting annotations")
    pending = {tuple(row) for row in report["pending"]}
    topic_rows, part_rows = defaultdict(list), []
    for label in sorted(labels, key=lambda row: (int(row["year"]), row["section"], row["q"])):
        ident = (str(label["year"]), label["section"], label["q"])
        if ident in pending:
            continue
        paper = str(label["year"]) + ("F" if label["section"] == "CalcFree" else "A")
        topic_rows[paper].append(str(label["q"]) + ":" + ",".join(label["topics"]))
        parts = " ".join((part["label"] or "-") + "=" + "+".join(part["tags"]) for part in label["parts"])
        part_rows.append(f"{paper} {label['q']} {parts}")
    header = "# MAA original annotations; PARTIAL until audit complete=true. See MAA/README.md.\n"
    (ROOT / "tools/tags_MAA.txt").write_text(header + "\n".join(paper + " " + " ".join(rows)
                                              for paper, rows in sorted(topic_rows.items())) + "\n", encoding="utf-8")
    (ROOT / "tools/parttags_MAA.txt").write_text(header + "\n".join(part_rows) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels", type=Path)
    parser.add_argument("--out", type=Path, default=ROOT / "evidence/maa/audit.json")
    parser.add_argument("--export-partial", action="store_true", help="Export non-pending annotations even if some papers are missing")
    parser.add_argument("--years", nargs="+", type=int, help="Audit selected years only; export still requires the full audit")
    args = parser.parse_args()
    labels = json.loads(args.labels.read_text(encoding="utf-8")) if args.labels else []
    if args.years and args.export_partial:
        parser.error("Use a full audit to export, so existing years are not overwritten")
    report = audit(labels, args.years)
    if args.export_partial:
        export_tags(labels, report)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["valid_pdfs", "questions", "labelled_questions", "primary_reviewed", "complete"]}))
    print(f"Missing {len(report['missing'])}; invalid {len(report['invalid'])}; errors {len(report['errors'])}")
    return 0 if report["complete"] else 1


if __name__ == "__main__":
    sys.exit(main())
