# BIV · Bivariate data analysis 双变量数据分析 (Unit 3.1)

Bank: `<ROOT>\MAA\topics\01_Bivariate_Data.md` / `.pdf`. 26 questions with BIV parts in 2016–2025 (no 2019 key), about 293 tagged marks (22% of the total). 12 of these questions sit in Calculator-free and 14 in Calculator-assumed.

## Scope
- Two-way frequency tables: totals, missing cells, row or column percentages.
- Comparing percentages and describing an association between categorical variables.
- Scatterplots: direction, form, strength; plotting points and axis labels.
- Correlation r and r²; least-squares line from the calculator; slope and intercept in context.
- Predicting from the line; interpolation versus extrapolation; how reliable a prediction is.
- Residuals, residual plots, and whether a linear model is appropriate.
- Explanatory versus response variable; association, causation, confounding.
- Rates from a multi-way table; recovering a total from a subgroup percentage.

## How SCSA asks it
- Two-way tables and percentage tables drawn from a survey (2016 CA Q11, 2017 CF Q5, 2022 CF Q3, 2025 CF Q2).
- A scatterplot, correlation and least-squares line on a small data set, with a summary of the findings (2017 CA Q12, 2021 CA Q9, 2023 CA Q10, 2025 CA Q9).
- Residuals, a residual plot, and a judgement of the model (2017 CA Q9, 2022 CA Q13, 2021 CF Q7).
- Short "explain in context" items on causation and on what the slope means (2022 CA Q11, 2025 CA Q9).

## Patterns

| code | pattern | questions / marks (2016–25) | median part marks (range) | CF / CA parts | key past refs |
|---|---|---|---|---|---|
| BIV1 | 双向频数表与边际量 Two-way frequency tables and margins | 10 / 46 | 2 (1–4) | 18 / 2 | 2016 CA Q11(a); 2017 CF Q5(a), (c); 2025 CF Q2(a) |
| BIV2 | 分类变量关联的比较描述 Describe association between categorical variables | 8 / 15 | 1 (1–2) | 12 / 1 | 2016 CF Q6(c); 2021 CF Q4(d); 2024 CF Q2(c) |
| BIV3 | 散点图与数值关联特征 Scatterplots and numerical association | 10 / 26 | 2 (1–2) | 2 / 13 | 2017 CA Q12(a), (d); 2022 CA Q11(a), (c) |
| BIV4 | 相关系数的计算与解释 Calculate and interpret correlation | 14 / 43 | 2 (1–3) | 3 / 20 | 2021 CA Q9(e); 2023 CA Q10(a); 2025 CA Q9(c) |
| BIV5 | 最小二乘回归线与残差检查 Least-squares line and residual diagnostics | 11 / 27 | 2 (1–3) | 1 / 16 | 2016 CA Q8(d); 2022 CA Q11(c); 2024 CA Q11(d) |
| BIV6 | 回归斜率与截距的语境解释 Interpret regression slope and intercept | 10 / 20 | 2 (1–2) | 1 / 11 | 2018 CF Q3(c)(i); 2024 CA Q11(e) |
| BIV7 | 决定系数与解释变异 Coefficient of determination | 11 / 18 | 1 (1–3) | 3 / 9 | 2016 CA Q8(e); 2020 CA Q10(f); 2025 CA Q9(i) |
| BIV8 | 预测与外推判断 Prediction and interpolation versus extrapolation | 13 / 38 | 1.5 (1–3) | 5 / 19 | 2016 CA Q8(f); 2020 CA Q10(g); 2025 CF Q5(a) |
| BIV9 | 关联、因果与混杂解释 Association, causation and confounding | 8 / 14 | 2 (1–2) | 2 / 7 | 2022 CA Q11(f); 2020 CF Q4(g); 2023 CA Q10(j) |
| BIV10 | 双变量统计调查结论整合 Bivariate investigation synthesis | 2 / 5 | 2.5 (2–3) | 1 / 1 | 2024 CA Q11(k); 2025 CF Q2(e) |
| BIV11 | 解释变量与响应变量识别 Identify explanatory and response variables | 10 / 11 | 1 (1) | 7 / 4 | 2016 CA Q8(a); 2024 CF Q2(b)(i); 2025 CA Q9(a) |
| BIV12 | 多分类表中的率值筛选与比较 Select and compare rates in categorical tables (related) | 2 / 12 | 2 (1–3) | 0 / 6 | 2016 CA Q11(b)–(d); 2018 CA Q10(b) |
| BIV13 | 由子群比例反求总体 Recover a population total from a subgroup proportion (related) | 1 / 2 | 2 | 0 / 1 | 2016 CA Q11(e) |
| BIV14 | 残差计算 Calculate residuals (related) | 8 / 21 | 2 (2–3) | 2 / 7 | 2017 CA Q9(b)(i); 2020 CA Q10(h); 2024 CA Q11(j) |
| BIV15 | 残差图绘制 Construct a residual plot | 8 / 19 | 2 (2–3) | 2 / 6 | 2021 CF Q7(b); 2022 CA Q13(d); 2025 CF Q5(d) |
| BIV16 | 用残差图评估线性模型 Assess a linear model from a residual plot | 8 / 14 | 2 (1–2) | 2 / 6 | 2020 CA Q10(e); 2021 CF Q7(c); 2025 CF Q5(e) |

