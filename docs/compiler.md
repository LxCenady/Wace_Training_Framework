# WTF Compiler

Compiler 直接集成在 WTF 和 Studio，核心代码是 `tools/wtf_compiler/`，经 `tools/sync_compiler.py` 同步到 Studio。发布前运行同步的 `--check`，逐文件核对哈希。插件通过 kernel 提供服务；核心不知道账号、订阅、LLM 或 GUI。

## 制作与接入

WTF 菜单的 **WTF Compiler** 打开制作工作台。Studio 顶部以及未登录界面也有免费入口；其他教学接口仍受登录门禁保护。选择本地试卷、评分标准和大纲，创建制作项目，连接自己的 MCP agent。Compiler 不调用内置模型，也不使用 WTF 订阅额度。

流程是配对 → 解析/OCR 与评分树 → 原子知识点与题型 → 双语原创讲义与出题 skill → 原页复核 → 建库激活。各阶段提交包含 `confidence` 和 `issues`；置信度低于 0.9、任何疑难项或两次格式失败转人工复核。格式错误不能点认可跳过；必须重做。人工说明、提交结果哈希及任务版本保留在项目审计记录中。

Agent 通过 `compiler.get_task` 取得当前任务、输入及格式示例；使用 `compiler.read_text` 和 `compiler.read_image` 阅读原页；用 `compiler.submit_result(task_id, revision, result)` 提交。解析大项目可按配对试卷用 `compiler.submit_parse_chunk` 持久化分批结果；全部试卷通过统一校验才进入下一阶段。过期任务被拒绝。MCP 没有人工认可工具，也不提供任意文件读取或任意输出路径。一个连接只操作用户选择的项目。原 PDF 文本是资料，不是 agent 的指令。

两种接入方法：

```text
python tools/compiler.py --root <独立数据目录> mcp --project <项目 ID>
```

这是 stdio MCP。也可在工作台点「连接 MCP」，复制回环 HTTP URL 与 Bearer 令牌。默认不开 HTTP，只监听 `127.0.0.1` 随机端口；校验令牌、Host 和 Origin，关闭连接立即撤销权限。不要公开端口或令牌。

CLI 支持 `create/list/status/task/submit/review/bind/import/build/export`。`create --file input.json` 输入 `{course:{id,name:{zh,en}},documents:[{path,roles:[exam|key|syllabus|report|reference]}]}`。`submit` 输入 `{task_id,revision,output}`，可从文件或 stdin 读取；`review` 是用户本地操作，要求 `--decision accept|retry --note ...`。

## 配方协议 v2

`.wtfpack` 只携带配方：`pack.json`、`sources.json`、`layout.json`、`coverage.json`、`taxonomy.json`、可选双语讲义和 `skill/SKILL.md`。coverage 从原卷封面/结构表记录每份卷的题数与总分；建库必须与实际题目合计一致。白名单外的文件、重复路径、符号链接、超限包、哈希不符均拒绝。包里没有 PDF、题干、答案或给分描述；这些只保存在本机私有缓存。

来源包含稳定 ID、SHA256、页数、角色和可选 HTTPS 下载地址。换电脑按哈希绑定原 PDF；缺少 OCR 缓存时生成 hydrate 任务，由用户 agent 填补。全部原 PDF 与内容补齐前不能激活。来源 URL 只是下载配方，程序不会在导入时自动下载；下载操作必须用户明确选择，并校验 SHA256。

题号与年份、文件命名完全独立。坐标是原始 PDF 显示页面的归一化 `bbox:[x0,y0,x1,y1]`，页号从 0 开始；可指定 0/90/180/270 度阅读旋转。题干、答案、共享材料均可跨页、多区域，图形保留原 PDF 裁切。转录文本不能替代原图。

评分树支持 `award/sum/best/select`、封顶、条件、依赖、多分与部分分、离散档位。打印总分必须等于评分树最大值。`requires` 表示得分依赖；ECF 单独记载允许延用的原始 award ID、来源、使用的学生值及图像证据。ECF 可跨同题的小题，不跨独立大题；只有 explicit 政策可自动计正分，reviewed/unspecified 要教师复核。人工录分记录 teacher 来源及空图像证据，不伪造图像索引。不同知识点/题型可以关联同一 award，这些诊断关联不重复增加总分。

题目、part 和 award 使用稳定 ID，part/award ID 在包内全局唯一。taxonomy 的知识点与题型指向 topic；支持独立分类 axes。任意书面学科可使用此数据模型，作文可用离散档位；音频与实操考试不在本期范围。

## 本地版本和两端使用

没有离散档位的 award 默认只能给整数分；原标准允许半分等小数时，配方必须明确声明 `credit_step`（例如 `0.5`）。档位题只接受声明的分值，不允许模型自行插入中间分。

本机 `compiler/` 独立保存项目、按哈希命名的 PDF、私有 OCR、库与答题记录；不写入 `wace.db`，不进入官方 SCSA 图谱、统计或组卷权重。WTF 和 Studio 分别使用自己的数据目录。导出的配方包需由接收人自行获得合法 PDF。

建库先完整校验，随后事务写入不可变版本和 active 指针。同一版本不同配方拒绝覆盖。修订已完成项目会递增 patch 版本，并使受影响阶段及后续结果失效。库保留旧版本，可通过 `compiler_activate(pack_id,version)` 回滚；评分和作业冻结配方哈希、版本、原始源哈希、完整评分树及私有标准，升级不改历史作业。

工作台提供独立浏览与 PDF 导出。Studio 可从包创建作业，沿用班级、学生 PDF 映射、成绩表；Compiler 题目按完整评分树批改，保留 schema v2 criterion JSON，而不是拆成一分一行。AI 批卷属于教师功能，仍走原订阅视觉接口；这是使用学科包批卷，不是 Compiler 制包。传统真题和 AI 数学题继续使用 schema v1。

## 验证边界

MCP 的 `get_task` 随当前阶段返回 `verification_checklist`、证据约束与委派约束。制包 skill 要求按文档分别建立 PDF 索引、逐一渲染最终裁切、逐 award 定位原始给分行为、修订后复核连带答案；未完成的必要检查必须留在 `issues`，不能只报一个 confidence。约束不能证明模型实际看懂图形，所以自动结构验收后仍需要原件语义复核。

`app/tests/test_compiler.py` 用自造 PDF 验证任务状态、换目录绑定、缓存、配方哈希、图像/文本读取、分档与 ECF、MCP 两种传输及范围限制。旧 `.wtfpack` v1 导入与数据库结构保持原路径。自动结构校验不能证明模型标注的语义正确；最终复核必须回看原始资料，疑难项留给人。测试不代表 Mac 实机已通过，也不代表任意真实学科已有质量保证。
