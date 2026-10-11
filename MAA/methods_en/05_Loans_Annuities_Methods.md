# MAA · Loans, Investments and Annuities — Patterns and Solution Approaches

> Source: past exam questions from 2016–2025 (excluding 2019, which has no marking key) with sub-questions tagged FIN. These cover 25 questions and 10 patterns. Only 2017F-Q4 is from the F paper (Calculator-free); all others are from the A paper (Calculator-assumed). Pattern definitions are taken from `tools/catalogue_MAA.json`. Tags are drafts (draft_for_review); some have been checked.
> Figures and mark-earning points are taken from the Specific behaviours in the marking keys and are paraphrased; formulas and steps are general solution methods. The original questions and marking files are kept in the local ignored directory, and this document does not copy question stems.
> Review status: checked on 2026-10-11 by an independent reviewer against the original papers and keys (results in the Chinese review log `MAA/methods/` for files 04–06). The only item still to be checked is the payment timing for 2017A-Q8: the stem says payment at the start of the year, but the key's solution treats payment at the end of the period. Relevant references in this document are marked accordingly (to be checked).

## Marking-key reminders

- **Financial functions on the calculator must be mastered** (2016 report): some candidates did not know how to use the calculator's financial functions; the 2017 report advises writing out N, I, PV and the other values one by one, so that markers can check them.
- **Round according to the question and context** (2016, 2018 reports): money answers are given to two decimal places, and financial answers are rounded to the cent (2018 report); discrete quantities such as numbers of periods or people must be rounded to a suitable whole number (2019, 2020 reports).
- **Working must be shown for calculation questions** (2017, 2018 reports): a 2-mark question with only an answer and no working loses marks if the answer is wrong; where a question asks for proof or explanation, every step must be written out.
- **Annuities and perpetuities are the weakest area**: 2023 report, the annuity and perpetuity question (Q14) had a mean of 41.05%, the hardest of that year; 2024 report, the loan interest question Q6(d) had a mean of 27.12%, and the annuity and perpetuity questions Q13(d)(i) and (e) had means of 33.84% and 34.74%; 2025 report, the annuity and perpetuity question Q12 was listed as challenging, and reaching a savings target with quarterly deposits was also a weak point.
- **Explanations must refer to the situation**: (2024, 2025 reports) where a question asks for an answer in context, write the specific quantity, unit and point in time. The 2024 report also notes that applying the steady-state solution is a weak point (Section Two). The report does not name a question number; the key involving a steady-state value is 2024A-Q7(f)(ii), which belongs to the sequences topic (SEQ7, see the 02 Sequences note), not to the patterns in this file.
- **Hard questions in the data**: 2016 report, the annuity question Q16 had a mean of 42.26% and was the hardest that year; 2017 report, the loan question Q14 had a mean of 28.3% and was the hardest that year; the 2020 and 2021 reports both list annuity or loan questions among the discriminating questions.
- **Be fluent with both calculator methods**: the 2019 report says candidates were more proficient using the CAS calculator for financial questions; the 2016 report says some candidates did not know the financial functions. Practise both methods, and check one against the other.

---

## Pattern 1: Compound interest recurrence model

**Recognition**: The stem gives an account or loan with interest compounded at an annual rate, and asks for a recursive rule or the balance period by period. The common wording is a deposit or repayment at the end of each period, with the request to write the recursive rule.

**Steps**
1. Find the rate per period: rate per period = annual rate ÷ number of compounding periods per year (e.g. for quarterly compounding, rate per period = annual rate ÷ 4).
2. Write the recursive rule: if interest only is added, A_{n+1} = (1 + r)A_n; if there is a deposit or repayment d each period, A_{n+1} = (1 + r)A_n ± d.
3. State the initial value A_0 (principal or current balance); write the recursive rule and the initial value separately.
4. When specific numbers are needed, substitute period by period, or use the compound interest formula in Pattern 3 to find the answer directly.

