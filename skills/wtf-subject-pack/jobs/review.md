# Job: review — an independent second assignment

Same input and output as [assign](assign.md), on a sample chosen by `flowjobs.py` (every topic, every
low-confidence award, about 20% of the rest). You do **not** see the first assignment. Do the job from scratch.

This job is also sent directly to API models, which cannot open the linked file. Its complete output schema is:

```json
{"items": [{"id": "2022E-37-a-3", "patterns": ["RX3"], "knowledge": ["RX.K4"], "confidence": 0.9, "note": ""}]}
```

- Use the top-level key `items`, and the plural array key `patterns` for every item; do not use `assignments` or `pattern`.
- Return every input award id exactly once. Pattern and knowledge codes must exist in the supplied catalogue.
- Choose one task pattern; use two only if this awarded criterion itself requires both performances. Choose 1–3 concept atoms.
- The previous bottom-up label is a hint. Decide independently from the original award, part stem, verified source context and catalogue `definition`/`not`.
- Confidence must be between 0 and 1. Below 0.8, cite the deciding definition or explain the missing source evidence in `note`.
- Preserve alternatives as alternatives. Unit, substitution and significant-figure criteria follow the substantive task as specified by the catalogue.
- If no task definition fits, return an empty `patterns` array and confidence 0 with an explicit coverage-gap note. This fails the completion gate and must be resolved through catalogue review, not by inventing a code.

`flowjobs.py check <S> review` compares the two: agreement per pattern and per topic is reported, and every
disagreement becomes an arbitration item for the strong model (you), who decides with the catalogue and the key,
and fixes the catalogue's `definition`/`not` when a boundary caused it. If more than 10% of the sample disagree on
the pattern, the catalogue is not ready: fix the definitions and re-run `assign` for the affected topic.
