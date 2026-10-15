# Subject pack downloads

| Pack | Course | Needs | Overview |
|---|---|---|---|
| [CHE-2026.10.1.wtfpack](CHE-2026.10.1.wtfpack) | Chemistry ATAR, 2016–2025, 400 questions, 64 patterns | WTF ≥ 2.0.0 | [review record](../CHE/methods/审校记录.md) |
| [PHY-2026.10.1.wtfpack](PHY-2026.10.1.wtfpack) | Physics ATAR, 2016–2025, 203 questions, 79 syllabus content nodes × 11 award skills | WTF ≥ 2.0.2 | [overview](../PHY/README.md) · [review record](../PHY/methods/审校记录.md) |
| [ACF-2026.10.1.wtfpack](ACF-2026.10.1.wtfpack) | Accounting and Finance ATAR, 2020–2025, 135 questions, 114 patterns, 283 knowledge atoms | WTF ≥ 2.0.4 | [overview](../ACF/README.md) · [review record](../ACF/methods/审校记录.md) |

Import through **题库 → 管理科目 → 导入学科包** (Subjects → Manage subjects → Import subject pack). Then obtain the
original PDFs yourself: the wizard lists the official sources, recognises each file and checks its SHA-256 against
the pack. The archives hold the course profile, the catalogue, a code for every awarded mark, original notes, cheat
sheets and skills — never exam or key PDFs, examiners' reports or text extracted from them.

Every pack here was exported, installed into an empty data folder, rebuilt from the original PDFs and compared table
by table with the reference build: 0 differing rows. The format is described in
[pack-format.md](../skills/wtf-subject-pack/references/pack-format.md). To make a pack for another course, use the
WTF Compiler with your own agent over MCP ([docs/compiler.md](../docs/compiler.md)) or the pack flow
([skills/wtf-subject-pack](../skills/wtf-subject-pack/SKILL.md)).

The DeepSeek-generated MAS Compiler fixture is a local protocol test, not a production subject pack, and is not
distributed here.
