# MAA · Sequences: Growth and Decay — Patterns and Solution Approaches

> Source: marking keys and exam reports for 23 past exam questions from 2016–2025 (excluding 2019) carrying the SEQ tag, 101 sub-questions in total (one sub-question may belong to several patterns). Based on the Specific behaviours descriptions in each sub-question's marking key, and on the exam reports for each year. 2019 has no marking key and is not included. Tags are drafts; some have been checked by hand. Pattern numbers agree with `evidence/maa/notes/SEQ.txt`. ★ = patterns ranked in roughly the top quarter by marks per sub-question in this topic (for this topic, Patterns 2 and 5).
> Review status: every item has been checked line by line by an independent reviewer; the record is in the Chinese review log `MAA/methods/审校记录.md`. The labelling was revised on 2026-10-12, and no open review items remain.

## Marking-key reminders

- **Keep recursive rules and general (nth-term) rules distinct** (2016 report: knowing the difference between a recursive rule and a general rule; 2024 report: confusing a recursive rule with the nth-term rule is a weak area). A recursive rule must always be written together with its initial value.
- **Basic arithmetic has been a recurring source of lost marks** (2020, 2021, 2022 and 2023 reports: converting fractions to percentages, simplifying, decimal calculation).
- **Round discrete quantities correctly** (2020 report: discrete quantities such as numbers of people, fish or weeks must be rounded to a suitable whole number; 2016 report: money is given to two decimal places).
- **The steady state is a weak area** (2024 report: candidates performed poorly on questions that apply the steady-state solution; 2025 report: candidates could not recognise when a steady-state solution is needed).
- **Explanation questions must be tied to the context** (2022 report stresses what "in the context of the question" means; 2023 report: questions requiring explanation or justification were generally difficult).
- **Two-mark questions also need intermediate steps shown** (2016, 2017, 2021 and 2025 reports).
- **Read the scale carefully when drawing graphs** (2017 and 2022 reports: reading scales and plotting points).

---

## Pattern 1: Generate an arithmetic sequence recursively

**Recognition**: The question describes "a fixed amount added (or subtracted) each period", and asks for the recursive rule, or for the first few terms calculated from the recursive rule.

**Standard procedure**
1. Confirm it is arithmetic: the difference between consecutive terms is the same constant d.
2. Recursive rule: T_{n+1} = T_n + d (d is negative when the quantity decreases), and state the initial value (T_0 or T_1, following the subscript used in the question).
3. Calculate term by term: start from the initial value and apply the recursive rule forward.

**Mark-earning points**: the value and sign of d each earn marks; the initial value and subscript match (the key for 2024F-Q1(a)(i) awards the "common difference" and T_0 separately); the recursive rule is written in full (2021F-Q6(a), 2023F-Q3(a)); term-by-term calculations are correct (2016F-Q4(b)(i): the key awards the 2nd term and the 3rd term separately).

**Common errors**: whether the subscript starts at 0 or 1 does not match the question; the sign of d reversed; only the recursive rule written, with the initial value omitted.

**Past questions**: 2016F-Q4(b)(i), 2017F-Q1(a), 2021F-Q6(a), 2022F-Q2(a)(i), 2023F-Q3(a), 2024F-Q1(a)(i), 2025A-Q6(a), 2025F-Q1(a)

---

## Pattern 2: Arithmetic nth term and prediction ★

**Recognition**: You are asked to derive the rule for the nth term, to decide which term a value is, or to find when a value is first reached, or how many weeks or years it takes.

**Standard procedure**
1. Write the nth term from the common difference d and the first term (or the intercept): the usual form is T_n = dn + c, or T_n = a + (n − 1)d (matched to the subscript in the question). The typical key wording states that the gradient is d and the vertical intercept is c (2017F-Q1(b)(i)).
2. Set T_n equal to the threshold given in the question, and solve for n.
3. Rounding: when the question asks for "the first term less than …", take the smallest integer n that satisfies the condition. The key for 2017F-Q1(b)(ii) gives the 171st term; the working first solves the inequality, then takes the whole number. When asked "when", take the whole-number period in the same way.
4. Consistent units: convert a daily change to a weekly change (× 7) (2017A-Q10(f)).
5. Piecewise situations: if the increment changes partway (e.g. a company gives a pay rise from a certain month), calculate in two parts, and the second part restarts the recursion from the term at which the change occurs (2023F-Q3(c), (d)).

