# 交接：发布 WTF v2.0.0（给 Codex）

日期：2026-10-12 · 仓库 `E:\WACE_Maths` · 分支 `main` · 本地领先 `origin/main` 35 个提交，未推送。
**用户已同意发布 v2.0.0，要求尽快上线。** 先读 `AGENTS.md`（"v2.0 status" 和 "Run, test, build" 两节）。

## 现状（全部已在本地提交，最新 `f4bc89c`）

- 版本号：`app/version.txt` = `2.0.0`。
- 新内容：化学（CHE）学科包，400 题（选择 250 + 简答 94 + 论述 56），64 个题型；中英文讲义、速查表、出题 skill；学科包协议（每科 `<S>/pack.json` + `<S>/sources.tsv`，含下载方式 / Wayback 存档时间戳 / sha256）；知识图谱学科下拉；数据手册面板按题目年份切换。
- 测试（2026-10-12 全部通过）：test_providers / test_subjects / test_packs / test_rubric / test_rubric_keys / test_external / test_pack_roundtrip（三科 0 差异）/ smoke_gui / smoke_en（0 CJK）/ smoke_che / smoke_external / smoke_setup。
- 已打包：`dist\WTF-Windows-v2.0.0.zip`、`dist\WTF-Setup-v2.0.0.exe`、`dist\WTF-Setup.exe`（固定名，README 下载链接指向它）。
  打包版已端到端验证：复制 `dist\WTF` 到临时目录，`WTF.exe --import <四科 papers 目录>… --build` → 0 缺卷、905 题；`--selftest` 全部 ok（LaTeX、figure、SymPy、HTTPS、题库）。
- `package_win.py` 的 `TOOL_MODULES` 已加入 `segment_mc`（少了它打包版建化学会崩）。若再改 tools/ 新增模块，记得加进去。

## 发布步骤

1. `git status` 应干净；`git log origin/main..HEAD` 约 35 个提交。
2. （可选，若在本交接之后改过代码）重跑测试与 `tools\package_win.py`。不需要重建打包。
3. `git push origin main`
4. 写发布说明（中文为主，下面是要点，可直接用）：
   ```
   WTF v2.0.0 — 化学来了，学科变成学科包
   - 新科目：Chemistry ATAR（2016–2025）。选择题 250 道 + 简答/论述 150 道，按 64 个题型标注；评分标准拆到每一分（选择题 250/250，简答/论述 136/150，其余显示 key 原图）；8 个主题的中英文解题思路讲义、速查表；右侧面板显示当年的数据手册。
   - 学科包：每个学科是一份只含数据的学科包（pack.json + 讲义 + 标注 + 真题来源清单），App 从包里读取科目、卷型、计时和评分方式；「题库 → 管理科目 → 导入学科包…」可导入本地 .wtfpack。
   - 真题来源清单带校验：每份 PDF 记录下载方式、Wayback 存档时间和 sha256，版本不对的文件会被拒收并提示；样卷和考试报告改为可选，不再挡着建库（每科少存 6 份）。
   - 知识图谱改为按学科切换（下拉菜单），卷型筛选随学科变化；公式表/数据手册面板用下拉选择科目和年份，看哪年的题就显示哪年的表。
   - MAA（数学应用）标注经过三轮独立复核与仲裁；Mac 下载证书问题修复（使用系统证书库）。
   - 已知：化学 2019 Q40/Q41 的官方 key 题头分值与卷面不一致；2023 Q39、2024 Q36(c) 等官方 key 自身问题已在讲义中注明。
   ```
5. `gh release create v2.0.0 dist\WTF-Setup-v2.0.0.exe dist\WTF-Setup.exe dist\WTF-Windows-v2.0.0.zip --title "WTF v2.0.0" --notes-file <上面的说明存成的文件>`
6. 发布会触发 `.github/workflows/build-mac.yml`，自动附上两个 Mac `.dmg`。用 `gh run list --workflow build-mac.yml` 看结果；失败就看日志修，不要关 TLS 校验。
   注意：Mac 的 CI 自检现在检查 `MAM/sources.tsv` 和 `MAM/pack.json`（根目录 `sources.tsv` 已删除）。
7. 发完用中文向用户汇报：release 链接、三个 Windows 文件、Mac 构建结果。

## 规矩（照旧）

- 只做发布，不改标注和讲义；不下载真题；不提交 SCSA 原卷或其衍生物（questions.json、wace.db、topics/、evidence/ 都在 .gitignore）。
- 测试不要碰用户的 `%APPDATA%\wace-maths\config.json`、`generated.db`、`wace.db`。
- 有问题先停下来问用户。

## 发布之后的待办（不属于本次）

- 学科包 Phase 5：`packs.json` 在线索引 + 管理科目里的在线安装。
- MAM/MAS 补正式题型目录（catalogue）；MAS 评分点 180/193。
- 化学：14 道简答/论述题的 key 仍显示原图；AI 出化学选择题的效果需真实 API 试用。
