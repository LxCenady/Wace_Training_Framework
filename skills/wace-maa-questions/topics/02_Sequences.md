# SEQ · Growth and decay in sequences 数列增长与衰减 (Unit 3.2)

Bank: `<ROOT>\MAA\topics\02_Sequences.md` / `.pdf`. 23 questions with SEQ parts in 2016–2025 (no 2019 key), about 193 tagged marks (14% of the total). 9 of these are Calculator-free and 14 Calculator-assumed. Geometric growth and decay (SEQ5) is the largest pattern in the whole course by parts.

## Scope
- Arithmetic sequences: common difference, recursive rule, nth-term rule, the first term past a threshold.
- Geometric sequences: common ratio, percentage increase or decrease as a ratio (a 14% decrease is r = 0.86), recursive and general rules, the nth term.
- First-order linear recurrences T(n+1) = aT(n) + b: term-by-term tables and graphs, steady state S = b/(1 − a), long-term behaviour, whether a level can be sustained.
- Modelling a practical situation with a recurrence: interpret a and b, compare two options.
- Partial sums and cumulative totals (distance, total cost, when a target is reached).

## How SCSA asks it
- Arithmetic and geometric sequences in exact form (Calculator-free): 2016 CF Q4, 2017 CF Q1, 2021 CF Q6, 2025 CF Q1.
- Car depreciation, population decay, growth with a weekly or yearly rate (Calculator-assumed): 2016 CA Q7, 2017 CA Q10, 2024 CA Q7, 2022 CA Q9.
- Recurrence modelling with stated initial values, steady-state checks, and a judgement of long-term outcome: 2017 CA Q16, 2018 CA Q9, 2025 CA Q6.

## Patterns

| code | pattern | questions / marks (2016–25) | median part marks (range) | CF / CA parts | key past refs |
|---|---|---|---|---|---|
| SEQ1 | 等差数列递推生成 Generate an arithmetic sequence recursively | 8 / 16 | 2 (1–3) | 7 / 1 | 2016 CF Q4(b)(i); 2024 CF Q1(a)(i); 2025 CF Q1(a) |
| SEQ2 | 等差数列通项与项数预测 Arithmetic nth term and prediction | 10 / 45 | 2 (1–3) | 19 / 4 | 2017 CF Q1(b)(i)–(ii); 2022 CF Q2(c); 2023 CF Q3(b)–(d) |
| SEQ3 | 等差模型表格与离散图像 Tabular and graphical arithmetic models | 2 / 4 | 2 (1–3) | 2 / 0 | 2017 CF Q1(a); 2025 CF Q1(b) |
| SEQ4 | 等比数列递推生成 Generate a geometric sequence recursively | 7 / 17 | 2 (2–3) | 3 / 5 | 2016 CA Q7(a); 2016 CF Q4(a)(i); 2021 CA Q11(b)(i) |
| SEQ5 | 等比数列通项与增长衰减预测 Geometric nth term and growth or decay prediction | 14 / 75 | 2 (1–4) | 4 / 35 | 2016 CA Q7(b)–(e); 2017 CA Q10(a)–(e); 2024 CA Q7(a)–(c); 2021 CA Q12 |
| SEQ6 | 一阶线性递推逐项计算与呈现 Generate and display first-order linear recurrences | 4 / 9 | 1.5 (1–2) | 1 / 5 | 2017 CA Q16(b); 2018 CA Q9(b); 2025 CF Q1(e)(i) |
| SEQ7 | 递推长期趋势与稳定值 Long-term behaviour and steady state | 6 / 17 | 2 (2–3) | 1 / 7 | 2017 CA Q16(c)–(d); 2020 CA Q8(d); 2022 CA Q9(d) |
| SEQ8 | 递推关系建立与情境分析 Model a practical situation with a recurrence | 7 / 22 | 2 (1–3) | 1 / 12 | 2017 CA Q16(a); 2024 CA Q7(e); 2021 CF Q6(c) |
| SEQ9 | 数列部分和与累计总量 Sequence partial sums and cumulative totals (related) | 2 / 6 | 2 (1–3) | 0 / 3 | 2020 CA Q7(d); 2025 CA Q6(e) |

## Method in brief

- **SEQ1.** Confirm the constant difference d. Write the recursive rule in full with its starting value and subscript: T(n+1) = T(n) + d (d negative for a decrease). Then calculate term by term.
- **SEQ2.** Write the nth term in the form the key uses: T(n) = dn + c (gradient d, intercept c) or a + (n − 1)d, matched to the subscript. To find the first term past a threshold, solve the inequality, then take the next whole number (smallest integer n that satisfies it). Convert units (a daily change to a weekly change is × 7).
- **SEQ3.** Calculate the first few terms, enter them in a table, and plot discrete points only (do not join them). Label the axes and the scale.
- **SEQ4.** Common ratio r: a decrease of x% gives r = 1 − x/100; an increase gives r = 1 + x/100. Ratio of consecutive terms to find r from data. Recursive rule T(n+1) = rT(n) with its initial value.
- **SEQ5.** General term T(n) = a·rⁿ (or a·r^(n−1), matched to the question). Find the percentage rate as 1 − r for a decrease. Solve for n with a solver or logarithms and take the first whole period that meets the condition; state the conclusion as a period ("at the end of year 5"). For piecewise growth, calculate each segment and start the second from the end value of the first. For an average rate, compute the value after the first period, then set up the equation for the second rate. Round as asked, and keep fractions exact in calculator-free questions.
- **SEQ6.** Identify a, b and T0 in T(n+1) = aT(n) + b. Generate term by term, check the subscript against the question's time ("start of week 5"), and plot at the interval the question gives. To find a and b from three consecutive terms, write two equations and solve them together.
- **SEQ7.** Steady state S = b/(1 − a), valid only when |a| < 1. Compare S with the threshold in the question. The conclusion gives the numerical steady state, and rounds in the direction the context needs (round down when counting what can be removed).
- **SEQ8.** Split the change in each period into a multiplier (the proportion kept, 1 − loss rate, or 1 + growth rate) and a fixed amount added or removed. Write T(n+1) = aT(n) + b with T0 from the question. Interpret a as "proportion kept each period" and b as "fixed amount each period" with units. Comparing options needs the values for both.
- **SEQ9.** Sum the first n terms: arithmetic S(n) = n(T1 + Tn)/2; geometric S(n) = T1(1 − rⁿ)/(1 − r). Add any initial quantity after summing. When comparing two people, find each one's arrival day separately, then conclude.

## Writing tips
- Recursive rules always carry their initial value. Distinguish a recursive rule from the general nth-term rule, and write both if asked.
- Discrete quantities (people, fish, weeks, periods) are whole numbers. Money is to two decimal places.
- Calculator-free sequences: keep exact values (for example, a ratio of 0.85 is 17/20 as a fraction). Avoid powers you cannot compute by hand.
- Steady-state questions are a weak area in the examiners' reports. Always write the equation S = aS + b, solve it, and state what it means in context.
- Use CA for geometric growth and decay questions with several parts, and CF for arithmetic sequences and recurrences set up as tables.
