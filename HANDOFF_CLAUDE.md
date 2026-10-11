# Claude 交接：化学标准学科包与评分原子模型

交接日期：2026-10-12。仓库 `E:\WACE_Maths`，Python `.venv\Scripts\python.exe`。
代码基线：`08fdca3`（Add rubric scoring trees and non-additive atomic coverage）。
本文是项目进度与后续任务说明，不包含官方试题或评分原文。

## 用户当前目标及边界

完成化学标准 `.wtfpack`，确保现有 MAM、MAS、MAA 和新增 CHE 都能正常跑通。
用户最新补充：分值与原子关联模型需要优化。已经完成评分模型基础，但**化学包仍未完成**。
请先完整阅读 `AGENTS.md`、`HANDOFF.local.md`、`skills/wtf-subject-pack/SKILL.md`，以及其
`references/pack-format.md`、`subject-profiles.md`、`rubric-format.md`、`pipeline.md`。

- 全程中文；KISS、一个模块一件事；插件用 kernel provide/get、on/emit；平台差异只放 `app/plat.py`。
- 不 push、不发布。可以本地 commit。最新这一轮没有发布授权。
- 用户的 WTF 可能锁住 `wace.db`。不要关闭程序或重建用户数据库，先在临时目录构建。
- 测试不得修改用户配置、generated.db、external.db、wace.db。不要输出 API key。
- SCSA 原件、原文、截图及其衍生题库都不得提交或放进学科包。
- 用户已授权化学资源下载，并指定 Luna 做化学证据工作。代码、正式目录、主审与仲裁留给主代理。
- 第一部分选择题整区保留，不逐题原子化、不加入 SA/ER 标签统计；整卷成绩仍含其权重。
- 化学图像必须复核，讲义结合大纲、marking scheme、真卷和公开阅卷分析。

## 已完成的框架工作

数学三科已有 pack.json；科目、section、计时、资料类型、评分权重等读取统一注册表。
支持共享试卷及 section-only 切分，保留 MC 区域，SA/ER 按题切分。
学科包只装数据，内置 handler 注册表拒绝未知能力；支持本地导出、检查、导入、失败回滚和向导接续。
在线索引/分发 Phase 5 尚未完成，本轮没有发布资产。

关键文件：`tools/subjects.py`、`handlers.py`、`pack.py`、`scoring.py`、`segment.py`。
共享试卷已修复补充答题页说明、MC 材料引用误识别题头、下一 section 标题混入上一题、key 版权页混入末题等问题。
这些修复没有改变数学数据库行。

## 最新提交：评分与原子模型

`tools/rubric.py` 是数据型评分树运算模块，**不是 Chemistry key parser，也尚未写入题库/作答数据库**。

| API | 已实现的行为 |
| --- | --- |
| validate(root, printed_marks=None) | 检查节点 ID、所有权、类型、分值、band、依赖引用及环、封顶、印刷满分一致性 |
| validate_associations(root, knowledge_ids, pattern_ids) | 每条 award 必须具有目录中有效的知识原子与操作题型引用 |
| score(root, credits, conditions=None) | 计算上下界、确定得分、相关未确认条件、采用的路径/任取选项 |
| coverage(root, field='knowledge') | 沿原评分树投影各原子或题型的潜在覆盖分，保持替代/任取/封顶 |

节点：award（可多分）、sum（累计）、best（完整替代路径取最高）、select（任取 N）。
共享给分点放在替代路径之外；Total/Subtotal 不能变成新增 award。
`positive_band: [1,2]` 不禁止零分；`requires` 当前语义是引用节点获得正分才满足依赖。
`conditions` 是人工/复核布尔判断；`conditional_caps` 在条件 true 时生效，绝不执行包内表达式。
未确认判断会产生保守上下界；上下界不同则 earned=null。不能把这个结果当成精确整卷成绩。
credits 未提供的 award 按零分处理，所以不能把尚未评分的输入直接当最终 credits。
相同得分的路径/选项按来源顺序打破平局；selections 是模型计算结果，不是学生实际路径的证据。

