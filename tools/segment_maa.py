"""Segment only validated MAA exam/key pairs, leaving the live database untouched."""
import json
import os

import fetch_maa
import segment


def main():
    root = fetch_maa.ROOT
    records = []
    for rel, _, _ in fetch_maa.sources():
        if "_Exam_" not in rel:
            continue
        key = rel.replace("_Exam_", "_MarkingKey_")
        try:
            fetch_maa.validate(root / rel, rel)
            fetch_maa.validate(root / key, key)
        except Exception as exc:
            print("SKIP", rel, str(exc))
            continue
        edoc, eh, es, eb = segment.scan(str(root / rel))
        kdoc, kh, ks, kb = segment.scan(str(root / key))
        try:
            er = segment.regions(eh, es, eb, len(edoc))
            kr = segment.regions(kh, ks, kb, len(kdoc))
            year, _, _, section = os.path.basename(rel).removesuffix(".pdf").split("_")
            for q, _, _, marks in eh:
                records.append(dict(subject="MAA", year=year, section=section, q=q, marks=marks,
                                    exam=rel, exam_regions=er[q], key=key, key_regions=kr.get(q, []),
                                    text=segment.text_of(edoc, er[q])))
        finally:
            edoc.close()
            kdoc.close()
    path = root / "MAA/questions.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("MAA", len(records), "questions from validated pairs")


if __name__ == "__main__":
    main()
