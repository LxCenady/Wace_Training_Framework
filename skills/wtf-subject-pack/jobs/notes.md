# Job: notes — the English pattern notes of one topic

English is written first; Chinese is translated from it (job translate). The app shows these notes beside every
question of the pattern, so they are what a student studies — practical, specific, exam-shaped.

## Input `evidence/<s>/flow/notes/in/<topic>.json`

`{"subject", "course", "topic": {"code", "file", "name"}, "patterns": [...]}`, per pattern:
`{"n", "id", "name_en", "definition", "stats": {"years_seen", "years", "parts", "marks", "mean_marks",
"share_of_paper"}, "parts": [{"ref": "2022 ER Q37(a)", "marks", "stem", "awards": ["..."]}], "reports": ["..."]}`
— everything you may use. Do not invent facts that the evidence does not support.

## Output: Markdown, exactly this shape (the app parses it)

```
# <S> · <Topic name> — Question Patterns and Methods

> Based on <n> past-exam parts, <years>, their marking keys and the examiners' reports.

## First: where marks are lost most
- 3–6 bullets, the most frequent lost marks across the topic, each tied to a report or a key criterion.

---

## Pattern 1: <title>

**How often**: <years_seen>/<years> papers · <mean_marks> marks when it appears · <share_of_paper> of a paper.

**Recognise it**: the wording and set-ups that signal this pattern.

**Method**
1. numbered steps a student follows, in exam order;
2. ...

**What the key rewards**: the typical awards, in the key's order, in your own words, one per mark.

**Common errors**: from the reports and from the awards students miss.

**Past questions**: 2022 ER Q37(a), 2019 SA Q30(b), …  (every part in the input, newest first)

---
```
- One `## Pattern N: title` per input pattern, N = its number, in order, none skipped or added.
- Quote nothing longer than a short phrase from the keys or reports; paraphrase.
- Use the course's notation and units. Maths in plain Unicode or `$…$` inline LaTeX.
