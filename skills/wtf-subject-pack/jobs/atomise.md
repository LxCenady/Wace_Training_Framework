# Job: atomise — patterns and knowledge atoms of one topic, from its labelled awards

Strong model only (you, or the strongest available). The catalogue decides every statistic and every note
downstream; the user signs it off before `assign` runs.

Two separate lists come out, because they answer different questions:
- **Patterns** (题型) — *what the student is asked to do*, recognisable from the question and with a recognisable
  mark scheme. The notes are written per pattern. 6–16 per topic.
- **Knowledge atoms** (知识点) — the smallest pieces of course content a mark depends on. Statistics of weakness
  and coverage use them. Usually 8–30 per topic.
An award gets one pattern (rarely two) and 1–3 knowledge atoms.

## Input `{"subject", "course", "topic": {"code", "name"}, "syllabus": "...", "labels": [...], "existing": {...}}`

`labels`: every labelled award of the topic: `{id, marks, skill, operation, knowledge, part_stem (short)}`.
`existing`: the current catalogue's patterns of this topic, if there is one — keep a pattern's number and meaning
when it still fits, so earlier tags and notes stay valid.

## Output `{"topic": "RX", "patterns": [...], "knowledge": [...], "unplaced": [...]}`

```json
{"id": "RX3", "name_en": "Write and balance redox half-equations", "name_zh": "写并配平氧化还原半反应",
 "definition": "what a part must ask for to get this pattern",
 "not": "near-misses that belong to another pattern, with its id",
 "operations": ["write-equation"], "members": ["2022E-37-a-3", "2022E-37-a-4", "..."]}
```
```json
{"id": "RX.K4", "name_en": "Half-equations in acidic solution", "name_zh": "酸性条件半反应",
 "definition": "one sentence", "syllabus": "the syllabus point it comes from"}
```
- Pattern ids `<TOPIC><n>` numbered from 1 in teaching order; atom ids `<TOPIC>.K<n>`.
- Build from the evidence: group awards whose `skill`/`operation` ask for the same performance; a pattern with
  under 3 awards across all years is merged into a neighbour unless it is a whole syllabus point.
- `members`: the ids of the input awards in this pattern. Every input award id appears in exactly one pattern's
  `members` or in `unplaced` (`{"id", "reason"}`) — `check` verifies this and computes each pattern's marks and
  years from the members, so never write counts yourself.
- Write `definition` and `not` carefully: reviewers cite them, and most later disputes are boundary cases.
