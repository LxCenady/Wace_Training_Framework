# Subject profiles — what differs between subjects, and where the code assumes maths

Fill the profile in stage 0 and keep it in `<S>/README.md`; it becomes `pack.json` (pack-format.md) at the end.

## The assumptions table

| Question | MAM / MAS / MAA (current) | Chemistry — first draft, **verify against a real paper cover and the syllabus** |
|---|---|---|
| Papers per year | 2 files each: Exam + MarkingKey per section | 1 exam booklet + 1 marking key (single paper) |
| Sections | Calculator-free `F` (50 min + 5 reading), Calculator-assumed `A` (100 + 10) | Section One multiple choice, Two short answer, Three extended answer; ~180 min + 10 reading; shares about 25/35/40 % |
| Question numbering | restarts per section file | runs 1…N through the booklet (MC 1–25 then written) |
| Part labels | (a)(b)…, (i)(ii)…, "(n marks)" after each | (a)(b)(i)…, marks often printed as "(n marks)" — check; MC has no parts |
| Key style | tick glyph per mark under "Specific behaviours" | description / marks tables ("Description · Marks"), "any two of…", MC answer grid, equations marked per species/state |
| Sheets | formula sheet (MAA 2016: "Formulae and Data sheet") | Chemistry data booklet (periodic table, constants, solubility, E° table) |
| Answer checking for generated questions | SymPy value check | numeric stoichiometry/equilibrium/pH with significant figures and units; equation balance (atoms + charge); rubric check for explanations |
| Figures | graphs, networks, tables | structural formulae, apparatus, titration/energy curves, spectra |
| "Draw" parts (`partmarks.SKETCH`) | sketch/draw/plot/shade/mark | draw structural formula, draw/complete the diagram, label, sketch the curve |
| Topic grouping | syllabus units → 6–7 topics each | Units 3–4: equilibrium, acids & bases, redox/electrochemistry, organic structure & reactions, synthesis/polymers, science inquiry |
| Examination reports | yes, per year | yes |
| Copyright | SCSA; not redistributed | same |

Chemistry specifics to settle with the user before coding:
- MC questions: one tag each, one mark each; store them as questions with no parts, section `MC`. The bank/search
  UI should let MC be filtered out of "practice" lists or shown as a quick quiz.
- Extended-answer marking: rubric lines (not ticks) become `points`; `points_ok` means rubric marks sum to the
  printed marks.
- Patterns: still "what the student is asked to do" (e.g. *write a balanced half-equation*, *predict the shift
  using Le Châtelier and justify*, *calculate pH of a buffer*, *identify functional group from data*), 8–16 per topic.
- Science inquiry skills questions span topics — expect many more cross-topic tags than MAA's 6/138.

## Where the assumptions live in code (generalise these, keep maths byte-identical)

Sections `CalcFree`/`CalcAssumed`, CF/CA labels, 50/100-minute timers:
`app/plugins/store.py`, `export_pdf.py`, `external_store.py`, `generator.py`, `llm_mock.py`, `ui_exam.py`
(`TIMES`, `SEC_NAME`), `ui_explain.py`, `ui_external.py`, `ui_generate.py`, `ui_mybank.py`, `ui_pattern.py`,
`ui_question.py`, `ui_search.py`, `ui_tree.py`, `ui_workspace.py` (`SEC`, `SEC_NAME`, `TIMES`, CA/CF meters in
出卷模式); tools `build_db.py` (`SECTION`), `segment.py` (one exam file per section), `paperid.py`
(section from "calculator-free/assumed"), `audit_totals.py` (section-total regex), `blueprint.py`.

Subject lists: `store.SUBJECT_NAMES`, `ui_setup.SUBJECTS` (duplicate — merge), `generator.SUBJECT`,
`build_docs.TOPICS`, `paperid.identify` titles, `fetch.subjects()`.

Marking: `markpoints.py` (ticks only), `partmarks.py` (`TOKEN`, `SKETCH`, `FIGURE`), generator SymPy step and
its prompts (LaTeX/figure JSON schema mention SymPy curves), `ui_formula` (formula sheet).

Approach: one small `subjects` module that loads every installed `<S>/pack.json` (maths subjects ship theirs),
exposing `names()`, `topics(S)`, `sections(S)`, `key_parser(S)`, `checker(S)`; every place above asks it
instead of its own dict. Do it as a separate commit, then prove non-regression: rebuild, compare MAM/MAS/MAA
rows, run all tests (`app/tests/*`), screenshot the exam and workspace panels.