**Mark-earning points**: the two coefficients of the nth term each earn marks (2020A-Q7(b): the constant term and the coefficient of n); finding the number of terms and the value of the term (2017F-Q1(b)(ii) in three steps: inequality, number of terms, value of the term); the conclusion is written as a full sentence, stating how many years have passed (2022F-Q2(c)).

**Common errors**: rounding the number of terms to the nearest integer instead of up to the next integer; confusing "the nth term" with "the nth week" or with the starting point (for example, the 12th month and the 11th term); using the original common difference after the change.

**Past questions**: 2016F-Q4(c), 2017A-Q10(f), 2017F-Q1(b)(i), 2017F-Q1(b)(ii), 2020A-Q7(a), 2020A-Q7(b), 2020A-Q7(c), 2021F-Q1(a), 2021F-Q1(b), 2021F-Q1(c), 2021F-Q6(d), 2022F-Q2(a)(ii), 2022F-Q2(b), 2022F-Q2(c), 2023F-Q3(b), 2023F-Q3(c), 2023F-Q3(d), 2024F-Q1(a)(ii), 2024F-Q1(b), 2024F-Q1(c), 2024F-Q1(d), 2025F-Q1(c), 2025F-Q1(d)

---

## Pattern 3: Tabular and graphical arithmetic models

**Recognition**: You are asked to enter the first few terms in a table, or to plot the first few terms as discrete points (display the first terms / complete the table). There are only 2 sub-questions in the evidence, so this section is brief.

**Standard procedure**: calculate the first few terms from the recursive or nth-term rule and fill in the table. When graphing, plot points only, without joining them (the sequence is discrete), and label the axes and scales.

**Mark-earning points**: at least two points correct, or all points correct (2017F-Q1(a)); the table entirely correct (2025F-Q1(b)); axes labelled clearly.

**Common errors**: joining the discrete points into a line or curve; scale misread (2017 and 2022 reports).

**Past questions**: 2017F-Q1(a), 2025F-Q1(b)

---

## Pattern 4: Generate a geometric sequence recursively

**Recognition**: The question describes "a fixed proportion multiplied each period", or "a decrease (increase) of x% each period", and asks for the recursive rule or for term-by-term calculation.

**Standard procedure**
1. Common ratio r: for a decrease of x%, r = 1 − x%; for an increase of x%, r = 1 + x% (e.g. a decrease of 14% corresponds to 0.86).
2. Recursive rule: T_{n+1} = r·T_n, and state the initial value (following the subscript in the question).
3. Find r from the data: the ratio of consecutive terms (the key for 2021A-Q11(b)(i) requires the ratio to be calculated first).
4. Rounding: when the question requires rounding (e.g. to the nearest dollar, 2016A-Q7(a)), round as required; do not round too early in intermediate steps.

**Mark-earning points**: the recursive rule and the initial value each earn marks (2016F-Q4(a)(i), 2018F-Q7(a): the common ratio, the decreasing geometric recursion and the initial value are each awarded marks); finding the ratio from data (2021A-Q11(b)(i)); the starting point specified in the question is stated clearly (the key for 2023A-Q13(c) awards T_0 a separate mark).

**Common errors**: using the reduction rate directly as the ratio (writing 0.14 instead of 0.86); taking the initial value at the wrong time; forgetting the rounding the question requires.

**Past questions**: 2016A-Q7(a), 2016F-Q4(a)(i), 2016F-Q4(b)(ii), 2018F-Q7(a), 2020A-Q8(a), 2021A-Q11(b)(i), 2022A-Q9(b), 2023A-Q13(a)(ii), 2023A-Q13(c), 2024A-Q7(b)

Note: 2016F-Q4(b)(ii) gives T_{n+1} = 1.5T_n and the value of T_2, and asks for the first three terms, so the earlier terms must be worked back from a known term (T_n = T_{n+1} ÷ ratio).

