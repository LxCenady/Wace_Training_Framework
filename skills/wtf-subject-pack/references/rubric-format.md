# Structured awards — working design for non-tick marking keys

Status: `tools/rubric.py` implements and tests the scoring algebra and diagnostic atomic coverage.
The Chemistry handler, pack validation and database/UI integration are still pending. This document
does not establish that a Chemistry pack is usable. Existing mathematics rows remain intact.

## Separate knowledge from the operation being scored

Each award carries two sets of references: atomic knowledge IDs and pattern/operation IDs, both defined
in the subject catalogue. A subject's broad topic tree is a navigation view over these references.
Award tags are the source of part/question tags; do not infer award tags from the words in a stem or
divide the whole part's marks equally among all its patterns.

The same two-mark criterion can assess two atoms: both have a potential coverage of two marks,
but together the criterion still earns at most two. Coverage values are overlapping diagnostic
projections, never a partition of question marks. Calculate each projection through the original
sum/best/select tree with its caps, so mutually exclusive routes cannot inflate a pattern's maximum.
Prerequisites may be fulfilled without contributing marks to the projected atom. Do not interpret
potential coverage as observed mastery or automatically allocate partial criterion credit to atoms.
Until the key defines separate conditions, a multi-mark criterion stays indivisible for attribution.

IDs are stable within a subject/year/section/question/part. The source location is separate from the ID:
replacing a page crop must not renumber the knowledge or the award. Table responses with no printed
letter receive documented stable response IDs, retaining their connection to the whole unpartitioned question.

## Preserve a scoring tree, not a flat list

Each part has its printed maximum and one scoring root. A node is one of:

| Kind | Meaning | Maximum |
| --- | --- | --- |
| `award` | One rubric criterion or explicitly grouped response | `max_marks`; optional original positive band |
| `sum` | Children may accumulate | Sum of child maxima, restricted by an explicit cap if present |
| `best` | Alternative complete routes sharing one score | Maximum of child route maxima, not their sum |
| `select` | Any N distinct accepted choices | Sum of the largest N child maxima, restricted by the group cap |

Every node has an ID. Children are owned by one parent; shared awards belong outside alternative routes,
not duplicated into each route. Dependencies and conditional caps are explicit references to node IDs.
Reject duplicate IDs, dangling references, cycles, unknown kinds, invalid marks and a root maximum that
does not equal the printed part maximum. Never repair a mismatch by inventing or truncating awards.

An `award` worth two marks can remain a two-mark criterion. Split it only when the key actually defines
separate rewarded conditions. A structure criterion with partial-credit rules is not two identical rows.
A positive `1–2` key band describes credited responses; an unmet award may still earn zero.
`Total` and `Subtotal` label group maxima; they are never additional awards.

Example (invented generic metadata, not a transcription of an exam):

```json
{
  "part": "b",
  "printed_marks": 2,
  "root": {
    "id": "b-choices",
    "kind": "select",
    "take": 2,
    "cap": 2,
    "children": [
      {"id": "b-observation", "kind": "award", "max_marks": 1,
       "knowledge": ["concept-observation"], "patterns": ["describe-evidence"]},
      {"id": "b-comparison", "kind": "award", "max_marks": 1,
       "knowledge": ["concept-comparison"], "patterns": ["compare-data"]},
      {"id": "b-limit", "kind": "award", "max_marks": 1,
       "knowledge": ["concept-limitation"], "patterns": ["evaluate-method"]}
    ]
  }
}
```

## Conditions and reviewing answers

Keep authored condition IDs and the affected node/cap together. A condition requiring a diagram judgment
or chemical interpretation is a review condition, not executable code supplied by a pack. An API can
propose whether it holds, but the record retains the proposal, evidence and review state. Never evaluate
pack strings as Python, shell commands, SQL or regex programs.

Scoring an attempt retains credited awards and the selected route/choices. A whole-question percentage
comes from the scoring tree, then whole-paper weights come from `tools/scoring.py`. For statistics,
alternative-route coverage must not be advertised as simultaneously attainable marks. An unreviewed
condition/route yields an unresolved result, rather than an invented definitive total.

Runtime API: `validate(root, printed_marks)` checks ownership, dependency cycles and maxima;
`score(root, credits, conditions)` returns lower/upper bounds and `earned: null` when those bounds
differ; `coverage(root, 'knowledge' | 'patterns')` returns non-additive potential coverage.
Unlisted award credits mean zero (a finalized credit input, not an unfinished assessment).
`requires` means positive credit on every referenced node. `conditions` gate a node on reviewed
booleans; `conditional_caps` apply their caps when their condition is true. Missing relevant
judgments propagate uncertainty. Conditions are inert IDs, not expressions. Store selected routes,
credit evidence and review status at the attempt layer; the algebra alone does not prove them.

## Source and visual evidence

Local evidence stores source PDF identity/hash, page number convention, region, original rubric text,
image crops, transcription confidence, source inconsistencies and review status. Linked question/context
regions include apparatus, structural formulae, axes, captions and continued pages. Page-level location
alone does not prove a diagram crop is complete.

The distributable `marktags` contains authored IDs, tags, grouping/caps, source references and review
metadata only. It must not embed official rubric text, official diagrams, source PDFs or rendered crops.
The installed framework reconstructs source content from the user's locally fetched originals. Any source
change/hash discrepancy invalidates the matching evidence until it has been reviewed.

MC may remain a section-only block: it participates in whole-paper weighting but has no atomic awards
or SA/ER pattern statistics. Partial SA/ER practice must not become a complete-paper result.

## Evidence needed before implementation acceptance

Use real key examples of any-N, complete alternative routes, shared conditions, structure bands,
conditional caps, nested subtotals and diagram scoring. Check part/question/section printed maxima and
sample the images independently. Keep official source discrepancies visible, retaining the ratified key
and the conflicting evidence separately. Then prove zero mathematical row differences and run all
application checks before committing a new handler/storage/UI integration.
