# MAA · Time Series Analysis — Patterns and Solution Approaches

> Source: marking keys and exam reports for 10 past exam questions from 2016–2025 containing time series material, 68 sub-question tags (one sub-question may belong to several patterns; 64 distinct sub-questions after removing duplicates). 2019 has no marking key and is not included. Tags are drafts; on 2026-10-11 they were checked by an independent reviewer against the original papers and keys (results in the Chinese review log `MAA/methods/审校记录.md`). The original questions and marking keys are not published with the repository; see the local `evidence/maa`.
> Numbering: `2023A-Q8(h)` = sub-question (h) of question 8 of the 2023 Calculator-assumed paper; `F` = Calculator-free. ★ = patterns ranked highest by marks per sub-question in this topic (roughly the top quarter): TSI4 and TSI7.
> Values marked as "author's check" were calculated by the note's author from the data in the evidence table, to illustrate the method. They are not the answers in the keys.

## Marking-key reminders

- **Percentages and basic arithmetic**: converting actual values into percentages of the mean, and multiplying and dividing decimals, is a source of lost marks every year (2017 report: converting 16 out of 80 to a percentage gave difficulty; 2021 report: converting fractions to percentages was weak; 2022 and 2023 reports: basic arithmetic is a general problem).
- **Write explanations tied to the context of the question**: the 2023 and 2025 reports both advise teachers to answer "in the context of the question"; the 2024 report notes that in-context explanation questions are a weak area. When explaining seasonal indices, trends or forecasts, name the specific season, period and unit.
- **Predictions outside the data range are unreliable**: the 2023 report advises teachers that regression predictions for values beyond the range of the data are unreliable; the 2025 report repeats that regression predictions outside the data range are not regarded as valid.
- **Drawing and writing least-squares lines**: draw the line with a ruler, and mark the points used to draw it (2017 report); write the equation with the variables given in the question (2023 report); draw lines with a ruler (2024 and 2025 reports).
- **Reading graph scales**: take care reading the scale when drawing time series plots and reading the vertical axis (2017, 2019 and 2022 reports).
- **Recognising moving averages**: the 2025 report identifies recognising a moving average from a time series graph as a weak point for candidates (Section Two).
- **Calculator and working**: the 2024 and 2025 reports encourage using the calculator for all numerical calculations in the Calculator-assumed paper; the 2019 and 2020 reports require two-mark questions to show working, and the 2022 report advises keeping working so that follow-through marks can be awarded.

---

## Pattern 1: Plot and read time series

**Recognition**: The question asks you to complete the time series plot, add points and join them on a time series graph, or draw the least-squares line on the graph (fit this line to the graph, draw the least-squares line).

**Approach**
1. The horizontal axis is time (quarter number Q, data number n, or date), and the vertical axis is the value. When filling in data, first find the corresponding time number in the table, then plot the point.
2. Join the points in time order to form a line; do not skip missing periods.
3. To draw the least-squares line: use the equation given in the question, calculate two points (usually the point with time number 1 and a point with a larger time number), join them with a straight line, and make sure the line extends across the range of the data.
4. The time numbering must match the question: if the equation has Q = 1 for the first quarter, do not start counting from 0.

**Mark-earning points (typical key wording)**
- The marks for the intercept and slope are set out under Pattern 6.
- At least two points plotted correctly; all points plotted correctly and joined into a line (2018A-Q13(a), 2 marks).
- A correct point is plotted first, then a second point is plotted and the least-squares line is extended through the given data (2021A-Q8(d)).

**Common errors**
- Off-by-one in the time numbering, leading to the intercept in the wrong place.
- The line does not pass through the data region, or only one point is plotted.
- The 2017 report advises that when drawing the least-squares line, the points used to draw it must be clearly marked.

**Past questions**: 2018A-Q13(a), 2021A-Q8(d)

---

## Pattern 2: Trend, seasonality, irregular variation and outliers

**Recognition**: The question asks you to describe the trend, or to describe the trend and seasonality, or asks how the sales or visits in a particular period should be interpreted.