**Mark-earning points (typical key wording)**: the two parts of the recursive rule each earn a mark, namely the multiplier (1 + r or an equivalent form) and the initial value (2018A-Q8(a)(ii), 2020A-Q12(a)(ii)); the rate per period must be correct for the compounding frequency in the question (2025A-Q8(b) requires the quarterly rate).

**Common errors**: using the annual rate directly as the rate per period; leaving out the ± d term when there are regular deposits; in 2020A-Q12(b), the repayment is made at the end of each year, so the time points must be aligned when writing the recursive rule.

**Past questions**: 2018A-Q8(a)(ii), 2018A-Q16(d), 2018A-Q16(e), 2020A-Q12(a)(i), 2020A-Q12(a)(ii), 2020A-Q12(b), 2024A-Q10(a)(i), 2024A-Q10(a)(ii), 2025A-Q8(b)

---

## Pattern 2: Effective annual rate and compounding comparison

**Recognition**: The question involves the effective annual rate (EAR), or gives schemes with different compounding frequencies (monthly, quarterly, half-yearly, daily), and asks for a comparison or judgement.

**Steps**
1. For each scheme, calculate the EAR = (1 + j/m)^m − 1, where j is the nominal annual rate and m is the number of compoundings per year; for daily compounding, m = 365.
2. When comparing for the same principal, choose the higher EAR for an investment and the lower EAR for a loan.
3. If the question asks for a nominal rate to be worked back from a target EAR, substitute the target EAR into the same formula and solve.
4. The conclusion must state clearly which scheme to choose, and give the two EAR values as the basis.

**Mark-earning points (typical key wording)**: correct substitution of the nominal rate and number of compoundings (2016A-Q13(b); for daily compounding use 365); both EARs calculated (2022A-Q8(a), 2024A-Q10(d)); the conclusion matches the data (in 2024A-Q10(d) the conclusion must correspond to the higher EAR); in 2020A-Q9(e)-type questions, calculate the effective rate and then judge whether the statement in the stem holds.

**Common errors**: comparing nominal rates without conversion; writing m as 360 or 12 for daily compounding; forgetting to divide by 100 when converting a percentage to a decimal. 2018A-Q8(b) asks how the nominal rate needed to reach the same final value changes when the compounding frequency changes; a conclusion without calculation loses marks. The reasons for the borrowing choice in 2017F-Q4(a) (choice of compounding period) must be based on this: at the same nominal rate, more frequent compounding gives a higher effective rate, and a higher cost of borrowing.

**Past questions**: 2016A-Q12(a), 2016A-Q13(b), 2016A-Q16(b)(i), 2016A-Q16(b)(ii), 2016A-Q16(b)(iii), 2017A-Q8(a) (to be checked), 2017A-Q8(b), 2017F-Q4(a), 2018A-Q8(b), 2018A-Q16(a), 2018A-Q16(b), 2018A-Q16(c), 2020A-Q9(b), 2020A-Q9(e), 2021A-Q10(a), 2022A-Q8(a), 2024A-Q10(d), 2024A-Q13(f)

---

## Pattern 3: Compound interest value and term calculations

**Recognition**: The question asks for the value of an investment after a period, the time needed for it to double, or the time needed to reach a target. The interest rate and compounding period may not match, so conversion is needed.

**Steps**
1. Unify the units: rate per period = annual rate ÷ compoundings per year; number of periods N = years × compoundings per year. Convert the result back to the unit the question asks for (years or months) at the end.
2. Future value formula: FV = PV(1 + r)^N. To find the number of periods: N = ln(FV ÷ PV) ÷ ln(1 + r), or enter PV, FV, I, P/Y and C/Y on the calculator to solve for N.
3. For doubling problems, take FV = 2PV.

**Mark-earning points (typical key wording)**: the rate and the number of periods are marked separately (2016A-Q13(a)(ii) splits the correct rate and the correct time into separate marks); the future value calculation is correct (2016A-Q13(a)(i)).

