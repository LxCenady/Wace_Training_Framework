# MAA · Bivariate Data Analysis — Patterns and Solution Approaches

> Source: marking keys and exam reports for 26 past exam questions from 2016–2025 (excluding 2019) carrying the BIV tag, 173 sub-questions in total (one sub-question may belong to several patterns). Based on the Specific behaviours descriptions in each sub-question's marking key, and on the exam reports for each year. 2019 has no marking key and is not included. Tags are drafts; some have been checked by hand. Pattern numbers agree with `evidence/maa/notes/BIV.txt`. ★ = patterns ranked in roughly the top quarter by marks per sub-question in this topic (for this topic, Patterns 1, 4, 5 and 8).
> Review status: every item has been checked line by line by an independent reviewer; the record is in the Chinese review log `MAA/methods/审校记录.md`. The labelling was revised on 2026-10-12, and no open review items remain.

## Marking-key reminders

- **Calculator-assumed (CA) papers: do all numerical calculations on the calculator** (2025 report: candidates are encouraged to use the calculator for every numerical calculation in the calculator-assumed section, even simple ones).
- **Draw least-squares lines with a ruler, and state the two points used to draw the line** (2017 report; the 2024 and 2025 reports repeat the ruler requirement).
- **Predictions outside the range of the data are unreliable** (2023 report: extrapolated predictions are unreliable; 2025 report: regression predictions outside the range are not regarded as valid). Writing a judgement of extrapolation or interpolation is a mark-earning point.
- **Explanations must be tied to the context** (2022 report stresses what "in the context of the question" means; 2023 report: questions requiring justification or explanation are generally difficult; 2024 report: in-context explanation questions are a weak area). Write the variable names, units and direction of change.
- **Identifying association from a table of percentages is a weak area** (2024 and 2025 reports; both years name it in Section One). See Patterns 1 and 2.
- **The sign of r and square roots** (2023 report: a square root cannot be negative). When finding r from r², the sign is set by the slope.
- **Two-mark questions also need working shown** (2017, 2021 and 2025 reports). An answer with no intermediate steps may earn no marks even if correct.
- **Write the regression equation with the variable names given in the question** (2023 report).

---

## Pattern 1: Two-way frequency tables and margins ★

**Recognition**: A cross-table of two categorical variables is given, and you are asked to complete the row and column totals, the missing cells, or a percentage table ("complete the two-way table" / "percentaged table").

**Standard procedure**
1. Row total = sum of the cells in that row; column totals are found the same way. The grand total must agree with both directions, which serves as a check.
2. Missing cell: work back from the total (total minus the known cells).
3. For a percentage table, first decide the direction: take percentages within the groups of the explanatory variable, so that each group of the explanatory variable sums to 100%. If the explanatory variable is in the rows, use row percentages (each row sums to 100); if it is in the columns, use column percentages (each column sums to 100). The key's ruling on row or column percentages is exactly this decision (2021F-Q4(c), 2023F-Q1(c)(i), 2024F-Q2(c)(i), etc.). How the explanatory variable is identified in each question is set out under Pattern 11. The key rulings on all five percentage tables agree with this.
4. Each percentage = cell frequency ÷ total of its group × 100. Keep enough decimal places on the calculator, then round to one decimal place or a whole number as the question requires.

**Mark-earning points (typical key wording)**: correct cells are awarded in steps (at least 2 or 3 correct, all correct); choosing the right row or column percentage is itself worth marks; when the question says "show how", write out the numerator, denominator and calculation (2017F-Q5(c)(i), 2022F-Q3(c)(i)).

**Common errors**: direction chosen wrongly, which makes the whole table's percentages meaningless; the denominator uses the grand total instead of the group total; forgetting the decimal places the question requires.

**Past questions**: 2016A-Q11(a), 2016F-Q6(a), 2017F-Q5(a), 2017F-Q5(c)(i), 2017F-Q5(c)(ii), 2018A-Q10(a), 2020F-Q1(b), 2021F-Q4(a), 2021F-Q4(c), 2022F-Q3(a), 2022F-Q3(c)(i), 2022F-Q3(c)(ii), 2023F-Q1(a), 2023F-Q1(c)(i), 2024F-Q2(a), 2024F-Q2(c)(i), 2025F-Q2(a), 2025F-Q2(b)(i), 2025F-Q2(b)(ii), 2025F-Q2(c)

