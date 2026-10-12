# Job: review — an independent second assignment

Same input and output as [assign](assign.md), on a sample chosen by `flowjobs.py` (every topic, every
low-confidence award, about 20% of the rest). You do **not** see the first assignment. Do the job from scratch.

`flowjobs.py check <S> review` compares the two: agreement per pattern and per topic is reported, and every
disagreement becomes an arbitration item for the strong model (you), who decides with the catalogue and the key,
and fixes the catalogue's `definition`/`not` when a boundary caused it. If more than 10% of the sample disagree on
the pattern, the catalogue is not ready: fix the definitions and re-run `assign` for the affected topic.
