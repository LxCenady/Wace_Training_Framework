# MAM · Exponential and Logarithmic Functions — Patterns and Solution Approaches

> Basis: 42 past exam questions containing exponentials/logarithms from 2016–2025, marking keys + exam reports (the 2016, 2018, 2022–2025 reports all list logarithm-related content as a weakness: logarithm laws 2016/2024/2025; logarithmic graphs 2018/2024; reading and interpreting logarithmic scales 2023; converting between exponential and logarithmic form 2022). Original questions are in `topics/04_Exp_Log.pdf`; two questions from the 2016 sample paper are also cited (`2016S-A10`, `2016S-A13`; original paper in `papers/2016Sample_*`).
> Review status: has undergone one round of independent review and was revised according to feedback (see `Review_log.md`).

## Toolbox

- Definition: y = logₐx ⇔ aʸ = x. **The first step in many questions is to convert between logarithmic and exponential form** (the key often awards 1 mark for "converts to index form / uses the inverse relationship").
- Logarithm laws: log(mn) = log m + log n; log(m/n) = log m − log n; log mᵏ = k log m; logₐa = 1; logₐ1 = 0; change of base logₐb = log_c b / log_c a.
- Constants can also be written as logarithms: 4 = 4 ln e = ln e⁴; 2 = log₁₀100; 9 = log₁₀10⁹. This is a key step in 2025F-Q7(a), 2020F-Q6(c), 2024A-Q15(c), 2019A-Q17(b)(iii).
- Calculus: (ln f)′ = f′/f; ∫f′/f dx = ln|f| + c (in exams f(x) > 0 generally, and the key often writes ln f(x) + c); (eᵏˣ)′ = keᵏˣ.

## Marking panel reminders

- Solving 2 ln x = …: ln x requires x > 0, so **negative roots must be rejected** (the 2025F-Q7 key explicitly requires only one solution).
- "How many times" questions on logarithmic scales: the difference in readings is not the answer; the difference must still be converted to a power of 10 (the 2016A-Q12 key awards 1 mark for "subtracts Richter magnitudes", then converts to exponential form). The 2023 report calls for stronger interpretation and reading of logarithmic scales (see 2023F-Q4(c): reading values from the graph of y = log₁₀x).
- When a question requires the use of a graph, show the reading process on the graph (2024A-Q15(a): You must show clearly how you have used the graph).
- Application questions require units. If asked for rate of change, give a signed value (e.g. the answer to 2018A-Q9(c) is −0.164 mg/L/h); only if asked for rate of decrease should you write it as a positive number and state that it is decreasing (2024A-Q8(c) key: "converts to a rate of decrease").

---

## Pattern 1: Expressing Logarithms Using Given Letters (CF)

**Recognition**: "Let p = ln 2, q = ln 3, r = ln 5. Express ln 6.25 in terms of …" "log₁₀2 = x, log₁₀7 = y".

**Approach**: Factor the argument into products, quotients and powers of the given numbers: 6.25 = 25/4 = 5²/2² ⇒ 2r − 2p; 17.5 = 7 × 10 / 4 ⇒ y + 1 − 2x; 14 = 2 × 7.
**Change-of-base type (2025F-Q7(b))**: m = log₃6, n = log₆5, find log₃10. First log₃10 = log₃2 + log₃5; then log₃2 = log₃6 − 1 = m − 1, log₃5 = log₃6 · log₆5 = mn ⇒ **log₃10 = m − 1 + mn**.
**e^{p+q} type**: e^{ln2 + ln3} = e^{ln 6} = 6 (index laws plus inverse relationship).

**Marking points**: ✓ factorise the argument ✓ use the correct logarithm laws ✓ final expression.

**Past exam questions**: 2017F-Q7, 2023F-Q2(a)(b), 2024F-Q5(a)(b), 2025F-Q7(b).

---

## Pattern 2: Solving Exponential / Logarithmic Equations (CF exact values)