---

## Pattern 2: Describe association between categorical variables

**Recognition**: You are asked to compare two groups' percentages and describe the association ("compare the percentages", "describe the association", "comment").

**Standard procedure**
1. Take the response percentages for each group of the same explanatory variable (if the question gives frequencies, convert them to percentages first).
2. Compare: which group has the higher or lower proportion, and by how much.
3. Put it in context: write the category names and the meaning of the variables into the conclusion, and make the direction clear.
4. If the question says "comment on", give both whether there is an association and its direction.

**Mark-earning points**: correctly calculate the percentages needed (2016F-Q6(b)); state the direction of the association (2016F-Q6(c)(i)–(iii), 1 mark for each comparison); describe it using the percentage difference (the key for 2020F-Q1(c) requires quoting the percentage difference from (b)).

**Common errors**: saying only "there is an association" without the direction; comparing frequencies instead of proportions; comparing groups that do not correspond (2016F-Q6(c)(iii) compares A with the combined B and C).

**Past questions**: 2016F-Q6(b), 2016F-Q6(c)(i), 2016F-Q6(c)(ii), 2016F-Q6(c)(iii), 2017F-Q5(d), 2018A-Q10(c), 2020F-Q1(c), 2021F-Q4(d), 2022F-Q3(d), 2023F-Q1(c)(ii), 2024F-Q2(c)(ii), 2025F-Q2(d)(i), 2025F-Q2(d)(ii)

---

## Pattern 3: Scatterplots and numerical association

**Recognition**: You are asked to plot points on a scatter diagram, label the axes, or describe the relationship between two numerical variables (direction, form, strength).

**Standard procedure**
1. Drawing: read the scale first (misreading the scale is a repeated point of lost marks, 2017 and 2022 reports). Plot the points on the axes the question specifies, and label both axes with the variable names.
2. When describing association, give three elements: direction (positive or negative), form (linear or non-linear), and strength.
3. If the form is clearly curved, state directly that it is non-linear (2017A-Q12(d)).

**Mark-earning points**: each correctly plotted point earns marks (2018A-Q15(a): 1 mark for each of two points; 2020F-Q4(a): at least 3 points, all points; 2017A-Q12(a): 2 points, 3 points); axis labels (2016A-Q8(b)); the description gives both strength and form (2018F-Q3(a)).

**Common errors**: axes not labelled; scale misread; saying "positive correlation" without the strength; describing a curved relationship as linear.

**Past questions**: 2016A-Q8(b), 2016A-Q8(c), 2017A-Q12(a), 2017A-Q12(d), 2018A-Q15(a), 2018F-Q3(a), 2020F-Q4(a), 2021A-Q9(b), 2022A-Q11(a), 2023A-Q7(b), 2023A-Q7(d), 2024A-Q11(b), 2025A-Q9(b)

---

## Pattern 4: Calculate and interpret correlation ★

**Recognition**: The question uses command words such as "calculate", "state", "describe" or "explain" and asks you to calculate or write r, describe its direction and strength, or explain what r means.

**Standard procedure**
1. Enter all the data in the calculator's two-variable statistics mode and read off r (the regression equation and r² can be read at the same time).
2. Sign: r has the same sign as the slope of the least-squares line. If only r² is given, r = ±√r², and the sign is set by the slope (2024A-Q11(a): the key requires both r² and r to be found, and accepts a negative value).
3. Description: direction (positive or negative) + strength (using the numerical value of r given in the question) + linear. In the evidence for this topic, a key with r ≈ −0.6 is described as moderate (2020F-Q4(b)); r = 0.97 is described as strong (2017A-Q9(a)(iv)), and r = 0.814 is a similar case under Pattern 3.
4. Explanation questions (in context): name both variables, and state that r describes only the strength and direction of a linear association.

**Mark-earning points**: the value of r (1 mark on its own, e.g. 2021A-Q9(e)(i)); direction and strength, 1 mark each (2021A-Q9(e)(iii), 2022A-Q11(d)); explanation questions must mention both variables (2022A-Q13(b)).