**Approach**
1. Trend: look at the overall direction over the long run. A negative slope of the least-squares line means a long-run decrease; a positive slope means a long-run increase (the key for 2016A-Q10(c)(i) judges a decrease on this basis).
2. Seasonality: identify the regular peaks and troughs, i.e. high and low seasons, and name the season or the day of the week (2018A-Q13(b)(ii)).
3. Irregular variation: the fluctuation that remains after the trend and seasonal components are removed. None of the time series sub-questions for 2016–2025 asks for outliers to be identified; outlier questions in bivariate data (BIV) are outside the scope of this note.
4. Choosing a period for staff leave (2020A-Q14(d)): to minimise the effect on business, choose the period with the lowest seasonal index (a low season), and use the seasonal indices as evidence. The key's answer is winter, on the basis that the winter seasonal index of 74.6 is the lowest of the four seasons.

**Mark-earning points (typical key wording)**
- Correct direction of the trend (2016A-Q10(c)(i), 1 mark).
- Both trend and seasonality mentioned: the overall trend is correct, and high and low seasons are both mentioned (2018A-Q13(b)(ii), 2 marks).
- Correct season chosen (winter), with the mathematical basis (the seasonal index of 74.6 is the lowest), 2 marks (2020A-Q14(d)).
- 2018A-Q12(c) also belongs to Pattern 3, asking for the most suitable moving average to be chosen with reasons.

**Common errors**
- Writing only "increasing" or "decreasing" without describing the seasonal pattern.
- Confusing the sign of the slope with whether the trend rises or falls, or stating the slope without explaining it in context.

**Past questions**: 2016A-Q10(c)(i), 2018A-Q12(c), 2018A-Q13(b)(ii), 2020A-Q14(d)

---

## Pattern 3: Simple moving average smoothing

**Recognition**: The question asks you to calculate a 3-point, 4-point, 5-point or 6-point moving average (or a centred moving average), to complete a table of moving averages, to explain the purpose of a moving average, or to choose the most suitable moving average.