**Common errors**: using a number of years when interest is compounded monthly; using the annual rate in a monthly-compounding formula; confusing the final value with the interest, when the question asks for the value of the investment and the total amount is what is required, not the interest.

**Past questions**: 2016A-Q13(a)(i), 2016A-Q13(a)(ii), 2017F-Q4(b), 2017F-Q4(c), 2018A-Q8(a)(i), 2018A-Q8(b), 2025A-Q8(a)

---

## Pattern 4: Reducing-balance loan recurrence ★

**Recognition**: A loan principal accrues interest each period, and is repaid by fixed amounts. The question asks for the balance after the nth repayment, for a repayment schedule to be completed (opening balance, interest, repayment, closing balance), or for a recursive rule to be written.

**Steps**
1. Find the rate per period r, the repayment per period R, and the initial value T_0 (the loan principal, or the balance given in the question).
2. Recursive rule: T_{n+1} = (1 + r)T_n − R. If the question writes it as T_{n+1} = aT_n − b, then a = 1 + r and b = R.
3. Substitute period by period to find the balance; or use the solver in Pattern 8, entering N, I, PV and PMT, to find FV (the balance).
4. If there is a one-off repayment: first find the balance at that time, subtract the one-off repayment from it to obtain the new PV, then use the remaining number of periods to find the final balance (2022A-Q16(b)).
5. If the rate or the repayment changes, continue the calculation from the balance at the time of the change, using the new recursive rule (2024A-Q6(d)).

**Mark-earning points (typical key wording)**: the recursive rule and the initial value are marked separately (2017A-Q14(a)(i), 2018A-Q14(a)(i)); every column of the repayment table must be correct (2021A-Q10(b) gives marks for the opening balance and the repayment, interest and closing balance separately; 2016A-Q12(b) requires A, the interest in the 6th month, to be 219.91, and B, the closing balance, to be 14 380.32); the balance after n payments (2022A-Q16(a)); the calculation using the new PV after a one-off repayment (2022A-Q16(b)).

**Common errors**: interest calculated using the annual rate; forgetting T_0, or writing T_0 as the balance after the first repayment (2021A-Q10(c) asks for the value at period 0 to be explained); using the old PV after a one-off repayment. The context of 2016A-Q12(e) states that if each repayment does not exceed the interest for that period, the balance does not fall and the loan is never repaid.

**Past questions**: 2016A-Q12(b), 2016A-Q12(e), 2017A-Q14(a)(i), 2017A-Q14(a)(ii), 2017A-Q14(b), 2018A-Q14(a)(i), 2020A-Q11(b)(i), 2020A-Q11(b)(ii), 2020A-Q12(c)(i), 2021A-Q10(b), 2021A-Q10(c), 2022A-Q16(a), 2022A-Q16(b), 2023A-Q9(b), 2023A-Q9(c)(i), 2023A-Q9(c)(iii), 2023A-Q9(g), 2024A-Q6(a)(i), 2024A-Q6(a)(ii), 2024A-Q6(d)

---

## Pattern 5: Repayment, rate and payoff duration

**Recognition**: The question asks how many months or years it takes to repay a loan, how long it takes after the repayment amount changes, or what each period's payment must be to clear the loan within a stated period. It may also be a comparison of two repayment plans.

**Steps**
1. For the payoff period, use the solver: PV = loan amount, PMT = each repayment (opposite sign to PV), FV = 0, solve for N. N is usually not a whole number; for the rounding method see Pattern 6.
2. To clear the loan within a stated period, work back to PMT: PV, FV = 0, N and I are known; solve for PMT. Give the precision the question requires; for example, 2016A-Q12(f) is marked on rounding the payment up to the nearest cent.
3. Comparing plans: find the number of periods, balance or total repayments for each plan, state which is better, and give the difference (2018A-Q14(c), 2020A-Q11(c)).
4. If each repayment is no more than the interest for the period, the balance does not fall and the loan is never repaid (2016A-Q12(e)).

