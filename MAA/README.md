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

本 README 不复制题目、评分标准或其图像。

## 数据流程（已并入通用管线）

MAA 自 2026-10 起是 WTF 的正式科目，与 MAM/MAS 走同一条管线，做法记录在 skill `skills/wtf-subject-pack/`：

- 来源：根目录 `sources.tsv` 的 MAA 行（40 份试卷与评分 key、10 份考试报告、4 份公式表）。2016–2018 与 2020/2021 公式表经 Wayback 下载，其余来自 SCSA 官网（被 403 拦截时在浏览器保存后用 `tools/fetch.py --from <下载文件夹>` 导入）。`tools/paperid.py` 按 PDF 正文识别科目、年份和卷型。
- **2019 不纳入**：两份评分 key 一份缺失、一份在存档中被截断，无法标注和核对分值。
- 切题：`tools/segment.py MAA`（只切 `sources.tsv` 中列出的试卷）→ 本地 `MAA/questions.json`（不提交）。
- 题型目录：`tools/catalogue_MAA.json`，6 个主题、67 个题型。
- 标注：`evidence/maa/labels.json`（本地，不提交）→ 导出 `tools/tags_MAA.txt`、`tools/parttags_MAA.txt`。
- 建库：`tools/build_all.py` → `wace.db`；`tools/blueprint.py` 把真卷统计写入 `skills/wace-maa-questions/SKILL.md`。

## 标注过程

1. 子代理逐题读题干与评分 key（必要时渲染原图）标注到小题，写理由与置信度；主代理复核 47/138 题（34%），覆盖每个 year/section。
2. `tools/audit_maa.py --labels evidence/maa/labels.json`：题号、分值（小题分值合计 = 题目分值 = 试卷总分）、标签合法性。0 错误（"缺 1、无效 1"即 2019 的两份评分 key）。
3. 2026-10-12 三个独立复核子代理分年份段复核全部小题，提出 48 条修改；按统一口径（FIN10 只在评分 key 单独给利率换算分时标注；哈密顿路线求最短 = GRF6 + GRF4，GRF9 只用于允许重复经过顶点的行程；关键路径题只有在评分 key 给浮时分时才加 NDM7 等）仲裁，41 个小题改标。记录见 `evidence/maa/tag_review/`（本地）与 `MAA/methods/审校记录.md`。
4. 2017 CalcAssumed Q8：评分 key 的 98 974 对应期末付款的永续年金，题干写年初付款。这是评分 key 自身的问题，讲义中注明为"已知问题"；标签按操作确定，已解除复核标记。

## 现状（2026-10-12）

- 138 题、698 个小题全部标注，67 个题型都有真题；`points_ok` 134/138（按每分一个勾拆出评分点）。2021 CalcAssumed Q9 的评分 key 文本顺序错乱，按设计显示评分 key 原图。
- 中英文解题思路讲义（每个题型一节）、审校记录、速查表（中英文）、出题 skill 均已完成，并已渲染 PDF。
- 原卷、切块文本、`questions.json`、`wace.db`、`evidence/` 均不提交。