一个两分准则关联两个知识原子时，两者各有两分重叠覆盖，实际准则仍最多两分。
覆盖分不能相加，不能当作已掌握程度；准则的部分得分也不能自动平均归因到多个原子。
coverage 是静态潜在覆盖，不解决所有化学语义条件的可满足性；依赖和复核证据需上层保留。
数学现有 pattern_marks 仍走旧的平均分配逻辑，**尚未迁移为新的 award 模型**。

kernel 已提供 `score.rubric`、`score.atom_coverage`（在 store.setup 中注册）。
Windows/Mac 共用的打包模块列表已包含 rubric；没有实际打包或 Mac 实机验证。
专项测试：`app/tests/test_rubric.py`，5 项通过。

## 化学本地资源与候选证据

原件：`evidence/che/originals/`（忽略目录）。共 24 PDF：
2020–2025 exam/key/公开报告共 18；2020–2023 和 2026 data booklet 共 5；现行 Year 12 syllabus 1。
URL、大小、页数、SHA-256：`evidence/che/download_inventory.json`；链接表 `source_links.tsv`。
2024/2025 booklet 未补齐，不能拿 2026 默默替代。2016–2019 未纳入当前六年范围，要在包中明确范围与排除理由。

切分预检：`evidence/che/preflight.py`、`evidence/che/segmentation/`。
预检不是正式安装 CHE。87 道笔答题均有印刷分及 key 区域；按 section 的题数/分值核对无差异。

| 年 | 笔答题数 | 响应单元数 | SA 分 | ER 分 | 笔答总分 |
| --- | --- | --- | --- | --- | --- |
| 2020 | 15 | 56 | 76 | 88 | 164 |
| 2021 | 14 | 47 | 76 | 90 | 166 |
| 2022 | 14 | 44 | 71 | 90 | 161 |
| 2023 | 14 | 42 | 79 | 86 | 165 |
| 2024 | 15 | 44 | 81 | 87 | 168 |
| 2025 | 15 | 50 | 65 | 113 | 178 |
| 合计 | 87 | 283 | | | 1002 |

Luna 每年成果：`evidence/che/<year>/rubric_inventory.json`、`inventory_notes.md`，附渲染页/图像引用。
上述数值来自预检和代理清单；主代理仍需独立仲裁，不能因代理 sum_check 为空就批准正式评分树。
清单包含印刷分、mark_groups、alternative_sets、候选知识/操作说明和来源区域。
它们包含官方原文，只能本地使用；不能直接作为 marktags.json 导出。
描述性候选标签不是正式 catalogue ID；部分 bbox 是整题范围，不是每条准则的精确定位。
置信度不能照抄代理统一填的数值，应根据实际来源和复核记录判断。
主代理已有部分复核：`evidence/che/primary_review/review.md` 及渲染文件。
2025 示例：`evidence/che/2025/rubric_sample.json`。

官方来源问题保留在各年 notes：2020 Q38(a) 中间数误印；2022 Q29(d) 两份 PDF 均以版权告示替代图像；
2023 Q34(b) 公式内容错贴；2024 Q34(d) 中间数差异；2025 Q38(d) key/报告的滴定数据取舍冲突及 Q39 多项误印。
不要静默改 ratified key；分别记录官方答案、矛盾证据、仲裁和教学解释。
特别复查 2023 Q37(a) 的 band/共享或封顶关系，不能仅把每个 mark_group 的最大值相加。

## 建议接续顺序与验收

1. 主代理审近年整卷、大纲、key，定稿 CHE catalogue：知识原子与被评分操作分开定义，稳定 ID、边界明确。
2. 将六年候选清单转为正式 award 树与原创 marktags；替代路径、any-N、band、共享给分、条件封顶逐例仲裁。
   树最大值需与小问、题目、section 印刷满分对账；主审至少约 20%，覆盖全部主题及复杂/图像案例。
