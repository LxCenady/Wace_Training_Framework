---
name: wtf-subject-pack
description: Turn a WACE ATAR subject's SCSA past papers into a WTF (Wace Training Framework) data pack — sources manifest, segmented questions, pattern catalogue, per-part tags, marks, mark points, bilingual 解题思路 notes, cheat sheet, question-generation skill and app integration — the workflow that took MAA from zero to MAM/MAS parity. Use this whenever the user wants to add a new subject to WTF (化学 Chemistry, Physics, Biology, another maths course…), says 接入/加入/做一个新学科/学科数据包/数据化, asks how far a subject is from "parity" with MAM/MAS, or resumes an unfinished subject pack — even if they don't name this skill.
---

# WTF subject pack — from past papers to a usable subject

A **subject pack** is everything WTF needs to treat a course as a first-class subject: the papers it can
fetch, every question cut out of them with marks and mark points, a pattern catalogue (题型) with every
part tagged, notes per pattern in Chinese and English, a cheat sheet, a question-generation skill with a
real-paper blueprint, and the few app hooks that list the subject. MAM and MAS were built by hand over many
sessions; MAA was the first pack built with this workflow (2026-10), and Chemistry is next.

The repo is `E:\WACE_Maths` (GitHub `LxCenady/Wace_Training_Framework`); `<ROOT>` below means that folder,
the Python is `<ROOT>\.venv\Scripts\python`. Read `<ROOT>\AGENTS.md` (a local file, not in git) first in a new session — it is the
handover and has the current state.

## What "done" means (parity)

A subject is at parity when all of these hold — run `scripts/pack_status.py <SUBJ>` (in this skill) to see
which are missing:

1. Every paper in the manifest is on disk and recognised by `paperid.py`; excluded years are written down with why.
2. `questions.json` has every question, marks sum to each section's printed total (`audit_totals.py`).
3. A pattern catalogue whose codes cover every question; every part of every question is tagged
   (`tools/parttags_<SUBJ>.txt`), with a human/primary review of at least ~20% and an independent second look.
4. Part marks come from the paper; key mark points split one-per-mark and agree per part (`points_ok`), and the
   few that can't are explained (shown as the key image).
5. Notes: one `## 题型 N：title` section per pattern in `<SUBJ>/methods/NN_Topic_解题思路.md`, an English edition
   in `methods_en/`, a review log (`审校记录.md`), all rendered to PDF.
6. A cheat sheet (zh + EN, PDF) and the formula/data sheets in the manifest.
7. `skills/wace-<subj>-questions/` with topic files and a blueprint block written by `tools/blueprint.py`.
8. The app lists the subject (wizard, 管理科目, generator, search, exam, external import) and the full test suite passes,
   with the existing subjects' rows **identical** to before (non-regression).
9. It exports as one `.wtfpack` that a clean WTF imports (题库 → 管理科目 → 导入学科包) and rebuilds into the same rows.

## The pack flow (start here)

Since 2026-10 a subject is built by one flow of six stages. Each stage is its own tool with a gate that checks
something printed on the paper; every step that needs a language model is a **fixed job** (`jobs/*.md`): the same
specification, input and output shape and checks whoever runs it (Haiku subagent, DeepSeek via `flowjobs.py run`,
or you). English comes first everywhere; Chinese is translated from it.

```
python tools/packflow.py <S>          # where the subject stands, and the exact next command
```