**Mark-earning points (typical key wording)**: PMT is correct and rounded as required (2016A-Q12(f)); the number of periods is correct (2021A-Q10(d), 2023A-Q9(d), 2024A-Q6(c)(i), 2025A-Q8(f)(i)); when comparing plans, the balance or total of each is written out and the difference is given (2020A-Q11(c)); the reason for the chosen plan is valid (2018A-Q14(c)).

**Common errors**: the unit of the number of periods (the question asks for months but the answer is given in years); the reason for paying in instalments must explain that the saving comes from reducing interest (2020A-Q11(a)); ignoring a final partial period's repayment (dealt with under Pattern 6).

**Past questions**: 2016A-Q12(c), 2016A-Q12(e), 2016A-Q12(f), 2017A-Q14(c), 2018A-Q14(a)(ii), 2018A-Q14(c), 2020A-Q11(a), 2020A-Q11(c), 2020A-Q12(c)(ii), 2021A-Q10(d), 2023A-Q9(a), 2023A-Q9(d), 2023A-Q9(g), 2024A-Q6(c)(i), 2024A-Q6(d), 2025A-Q8(f)(i)

---

## Pattern 6: Total loan interest and final adjusted repayment

**Recognition**: The question asks for the total repayments, the total interest, the final repayment, or the total cost (including the deposit). The final repayment is usually different from the others.

**Steps**
1. Find the number of complete periods N (the whole-number part), and use the recursion or the solver to find the balance T_N after the Nth repayment.
2. Interest for period N + 1 = r × T_N; final repayment = T_N + the interest for this period.
3. Total repayments = N × repayment per period + final repayment; total interest = total repayments − loan principal. If the question asks for the total cost, add the deposit.
4. For questions where the number of periods must be rounded, first calculate the full-period case, then compare with one more period, and finally determine the total (2025A-Q8(f)(ii)).

**Mark-earning points (typical key wording)**: usually three mark-earning points, namely the balance after the Nth repayment, the interest for period N + 1, and the total (2016A-Q12(d), 2020A-Q12(c)(iii)); the final repayment is correct (2017A-Q14(d)); the total cost includes the deposit (2017A-Q14(e)); the complete number of periods is used correctly (2022A-Q15(b)(iv)).

**Common errors**: writing the final repayment as an ordinary repayment; confusing total interest with total repayments; forgetting the deposit. The key note for 2022A-Q15(b)(iii) and (iv) says: if 6.1 ÷ 1200 is used instead of the rounded 0.00508, the final repayment becomes 5161.09 (rather than 4858.42), and the total interest also changes; so the intermediate rate and balance must be kept to sufficient decimal places.

**Past questions**: 2016A-Q12(d), 2017A-Q14(d), 2017A-Q14(e), 2018A-Q14(c), 2020A-Q12(c)(iii), 2021A-Q10(e), 2022A-Q15(b)(iii), 2022A-Q15(b)(iv), 2023A-Q9(c)(ii), 2023A-Q9(e), 2023A-Q9(f), 2023A-Q9(g), 2024A-Q6(c)(ii), 2024A-Q6(d), 2025A-Q8(f)(ii)

---

## Pattern 7: Annuity recurrence and balance changes ★

**Recognition**: A principal has a fixed amount withdrawn each period (retirement income, scholarship, holiday expenses, etc.). The question asks for the balance after withdrawals, how many years it can be sustained, or the largest amount that can be withdrawn each period.

**Steps**
1. Match the rate periods: if interest compounds monthly and withdrawals are annual, first convert the compound rate to the equivalent effective annual rate (the key for 2025A-Q12(a)(ii) first finds the effective annual rate, and then writes the recursive rule).
2. Initial value T_0 is the starting principal; recursive rule T_{n+1} = (1 + r)T_n − P, where P is the withdrawal per period.
3. When the question asks for the balance after a withdrawal, take the value at the moment just after the withdrawal.
4. To find the number of years it can be sustained: use the solver with PV, PMT, I and FV = 0 to obtain N in decimal form, then round it (2016A-Q16(a)(ii)).
5. The largest withdrawal that does not reduce the principal equals the interest each period, i.e. P = r × PV (2016A-Q16(a)(iii): first calculate the 6% interest, then explain that the principal will not fall).