**Common errors**: treating r² as r; dropping the minus sign (2023A-Q10(g) asks for an explanation of why r is negative, and needs the link between the square root and the slope); describing r as "causing" something (see Pattern 9); for "choose the most likely r" questions such as 2017A-Q12(c), look at both the direction and the spread of the graph.

**Past questions**: 2016A-Q8(c), 2016A-Q8(f)(i), 2017A-Q9(a)(iv), 2017A-Q12(c), 2018A-Q15(b)(i), 2018A-Q15(b)(ii), 2020A-Q10(a), 2020F-Q4(b), 2021A-Q9(e)(i), 2021A-Q9(e)(ii), 2021A-Q9(e)(iii), 2021F-Q7(d), 2022A-Q11(b), 2022A-Q11(d), 2022A-Q13(b), 2023A-Q10(a), 2023A-Q10(g), 2023A-Q10(h), 2024A-Q11(a), 2024A-Q11(c), 2025A-Q9(c), 2025A-Q9(g), 2025F-Q5(f)

---

## Pattern 5: Least-squares line and residual diagnostics ★

**Recognition**: You are asked to determine the least-squares equation, or to draw the least-squares line on a scatter diagram.

**Standard procedure**
1. Use the calculator's linear regression to read the intercept and slope.
2. Form of the equation: use the variables given in the question (if the question uses w and v, write w and v; the 2023 report requires this). Round to the number of decimal places the question asks for (e.g. one decimal place, 2016A-Q8(d)(i)).
3. Drawing the line: take two values of x (usually the two ends of the data range), calculate the corresponding y, plot the two points, and join them with a ruler. Key checks: whether the line passes near the approximate points (e.g. (28, 29) in 2022A-Q11(c)) and whether the direction of the slope is correct.
4. If the same question also asks for r, write both (2018A-Q15(b)(i), 2023A-Q10(a)).

**Mark-earning points**: the slope and intercept each earn marks (2016A-Q8(d)(i)); the two points used to draw the line are correct and stated (2016A-Q8(d)(ii)); the drawn line passes near the approximate points and has the correct slope (2022A-Q11(c), 2023A-Q7(c)).

**Common errors**: intercept and slope written the wrong way round; variable names not taken from the question; only one point plotted, or the two points used to draw the line not stated; line not drawn with a ruler.

**Past questions**: 2016A-Q8(d)(i), 2016A-Q8(d)(ii), 2017A-Q9(a)(i), 2017A-Q12(b), 2018A-Q15(b)(i), 2020A-Q10(b), 2021A-Q9(c), 2021A-Q9(g)(ii), 2022A-Q11(b), 2022A-Q11(c), 2023A-Q7(c), 2023A-Q10(a), 2023A-Q10(f), 2024A-Q11(d), 2024A-Q11(i), 2025A-Q9(c), 2025A-Q9(d), 2025F-Q5(c)

---

## Pattern 6: Interpret regression slope and intercept

**Recognition**: You are asked to interpret the slope (gradient) or the intercept, or to explain why the intercept has no practical meaning.

**Standard procedure**
1. Slope: for each increase of 1 unit of x (state the unit), y increases on average (if positive) or decreases (if negative) by the size of the slope. Write the names and units of both variables.
2. Intercept: the predicted value when x = 0. If x = 0 is unrealistic in context or outside the range, state that the intercept has no practical meaning (2024A-Q11(f)).
3. Use the wording "on average" or "predicted", not a definite change.

**Mark-earning points**: direction (increase or decrease), and the numerical value and unit, each earn marks (2018F-Q3(c)(i): 1 mark for direction, 1 mark for the value and unit; 2024A-Q11(e): the wording of a decrease of 0.38 kg); both variables must appear (2016A-Q8(d)(iii), 2021A-Q9(d)).

**Common errors**: writing "increase" when the slope is negative (the key for 2024A-Q11(e) requires "decrease"); omitting the unit; saying only "for each unit increase" without stating the unit of x (2020A-Q10(c) requires the wording "per 1 cm").

**Past questions**: 2016A-Q8(d)(iii), 2017A-Q9(a)(iii), 2018A-Q15(b)(iii), 2018F-Q3(c)(i), 2020A-Q10(c), 2021A-Q9(d), 2022A-Q13(a), 2023A-Q10(b), 2023A-Q10(i), 2024A-Q11(e), 2024A-Q11(f), 2025A-Q9(e)