| # | Stage | Tool / job | Gate |
|---|---|---|---|
| 1 | **pair** — resource judgement | `packflow.py <S> run pair` (`pairs.py`) | every exam has its own key: covers identify both, same question numbers, same marks; a real source discrepancy is checked by hand and written in `pack.json papers.acknowledged` |
| 2 | **cut** — PDF segmentation and mark points | `run cut` (`segment.py`, `audit_totals.py`, `awards.py`) → job **split** for parts the parser could not divide | section totals; every part's awards add up to its printed marks |
| 3 | **label** — bottom-up, per mark point | job **label** (Haiku) | every award has topic, skill, operation, 1–3 knowledge names |
| 4 | **atomise** — patterns and knowledge atoms | job **atomise** (strong model) → `packflow.py <S> approve` (the user signs off) → job **assign** → job **review** (blind 20%) → `packflow.py <S> export` | every award in one pattern; review agreement ≥ 90%; part tags and question topics are *derived* from award codes |
| 5 | **build** — database and statistics | `run build` → `evidence/<s>/flow/check.db`, `stats.json` | build problems = 0; frequency, marks per appearance, share of a paper, co-occurrence, knowledge coverage |
| 6 | **notes** — English notes, then Chinese | job **notes** → job **translate** → `render_methods.py` | one section per pattern; every cited past question carries that pattern |

AI job cycle, the same for every job:
```
python tools/flowjobs.py tasks  <S> <job>          # input batches (evidence/<s>/flow/<job>/in/)
python tools/flowjobs.py prompt <S> <job> <batch>  # the exact prompt: give it to a Haiku agent unchanged
python tools/flowjobs.py check  <S> <job>          # schema + invariants; low-confidence count
python tools/flowjobs.py merge  <S> <job>          # into the flow's files (refuses while check fails)
```
Run independent batches in parallel (background Haiku agents, one batch each). `atomise` and arbitration of
review disputes need the strong model: do them yourself. Never edit a job's output by hand to pass `check` — fix
the input or the specification and re-run the batch.

Why bottom-up (label → atomise): describing each mark point first and clustering afterwards makes the catalogue
come from what the keys actually reward (cf. LLM knowledge-component generation: Moore et al. 2024, Duan et al.
2025), and a pattern's marks become the marks of its awards instead of a part's marks split by guesswork.

Subjects built before the flow (MAM, MAS, MAA, CHE) keep their reviewed tags; the flow's stages 1–2 run on them as
checks, and stages 3–4 only when the user asks to rebuild a catalogue.

The older stage-by-stage notes below (`references/pipeline.md`) still describe the tools the flow calls.

### The tools behind the flow (reference)

```
sources.tsv ─fetch.py/paperid.py─▶ <S>/papers/*.pdf ─segment.py─▶ <S>/questions.json
                                                      │            (+ partmarks.py: part marks, sketch, figure)
catalogue_<S>.json ──labelling (agents + review)──▶ evidence/<s>/labels.json ─export─▶ tools/(part)tags_<S>.txt
evidence.py ─▶ evidence packs ─writers+reviewers─▶ <S>/methods/*.md ─translate.py─▶ methods_en/ ─render_methods.py─▶ PDFs
build_all.py (segment → build_docs → build_bank → build_db) ─▶ wace.db ─blueprint.py─▶ skills/wace-<s>-questions
```

Besides the six stages, a pack also needs (unchanged): stage 0 subject profile, cheat sheet, the
question-generation skill + `blueprint.py`, app hooks/tests/docs, and `pack.py export` — see below and
`references/pipeline.md` §9–11.

## The deliverable: one pack file

The workflow ends in a single `<S>-<version>.wtfpack`: a zip whose `pack.json` is the index/protocol —
subject profile (names, sections, topics, key style, answer checker, sheets) plus every hand-made file, and only
*references* to the papers (copyright). WTF imports it in one click, fetches the listed papers and builds the subject.
The format, the import/export steps and the list of hard-coded places the app must read from the pack instead are
in `references/pack-format.md` — read it at stage 0 too, because the profile you write there *is* `pack.json`.

## Stage 0: the subject profile (the reserved space)

The maths pipeline assumes things that are *not* true of every WACE subject. Before fetching anything, write
down in `<S>/README.md` how the new subject answers each question below, and tell the user which code paths
will need generalising. `references/subject-profiles.md` has the full list with the current answers for the
three maths courses, a worked first draft for Chemistry, and the code that each assumption lives in.

- **Paper structure**: maths has two papers (Calculator-free / Calculator-assumed, codes `F`/`A`, 50/100 min).
  Chemistry has one paper with Section One multiple choice, Two short answer, Three extended answer.
  `CalcFree/CalcAssumed` is hard-coded in ~15 app files today (listed in the reference) — that is the first
  thing to generalise, behind a per-subject section table, not by adding `if subj == "CHE"` branches.