---

## Pattern 5: Geometric nth term and growth or decay prediction ★

**Recognition**: A fixed proportional growth or decay is given, and the question asks for the general term, the value at a particular time, when a threshold is reached, or to explain a growth rate. There are 37 sub-questions in the evidence, making this the most common pattern in this topic.

**Approach and steps**
1. General term: T_n = a·r^n (or a·r^(n−1), following the subscript in the question). The coefficient a is the initial value, and the base r is the common ratio (the key awards these separately, e.g. 2016A-Q7(c), 2024A-Q7(c)).
2. From the common ratio, find the annual or period rate of change: r = 0.85 means a decrease of 15% per period, and the average rate of change is 1 − r (2016A-Q7(b); in 2018A-Q14(b), the ratio is first found from the ratio of the end values, then converted to a percentage).
3. Find the value at a given period: substitute into the general term, and round as the question requires (2016A-Q7(d): to the nearest dollar).
4. Find n (the first time a value is reached): solve the exponential equation (calculator solve function or logarithms), then take the smallest whole-number period that satisfies the condition, and write the conclusion (2016A-Q7(e): the key requires stating that the sale takes place at the end of year 5; 2017A-Q10(c): at week 6; 2023A-Q13(e): the first time the value falls below 5000).
5. Piecewise growth rates: use a different r for the earlier and later segments, calculate segment by segment, and the second segment starts from the value at the end of the first (2017A-Q10(d); the key for 2023A-Q13(a)(i) writes out the successive yearly multiplying factors).
6. Average growth rate: first calculate the value after a period using the average rate, then set up an equation for the later r (2021A-Q12(c): the key gives three marks in turn: calculate the value at the end of year 6 using the average rate, set up the equation, and solve for r).
7. Exact form: when the question asks for exact or fractional answers, keep the fraction form (2016F-Q4(a)(ii) asks for a fraction; 2018F-Q7(c) asks for the exact value and the simplification working).
8. Discrete quantities: rounding numbers of people, fish, etc. to whole numbers (2022A-Q17(b): the key requires an integer value).
9. Finding the coefficients: when several data are given, find r from the ratio of two terms, then write T_n (2021F-Q6(b)).

**Mark-earning points**: the coefficient and the base of the general term each earn 1 mark (2016A-Q7(c)); after finding the value, round as the question requires (2016A-Q7(d)); the conclusion sentence states when (2016A-Q7(e)); for piecewise cases, each segment is written out (2017A-Q10(d) in three steps: the value after 8 weeks, the equation for the new growth rate, the total number of weeks); where the question asks for a proof, every simplification step is written out (2018F-Q7(c)).

**Common errors**: r and 1 − r confused (using 0.15 in place of 0.85, or the reverse); the starting point of the exponent (whether n starts at 0 or 1) does not match the question; rounding n to the nearest integer instead of up to the next integer; the second segment uses the wrong starting value; forgetting the final rounding or not giving the answer to the precision the question requires.

