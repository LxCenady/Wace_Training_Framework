# TSI · Time series analysis 时间序列分析 (Unit 4.1)

Bank: `<ROOT>\MAA\topics\04_Time_Series.md` / `.pdf`. 10 questions with TSI parts in 2016–2025 (no 2019 key), about 124 tagged marks (9% of the total). 9 of these are Calculator-assumed and only one (2022 CF Q5) is Calculator-free. Treat this as a calculator-assumed topic.

## Scope
- Plotting a time series; reading the trend, seasonality and irregular variation.
- Simple moving averages: odd windows (3, 5) and even windows (4, 6) that need centring.
- Seasonal indices by the average percentage method, normalised to average 100%.
- Deseasonalising (divide by the index) and restoring actual values (multiply).
- Least-squares linear trend fitted to the deseasonalised data.
- Trend prediction with a seasonal adjustment, and whether the prediction is reliable.
- Investigation: what the trend and seasonality mean for the business.

## How SCSA asks it
- A quarterly series (sales or installations) with moving averages, seasonal indices and a trend forecast: 2017 CA Q15, 2020 CA Q14, 2023 CA Q8.
- Weekly data with a 5-, 6- or 7-day cycle (sales, canteen takings, visits), with the same steps: 2016 CA Q10, 2021 CA Q8, 2024 CA Q8, 2025 CA Q7. In 2018 CA Q12 the key chooses a 5-point moving average for its series, which shows why the cycle length must be read from the data.
- A three-day cycle in the Calculator-free part of the paper: 2022 CF Q5 (moving averages, indices, deseasonalising, trend).

## Patterns

| code | pattern | questions / marks (2016–25) | median part marks (range) | CF / CA parts | key past refs |
|---|---|---|---|---|---|
| TSI1 | 时间序列图绘制与读图 Plot and read time series | 3 / 8 | 2 (2) | 0 / 4 | 2017 CA Q15(b)(iv); 2018 CA Q13(a)–(b)(i); 2021 CA Q8(d) |
| TSI2 | 趋势、季节性、随机波动与异常值 Trend, seasonality, irregular variation and outliers | 4 / 7 | 2 (1–2) | 0 / 4 | 2016 CA Q10(c)(i); 2018 CA Q13(b)(ii); 2020 CA Q14(d) |
| TSI3 | 简单移动平均平滑 Simple moving average smoothing | 7 / 21 | 2 (1–4) | 1 / 9 | 2017 CA Q15(a)(i)–(ii); 2018 CA Q12(a)–(c); 2025 CA Q7(a) |
| TSI4 | 平均百分比法求季节指数 Seasonal indices by average percentage method | 9 / 41 | 2 (1–4) | 2 / 18 | 2016 CA Q10(a)–(b)(i); 2020 CA Q14(a)–(b); 2023 CA Q8(b)–(c); 2025 CA Q7(c) |
| TSI5 | 去季节化数据 Deseasonalise time series | 8 / 20 | 2 (1–2) | 2 / 11 | 2018 CA Q13(d)(ii); 2022 CF Q5(c)(i)–(ii); 2024 CA Q8(c) |
| TSI6 | 时间序列线性趋势回归 Least-squares linear trend | 3 / 5 | 1 (1–2) | 1 / 3 | 2020 CA Q14(e); 2022 CF Q5(d); 2023 CA Q8(f) |
| TSI7 | 趋势预测与季节调整 Trend prediction with seasonal adjustment | 9 / 31 | 2 (2–3) | 1 / 12 | 2016 CA Q10(c)(ii); 2021 CA Q8(e)(i)–(ii); 2023 CA Q8(h)–(i); 2025 CA Q7(e)–(f) |
| TSI8 | 时间序列调查结论整合 Time series investigation synthesis | 1 / 2 | 2 (2) | 0 / 1 | 2020 CA Q14(g) |

## Method in brief

- **TSI1.** Time on the horizontal axis (number, quarter or day), value on the vertical. Plot in time order, join the points, and do not skip periods. For a least-squares line, use the equation in the stem: find the point at the first time number and another point further along, join them, and make the line span the data.
- **TSI2.** Trend: the long-run direction (the sign of the slope of the fitted line). Seasonality: the regular peaks and troughs, named by season or day. Irregular variation: what remains after the trend and seasonal parts. Explain in context, with the season or day named.
- **TSI3.** Odd windows: average the window and put it in the middle period. Even windows (4 or 6) cannot be centred directly: for a window of n periods, take n + 1 values centred on the period, halve the two end values, sum, and divide by n. Choose the window to match the cycle: quarterly data use 4, a 5-day week uses 5, a 6-day week uses 6. Missing moving averages can be worked back from the known ones.
- **TSI4.** For each period, seasonal mean = centred moving average (quarters) or the average of the cycle (days). Percentage = actual ÷ seasonal mean × 100. Average the percentages within each season or day, then normalise so the indices average 100% (quarterly indices sum to 400%). A missing index can be found from the normalising total. Use decimals (110.76% becomes 1.1076) in later calculations.
- **TSI5.** Deseasonalised value = actual ÷ seasonal index (decimal). To restore, multiply. Round only at the end, to the precision asked. Check the units in the stem (figures in hundreds). The reason for deseasonalising is to remove the seasonal effect, so the trend is clearer.
- **TSI6.** Fit the least-squares line of deseasonalised values on the time number. Write the equation with the variable names used in the stem. The slope is the average change per period: its sign gives the trend direction and its size gives the rate of change. Draw the line by marking the intercept and using the slope.
- **TSI7.** Three steps, each worth a mark: (1) find the time number t (or n, d) for the period being predicted, counting cycles carefully; (2) substitute into the deseasonalised trend line; (3) multiply by the seasonal index for that period and round. Reliability: a period beyond the last observed one is extrapolation, so say the prediction is unreliable and give that reason.
- **TSI8.** Use the long-run direction (the slope) and the seasonal pattern to make one or two statements for the business, each citing the slope or the equation.

## Writing tips
- Numbering is where most lost marks happen. Count the days in the cycle (5, 6 or 7) before numbering weekly data, and check the first and last periods against the table.
- Use the index as a decimal in calculations. Never multiply or divide by a percentage directly.
- Say which season or day an index refers to, and whether the index is above or below average (above 100% or 1.00 is above the average level).
- In-context explanations name the period, the variable, the unit, and say "on average" or "trend value" where appropriate.
- Default rule for reliability: a forecast beyond the last data point is extrapolation and is unreliable. The one real key that called a forecast one cycle beyond the data reliable (2017 CA Q15(b)(vi)) is an exception; do not copy it unless the question is built around that reasoning.
- Calculator-assumed: the calculator's regression and table functions are expected for every numerical step. Show the setup (the sums, the division, the equation) so that follow-through marks can be awarded.