**Approach**
1. Odd-point moving averages (3-point, 5-point): take a set of consecutive data centred on the period, average them, and place the result in the middle period.
   Example (author's check, data from 2017A-Q15(a)): the 3-point moving average at t = 4 = (18 + 24 + 21)/3 = 21.
2. Even-point centred moving averages (4-point, 6-point): the window has an even number of values, so the average cannot sit exactly on one period. Use half weights on the first and last values, then divide by the window length.
   Example (author's check): the 6-point centred moving average at t = 4 = (½ × 14 + 17 + 18 + 24 + 21 + 19 + ½ × 16)/6 = 19.
3. Completing a table: where some moving average values are known, the missing data or intermediate values can be worked back (2018A-Q12(b) requires the three missing values A, B and C to be found).
4. Choosing a suitable moving average: the length of the cycle (season) determines the window. Quarterly data have a cycle of 4; daily data have a cycle equal to the number of trading days in a week (the data in 2021A-Q8(a) give a seasonal mean of 17.6 = (12 + 14 + 14 + 20 + 28)/5, showing a 5-day cycle; the key's answer is the 5-point moving average).
5. Explaining the purpose of a moving average: it smooths out short-term, periodic fluctuations so that the long-run trend is clearer (the key for 2018A-Q12(a) accepts this reason).
6. Working back from a centred moving average to actual values (2018A-Q13(c)): first find the period that corresponds to the 4-point centred moving average, then work back from the values given in the question.

**Mark-earning points (typical key wording)**
- The 3-point moving average is calculated correctly (2017A-Q15(a)(i), 1 mark).
- 6-point centred moving average: halve the first and last data, then average (2017A-Q15(a)(ii), 2 marks; the 2017 key gives this halving step explicitly).
- Explain the purpose of moving averages, with reasons that have practical meaning (2018A-Q12(a), 1 mark).
- Completing the table: A, B and C, 1 mark each (2018A-Q12(b), 3 marks).
- Choosing a moving average and giving a reason (2018A-Q12(c), 2 marks): the key's answer is the 5-point moving average, with the reason that the data have a 5-point cycle or that the 5-point column keeps falling.
- 2025A-Q7(a) (2 marks): the key's answer is the 6-point centred moving average; the two mark-earning points are "writing a correct moving average" and "stating that it is centred".
- 2022F-Q5(a) requires the full working for the bold figures in the table: addition, division by 3, conversion to a percentage (3 marks).

**Common errors**
- Forgetting to centre an even-point moving average, or forgetting to halve the first and last values.
- Placing moving average values in the wrong row, away from the central period.
- In 2018A-Q12(c), the 3-point or 4-point column cannot be chosen; the key chooses the 5-point column.

**Past questions**: 2017A-Q15(a)(i), 2017A-Q15(a)(ii), 2018A-Q12(a), 2018A-Q12(b), 2018A-Q12(c), 2018A-Q13(c), 2021A-Q8(a), 2022F-Q5(a), 2023A-Q8(a), 2025A-Q7(a)

---

## Pattern 4: Seasonal indices by average percentage method ★

**Recognition**: The question asks you to use the average percentage method, to calculate the percentage of actual values to the mean for a period, to complete a table of seasonal indices, to find the seasonal index for a season or a day of the week, or to explain the meaning of a seasonal index.

**Approach (steps)**
1. Find the seasonal mean: for quarterly data, use the centred 4-point moving average or the quarterly average; for daily data, use the weekly average, or a moving average matching the cycle.
2. Calculate percentages: the percentage for a period = actual value ÷ corresponding seasonal mean × 100%.
   Check (author's check, data from 2021A-Q8): the seasonal mean of 17.6 corresponds to a 5-day week with data 12, 14, 14, 20, 28; the entry 14 gives a percentage of 14 ÷ 17.6 = 79.55%, which agrees with the table.
3. Group the percentages by season or day of the week, and average the percentages for each group, giving the raw seasonal index (average percentage).
4. Normalising: the indices must average to 100%. The quarterly indices sum to 400% (note in the key for 2023A-Q8(b)), so the average of the seasonal indices is 100%.
   Check (data from 2016A-Q10(b)(i)): the indices for the five weekdays are 1.294, 1.520, ?, 0.568, 1.028. The key's main answer averages the three Wednesday percentages, (63.3% + 60.8% + 63.4%) ÷ 3 = 62.5%, i.e. 0.625; the key also accepts 0.590 (59.0%), obtained as "5 minus the sum of the other four indices".
5. Interpreting indices: an index above 100% means that season (or day) is above the average level; below 100% means below average. When explaining, state the specific season or day of the week, and say whether it is compared with the mean or with the trend value.
6. In calculations, use the decimal form (e.g. 1.1076); do not multiply or divide percentages directly.

**Mark-earning points (typical key wording)**
- Find each missing value in the table, rounding as required: 2016A-Q10(a) requires C to one decimal place (4 marks in total).
- Completing the seasonal index table: 2016A-Q10(b)(i), 2017A-Q15(b)(ii), 2018A-Q13(d)(i), 2021A-Q8(c), 1 mark each.
- Completing several cells: one mark per blank (2020A-Q14(b): the winter and spring indices, 1 mark each). For 2023A-Q8(b) (1 mark): the key's table gives 58.83%, 76.19%, 155.72%, 109.26%, which sum to 400%; the key's note says that averaging the winter components directly gives 155.55%, but the table states 155.72%, so the answer follows the key.
- Interpreting seasonal indices (2023A-Q8(c), 2024A-Q8(d), 2025A-Q7(c)): state the season or day, and state how far it is above or below average. 2025A-Q7(c) (2 marks) is a fill-in: "On average, Thursday's sales are ___ % ___ the trend value"; the key accepts "10.21% below" or "89.79% of".
- 2022F-Q5(b): calculate the seasonal index for Friday (50), and explain its relationship to the daily average (2 marks).
- 2024A-Q8(a) (2 marks): the table gives the indices for Monday to Friday; two blanks for Saturday (130.9%) and Sunday (121.4%) must be filled, 1 mark each.
- 2025A-Q7(b): complete the daily indices for two days of the week (2 marks).

**Common errors**
- Treating a percentage as a decimal directly in multiplication or division (110.76% must be written as 1.1076).
- Indices not normalised, or the normalised sum not matching the length of the cycle.
- The mean used in the calculation is for the wrong period (the position of the seasonal mean).
- The 2017, 2022 and 2023 reports note that basic arithmetic is a common weak point; take care with division and conversion between percentages.

**Past questions**: 2016A-Q10(a), 2016A-Q10(b)(i), 2017A-Q15(b)(i), 2017A-Q15(b)(ii), 2018A-Q13(d)(i), 2020A-Q14(a), 2020A-Q14(b), 2021A-Q8(b), 2021A-Q8(c), 2022F-Q5(a), 2022F-Q5(b), 2023A-Q8(a), 2023A-Q8(b), 2023A-Q8(c), 2024A-Q8(a), 2024A-Q8(b), 2024A-Q8(d), 2024A-Q8(e), 2025A-Q7(b), 2025A-Q7(c)

---

## Pattern 5: Deseasonalise time series

**Recognition**: The question asks you to deseasonalise, to use seasonal indices to obtain deseasonalised data, to explain the reason for or the definition of deseasonalising, or to work back from deseasonalised data to actual values.

**Approach**
1. Deseasonalising: actual value ÷ seasonal index (the index in decimal form).
   Example: 2018A-Q13(d)(ii) divides the actual value 3521.40 by the December 2016 seasonal index (110.76%, i.e. 1.1076), giving the deseasonalised value.
2. Working back to actual values: deseasonalised value × seasonal index.
   Example: 2024A-Q8(f) (1 mark): the deseasonalised value for Monday in week 1 is already given in the table as 42.4; multiplying by the Monday index of 0.896 gives the actual number of visits, 38 (the key's answer is simply 42.4 × 0.896 = 38, with no need for a least-squares line).
3. Rounding as required: 2016A-Q10(b)(ii) requires rounding to the nearest 10; round only at the final step.
4. Units: in 2025A-Q7(d), sales are in hundreds; when the stem gives $1530, first convert it to 15.30 before calculating.
5. Reason and definition: the reason for deseasonalising is to remove the effect of seasonality (the key for 2022F-Q5(c)(i) requires only this point). The definition is the series with seasonal components removed from the data (2023A-Q8(d)).
6. Deseasonalised data are also used to fit a trend line (see Pattern 6).

**Mark-earning points (typical key wording)**
- Use the correct seasonal index and divide to obtain the deseasonalised value (2017A-Q15(b)(iii), 2018A-Q13(d)(ii), 2020A-Q14(c)).
- 2018A-Q13(d)(ii): use the index in decimal form and divide 3521.40 by it, 2 marks in total.
- 2016A-Q10(b)(ii): calculate the deseasonalised value and round to the nearest 10 (2 marks).
- 2022F-Q5(c)(ii): divide by 50% or 0.5, and obtain the result 6 (author's check: 3 ÷ 50% = 6), 2 marks in total.
- 2024A-Q8(e): first calculate the deseasonalised figure, then estimate the total weekly visits from it (2 marks).
- 2024A-Q8(c) (2 marks): write out 45 ÷ 0.883 to obtain B ≈ 51.0 (the key gives 50.96, rounded to 51.0).
- 2025A-Q7(d): use the correct seasonal index and find A (2 marks).

**Common errors**
- Operations reversed: deseasonalising is division by the index, and restoring actual values is multiplication by it (a similar case is under Pattern 7).
- Using a percentage index instead of converting it to a decimal.
- Forgetting the units in the question (e.g. hundreds of dollars).
- Estimating a weekly total of visits as a single day's value (the key for 2024A-Q8(e) requires an estimate for the week).

**Past questions**: 2016A-Q10(b)(ii), 2017A-Q15(b)(iii), 2018A-Q13(d)(ii), 2018A-Q13(d)(iii), 2020A-Q14(c), 2022F-Q5(c)(i), 2022F-Q5(c)(ii), 2023A-Q8(d), 2023A-Q8(e), 2024A-Q8(c), 2024A-Q8(e), 2024A-Q8(f), 2025A-Q7(d)

---

## Pattern 6: Least-squares linear trend

**Recognition**: The question asks you to use deseasonalised data (or seasonally adjusted data) to find the least-squares line, to write the equation, to explain the slope, or to draw the line on the graph.

**Approach**
1. Regress the deseasonalised data (dependent variable) on the time number (independent variable), obtaining an equation of the form y = bt + a (use CAS or the calculator's regression function).
2. Write the equation using the variable names given in the question (the 2023 report advises using the question's variables).
3. Explaining the slope: the sign of the slope gives the direction of the trend; its absolute value is the average change per period (2022F-Q5(d): the slope is positive, so sales are growing).
4. Drawing the line: mark the vertical intercept on the graph, and draw the line using the slope.
5. Conclusion in context: interpret the slope to describe the long-run outlook (see Pattern 8).

**Mark-earning points (typical key wording)**
- The equation is correct (2020A-Q14(e) and 2023A-Q8(f), 1 mark each).
- Link between slope and context: state that the slope is positive (or negative) and that it represents growth (or decline) (2022F-Q5(d), 1 mark).
- Draw the line on the time series graph: the vertical intercept and slope are correct (2023A-Q8(g), 2 marks).

**Common errors**
- Regressing the original data rather than the deseasonalised data, so the result cannot be used for deseasonalised predictions.
- Writing the equation as y = t + ... with variable names that do not match the question.
- Giving only the slope, without explaining what it means.

**Past questions**: 2017A-Q15(b)(iv), 2018A-Q13(b)(i), 2020A-Q14(e), 2022F-Q5(d), 2023A-Q8(f), 2023A-Q8(g)

---

## Pattern 7: Trend prediction with seasonal adjustment ★

**Recognition**: The question asks you to use the trend equation to predict sales, visits or installations for a future period, or to comment on the reliability of such a prediction.

**Approach (three steps)**
1. Determine the time number: convert the period in the question to its number.
   - Quarterly data: four quarters per year, numbered consecutively. Example (author's check, data from 2017A-Q15(b)): March 2013 is n = 1, and December 2017 is n = 20.
   - Data in 2023A-Q8: summer 2019 is t = 1, and spring 2024 is t = 24 (author's check).
   - Weekly data: the 2016 data have 5 days per week (Monday to Friday), so Friday of week 4 is d = 20; 2022F-Q5 has 3 days per week, so Friday of week 4 is t = 10; 2021A-Q8 has 5 days per week, so Saturday of week 5 is n = 25 (author's check).
   - The 2025A-Q7 data have 6 days per week (Tuesday to Sunday), so Thursday of week 4 is t = 21 (author's check).
   - The 2024A-Q8 data have 7 days per week, so Tuesday of week 5 is t = 30 (consistent with the key).
2. Substitute into the trend equation to obtain the deseasonalised predicted value.
3. Multiply by the seasonal index or day-of-week index for the period to obtain the actual predicted value. When predictions are expressed as actual sales or visits, the index must be multiplied in.
4. Commenting on reliability: if the forecast period in the question lies outside the range of the data's numbering, it is extrapolation, and the conclusion should be that the prediction is unreliable (the keys for 2021A-Q8(e)(ii), 2023A-Q8(i) and 2025A-Q7(f) all reach this conclusion). 2017A-Q15(b)(vi) is an exception, see the mark-earning points below.

**Mark-earning points (typical key wording)**
- Write the values of d, n and t (for example, 2016A-Q10(c)(ii) first defines d, 2021A-Q8(e)(i) uses n = 25, 2022F-Q5(e) substitutes t = 10, 2023A-Q8(h) uses t = 24).
- The deseasonalised predicted value is correct, then multiplied by the seasonal index and rounded as required (2020A-Q14(f), 2025A-Q7(e)).
- 2016A-Q10(c)(ii): 3 marks in total, one for each of the three steps.
- Commenting on predictions: state the conclusion (unreliable or not valid) and give the reason of extrapolation (2021A-Q8(e)(ii), 2023A-Q8(i), 2025A-Q7(f)).
- 2024A-Q8(g): give the value of t, the trend value and the predicted value separately (3 marks).
- 2017A-Q15(b)(vi) (2 marks): comment on the reliability of the prediction for December 2017 (n = 20). The key judges it reliable, on the reason that it lies "within one cycle of known data": the last data point is December 2016 (n = 16), so the prediction goes only one year beyond the data. This differs from the general rule that any value beyond the data range is extrapolation. The prediction in 2023A-Q8(h)–(i) (t = 24) lies two years beyond the last data point (t = 16), and the key judges it extrapolation. The boundary between the two questions follows each question's own key; the 2023 and 2025 reports still advise that regression predictions beyond the data range are unreliable.

**Common errors**
- Wrong time numbering (the most common lost mark). Take particular care with the number of days in the cycle: weekly data of 5, 6 or 7 days are numbered differently.
- Multiplying and dividing by the seasonal index in the wrong direction.
- Using a percentage index instead of its decimal form.
- Treating an extrapolated result as a reliable prediction.
- Not converting the units in the stem (hundreds of dollars).

**Past questions**: 2016A-Q10(c)(ii), 2017A-Q15(b)(v), 2017A-Q15(b)(vi), 2020A-Q14(f), 2021A-Q8(e)(i), 2021A-Q8(e)(ii), 2022F-Q5(e), 2023A-Q8(h), 2023A-Q8(i), 2024A-Q8(g), 2025A-Q7(e), 2025A-Q7(f)

---

## Pattern 8: Time series investigation synthesis

**Recognition**: The question asks you to combine the graph, trend and seasonal pattern of the time series, and to draw a conclusion about the long-term prospects of the business (comment on the long-term prospects).

**Approach**
1. Read the long-run direction from the slope of the least-squares line: a negative slope means the quantity is falling; a positive slope means growth.
2. The conclusion must be tied to the context, and say what it means for the business (e.g. the number of installations is falling, so the long-term prospects are not encouraging).
3. The conclusion must cite the slope or the equation (not just describe the graph).

**Mark-earning points (typical key wording)**
- State that the number of installations is falling (2020A-Q14(g), 1 mark).
- Cite the slope of the least-squares line (2020A-Q14(g), 1 mark).

**Common errors**
- Saying only that the data fluctuate a lot, without giving the long-run direction.
- The conclusion does not cite the slope.

**Past questions**: 2020A-Q14(g)

---

## Review outcome (2026-10-11)

The following items that were previously marked for checking have been verified against the original papers and keys. The text has been revised, and they are no longer marked for checking:
- Pattern 2: the key for 2020A-Q14(d) is winter (seasonal index 74.6, the lowest); there is no outlier question in the TSI set.
- Pattern 3: the key for 2018A-Q12(c) is the 5-point moving average; the key for 2021A-Q8(a) is the 5-point moving average; the key for 2025A-Q7(a) is the 6-point centred moving average.
- Pattern 4: the seasonal index sum in the key table for 2023A-Q8(b) is 400%; the key's main answer for 2016A-Q10(b)(i) is 0.625, and 0.590 is the other method listed in the key.
- Pattern 5: the key for 2024A-Q8(c) is 45 ÷ 0.883 ≈ 51.0.
- Pattern 7: the key for 2024A-Q8(g) also uses t = 30; the key for 2017A-Q15(b)(vi) judges the prediction reliable (within one cycle); this is written into the mark-earning points.
- Pattern 8: this pattern has only one sub-question (2020A-Q14(g)), so its conclusions are thin.
- The labelling was revised on 2026-10-12 to match the final tags; see the Chinese review log `MAA/methods/审校记录.md`.