---

## Pattern 7: Coefficient of determination

**Recognition**: You are asked to calculate the coefficient of determination r², or to state what proportion of the variation is explained and what proportion is unexplained.

**Standard procedure**
1. r² = r squared; when written as a percentage, multiply by 100%.
2. Interpretation: state that about x% of the variation in y can be explained by the linear relationship with x, and the rest is unexplained variation; use the variable names from the context.
3. Reverse questions: when the unexplained proportion is given, r² = 1 − unexplained proportion, and r is then found from r² (sign from the slope, see Pattern 4). For example, 2024A-Q11(a): from "51% cannot be explained", obtain the value corresponding to r², and then find r.
4. Given r, find r²; or given the explained proportion, find r (2018F-Q3(b)).

**Mark-earning points**: r² or the percentage correct (e.g. in 2016A-Q8(e), the calculation and the interpretation each earn marks); interpretation in context (2020F-Q4(d), 2023A-Q7(e)); the unexplained proportion (the key for 2020A-Q10(f) awards it separately).

**Common errors**: mixing percentages and decimals; confusing "explained" with "unexplained"; giving the number without the context; forgetting the sign when finding r.

**Past questions**: 2016A-Q8(e), 2017A-Q9(a)(v), 2018A-Q15(b)(iv), 2018F-Q3(b), 2020A-Q10(f), 2020F-Q4(c), 2020F-Q4(d), 2021A-Q9(f), 2022A-Q11(e), 2023A-Q7(e), 2024A-Q11(a), 2025A-Q9(i)

---

## Pattern 8: Prediction and interpolation versus extrapolation ★

**Recognition**: You are asked to predict, to estimate using the equation, to comment on whether a prediction is valid, or to judge whether a prediction is reliable. The pattern also includes the reverse: given a predicted value, find the original variable (2023A-Q10(e)).

**Standard procedure**
1. Substitute: put the x given in the question into the regression equation. Watch the variable coding, e.g. n = 25 represents a particular year (2025F-Q5(a)).
2. Check the range: if x is within the observed data range, it is interpolation; if outside, it is extrapolation.
3. Combine with the strength of r: within the range and with strong r, the prediction is reliable (2016A-Q8(f)(i), 2022A-Q13(c)(ii), 2025F-Q5(b)); outside the range, the prediction is unreliable (2018F-Q3(c)(ii), 2020A-Q10(g)(ii), 2022A-Q11(g)(ii), 2024A-Q11(h)).
4. When there is more than one predictor variable, choose the one with the strongest r as the basis for prediction, and give the reason (2023A-Q10(h)).
5. If the predicted value differs from the actual value in the table, explain it by the residual or by the imperfection of the model (2025A-Q9(f)(ii)).
6. Explain why extrapolation is meaningless, usually in context (2021A-Q9(h), 2025A-Q9(f)(iii)).

**Mark-earning points**: correct substitution (1 mark for each predicted value); the conclusion is valid or invalid, with reasons, and the reasons include the range judgement (interpolation or extrapolation) and the strength of r (2020F-Q4(f): when r is only moderate, the conclusion should be written as possibly not valid).

**Common errors**: judging the range using the value of r rather than the values of x; writing "not valid" without writing extrapolation; writing "reliable" when r is only moderate; substituting without a consistent variable coding.

**Past questions**: 2016A-Q8(f)(i), 2016A-Q8(f)(ii), 2017A-Q9(a)(ii), 2018A-Q15(d), 2018F-Q3(c)(ii), 2020A-Q10(g)(i), 2020A-Q10(g)(ii), 2020F-Q4(e), 2020F-Q4(f), 2021A-Q9(g)(i), 2021A-Q9(h), 2022A-Q11(g)(i), 2022A-Q11(g)(ii), 2022A-Q13(c)(i), 2022A-Q13(c)(ii), 2023A-Q10(e), 2023A-Q10(h), 2024A-Q11(g), 2024A-Q11(h), 2025A-Q9(f)(i), 2025A-Q9(f)(ii), 2025A-Q9(f)(iii), 2025F-Q5(a), 2025F-Q5(b)

---

## Pattern 9: Association, causation and confounding

**Recognition**: You are asked to judge whether a statement is correct, give a non-causal explanation, identify other factors, or judge whether there is evidence to support causation.

