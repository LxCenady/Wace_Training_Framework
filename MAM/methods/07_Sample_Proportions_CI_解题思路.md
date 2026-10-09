# MAM · 样本比例与置信区间 — 题型与解题思路

> 依据：2016–2025 共 29 道真题 marking key + 考试报告（几乎每年都点名「会算不会解释」）。原题见 `topics/07_Sample_Proportions_CI.pdf`。文中数值例已用 Python 验算。
> 审校状态：已经过一轮独立审校并按意见修订（见 `审校记录.md`）。

## 公式卡

- p̂ = x/n；p̂ 的近似分布：**p̂ ~ N(p, p(1−p)/n)**（n 足够大时）。
- 置信区间：p̂ ± z·√(p̂(1−p̂)/n)；误差范围 E = z·√(p̂(1−p̂)/n)；区间宽度 = 2E。
- z 值：90% → 1.645，95% → 1.960，99% → 2.576。
- 由区间反推：p̂ = (上界 + 下界)/2，E = (上界 − 下界)/2。
- 样本量：n = z²p̂(1−p̂)/E²。**求最小样本量（minimum / guarantee / ensure margin at most …）一律用 p̂ = 0.5**（最坏情况），**即使前面已经算出 p̂**（2023A-Q7(c)、2024A-Q10(f)、2025A-Q16(e) 的 key 都这样；2023 报告专门提醒）。只有题目明确要求用某个样本比例时才代入它（2016A-Q10(d)："Using the sample proportion of the survey…"）。

## 阅卷组提醒（这一章报告写得最多）

1. **根据区间下结论时必须表态**（2023 报告）：不能用「无法 100% 确定」来回避结论。例（2024A-Q11(b)）：「The claimed value 0.74 lies inside the 95% CI (0.652, 0.748), so there is insufficient evidence to reject the claim.」
2. **偏差题要具体**（2022–2024 报告）：说出偏差来源 + 解释**哪一类人更可能或更不可能被抽到** + 结合语境。时间和地点是**两个**不同的偏差来源，不要合并成一条。
3. **样本量要向上取整**；反推样本量时四舍五入到最近整数（两者区别见题型 4）。
4. 「95% 置信」的含义：如果重复抽样很多次，大约 95% 的区间会包含真实 p；**某一个具体区间要么包含、要么不包含 p**。

---

## 题型 1：写出 p̂ 的分布并求概率

**识别**：「What is the (approximate) distribution of the sample proportion?」「P(p̂ < 0.58)」。

**思路（3 分模板）**：✓「approximately normal (since n is large)」✓ 均值 = p ✓ 方差 p(1−p)/n（或写标准差）。然后用 normCdf 计算，写出概率表达式。
**何时不能用正态近似**：分布图明显右偏、n 小、np 太小（2023A-Q10(a)：n = 36、p = 0.05，图像不对称 ⇒ 不合适）。(a) 的理由写「不对称」即可。(b) 换成 n = 500、问人数 X，所以用二项；(c) 在 n = 500 时又可以用正态近似。
**样本量增大会怎样**：p̂ 的标准差变小、分布更集中，所以 P(p̂ ≤ 0.03) 会**增大**（2017A-Q18(d)(ii)：两点分别给「SD 减小」和「分布更集中 ⇒ 概率更高」）。

**真题**：2016A-Q14(b)、2017A-Q18(d)、2018A-Q17(a)(b)、2019A-Q13(a)、2020A-Q12(b)(c)、2021A-Q11(a)(b)、2022A-Q13(a)、2023A-Q10、2024A-Q10(b)、2025A-Q10(d)。

---

## 题型 2：计算置信区间与误差范围

**思路**：p̂ → 选对 z → 代入公式（或用 CAS 的 1-Prop z Interval）→ 按要求保留小数。
例（2023A-Q7）：76/200 = 0.38，95% CI ≈ (0.3127, 0.4473)。
**假设**：p̂ 近似正态（n 足够大）——2016A-Q10(a) 的 key 要求写这一条；随机抽样可作补充。

**真题**：2016A-Q10、2017A-Q18(b)(c)、2018A-Q17(e)、2019A-Q8、2020A-Q12(d)(e)、2021A-Q11(d)(e)、2023A-Q7(b)、2024A-Q9(a)、2025A-Q16(b)(c)。

---

## 题型 3：用置信区间检验说法 ★ 每年都有

**标准两句话（key 的 2 分）**
1. 「The claimed proportion p = 0.6 is **not** within the 95% confidence interval (0.4562, 0.5438).」
2. 「Therefore there is sufficient evidence (at the 95% level) to conclude that the claim is incorrect / that Tina is unlikely to be correct.」

反过来，如果说法的值落在区间内：「not enough evidence to conclude that the proportion has changed」。
**比较两个区间**（2020A-Q12(f)）：两个区间重叠 ⇒ 没有充分证据说明财务建议降低了失败率。
**为什么真实值不在区间里，也不一定是算错了**（2019A-Q8(b)、2021A-Q13(g)）：「Not all 95% confidence intervals contain the true proportion; about 5% will not, and this may be one of them.」

**区分两种问法**（2025 报告：statistical significance, as distinct from proving a result）：
- 问「is it different / what does it suggest」⇒ 按上面的两句话表态。
- 问「does it **prove** the claim is incorrect / was a mistake made」⇒ 回答 **No**：区间不能证明任何事，并非所有区间都包含 p，不知道这个区间是不是没包含 p 的那一部分（2025A-Q15(f)）。

