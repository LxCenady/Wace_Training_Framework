# WTF Hub packs

WTF ships no subject: every course is one of these packs, listed in [hub/index.json](../hub/index.json) and installed
from the app (题库 → 管理科目 → WTF Hub 学科包…). A downloaded pack is checked against the index's SHA-256 before it is
installed. The packs carry no exam or key PDFs, examiners' reports or text taken from them: each asks for the original
papers on your computer.

| Pack | Course | Kind | Needs | Notes |
|---|---|---|---|---|
| MAM-2026.10.2 | Mathematics Methods ATAR, 2016–2025, 174 questions | data | WTF ≥ 2.0.0 | [review record](../MAM/methods/审校记录.md) |
| MAS-2026.10.2 | Mathematics Specialist ATAR, 2016–2025, 193 questions | data | WTF ≥ 2.0.0 | 13 keys shown as images (declared in the pack) |
| MAA-2026.10.2 | Mathematics Applications ATAR, 2016–2025, 138 questions | data | WTF ≥ 2.0.0 | [review record](../MAA/methods/审校记录.md) |
| CHE-2026.10.2 | Chemistry ATAR, 2016–2025, 400 questions | data | WTF ≥ 2.0.0 | [review record](../CHE/methods/审校记录.md) |
| PHY-2026.10.2 | Physics ATAR, 2016–2025, 203 questions | data | WTF ≥ 2.0.2 | [overview](../PHY/README.md) |
| ACF-2026.10.2 | Accounting and Finance ATAR, 2020–2025, 135 questions | data | WTF ≥ 2.0.4 | [overview](../ACF/README.md) |
| CAIE9709-1.0.0 | Cambridge International AS & A Level Mathematics (9709): June 2024 and 2020 specimen papers, 100 questions | recipe | WTF ≥ 2.1.0 | experimental: compiled through MCP by agents, not reviewed by a person |

Every data pack here was exported, installed into an empty data folder, rebuilt from the original PDFs and compared
table by table with the reference build: 0 differing rows (`tools/export_packs.py`). The recipe pack was built and
installed from its originals without an agent (`wtf_compiler`). To publish a pack, add its file here and regenerate
the index with `tools/hub_index.py`. To make one, use the WTF Compiler with your own agent over MCP
([docs/compiler.md](../docs/compiler.md)) or the pack flow ([skills/wtf-subject-pack](../skills/wtf-subject-pack/SKILL.md)).