**Standard procedure**
1. Core point: an observed association, even a strong r, cannot on its own prove causation.
2. Common non-causal explanations: a third variable (a confounding factor) affecting both variables; the direction of causation is reversed; coincidence.
3. For a causal statement of the form "X causes Y": state that a statistical association does not establish causation, and give one possible other factor (2022A-Q11(f)).
4. For outliers: give a possible real-world explanation (2022A-Q13(f)).

**Mark-earning points**: judging the statement not valid (2017A-Q12(e), 2021A-Q9(i), 2023A-Q10(j)); the reason states that other factors are possible (2020F-Q4(g)); a specific non-causal explanation (2018F-Q3(d)).

**Common errors**: concluding causation because r is strong; reasons too general, with no specific factor named in context; for 2-mark questions, writing only that correlation is not causation without giving the context.

**Past questions**: 2017A-Q12(e), 2018F-Q3(d), 2020F-Q4(g), 2021A-Q9(i), 2022A-Q11(f), 2022A-Q13(f), 2022A-Q13(g), 2023A-Q10(j), 2025A-Q9(h)

---

## Pattern 10: Bivariate statistical investigation synthesis

**Recognition**: At the end of an investigation question, you are asked to make reasonable statements, or to judge in an overall question whether a conclusion is reasonable.

**Standard procedure**: bring together the associations found in the earlier sub-questions (in both directions, rows and columns), the reliability of predictions, and whether the model is appropriate, and write 2–3 well-supported statements. Each statement includes the variables, a direction, strength or the basis for it.

**Mark-earning points**: each valid statement earns marks (the key for 2024A-Q11(k) awards marks by the number of valid statements); comment on the association in both rows and columns (2025F-Q2(e)).

**Common errors**: statements with no context, which only restate numbers.

**Past questions**: 2024A-Q11(k), 2025F-Q2(e)

---

## Pattern 11: Identify explanatory and response variables

**Recognition**: You are asked to identify the explanatory or response variable, or to explain why a view is incorrect.

**Standard procedure**: first read the research question (e.g. "use … to explain …", "predict …"). The explanatory variable is the one used to explain or predict; the response variable is the outcome being explained or predicted. If the question involves time order, or a variable is set by a person (for example, a price set by the business), give the reason (2024F-Q2(b)(i)).

**Mark-earning points**: variable names match the stem; when used for a percentage table, the explanatory variable determines the direction of the percentages (see Pattern 1).

**Common errors**: the two roles reversed; writing only "age" instead of the full variable name; ignoring the causal direction given in the question.

**Past questions**: 2016A-Q8(a), 2017F-Q5(b), 2020F-Q1(a), 2021A-Q9(a), 2021F-Q4(b), 2022F-Q3(b), 2023A-Q7(a), 2023F-Q1(b), 2024F-Q2(b)(i), 2024F-Q2(b)(ii), 2024F-Q2(c)(i), 2025A-Q9(a)

---

## Pattern 12: Select and compare rates in categorical tables

**Recognition**: You are asked to find which state, age group or sex has the highest or lowest rate, or to compare one category's rate with the others. The table has many dimensions, and the question asks for the largest or smallest rate.

**Standard procedure**
1. In a multi-way table, first fix the base for the comparison (for example, the total for one dimension), then calculate or read each cell's percentage.
2. Work through each dimension in turn (sex, age, state), settling each level.
3. Compare using rates, not counts (2018A-Q10(b): first take the numerator, then calculate the percentage for each state).
4. Statements such as "almost the lowest" or "the only exception" must be checked against each of the other groups (2016A-Q11(d)).

**Mark-earning points**: the correct category for each dimension, 1 mark each (2016A-Q11(b) has three dimensions); the comparison conclusion identifies the exception (2016A-Q11(d)); compare the percentage difference between two states (2018A-Q10(b)).

**Common errors**: comparing counts instead of rates; leaving out the base group for comparison.

**Past questions**: 2016A-Q11(b), 2016A-Q11(c), 2016A-Q11(d), 2018A-Q10(b), 2018A-Q10(d)


---

## Pattern 13: Recover a population total from a subgroup proportion