**Mark-earning points (typical key wording)**: the growth rate is correct (2016A-Q16(a)(i)); the withdrawal is correct; T_0 is correctly defined (2016A-Q16(a)(i) marks the growth rate, the withdrawal and T_0 separately); for balance questions, the initial balance and the balance at the time asked are marked separately (2016A-Q16(b)(ii)); the largest withdrawal is rounded down to the nearest hundred (2016A-Q16(b)(iii)); 2025A-Q12(a)(ii) requires the effective annual rate to be written before the recursive rule.

**Common errors**: applying the annual rate directly when the compounding period and withdrawal period differ; calculating the largest withdrawal as a fraction of the principal, rather than as the period's interest; mixing up the timing of withdrawals and balances. The 2016 Q16 question was the hardest of that year (mean 42.26%); this pattern's sub-questions cover recursion, the number of years and the largest withdrawal.

**Past questions**: 2016A-Q16(a)(i), 2016A-Q16(a)(iii), 2016A-Q16(b)(i), 2016A-Q16(b)(ii), 2016A-Q16(b)(iii), 2020A-Q9(a), 2021A-Q14(a)(i), 2021A-Q14(a)(ii), 2021A-Q14(a)(iii), 2022A-Q15(b)(i), 2023A-Q14(a), 2023A-Q14(b), 2024A-Q13(a), 2024A-Q13(b), 2024A-Q13(d)(ii), 2025A-Q12(a)(ii), 2025A-Q12(b)(i), 2025A-Q12(d)

---

## Pattern 8: Annuity value, payment and duration calculations ★

**Recognition**: The question involves an annuity or a fixed-term savings target, and asks for the present value, the payment per period, the number of years available, or the required interest rate. A financial calculator or solver is usually needed.

**Steps**
1. Parameters: N = total number of payments (years × P/Y); I = nominal annual rate; PV = present value; PMT = payment per period; FV = future value (balance 0 at the end, or the target amount); P/Y and C/Y are the number of payments per year and compoundings per year, entered as the question requires (2018A-Q11(a): both are 12).
2. Sign convention: for the saver, PV and PMT have the same sign (both outgoing), and FV has the opposite sign if it is a target; for the borrower, PV is the principal received, the repayment PMT has the opposite sign to PV, and FV = 0 when the loan is cleared. Write the value of each parameter on the answer sheet so that it can be checked.
3. Timing of payments: for payments at the end of each period, use the END mode; if the question states that interest is added before the payment, process it using the recursive rule (2022A-Q15(b)(i)).
4. When N is not a whole number, round it: the key for 2018A-Q11(b)(i) requires N to be rounded down to 12 years; the remainder after rounding is handled under the final-period treatment in Pattern 6.
5. To find the rate: with N, PV, PMT and FV known, solve for I (2018A-Q11(b)(ii)).

**Mark-earning points (typical key wording)**: at least three to four parameters correct, with the result calculated only after all parameters are correct (2017A-Q8(b), 2022A-Q8(b)(i)); N correct (60 months in 2018A-Q11(a); 20 payments in 2018A-Q11(b)(ii)); P/Y and C/Y both entered correctly (2018A-Q11(a), 2025A-Q8(d)); the shortfall is found (2022A-Q8(b)(i)).

**Common errors**: N given as the number of years rather than the number of payments; deposits and withdrawals given the same sign; forgetting the balance left at the end of the term. 2016A-Q16(a)(ii) asks for the number of years in decimal form first, and then the whole number of years.