**二项分布的假设题**（2020A-Q12(h) 4 分、2021A-Q11(g) 3 分；2020 报告点名答得差）：写出假设（各对象独立、概率 p 相同且不变）→ 结合语境判断是否合理 → 给出理由。

**真题**：2016A-Q20(f)、2017A-Q12(e)、2018A-Q17(f)、2020A-Q12(f)、2021A-Q11(f)、2022A-Q12(g)、2023A-Q12(e)、2023A-Q13(d)、2024A-Q10(d)、2024A-Q11(b)、2025A-Q16(f)。

---

## 题型 4：样本量 / 由区间反推 ★

**A. 求最小样本量（向上取整）**
- 「within 0.01 with 95% confidence」⇒ n = 1.96² × 0.25 / 0.01² = 9604（用 CAS 的精确 z 得 9603.6，向上取整也是 **9604**）（2019A-Q14(a)）。
- 2023A-Q7(c)：前面已算出 p̂ = 0.38，但求「至少多少只鸟」仍用 0.5 ⇒ n = 2400.9 ⇒ **2401**（代 0.38 会得 2263，丢分）。
- 2018A-Q13(b)：99%、E = 0.08 ⇒ n = 259.2 ⇒ **260**（key 原话：rounds up to 260）。
- 2018A-Q13(a) 要求**用微积分证明 p̂ = 0.5 时误差最大**：E ∝ √(p̂(1−p̂))，求导令其为 0 ⇒ p̂ = 0.5，再用二阶导或符号表确认是最大。

**B. 由区间反推 p̂、E、n、人数（四舍五入到最近整数）**
- 2024A-Q11：p̂ = 0.70，宽度 0.096 ⇒ E = 0.048 ⇒ n = 1.96² × 0.21 / 0.048² = 350.1 ⇒ **350**。
- 2018A-Q13(c)：(0.342, 0.558) ⇒ p̂ = 0.45，E = 0.108 ⇒ n ≈ 140.8 ⇒ 141，人数 ≈ 0.45 × 141 ≈ 63。
- 2022A-Q13(d)、2023A-Q12(c)(d)：已知区间和 n，反求置信水平：先求 E，再求 z = E/SE，最后由 z 得到置信水平（如 z = 1.645 ⇒ 90%）。

**C. 比例关系（CF）**：E ∝ 1/√n ⇒ 误差减半需要 n × 4（2017F-Q4）；宽度变为 1/3 需要 n × 9（2018F-Q5：200 → 1800）。

**真题**：2016A-Q10(d)、2017F-Q4、2018A-Q13、2018F-Q5、2019A-Q14、2020A-Q14、2022A-Q12(f)、2022A-Q13(d)、2023A-Q7(c)、2024A-Q10(f)、2024A-Q11(a)、2025A-Q16(e)。

---

## 题型 5：影响区间宽度的因素

| 变化 | 区间宽度 | 原因 |
|---|---|---|
| n 增大 | 变窄 | SE = √(p̂(1−p̂)/n) 变小 |
| 置信水平提高（90% → 99%） | 变宽 | z 变大 |
| p̂ 更接近 0.5 | 变宽 | p̂(1−p̂) 变大（2025A-Q16(d)(iii)：p̂ 远离 0.5 ⇒ E 减小） |

答题时要同时写「方向 + 原因」（2019A-Q14(b) 4 分：两个因素各占「因素」1 分、「影响」1 分）。若 n 变为 4 倍，宽度减半（2021A-Q13(f)）。

**真题**：2016A-Q14(c)、2019A-Q14(b)、2020A-Q12(g)、2021A-Q13(d)(f)、2022A-Q12(e)、2023A-Q12(f)、2024A-Q10(e)、2024A-Q11(c)、2025A-Q16(d)。

---

## 题型 6：抽样偏差 ★ 多数年份都有

**写法模板**（通常每个来源 1–2 分：指出来源 + 解释）
1. **指出来源**：location（只在商场/图书馆外）、time（工作日上午、午餐时间）、self-selection（自愿回答）、wording（问题带引导性，如「or an inferior brand?」）、sampling frame（只打手机号码、只抽转诊病历）、convenience（最先印出的 200 本、最新那台印刷机）。
2. **解释哪类人更多或更少被抽中**，并结合语境：时间和地点要分成两条写（2022 报告）。例（2020A-Q14(c)）：
   - Location：「Surveying outside the library over-represents people who already use the library, so p̂ would overestimate the proportion of residents who use it.」
   - Time：「Surveying only at lunchtime under-represents residents who work or study during the day and cannot be there then.」

**改进方法**：在整个总体（整周、全部四台印刷机）上随机抽样；用随机数选出时间和对象。

**真题**：2017A-Q12(a)、2018A-Q17(c)、2019A-Q13(b)(c)、2020A-Q14(c)、2022A-Q13(b)、2023A-Q7(d)、2024A-Q10(a)、2025A-Q16(a)。

---

## 题型 7：区间个数的二项分布

**识别**：「20 students each compute a 90% CI. X = number of intervals containing the true proportion.」
**思路**：X ~ Bin(20, 0.9)，E(X) = 18，Var(X) = 1.8；「3 个区间不包含 p」⇔ X = 17（2024A-Q9(d) 的 key 有 1 分给这一转换）。
**真题**：2016A-Q20(d)、2024A-Q9(b)–(d)。
