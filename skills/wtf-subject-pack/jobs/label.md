# Job: label — what each mark point assesses

The unit of every statistic in WTF is the award: one criterion of the marking key that earns marks. Before any
catalogue exists, each award is described from the bottom up — what the student had to *do* to earn it and which
pieces of course *knowledge* it needed. These descriptions are later clustered into patterns and knowledge atoms
(job atomise), so they must be generic: two awards testing the same thing in different questions should get the
same words.

## Input `{"subject", "course", "syllabus_topics": {...}, "items": [...]}`

```json
{"id": "2022E-37-a-3", "marks": 1, "award": "reduction half equation has correct species",
 "part_stem": "the part's question text", "question_context": "the question's opening text, shortened"}
```

## Output `{"items": [...]}`, one per input item

```json
{"id": "2022E-37-a-3", "topic": "RX",
 "skill": "write a reduction half-equation in acidic solution",
 "operation": "write-equation",
 "knowledge": ["half-equations", "redox in acidic solution"],
 "confidence": 0.9, "note": ""}
```
- `topic`: one code from `syllabus_topics` — the unit whose knowledge earns the mark (not where the story is set).
- `skill`: ≤ 12 words, starts with a verb, **generic** — no numbers, compounds or contexts from this question
  unless the skill is about that substance class ("name an ester", fine; "calculate moles of Mg", no → "calculate
  amount in moles from mass").
- `operation`: exactly one of
  `recall` `define` `identify` `name` `describe` `explain` `compare` `predict` `calculate` `write-equation`
  `draw` `interpret-data` `design-method` `evaluate` `state-units` `show-working` `justify-choice`
  (maths subjects also: `differentiate` `integrate` `solve` `sketch-graph` `prove` `model` `use-calculator`).
- `knowledge`: 1–3 atomic concept names, ≤ 5 words each, the syllabus's own nouns ("Le Chatelier's principle",
  "conjugate acid-base pairs", "chain rule"). Atomic = cannot be split into two things a student could know separately.
- An award for communication only (units, significant figures, "shows working") still gets its real topic, the
  operation `state-units`/`show-working`, and the knowledge it applies to.
- A multi-mark award listing options ("any four of …") → describe what the options have in common; list up to 3
  knowledge atoms across the options.
- Multiple-choice awards ("Answer: c"): read the part stem to see what it tests.
