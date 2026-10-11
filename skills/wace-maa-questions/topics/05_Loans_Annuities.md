# FIN · Loans, investments and annuities 贷款、投资与年金 (Unit 4.2)

Bank: `<ROOT>\MAA\topics\05_Loans_Annuities.md` / `.pdf`. 25 questions with FIN parts in 2016–2025 (no 2019 key), about 262 tagged marks (19% of the total). 24 of these are Calculator-assumed; the only Calculator-free one is 2017 CF Q4. The examiners' reports single out annuities and perpetuities as the weakest area: the hardest annuity items in 2016, 2023 and 2024 had means of only about 34–42%.

## Scope
- Compound interest: rate per period, recurrence, future value, number of periods.
- Effective annual rate (EAR) and comparing compounding frequencies; nominal and periodic rates.
- Reducing-balance loans: the balance recurrence, repayment schedules, a one-off repayment, a change of rate or repayment.
- Total interest and the final adjusted repayment.
- Payoff time and the repayment needed to clear a loan within a stated term.
- Annuities: a balance that is drawn down each period, how long it lasts, the largest sustainable withdrawal, a target savings goal.
- Perpetuities, and an annuity that converts to a perpetuity.

## How SCSA asks it
- A reducing-balance loan with a repayment schedule and total interest: 2016 CA Q12, 2017 CA Q14, 2021 CA Q10, 2023 CA Q9, 2024 CA Q6.
- Retirement or withdrawal annuities: 2016 CA Q16, 2021 CA Q14, 2025 CA Q12.
- Saving for a goal with regular deposits, and comparing two savings plans: 2018 CA Q11, 2022 CA Q8, 2025 CA Q8.
- Compound interest and effective rates: 2016 CA Q13, 2018 CA Q8, 2022 CA Q8, 2024 CA Q10.

## Patterns

| code | pattern | questions / marks (2016–25) | median part marks (range) | CF / CA parts | key past refs |
|---|---|---|---|---|---|
| FIN1 | 复利投资或贷款递推建模 Compound interest recurrence model | 5 / 15 | 2 (1–2) | 0 / 9 | 2018 CA Q8(a)(ii); 2020 CA Q12(a)–(b); 2025 CA Q8(b) |
| FIN2 | 有效年利率与计息频率比较 Effective annual rate and compounding comparison | 12 / 39 | 2 (1–3) | 1 / 17 | 2016 CA Q13(b); 2016 CA Q16(b)(i)–(iii); 2022 CA Q8(a); 2024 CA Q10(d) |
| FIN3 | 复利现值、终值与期限求解 Compound interest value and term calculations | 4 / 13 | 2 (1–3) | 2 / 5 | 2016 CA Q13(a)(i)–(ii); 2017 CF Q4(b)–(c); 2025 CA Q8(a) |
| FIN4 | 递减余额贷款递推 Reducing-balance loan recurrence | 9 / 46 | 2 (1–5) | 0 / 20 | 2016 CA Q12(b); 2017 CA Q14(a); 2021 CA Q10(b)–(c); 2023 CA Q9(b)–(c) |
| FIN5 | 还款额、利率与清偿时间关系 Repayment, rate and payoff duration | 9 / 34 | 2 (1–5) | 0 / 16 | 2016 CA Q12(c), (f); 2018 CA Q14(a)(ii); 2024 CA Q6(c)(i); 2025 CA Q8(f)(i) |
| FIN6 | 贷款总利息与末期调整还款 Total loan interest and final adjusted repayment | 9 / 42 | 3 (1–5) | 0 / 15 | 2016 CA Q12(d); 2017 CA Q14(d)–(e); 2022 CA Q15(b)(iii)–(iv); 2025 CA Q8(f)(ii) |
| FIN7 | 年金递推与余额变化 Annuity recurrence and balance changes | 7 / 45 | 2 (1–6) | 0 / 18 | 2016 CA Q16(a)(i), (iii); 2021 CA Q14(a); 2025 CA Q12(a)(ii) |
| FIN8 | 年金现值、期款与期限求解 Annuity value, payment and duration calculations | 13 / 51 | 2 (1–6) | 0 / 19 | 2016 CA Q16(a)(ii); 2018 CA Q11(a)–(b); 2022 CA Q8(b)(i); 2025 CA Q8(c)–(d) |
| FIN9 | 永续年金与无限期付款 Perpetuity calculations | 7 / 27 | 3 (1–5) | 0 / 9 | 2021 CA Q14(b); 2023 CA Q14(b); 2025 CA Q12(c)–(d) |
| FIN10 | 名义年利率与每期利率换算 Nominal annual and periodic interest rates (related) | 4 / 4 | 1 (1) | 0 / 4 | 2024 CA Q6(b); 2025 CA Q8(e); 2025 CA Q12(a)(i) |