**Note**: 2022A-Q9(a) asks for an explanation of why "1200 × (0.86)^n" is the population after n weeks. The arguments accepted by the key include: a 14% decrease leaves 86% of the original, and 1200 is the initial population. There is also an alternative argument: if 0.86 corresponds to a yearly change, the expression is not one in weeks. (Checked: the question states "a decrease of 14% per year", but the key's main solution treats it as a weekly decrease (r = 0.86, initial value 1200); the alternative solution points out that under a yearly change the expression gives the population after n years, not n weeks.)

**Past questions**: 2016A-Q7(b), 2016A-Q7(c), 2016A-Q7(d), 2016A-Q7(e), 2016F-Q4(a)(ii), 2017A-Q10(a), 2017A-Q10(b), 2017A-Q10(c), 2017A-Q10(d), 2017A-Q10(e), 2018A-Q14(b), 2018F-Q7(b), 2018F-Q7(c), 2020A-Q8(b), 2020A-Q8(c), 2021A-Q11(a)(i), 2021A-Q11(a)(ii), 2021A-Q11(b)(ii), 2021A-Q12(a), 2021A-Q12(b), 2021A-Q12(c), 2021F-Q6(b), 2022A-Q9(a), 2022A-Q9(c), 2022A-Q17(a), 2022A-Q17(b), 2022A-Q17(c), 2023A-Q13(a)(i), 2023A-Q13(b), 2023A-Q13(d), 2023A-Q13(e), 2024A-Q7(a), 2024A-Q7(c), 2024A-Q7(d), 2024A-Q7(f)(i), 2025A-Q6(c), 2025A-Q6(d)

---

## Pattern 6: Generate and display first-order linear recurrences

**Recognition**: The recursive rule has the form T_{n+1} = aT_n + b (both a multiplier and a fixed addition or subtraction), and the question asks for term-by-term calculation, a table, or a graph of the values (display / graph the values).

**Standard procedure**
1. Identify a, b and the initial value T_0.
2. Substitute forward term by term from the initial value. Note whether the question asks "at the start of which week", and check that the corresponding term's subscript matches.
3. When graphing, plot points at the interval the question specifies (e.g. one point every 5 years, starting at n = 5), then look at the trend.
4. To find a and b from three consecutive terms: substitute into T_{n+1} = aT_n + b to obtain two equations, then solve them simultaneously (method as in Pattern 8).

**Mark-earning points**: term-by-term values correct (2025F-Q1(e)(i); 2018A-Q9(b), see the note below); points correct on the graph and covering all the points the question specifies (2017A-Q16(b): at least two points, all points); the value of the parameter c or k (2018A-Q9(d)(i)).

**Common errors**: subscripts shifted (for example, matching "the start of week 5" to the wrong term); horizontal spacing on a graph not the interval the question requires.

**Past questions**: 2017A-Q16(b), 2018A-Q9(b), 2018A-Q9(d)(i), 2018A-Q9(d)(ii), 2025F-Q1(e)(i)

**Note (2018A-Q9(b))**: the recursive rule in the question is M_{n+1} = 0.9(M_n − 12) + 15 with M_1 = 50. Calculating term by term, the fifth week gives 47.249, which rounds to about 47. The key's own calculation table also lists 47.249, but its written answer gives 48, which does not match the table. This note takes 47 as correct; the key's 48 is recorded in the review log.

---

## Pattern 7: Long-term behaviour and steady state

**Recognition**: The question asks about long-term behaviour, the steady state, whether something will run out in the long run, or whether a level is sustainable.

**Standard procedure**
1. A steady state S satisfies S = aS + b, so S = b ÷ (1 − a). Before using this, confirm that |a| < 1; otherwise the sequence does not converge.
2. To keep the level steady: the amount removed or added each period equals the growth at the steady-state value (2020A-Q8(d) and 2018A-Q9(e) are both questions of this type).
3. Judging "will it run out" or "can it reach a certain level": compare the steady-state value with the threshold given in the question (2024A-Q7(f)(ii), 2025F-Q1(e)(ii)).
4. The conclusion must state the numerical steady-state value, and be checked against the conditions in the question. Do not write only "yes" or "no".

**Mark-earning points**: the steady-state equation is written out (2017A-Q16(d): the key requires the steady-state equation to be written); the steady-state value is found and rounded to the nearest integer (2017A-Q16(d)); when judging the amount that must be removed to keep the level steady, round down (2020A-Q8(d): the key requires fish numbers to be rounded, and the rounding must be downward); 2022A-Q9(d) states the stable number of penguins (2400); 2024A-Q7(f)(ii) compares the steady-state value with the target of 8.5 million.

**Common errors**: steady-state equation written incorrectly (treating T_n and T_{n+1} as different unknowns, or forgetting to bring b in); convergence not checked; rounding in the wrong direction.

**Past questions**: 2017A-Q16(c), 2017A-Q16(d), 2018A-Q9(c), 2018A-Q9(e), 2020A-Q8(d), 2021F-Q6(c), 2022A-Q9(d), 2024A-Q7(f)(ii), 2025F-Q1(e)(ii)

**2018A-Q9(c) (checked)**: (c) follows the model given at the start of the question, M_{n+1} = 0.9(M_n − 12) + 15. The steady state is M = 0.9(M − 12) + 15, which gives M = 42, so the key's 42 is correct. The steady state for N_{n+1} = 0.8(N_n − 12) + 15 is 27, which appears in (d)(ii); the key's 27 is also correct. The two models must not be mixed: for (c), the model for M (factor 0.9) is used, not the model for N (factor 0.8).

---

## Pattern 8: Model a practical situation with a recurrence

**Recognition**: A situation gives a rule for the change in each period, and the question asks you to write a recursive model ("write a recursive rule for …"), interpret a coefficient ("interpret the coefficient"), or compare two options ("explain which program …").

**Standard procedure**
1. Split the change in each period into two parts: a proportional change (a multiplier: the proportion retained = 1 − loss rate, or 1 + growth rate) and a fixed increase or decrease (adding or subtracting a constant).
2. Write T_{n+1} = aT_n + b, and state the initial value T_0 (the time given in the question).
3. Interpret the coefficients: a is the proportion kept each period, and b is the fixed number added each period; write them in terms of the context of the question (2017A-Q16(a)(i), 2024A-Q7(f)(i)).
4. Analysis: list the iterated values or graph them to see the trend; when comparing options, give reasons (examples of comparing options are under Pattern 7).
5. Find a and b from given data: take three consecutive terms and write two equations (2025A-Q6(f)).

**Mark-earning points**: a and b each earn 1 mark (2024A-Q7(e)); when interpreting a coefficient, state both "each period" and the quantity that changes (2024A-Q7(f)(i)); 2017A-Q16(a)(ii) separately asks for the value of b.

**Common errors**: confusing the proportion kept (a) with the rate of decay (1 − a); the units of b do not match the units of T; when comparing options, only a conclusion is given, with no reasons.

**Checked, 2024A-Q7(e)**: the key gives a = 0.986 and b = 100. a comes from the decay rate changing from 3% to 1.4% (1 − 1.4% = 0.986). The unit of T is thousands of people, and the statement "100 000 new people each week" corresponds to b = 100 (thousands), so the units agree with T.

**Past questions**: 2017A-Q16(a)(i), 2017A-Q16(a)(ii), 2017A-Q16(b), 2017A-Q16(c), 2017A-Q16(d), 2018A-Q9(a), 2018A-Q9(e), 2020A-Q8(d), 2023A-Q13(c), 2024A-Q7(e), 2024A-Q7(f)(i), 2025A-Q6(f)

---

## Pattern 9: Sequence partial sums and cumulative totals

**Recognition**: Questions such as total distance travelled, maximum height, or who reaches a point first need the first few terms to be added together. There are only 3 sub-questions in the evidence (from 2 questions).

**Standard procedure**
1. Cumulative total = sum of the first n terms. Arithmetic: S_n = n(T_1 + T_n) ÷ 2; geometric: S_n = T_1(1 − r^n) ÷ (1 − r). The calculator's sum or table functions can also be used to check.
2. If there is an initial height or initial quantity, sum first and then add the initial quantity (2020A-Q7(d): the key requires the sum of several terms first, then adding the initial 60).
3. When comparing the cumulative totals of two people or two options, find the date each reaches the target separately, then compare (2025A-Q6(e): the key gives the arrival day for each person separately, then gives the conclusion with reasons).

**Mark-earning points**: the sum expression is correct (2020A-Q7(d) in two steps: the sum, then adding the initial quantity); each person's arrival day earns marks (2025A-Q6(e)); the conclusion is supported by reasons.

**Common errors**: an off-by-one error in the number of terms (only adding up to term n − 1); forgetting the initial quantity; giving only a conclusion when comparing, without the dates for each person.

**Past questions**: 2020A-Q7(d), 2025A-Q6(b), 2025A-Q6(e)

---

## Notes

- The evidence covers only sub-questions carrying the SEQ tag. The pattern structure and the assignment of sub-questions in this note follow `SEQ.txt` completely; no extra tags have been added.
- Exam papers from 2019 are not included (there is no marking key for that year).
