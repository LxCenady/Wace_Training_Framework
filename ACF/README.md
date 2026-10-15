# Accounting and Finance ATAR

The first pack covers 2020–2025 papers, mapped to the 2026–2027 Year 12 syllabus. The owner approved the catalogue on 2026-10-15. Every award is assigned; a blind second assignment of 308 awards agreed on the pattern for 92.5% (knowledge sets: 65.6% exact, 95.5% overlapping), and the 23 disputes were arbitrated (`methods/审校记录.md`). An exported pack installed into an empty root rebuilds every table identically. It has not been published.

The catalogue has 135 questions, 264 parts, 1,111 award records (including accepted alternatives and indivisible descriptive bands), 114 patterns and 283 knowledge atoms (`tools/catalogue_ACF.json`; the reviewed draft is in `目录确认.md`). Part scoring structures agree with all printed marks. Eight patterns are current syllabus content without a past question (`examined: false`).

One shared paper contains multiple-choice (15%), short answer (70%) and extended answer (15%). Reading time is 10 minutes, working time 180 minutes. Each extended-answer section supplies two questions but requires one; both stay searchable, while attainable marks and paper plans use one answer. Raw short-answer totals vary by year.

Bank frequencies count both offered extended-answer questions. A proportion of pooled raw marks is not a weighted examination percentage: the latter must use the section weights and the question explicitly chosen by the student. Do not present an equally weighted average of the alternatives as an individual's attempted score.

Every year requires its own exam, marking key, information booklet and applicable specifications booklet. The current 2026 booklet is comparison evidence, never a substitute for a missing historical edition. Reports and downloaded source material stay local and outside Git.

The published 2027 change summary replaces the one-statement financial report's title, while the downloaded 2027 main syllabus still prints the older title. This is a recorded source discrepancy, not evidence of a removed knowledge concept. Prior Year 11 knowledge is not automatically outside the Year 12 course.

Written marking tables require visual checks, including journal debit/credit columns, financial-statement row ownership, alternative formats, mark ranges, deductions and consequential-error credit. Equal mark totals do not establish correct criterion boundaries. Follow-through must not require a correct preceding numerical answer. No automatic accounting answer checker is claimed.

2021 multiple-choice Q2 was officially awarded to all candidates: the date required for weighted-average shares was omitted. Its official answer stays `all`; a credited answer does not demonstrate mastery. Notes and review must distinguish this from an ordinary earnings-per-share calculation.

The cancelled item is isolated in administrative pattern RAT12, rather than EPS pattern RAT5. Its `diagnostic: false` and `historical_only: true` flags and the OUT topic's `historical_only` flags are written to the database table `pattern_flags`: AI papers never draw those patterns (`tools/blueprint.py`), and RAT12 is left out of practice mastery (`store.mastery`). A teacher or student can still ask for a historical pattern by name. Current but unexamined climate content (GOV10–12) stays available.

Any-N response counts describe accepted response records rather than independently attempted questions. For example, the ten accepted choices for 2021 short-answer Q21(b) retain a four-mark cap; the legacy fractional credit used in frequency statistics is not a student's observed mastery.

Questions, answers, crops, source evidence and databases are never included in Git or the distributable pack. The pack contains original catalogue definitions, code-only award associations, notes, skill instructions, metadata and source URLs.