**Approach**
- Collect like terms: 4e²ˣ = 81 − 5e²ˣ ⇒ 9e²ˣ = 81 ⇒ e²ˣ = 9 ⇒ x = ln 3.
- Quadratic in eˣ: let u = eˣ, factorise, and reject roots with u ≤ 0 (2020F-Q7(a): eˣ(eˣ − 4) = 0 ⇒ only x = ln 4).
- Logarithmic equations: first combine all terms into a single logarithm (log₂(x+y) + 2 = log₂(x − 2y) ⇒ log₂[4(x+y)] = log₂(x − 2y)), then remove the logarithms, and finally **check the domain**.

**Past exam questions**: 2017F-Q3, 2016F-Q1(b), 2020F-Q7(a), 2024F-Q5(c), 2025F-Q7(a).

---

## Pattern 3: Logarithmic Function Graphs and Transformations

**Recognition**: "sketch y = ln(x − 2) + 1" "determine the equation of g" "explain why p = 5" "find m, q".

**Approach**
1. y = m logₐ(x − p) + q: vertical asymptote x = p; always passes through (p + 1, q); increasing when a > 1 and m > 0.
2. Three essentials for sketching (1 mark each in the key): **asymptote** (draw and label its equation; a dashed line is conventional), **one key point** (e.g. (3, 1)), **correct shape** (including behaviour near the asymptote).
3. Determine parameters from a graph: first use the asymptote to find p, then substitute two points to solve for m and q (2021A-Q15).
4. Recognising transformations: ln(4x) = ln x + ln 4 → translate up by ln 4; ln√x = ½ln x → vertical dilation by ½; ln x + 4 = ln(e⁴x) → horizontal dilation by a factor of 1/e⁴ (2020F-Q6).
5. log₂(1/(x−1)) = −log₂(x − 1): first reflect in the x-axis, then translate right by 1 (2022F-Q4(c)).

**Solving equations or estimating from a graph**: e.g. √7 ⇒ log₂√7 = ½log₂7 ≈ ½ × 2.8 = 1.4 ⇒ read x ≈ 2.6 (2022F-Q4(a)(ii)).

**Past exam questions**: 2018A-Q8, 2019F-Q4, 2020F-Q6, 2021A-Q15, 2022F-Q4, 2024F-Q5(d).

---

## Pattern 4: Exponential Growth/Decay Models ★ CA high-frequency

**Recognition**: P = P₀eᵏᵗ, C = 4e^{−0.05t}, T = T₀ − 175e^{−0.07t}, half-life, "in danger if below …".

**Standard procedure**
1. **Initial value**: substitute t = 0 (with units).
2. **Find k**: use the half-life ½ = e^{k·100.5}, or use two data points. Round to the required number of significant figures.
3. **Time to reach a value**: set the model equal to the target value and solve using ln; convert to a specific time according to the context, and **round as required by the question**. Example: in 2018A-Q9(d), 4e^{−0.05t} = 2.5 ⇒ t = ln 1.6 / 0.05 ≈ 9.40 h ⇒ 9 am + 9 h 24 min = **6:24 pm** (for "latest", round down; the key notes 6:25 would be too late). State any roots outside the domain as rejected (2025A-Q9(b)).
4. **Rate of change**: dP/dt = kP, substitute the time; see the reminder above about signs.
5. **Piecewise models**: the initial value of the later model = the value at the end of the previous model (2017A-Q16(c), 2023A-Q6(e)).
6. **Long-term behaviour**: as t → ∞, e^{−kt} → 0, so T → T₀ and rate of change → 0 (the three points in 2020A-Q15(e): rate of change → 0, temperature tends to a constant, and the constant equals T₀).

**Marking points**: ✓ set up the equation ✓ solve ✓ round or convert time as required ✓ differentiate ✓ substitute values.

**Past exam questions**: 2016A-Q9, 2016S-A10, 2017A-Q16, 2018A-Q9, 2020A-Q15, 2022A-Q14, 2023A-Q6, 2024A-Q8, 2025A-Q9(b).

---

