# MAA 真题分类目录

本目录为 Mathematics Applications ATAR Year 12 2016–2025 真题的后续人工标注准备稳定 topic code 和解题操作 pattern。分类依据题目要求学生实际执行的数学操作；同一小题可同时标多个 pattern，例如先建立贷款递推再求清偿期数。题目语境本身不作为 pattern。

## Topic code

| Code | Topic |
| --- | --- |
| `BIV` | 双变量数据分析 |
| `SEQ` | 数列增长与衰减 |
| `GRF` | 图与网络 |
| `TSI` | 时间序列分析 |
| `FIN` | 贷款、投资与年金 |
| `NDM` | 网络与决策数学 |

Pattern ID 由 topic code 和序号组成，例如 `TSI4` 表示时间序列主题下的第四种操作。序号一经采用应保持稳定；新增操作使用新编号，不因改名或重排而复用已有编号。JSON 中的中英文名称、说明和 syllabus 引用是目录定义，不是对具体真题的标注结论。

## 标注边界

- 以子题中要求完成的操作为单位。整道题可以跨主题，同一子题也可以多标签。
- 将可区分的计算步骤拆开，例如移动平均、季节指数、去季节化、趋势预测和季节调整分别编码；贷款余额递推、有效年利率、清偿期数和年金计算也分别编码。
- 图网络分别标识邻接矩阵、最短路径、欧拉/哈密顿性质、最小生成树、项目关键路径、最大流和分配问题。
- 题目只要求解释或判断时，标对应解释/判断操作；不要因为题干出现某领域名词，就自动标注该领域的所有 pattern。
- 先保留题目中可确认的数学操作。历年 syllabus 是否适用另行核证；不可从当前 syllabus 的编号或描述倒推旧版课程适用性。

## Syllabus 引用状态

`tools/catalogue_MAA.json` 对每个 pattern 分别记录 2025 和 2027 的 syllabus 编号及状态。`explicit` 表示该版本正文明确列出所引用的内容点；它只说明该操作对应当前列出的课程范围。这里已核对 SCSA 的 2025 年 1 月生效版与 2027 教学版，未逐年核对 2016–2024 的旧 syllabus，因此 JSON 不对这些旧年份作适用性声明。即使 pattern 的广义数学操作在旧卷出现，也应先按具体试卷和当年纲要复核再记录。

- [SCSA Mathematics Applications ATAR Year 12 syllabus, effective 2025](https://senior-secondary.scsa.wa.edu.au/__data/assets/pdf_file/0009/1121310/Mathematics-Applications-ATAR-Year-12-Syllabus-for-teaching-from-January-2025_pdf.PDF)
- [SCSA Mathematics Applications ATAR Year 12 syllabus, teaching from 2027](https://senior-secondary.scsa.wa.edu.au/__data/assets/pdf_file/0018/1262133/Mathematics-Applications-ATAR-Year-12-Syllabus-for-teaching-from-2027.PDF)

目录完成审阅后，再把正式 pattern 标签写入独立的 MAA 标签文件；本 README 不复制题目、评分标准或其图像。题目 PDF、结构化题目文本和标注证据应留在仓库忽略规则覆盖的本地数据目录中。

## 独立数据流程

`tools/sources_MAA.tsv` 包含 2016–2025 的 40 份试卷/评分 key，以及 10 份考试报告。2020–2025 链接来自 SCSA 当前课程与历年考试页面；2016–2019 的旧官方 URL 从历史目录恢复，下载使用 Wayback。没有 sample 卷。清单不加入根目录 `sources.tsv`，现有安装向导仍只要求 MAM/MAS。

```powershell
.venv/Scripts/python tools/fetch_maa.py
.venv/Scripts/python tools/fetch_maa.py --years 2016 2017 2018 2019
.venv/Scripts/python tools/fetch_maa.py --years 2020 --archive-year 2021
.venv/Scripts/python tools/fetch_maa.py --from C:/Users/you/Downloads
.venv/Scripts/python tools/fetch_maa.py --check
.venv/Scripts/python tools/segment_maa.py
.venv/Scripts/python tools/audit_maa.py --labels evidence/maa/labels.json
```

下载/导入按 PDF 正文核对科目、年份、section、exam/key 类型，拒绝 sample 与零页文件。下载先写临时文件，校验后替换；历史存档可能被截断，不能把带 `%PDF-` 文件头当作成功。`segment_maa.py` 只切已校验的 exam/key 配对，沿用现有 `(page, y0, y1)` 格式，关闭 PDF 后写入被忽略的 `MAA/questions.json`。

Luna 必须读具体题目与评分 key，必要时查看原卷图，逐小题推理标签。`evidence/maa/labels.json` 保存理由、分值、置信度、图像检查、待复核原因；不能以关键词脚本代替读题。主代理至少按 year/section 抽查 20%，并复核混合主题、切块/分值冲突和疑点。已复核数量是覆盖数据，不是准确率估计。

审计检查来源配对、题号序列、exam/key 分值、子题分值与覆盖、合法标签、重复、未标注与人工抽查覆盖。仍有缺失/无效 PDF、疑点或未标注时，报告 `complete=false` 并退出 1。如需保存已完成部分，可显式运行 `--export-partial` 导出非 pending 的原创标签；文件头保留 PARTIAL。不能据此声称十年数据已完成。

所有上述命令不调用 `build_db.py`，不修改 `wace.db`、`generated.db`、`external.db` 或用户配置，也不接入 GUI。原卷、切块文本、图像和证据保持在忽略路径内；只有来源清单、原创目录/标签与工具可以提交。

来源目录：[SCSA 当前课程](https://senior-secondary.scsa.wa.edu.au/syllabus-and-support-materials/mathematics/mathematics-applications)、[SCSA 历年考试](https://senior-secondary.scsa.wa.edu.au/further-resources/past-atar-course-exams/mathematics-past-atar-course-exams)、[历史 URL 目录](https://fuckscsa.github.io/list/mathematics_applications_file_listing.html)。历史目录只用于发现官方 URL，不代替科目/年份/类型校验。

## 本地检查点（2026-10-11）

已验证 31/50 份 PDF，其中试卷和评分 key 为 24/40。2016、2017、2018、2020、2021 两个 section 的配对完整；Luna 已标注 81 道题、394 个子题，主代理复核 27 道，每个 year/section 均达到至少 20% 覆盖。导出 80 道非 pending 题的原创标签；2017 CalcAssumed Q8 的付款时点疑点仍待核证。

十年全集尚未完成：18 份文件缺失，另有一份历史评分 key 被存档服务截断，审计为 `complete=false`。详细缺项和复核理由保存在本地忽略文件 `evidence/maa/audit.json` 与 `labels.json`。

2021 CalcAssumed Q9 的独立小题 `(i)` 被通用 `partmarks` 解析器误作 `(h)` 的罗马子题。本次保留真实标签 `i`，用显式人工分值核验记录处理；正式接入数据库前必须修正共享解析器，不能直接把这份部分标签用于建库。

独立工具的三个合成测试通过；四项应用测试通过，英文测试报告 0 处残留中文，测试前后用户配置与数据库哈希未变。尚未做 MAA 的 GUI、数据库接入或 Mac 实机验证。
