# Job: assign — catalogue codes for each award

With the approved catalogue, every award gets its pattern and knowledge atoms. A part's patterns are then the
patterns of its awards, and a pattern's marks are the marks of its awards — no more splitting a part's marks
evenly among its tags.

## Input `{"subject", "catalogue": {"patterns": [...], "knowledge": [...]}, "items": [...]}`

```json
{"id": "2022E-37-a-3", "marks": 1, "award": "...", "part_stem": "...",
 "label": {"topic": "RX", "skill": "...", "operation": "...", "knowledge": ["..."]}}
```
`label` is the earlier bottom-up description; use it as a hint, not as the answer.

## Output `{"items": [...]}`

```json
{"id": "2022E-37-a-3", "patterns": ["RX3"], "knowledge": ["RX.K4"], "confidence": 0.9, "note": ""}
```
- `patterns`: one code, two only when the award itself needs both performances; codes from the catalogue only.
- `knowledge`: 1–3 atom codes from the catalogue.
- Decide by the catalogue's `definition` and `not` — cite the deciding phrase in `note` when confidence < 0.8.
- If no pattern fits: `"patterns": []`, confidence 0, and `note` says which definition is missing.