3. 实现通用结构化 rubric 的导入校验、存储、查询与来源重建。数学旧表保持兼容；不要复制多分准则成重复一分行。
   数据包不含官方文本/图像，只带原创关联、结构、位置和审核元数据；来源 hash 变化须失效待复核。
4. 实现 description-marks handler，明确 handler 接口及结构化数据路径；当前 handlers.py 只有 ticks，checker 只有 sympy/none。
   不要直接装 CHE profile 或把 key_style 伪装 ticks。chem checker 尚未实现，不能报告化学正确性已验证。
5. 连接评分/原子模型到题库、作答记录与界面。保留学生获分证据、人工/API 提议及审核状态；统计区分覆盖与实际成绩。
   MC 整区存储/服务仍需落地；paper_totals 当前只查 questions，不能误称其包含 MC 整卷分数。
6. 清理余留数学假设：build_docs/build_bank 的 CF/CA 显示与排序、audit_totals 的前六页扫描、paperid 的 DataBooklet 识别。
7. 完成六年 CHE profile/sources、标签、双语讲义及 PDF、审校日志、速查表、出题 skill 和真实统计 blueprint。
   依照审核后的目录委派廉价代理写原创讲义，主代理核对来源与翻译，不复制官方讲义/题文。
8. 临时根中完成 CHE strict export/import/build，再验证四科向导、浏览、检索、导出、组卷和评分。
   未开发或未测的能力必须明确报告，不能用已有数学测试代替 CHE 端到端测试。

数学包现有缺口：MAM/MAS 无正式 catalogue，MAS points_ok 180/193，严格导出拒绝；MAA 严格导出通过。
只读审计在 `evidence/packs/math-gaps/audit.md`，16 题涉及多 tick、alt 状态、裁切截断或替代重复累计。
尚未修复，不要机械截断/补足 tick 来凑满分。若修数学，要比较预期变更与无关行；不要同时偷偷重建用户库。

## 已验证与复现

08fdca3 阶段：5 个 rubric 专项测试、4 个 subject 测试、4 个 pack 测试通过；六项应用检查通过。
smoke_en 与 smoke_external(en) 均 0 CJK；首次建库 505 题/4240 points（仅数学三科）。
三包导出/导入后临时重建：15 个科目/表组合、8740 行、0 差异。
日志 `evidence/che/rubric-roundtrip.log`。MAM/MAS roundtrip 使用 draft，不代表严格包就绪。
GUI 第一次曾因 GBK 无法输出特殊字符中断，设置 PYTHONIOENCODING=utf-8 后重跑通过。
setup 结束时有 Tk after 回调警告，验收断言与建库通过；不把它隐瞒成完全没有任何日志警告。

PowerShell 中先设置：
```powershell
$env:PYTHONIOENCODING='utf-8'
$env:TEMP='E:\WACE_Maths\evidence\runtime'
$env:TMP=$env:TEMP
```

`evidence/che/verify_run.py` 包装测试，前后检查用户 config/generated/wace/external 的 SHA-256。
在 app 目录用 `..\.venv\Scripts\python ..\evidence\che\verify_run.py tests/<测试名>.py <参数>`。
六项测试及参数见 AGENTS.md；GUI/EN 工作目录先创建，setup 必须用新建、明确属于本次测试的目录。
`test_pack_roundtrip.py` 可同样包装执行。首次安装测试从 git ls-files 复制，新增正式文件需要先 git add 才会进入其临时根。
独立测试命令：`.venv\Scripts\python app/tests/test_rubric.py`。
未改 UI 文案所以最新模型提交没有翻译变更；后续新增 UI 文案须运行 tools/translate.py ui 并人工审查。

不要把“模型已实现、六年证据清单已齐备”写成“化学标准包已完成”。下一步最重要的是正式目录和逐准则标注，
然后真实的结构化存储/handler/界面接入与四科端到端验收。
