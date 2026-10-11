# Chemistry 学科包：Stage 0

状态：profile 设计核证中，尚未安装为学科包。仅核对 2025 真卷和评分 key，以及现行 Year 12 syllabus、2026 data booklet；不能据此声称 2016–2025 全部格式一致。本文件为原创设计说明，不复制试题或评分内容。

## 已核实的结构

一份 exam 和一份 marking key 包含三个 section，题号贯穿试卷。2025 共 40 题：MC 1–25，SA 26–34，ER 35–40。整卷读题 10 分钟、作答 180 分钟；分区建议作答时间为 50、60、70 分钟，不能作为数学两份卷各自独立的读题/作答计时。

| Section | Letter | 中文 | 2025 题数 | 原始分 | 成绩权重 | 建议作答分钟 |
| --- | --- | --- | --- | --- | --- | --- |
| MC | M | 选择题 | 25 | 25 | 25% | 50 |
| SA | S | 简答题 | 9 | 65 | 35% | 60 |
| ER | E | 综合作答题 | 6 | 113 | 40% | 70 |

2025 总原始分 203，与成绩百分比不是同一量。按各区得分除以该区满分、再乘权重计算百分制结果；题数、原始分和题号范围属于逐年数据，不能写成所有年份的常量。

## 评分与检查边界

- MC 官方 key 是答案表；同题可能接受多个备选字母（2025 Q6），这是任选其中一个可得分，不是要求多选。保存 accepted answers 集合、selection mode 和满分，不能把答案硬编码为单字母。MC 没有打印子题，数据库如何表示无子题题目应沿用统一约定，避免另造半套题目模型。
- 笔答使用 Description/Marks 表，含替代解、任取若干条、1–2 分范围、图像答案、Total/Subtotal 和封顶约束。备选列表不能每条都计分，Total 与 Subtotal 不能成为新评分点。保留 rubric 分组、可选关系及上限；不能强制把任意 rubric 拆成独立的一分断言。
- key_style 暂拟 `description-marks`，涵盖 MC 表和笔答 rubric；框架未提供该 handler 时必须拒绝安装。不能伪装成数学 `ticks`。
- checker 暂拟 `chem`：计算题检查数值、量纲和有效数字；方程检查原子和电荷守恒；解释题检查 rubric，结构式需要保留图像核对。未实现的检查器不能报告“已通过”，也不能沿用 SymPy 数学检查当化学正确性证明。
- 资料是 DataBooklet；需按年份关联，不把当前 2026 booklet 自动用于旧卷。结构式、装置、曲线和共用题干必须完整保留，切块不能丢失题组的共同背景。

课程主题候选：平衡、酸碱、氧化还原/电化学、有机结构与反应、化学合成/聚合物、科学探究。依据 Unit 3/4 内容，尚不是已批准的题型目录；具体操作边界需另读近年整卷后确定。

## 协议开发需要的最小扩展

1. 先完成数学三科学科注册表，所有显示名、课程、主题和 section 元数据从 pack 读取；数学数据库与现状逐表比较必须零差异。
2. 明确 paper layout：每 section 独立文件，或单文件包含多个 section。CHE 的文件为 `<year>_CHE_Exam.pdf` / `MarkingKey.pdf`，section 在切块后赋给题目。
3. 区分 `paper_minutes`（整卷）与 `suggested_minutes`（分区建议）；`sections[].minutes` 继续表示独立纸卷的读题/作答时间。权重单独用 `share`，原始满分从真实数据计算。
4. 分离题目扫描与 key 解析。数学的 Question N/ticks 与化学 MC 的数字题头/答案表不是同一格式。共享背景题组需要显式的 context 关联。
5. handler registry 只选择内置能力，学科包不含可执行代码；未知 handler 拒绝，数据包版本和最低框架版本明确记录。化学 handler 在数学协议回归通过后单独开发。

当前阶段不下载全套卷，不标注、不建库、不改现有三科标签。待 profile 决策确定后再开展来源和数据流程。

## 核证来源

- [SCSA 2025 Chemistry examination](https://senior-secondary.scsa.wa.edu.au/__data/assets/pdf_file/0008/1231010/2025-CHE-Examination.PDF)：封面、结构表、题头和共同背景。
- [SCSA 2025 Chemistry marking key](https://senior-secondary.scsa.wa.edu.au/__data/assets/pdf_file/0009/1231011/2025-CHE-Ratified-Marking-Key.PDF)：MC 表和不同 rubric 形式。
- [Year 12 syllabus，2024 起教学版](https://senior-secondary.scsa.wa.edu.au/__data/assets/pdf_file/0005/1089527/Chemistry-ATAR-Year-12-Syllabus-for-teaching-from-January-2024_pdf.PDF)：Unit 3/4 与考试设计。
- [2026 Chemistry Data Booklet](https://senior-secondary.scsa.wa.edu.au/__data/assets/pdf_file/0003/1230654/2026-CHE-Data-Book.PDF)：资料类型核证，不代替旧年份资料。