## Method in brief

- **FIN1.** Rate per period = annual rate ÷ compoundings per year (quarterly: ÷ 4; monthly: ÷ 12). Recurrence A(n+1) = (1 + r)A(n) ± d, where d is a deposit (+) or repayment (−). Write the recurrence and the starting value A0 separately, and check the timing of each deposit against the stem.
- **FIN2.** EAR = (1 + j/m)^m − 1, where j is the nominal annual rate and m the compoundings per year (daily: m = 365). For the same principal, a saver chooses the higher EAR and a borrower the lower. To find a nominal rate that matches a target EAR, substitute the target and solve. The conclusion names the scheme and gives both EARs.
- **FIN3.** Future value FV = PV(1 + r)^N, with r per period and N = years × periods per year. To find N, use logarithms (N = ln(FV/PV)/ln(1 + r)) or the solver with PV, FV, I, P/Y and C/Y. For doubling, FV = 2PV. Keep the value and the interest separate when the question asks for one of them.
- **FIN4.** Loan recurrence T(n+1) = (1 + r)T(n) − R, with T0 the principal. A schedule has four columns for each period: opening balance, interest (= r × opening), repayment, closing balance. Keep decimals until the end of each row as the stem requires. After a one-off repayment, subtract it from the balance at that time and continue with the remaining periods. After a rate or repayment change, start the new recurrence from the balance at the change.
- **FIN5.** Payoff time: solver with PV (loan, positive), PMT (repayment, negative), FV = 0, and solve for N. N is usually not whole. To clear a loan within a stated term, solve for PMT with N, I, PV and FV = 0 and round as asked. To compare two plans, find each plan's total repayments or balance and state the difference. If a repayment is no larger than that period's interest, the balance does not fall and the loan is never repaid.
- **FIN6.** Find the whole number of complete periods N, the balance T_N after the Nth repayment, the interest for period N + 1 (= r × T_N), and the final repayment (= T_N + that interest). Total repayments = N × R + final repayment. Total interest = total repayments − principal. For a total cost, add the deposit. Rounding a rate early changes the final repayment, so keep enough decimals.
- **FIN7.** Match the periods first: if interest compounds monthly and withdrawals are annual, convert to the EAR. Recurrence T(n+1) = (1 + r)T(n) − P, with T0 the starting principal. A balance "after a withdrawal" is the value just after that withdrawal. Years sustained: solver with PV, PMT, I and FV = 0, rounded in the direction the question asks. Largest withdrawal that leaves the principal unchanged: P = r × PV, rounded down to the nearest dollar or hundred when the question asks for it.
- **FIN8.** Parameters: N = total number of payments (years × P/Y), I = nominal annual rate, PV, PMT, FV, P/Y and C/Y. Sign convention: money received and money paid take opposite signs. Timing: END for payments at the end of each period; if interest is added before a payment, use the recurrence. If N is not whole, round it in the direction the context needs (for example, down to 12 full years), and handle the remainder under FIN6. To find a rate, solve for I with N, PV, PMT and FV known.
- **FIN9.** Perpetuity: PV = PMT ÷ r(period), and PMT = PV × r(period). For an annuity that becomes a perpetuity, first find the annuity balance at the conversion point (this is the new PV), then the payment. Compare the balances at successive years to find the longest period.
- **FIN10.** Rate per period = growth factor − 1, or interest ÷ opening balance. Nominal annual rate = rate per period × compoundings per year. This is not the EAR.

## Writing tips
- Write out the solver's parameters (N, I, PV, PMT, FV, P/Y, C/Y, timing) in the working, one per line, so that the markers can check them.
- Keep the sign convention consistent and say which direction is money in and out.
- Interest is calculated on the balance at the start of each period, not on the original principal.
- N for a loan is the number of payments, not years, unless the question says so.
- State the timing (start or end of period) in every generated question. The 2017 CA Q8 key solves with end-of-period payments although its stem says start of year, so do not reuse that wording.
- Money answers to the cent. Discrete counts (periods, people) are rounded to whole numbers in the direction the context needs.
- Calculator-assumed: finance questions are where the CAS and financial solver save the most time, but the working must still show the parameters and the final rounding.