## Pattern 5: Logarithmic Scales (decibels, Richter, site ranking, moment magnitude)

**Recognition**: L = 10 log(I/I₀), M = log₁₀(A/A₀), R = 2 log₁₀(S/S₀), ask "how many times larger / more intense".

**Approach (ratio questions)**
1. General form L = k·log₁₀(I/I₀). Convert the two readings to exponential form: I₁ = I₀·10^{L₁/k}, I₂ = I₀·10^{L₂/k}.
2. Divide; I₀ cancels: I₂/I₁ = 10^{(L₂−L₁)/k}. **k varies by question**: decibels L = 10 log ⇒ 90 dB vs 60 dB is 10³ = 1000 times; sound pressure D = 20 log (2016S-A13) ⇒ a 30 dB difference is 10^{1.5} ≈ 31.6 times; Richter k = 1 (2016A-Q12) ⇒ 10^{2.1} ≈ 126 times; site ranking R = 2 log (2023F-Q4).
3. Find the reference value I₀ or S₀: substitute one pair (L, I), convert to exponential form and solve.

**Linearisation (log against t is a straight line)**: log₁₀P = At + B ⇒ P = 10^B·(10^A)ᵗ; the slope A reflects the growth rate (in 2019A-Q17(c), comparing growth rates at two temperatures requires referring to the slope or base).

**Marking points**: ✓ convert to exponential form ✓ write the ratio and cancel ✓ conclusion ("… times").

**Past exam questions**: 2016A-Q12, 2016S-A13, 2018A-Q18, 2019A-Q17, 2022A-Q14(c)–(e), 2023F-Q4, 2024A-Q15, 2025A-Q17.

---

## Pattern 6: Logarithmic models + differentiation + drawing a conclusion

**Recognise**: s = 40.6 ln(0.15D), A(t) = b log₄(t+1) + c, P(x) = 20 ln(x+a)/(x+5).

**Approach**
- Determine parameters from given points: A(0) = 21 ⇒ c = 21; A(1) = 53 ⇒ b·log₄2 = 32 ⇒ b = 64.
- Interpret the derivative: ds/dD = 40.6/D decreases as D increases ⇒ for the same 8 m reduction, roads with a larger original stopping distance have a smaller reduction in speed limit (2025A-Q11(c)).
- Determine whether the target can be achieved: solve A(t) = 493, check whether t is reasonable (2024A-Q17(c)), and give a conclusion with reasons.
- Round according to context: round quantities down (2024A-Q17(b)); compare adjacent integers (2020A-Q13 compares 74 and 75).
- “during which week”: x is the week number from the start; 1 < x < 2 is in **week 2**, not week 1 (the key for 2021A-Q16(d) says “occurs in the second week”).

**Past exam questions**: 2018F-Q6, 2020A-Q13, 2021A-Q16, 2024A-Q17, 2025A-Q11.

---

## Pattern 7: Calculus of eˣ / ln x (cross-reference)

The methods for this question type are covered in the differentiation and integration handouts; only the questions are listed here, to make it easy to practise by the “exponential and logarithmic” topic:
- Use d/dx(x ln x) to evaluate ∫ln x: 2018F-Q7, 2023F-Q2(c) → see `02_Integration_Methods.md` Pattern 2.
- Areas involving eˣ, ln x (including inverse-function area), and the area correspondence between ∫1/x and ln: 2017F-Q5, 2019F-Q5, 2020A-Q11, 2021F-Q7 → Integration handout Patterns 5, 6.
- Finding f from f′, and ∫f′/f: 2020A-Q10 → Integration handout Pattern 1.
- Increment formula to estimate ln 2.02: 2021F-Q3 → Differentiation handout Pattern 7.
- For functions involving ln, eˣ, find stationary points and sketch the graph: 2016A-Q13, 2017A-Q14, 2020F-Q7(b)–(d), 2019A-Q12 → Differentiation handout Pattern 4.
- Derivative of aˣ and the definition of e: 2018A-Q14.
