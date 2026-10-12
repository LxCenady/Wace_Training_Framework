# Job: split — divide a part's marking key into its awards

`tools/awards.py` turns each key into awards (one scoring criterion each). For some parts the parser's awards do
not add up to the marks printed on the paper — tables broken across pages, alternative solutions, "any two of",
answers drawn in the key. You read the key and write the part's awards yourself.

## Input `{"subject", "course", "items": [...]}`, one item per part

```json
{"id": "2018E-35-0", "question": "2018E-35", "label": "", "marks": 16,
 "stem": "the part's text from the exam", "key_text": "the whole question's key, as extracted",
 "parser_awards": [{"marks": 1, "text": "..."}]}
```
`label` "" means an unpartitioned question; `key_text` holds every part of the question — use only this part's.

## Output `{"items": [...]}`

```json
{"id": "2018E-35-0", "awards": [{"n": 1, "marks": 1, "kind": "award", "text": "states that ... (own words)"}],
 "structure": "sum", "take": null, "confidence": 0.85, "note": ""}
```
- `awards`: the criteria in key order, `n` from 1. `marks` sum to the part's `marks` **exactly**.
- `kind`: `award` (one criterion), `choice` (one accepted option of an "any N" list).
- `structure`: `sum` (marks accumulate), `any` (any `take` of the `choice` awards count — then the choice awards'
  marks sum to more than the part's marks and `take` × choice mark = the part's marks), `best` (alternative full
  methods — list only the first method's awards and say so in `note`).
- `text`: what the student must write/do to earn it, ≤ 25 words, your own words; a drawn answer is
  `"draws ... (drawn answer, see key image)"`.
- A key row worth 2+ marks stays one award of 2+ marks unless the key itself lists separate conditions.
- `Total` / `Subtotal` rows are sums, never awards. "Alternatively …" rows belong to `best`.
- If the key text for this part is missing or unreadable: `"awards": []`, confidence 0, `note` saying what is missing.