**Past questions**: 2016A-Q16(a)(ii), 2017A-Q8(b), 2018A-Q11(a), 2018A-Q11(b)(i), 2018A-Q11(b)(ii), 2018A-Q16(f)(i), 2018A-Q16(f)(ii), 2020A-Q9(c), 2021A-Q10(f), 2022A-Q8(b)(i), 2022A-Q8(b)(ii), 2022A-Q15(b)(ii), 2023A-Q14(a), 2024A-Q10(b), 2024A-Q10(c), 2024A-Q13(d)(i), 2025A-Q8(c), 2025A-Q8(d), 2025A-Q12(b)(ii)

---

## Pattern 9: Perpetuity calculations

**Recognition**: The question asks for an amount to pay a fixed sum every period indefinitely, or for an annuity that becomes a perpetuity (perpetuity) when it ends.

**Steps**
1. Convert the rate per payment period: if payments are made quarterly and interest is compounded monthly, convert the monthly rate to a quarterly rate, or set P/Y and C/Y both on the solver.
2. The present value needed to sustain perpetual payments: PV = PMT ÷ rate per period.
3. Given the present value, find the payment per period: PMT = PV × rate per period.
4. Annuity converting to perpetuity: first find the annuity balance at the time of conversion (this becomes the new PV), then find the payment per period (2023A-Q14(b), 2025A-Q12(c)).
5. When using the solver, PV and FV should have opposite signs (the key for 2025A-Q12(c) includes this).

**Mark-earning points (typical key wording)**: the rate per period is correct (2017A-Q8(a), to be checked: the key's solution is x = x(1 + 5.9%/12)¹² − 6000, i.e. x = 6000 ÷ i, where the effective annual rate i ≈ 6.06%, giving 98 974; the stem says the payment is made at the start of the year, but the key's solution uses end-of-period timing; with start-of-period payment the answer would be 104 974, so the key and the stem disagree on timing); P/Y, C/Y, PV and FV are all entered correctly (2020A-Q9(d), 2021A-Q14(b), 2024A-Q13(e)); the balance at conversion is correct (2023A-Q14(b)); 2025A-Q12(c) requires the annuity balance to be calculated, the equation set up, and a conclusion drawn; 2025A-Q12(d) requires the balances at year 8 and year 9 to be compared, to determine the longest period.

**Common errors**: dividing the annual rate directly by the number of payments; not converting when payment and compounding frequencies differ; treating a perpetuity as a finite annuity. The key for 2025A-Q12(d) gives two items, the balance at year 9 and the balance at year 8, so both comparison values must be written out before reaching a conclusion.

**Past questions**: 2017A-Q8(a) (to be checked), 2020A-Q9(d), 2021A-Q14(b), 2022A-Q15(a), 2022A-Q15(c), 2023A-Q14(b), 2024A-Q13(e), 2025A-Q12(c), 2025A-Q12(d)

---

## Pattern 10: Nominal annual and periodic interest rates

**Recognition**: The question gives the growth factor of a balance or the interest per period, and asks for the rate per period or the nominal annual rate.

**Steps**
1. Rate per period r = growth factor − 1 (or interest for the period ÷ opening balance).
2. Nominal annual rate = rate per period × compoundings per year. This is simple multiplication, not the effective annual rate.
3. If the effective annual rate is needed, use (1 + r)^m − 1 (see Pattern 2).

**Mark-earning points (typical key wording)**: rate per period is correct; nominal annual rate is correct (2024A-Q6(b), 2025A-Q8(e), 2025A-Q12(a)(i)); 2024A-Q13(c) asks for the annual rate of an annuity, which is calculated in the same way.

**Common errors**: treating the nominal annual rate as the effective annual rate; using the wrong number of periods per year (12 for monthly, 4 for quarterly, 2 for half-yearly).

**Past questions**: 2024A-Q6(b), 2024A-Q13(c), 2025A-Q8(e), 2025A-Q12(a)(i)

> Note: Pattern 10 (FIN10) has only 4 tags, so this section is brief.