## Method in brief

- **BIV1.** Row and column totals, the grand total checked both ways, then missing cells by subtraction. For a percentage table, take percentages within the groups of the explanatory variable. Put that variable in the rows for row percentages, in the columns for column percentages. Show the numerator, the denominator and the rounding.
- **BIV2.** Compare the matching percentages between groups and state the direction and size of the gap, in words that name the categories. Compare proportions, not counts.
- **BIV3.** Scatter diagram with labelled axes, the scale read carefully, and each point plotted. Describe direction, form (linear or curved) and strength.
- **BIV4.** Read r from the calculator's two-variable mode. The sign of r matches the slope. Describe r by direction and strength, and explain it using both variables. r describes linear association only.
- **BIV5.** Read the intercept and slope from the regression. Write the equation with the question's variable names, rounded as asked. Draw the line with a ruler between two x-values inside the data, state the two points, and check that the line passes near the plotted points.
- **BIV6.** Slope: for each one-unit increase in x (with its unit), y changes on average by the slope (name the direction, the size and the units). Intercept: the predicted y at x = 0; say it has no practical meaning if x = 0 is outside the data or unrealistic.
- **BIV7.** r² as a proportion or percentage. "About x% of the variation in y is explained by the linear relationship with x; the rest is unexplained." Going backwards: r² = 1 − unexplained proportion, then r takes the sign of the slope.
- **BIV8.** Substitute the given x. Check whether it lies within the observed range (interpolation) or outside it (extrapolation). Within range and r strong: reliable. Outside range: unreliable, whatever r is. When r is only moderate, say the prediction may not be valid.
- **BIV9.** Strong correlation does not prove causation. Name a specific third variable or the reverse direction, in context. For an outlier, give a real-world explanation.
- **BIV10.** Two or three statements that each combine a variable pair, a direction and a strength or basis, drawn from earlier parts.
- **BIV11.** The explanatory variable explains or predicts; the response variable is what is explained or predicted. A time order or a price set by a business can settle it. Give full variable names.
- **BIV12.** In a multi-way table, fix the base first (for example, the total for one dimension), then compare percentages, not counts. Each "highest" or "exception" claim must be checked against every other group.
- **BIV13.** Total = subgroup count ÷ the percentage (as a decimal). Convert units (for example, to millions).
- **BIV14.** Residual = observed − predicted. A negative residual means the observed value is below the prediction. Say whether the actual value is high or low relative to the prediction.
- **BIV15.** Horizontal axis is the explanatory variable (or the x-value of each residual); vertical axis is the residual; draw the zero line; plot each residual to scale.
- **BIV16.** Random scatter above and below zero with no trend: the linear model is appropriate. A curve, a funnel or a trend: it is not. Base the conclusion on the pattern in the plot, not only on the size of r.

## Writing tips
- Keep the explanatory variable first when you ask for percentages. The key checks the direction.
- Regression answers need the variable names from the stem, the rounding asked for, and a ruler-drawn line with two stated points.
- "Explain in context" means name both variables, the direction, the units, and "on average" or "predicted".
- Two-mark questions need working, not only a final answer.
- Use CF questions for BIV1, BIV2, BIV11 and the table-reading parts. Put regression, correlation, residuals and prediction in CA questions.