- **Marking keys**: maths keys put one tick glyph per mark under "Specific behaviours". Other keys use
  description/marks tables, MC answer grids, or "any two of…" lists. `markpoints.py` needs a per-key-style
  parser, chosen by the profile.
- **Sheets**: formula sheet (maths) vs data booklet (Chemistry: periodic table, constants, solubility etc.).
- **Checking generated questions**: SymPy verifies maths answers; Chemistry needs stoichiometry/equilibrium
  arithmetic checks, equation balancing and unit checks instead, and a rubric check for extended answers.
- **Figures**: graphs/networks vs structural formulae, apparatus, titration curves; "draw" parts (sketch
  detection words differ: *draw the structural formula*, *complete the diagram*).
- **Question IDs**: `<S>-<year><section>-Q<n>`; the section letter set comes from the profile.

When the profile needs code changes, propose the smallest generalisation that keeps MAM/MAS/MAA byte-identical
(UNIX philosophy, thin glue, one job per tool — the user cares about this), get the user's go-ahead, and do it as
its own commit *before* the data work, with the non-regression check from stage 8.

## How to run the work

**Divide labour by how much judgment a step needs.** The user's rule: work that does not need intelligence goes
to Haiku (`model: "haiku"` in the Agent tool → claude-haiku-5-5); you keep the catalogue, the review sample,
arbitration and anything touching code. Run independent agents in parallel (one per year range or topic group),
in the background, and keep working while they run. Templates for every delegated job are in
`references/delegation.md` — they carry the constraints each agent must respect (read-only paths, no commits,
evidence fields, confidence scores), which is what made their output usable without rework.

**Never trust a count you did not check.** Every stage has a verification that compares against something
printed on the paper (section totals, "(n marks)", the key's ticks). When an agent reports numbers, spot-check
them; MAA had a "96 patterns" slip (that was MAM+MAS) and a reviewer that audited the wrong question.

**Keep the user's constraints** (they are also in AGENTS.md):
- SCSA papers and everything derived from them (`questions.json`, `wace.db`, topic PDFs, `evidence/`) are never
  committed. Hand-written inputs (catalogue, tags, notes, skills, cheat sheets) are.
- Downloading needs the user's say-so. Never turn off TLS verification; SCSA's 403s are solved by the user saving
  files in a browser and `fetch.py --from <Downloads>`, or by the Wayback Machine for archived years.
- Tests never touch `%APPDATA%\wace-maths\config.json`, the user's `wace.db` or `generated.db`; build into a temp
  root when the user's WTF is running, and ask before killing their process.
- Commit locally; push or release only when the user says so (发布 / 发 / push).
- Reply to the user in Chinese.

## Reporting progress

At the end of each stage, tell the user in Chinese, briefly: what was produced, the check and its result
(e.g. "MAA 138 题，分值全部与封面总分一致；2019 无评分 key 已排除"), and what is open. Re-run
`scripts/pack_status.py` and quote its table when the user asks "做到哪了".

## Reference files

- `references/pipeline.md` — per stage: commands, file formats, checks, the pitfalls MAA hit.
- `jobs/README.md` + `jobs/*.md` — the fixed AI jobs of the pack flow (split, label, atomise, assign, review, notes, translate).
- `references/delegation.md` — older free-form prompt templates (per-part labelling); prefer the fixed jobs.
- `references/pack-format.md` — the `.wtfpack` protocol (`pack.json` fields, import/export, what the app must read from it).
- `references/subject-profiles.md` — the assumptions table (maths answers, Chemistry draft) and where each lives in code.
- `references/rubric-format.md` — draft structured-award design for non-tick keys: atomic tags, any-N, alternative routes, caps and source/visual evidence; not yet a supported runtime format.
- `scripts/pack_status.py` — parity checklist for one subject: `python scripts/pack_status.py CHE [--root E:\WACE_Maths]`.