**Recognition**: The number of people in a subgroup and the percentage it forms of the whole are known, and the total population is asked for. There is only one sub-question in the evidence (2016A-Q11(e)), so this section is brief.

**Standard procedure**: total = subgroup number ÷ percentage (convert the percentage to a decimal first). If the question asks for a unit (e.g. millions), convert.

**Mark-earning points**: use the correct formula (the key checks whether the correct formula is used); unit conversion (the key requires the answer in millions).

**Common errors**: percentage not converted to a decimal; unit conversion forgotten.

**Past questions**: 2016A-Q11(e)

---

## Pattern 14: Calculate residuals

**Recognition**: You are asked to calculate residuals, or to find a missing residual.

**Standard procedure**
1. Definition of a residual: residual = observed value − predicted value (consistent with the catalogue definition).
2. Predicted value = the explanatory variable's value substituted into the least-squares equation.
3. Check the sign: a negative residual means the observed value is below the predicted value (the key for 2020A-Q10(h) requires the statement "below the prediction").
4. Residuals can be used directly to draw a residual plot (Pattern 15).

**Mark-earning points**: each residual earns 1 mark (2017A-Q9(b)(i): C and D, 1 mark each; 2024A-Q11(j): the key awards the first missing residual, the second missing residual and the plot in turn); when explaining what a residual means, state whether the actual value is high or low relative to the predicted value (2020A-Q10(h)).

**Common errors**: residual direction reversed (predicted minus observed); wrong variable substituted into the equation; explaining a residual only as "high" or "low" without saying relative to the prediction.

**Past questions**: 2017A-Q9(b)(i), 2018A-Q15(c)(i), 2020A-Q10(d), 2020A-Q10(h), 2021F-Q7(a), 2022A-Q13(d), 2023A-Q10(c), 2024A-Q11(j), 2025F-Q5(d)

---

## Pattern 15: Construct a residual plot

**Recognition**: You are asked to plot residuals on a graph, or to complete a residual plot.

**Standard procedure**
1. The horizontal axis is the explanatory variable the question specifies (e.g. age, price, year, or the x-value to which each residual belongs); the vertical axis is the residual.
2. Draw the zero line (residual = 0) as a reference.
3. Plot the points to scale; negative residuals go below the zero line. Read the scale carefully (2017 and 2022 reports).

**Mark-earning points**: each residual point is correct (2021F-Q7(b): 1 mark for each of two residuals; 2022A-Q13(d): at least one, at least three, all points); the residuals are values calculated in the preceding part (2025F-Q5(d) requires predicted values to be calculated first, then residuals).

**Common errors**: horizontal axis wrongly chosen; negative residuals plotted above the zero line; scale misread.

**Past questions**: 2017A-Q9(b)(ii), 2018A-Q15(c)(i), 2020A-Q10(d), 2021F-Q7(b), 2022A-Q13(d), 2023A-Q10(c), 2024A-Q11(j), 2025F-Q5(d)

---

## Pattern 16: Assess a linear model from a residual plot

**Recognition**: You are asked to judge from a residual plot whether a linear model is appropriate, which feature shows that the model is appropriate, or to argue whether the least-squares line is a good model.

**Standard procedure**
1. Check whether the residuals show a systematic pattern: if they are scattered randomly on both sides of the zero line with no obvious trend, the linear model is appropriate (2020A-Q10(e)).
2. If the residuals are curved, funnel-shaped, or show a clear trend, the linear model is not appropriate (2017A-Q9(b)(iii), 2025F-Q5(e)).
3. The conclusion must be supported: write the pattern of the residuals itself, not just the conclusion.
4. When combined with r, the value of r must be considered together with the residual pattern (the key for 2021F-Q7(c) gives the reason the pattern is inappropriate).

**Mark-earning points**: the conclusion is correct (appropriate or not appropriate); the basis is correct (state that there is no pattern, or state the pattern that is present).

**Common errors**: writing "not appropriate" without describing the residual pattern; using the size of r in place of the residual plot as the basis (the size of r is a separate basis, covered under Pattern 4, and the two must be written separately).

**Past questions**: 2017A-Q9(b)(iii), 2018A-Q15(c)(ii), 2020A-Q10(e), 2021F-Q7(c), 2022A-Q13(e), 2023A-Q10(d), 2025A-Q9(g), 2025F-Q5(e)

---
