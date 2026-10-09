# MAS Solution Strategies · Independent Review Record

**Review method**: Each set of notes is reviewed by an independent sub-agent. The reviewer did not take part in writing, works with fresh context, and only reads—does not edit. The basis for checking includes: the original "Specific behaviours" in the marking key for each question in `evidence/`, the full 2016–2025 exam reports, the PDF pages of the original papers and keys, with independent calculations using sympy/scipy/numpy.

**Handling principles**: The author reviews each review comment one by one. All high-severity comments are checked back against the original paper text; anything that can be verified has been re-verified. Items marked "doubtful" by the reviewer are only changed when supporting evidence is found.

**Conclusion categories**: Accepted = changed as per the comment; Partially accepted = wording changed but the suggestion was not followed completely; Rejected = not changed, with reasons stated.

---

## 01 Complex numbers (12 items: accepted 12)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | Regular hexagon written incorrectly: in 2025F-Q7, z₀ is at the origin, the hexagon is not centred at O, and the product is 6r⁵, not r⁵ | Accepted: the author recalculated (moduli in order are r, √3r, 2r, √3r, r) and corrected it; the question-setting skill was also corrected |
| 2 | Medium-high | 2025A-Q19(b) omits the periodic solutions n = 3,4,5 + 12k | Accepted |
| 3 | Medium | Maximum argument: sin θ = r/d does not give the argument | Accepted |
| 4 | Medium | 2020A-Q10(b): the ray endpoint i is on the locus (solid point) | Accepted |
| 5 | Low | The closest-distance formula only holds when the point is outside the circle | Accepted |
| 6 | Low | "Always use polar form for multiplication and division" contradicts "use the conjugate for division" | Accepted |
| 7 | Low | Report year and content mismatch (−z is from the 2021 report) | Accepted |
| 8 | Low | The third-quadrant example is not the original report wording; 5π/4 cannot be written either | Accepted |
| 9 | Low | Missing citation of 2022F-Q6; the sample paper is not specified | Accepted |
| 10 | Low | The "CF opening / CF hard question" labels do not match the cited CA questions | Accepted |
| 11 | Low | "iⁿ is periodic with period 4" is inaccurate (n·iⁿ is not periodic) | Accepted |
| 12 | Low | When θ < 0, it should be written as clockwise by \|θ\| | Accepted |

## 02 Functions and graphs (16 items: accepted 16)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | Reciprocal-function table "f → ±∞ ⇒ horizontal asymptote y = 0" is wrong: a vertical asymptote of f corresponds to an open point (b, 0) of 1/f | Accepted: split into two rows |
| 2 | Medium | The table omits "horizontal asymptote y = c → y = 1/c" | Accepted |
| 3 | Medium | "Hole-to-hole" only holds when b ≠ 0 | Accepted |
| 4 | Medium | The original 2016A-Q12(b) is \|f(x)\| = d, not f(x) = d | Accepted |
| 5 | Medium | "Flat bottom of two V-shaped lines" is described incorrectly | Accepted: changed to the flat bottom of the sum of two absolute values; the author calculated a = 3, k = 2 |
| 6 | Low | The integral of the W-shaped graph is one triangle, not two | Accepted |
| 7 | Medium | The sign of the inverse function should be determined by ran f⁻¹ = dom f | Accepted |
| 8 | Medium | When a square root is in the denominator, it must be > 0 (2025F-Q2(a)) | Accepted |
| 9 | Medium | "c > 0 guarantees no zeros" is not enough; a and c must have the same sign | Accepted |
| 10 | Low | "Turning point (if the question requires it)": 2017F-Q5 awarded marks even though it was not required | Accepted |
| 11 | Low (doubtful) | The fabricated "c = 2 touches the x-axis" example conflicts with the meaning of c in the actual question | Accepted: used the original question wording instead |
| 12 | Low | "Most stable in the whole course" is an overgeneralisation (in 2018 it was instead listed as well answered) | Accepted |
| 13 | Low | "Do not use it" omits the 2019 report | Accepted |
| 14 | Low | The example ln\|x − 3\| does not come from the 2022 report | Accepted |
| 15 | Low | Missing citations of 2016F-Q8(b), 2022F-Q2(a) | Accepted |
| 16 | Low | "Intersection points unchanged" is vague | Accepted |

## 03 3D vectors and systems of linear equations (13 items: accepted 13)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | Laser reflection direction written incorrectly: the vector obtained by adding in the S→B direction is parallel to the mirror; it should be the sum of the unit vectors of B→S and B→R, or d̂_out − d̂_in ∥ n | Accepted: the author used numpy to verify d̂_out − d̂_in = (0, 0.23, 0.46) ∥ (0, 1, 2) |
| 2 | High | 2024A-Q16(c) is the shortest distance between two lines (two independent parameters), while 2017A-Q14 is solving an inequality to find the duration; the two questions were conflated | Accepted: split into two categories |
| 3 | Medium | "CF is tested every year" is untrue (not tested in 2017 or 2019; in 2021 it was in CA) | Accepted |
| 4 | Medium | "Named for five consecutive years" does not match the reports; 2024 is missing | Accepted |
| 5 | Medium | "Must write parametric form" is an overgeneralisation; the key accepts representation using variable relationships | Accepted |
| 6 | Medium | "Wavy lines, dot product, cross product" is not the original report wording | Accepted: marked as author's suggestion |
| 7 | Low-medium | The point-to-plane distance formula is not on the formula sheet | Accepted |
| 8 | Low | "Many people have never seen it" is an exaggerated paraphrase | Accepted |
| 9 | Low | The line-plane angle formula lacks absolute value, making it inconsistent | Accepted |
| 10 | Low | The geometric interpretation table omits "three planes coincident"; 2021A-Q14 requires both points to be written | Accepted |
| 11 | Low | The letters a and d are each used for two things | Accepted |
| 12 | Low | "Final CA question" does not match 2018F-Q8 | Accepted |
| 13 | Low (doubtful) | Sample paper question not specified | Accepted |

## 04 Vector calculus and motion (12 items: accepted 11, partially accepted 1)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | 2019A-Q13(d) is not a parabola; it is a figure-eight shape | Accepted |
| 2 | High | The three examples of value restrictions all disagree with the key (2024A-Q18 requires x ≥ 2 and y ≥ 0) | Accepted: replaced with the original key wording |
| 3 | Medium | "One loop = 0 to 2π" is an overgeneralisation (2017A-Q15 is 6π, 2019A-Q13 is 4π) | Accepted |
| 4 | Medium | 2021A-Q19 has no wind and no launch angle, but has lift | Accepted: split into two models |
| 5 | Medium | "Uniform velocity" should be "constant speed" | Accepted |
| 6 | Medium | The descent angle 90° − φ gives a negative value (φ = 143.3°) | Accepted: changed to \|90° − φ\|; the author verified 53.3° |
| 7 | Low | "Three scoring points" is an overgeneralisation | Accepted |
| 8 | Low | The height is relative to the centre; 100 m above the ground corresponds to y = 20 | Accepted |
| 9 | Low | The order of subtraction is not given a source or rule | Accepted |
| 10 | Low | In 2024A-Q16(c), both speed and departure time are adjustable | Accepted |
| 11 | Low | Parameter elimination omits the "x is linear in t" type (named in the 2018 report) | Accepted |
| 12 | Low (doubtful) | The SHM in 2019A-Q18(d) is not mentioned | Partially accepted: added a cross-reference; the method is in the differential equations notes |

## 05 Integration techniques and applications (11 items: accepted 11)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | Medium | "Irreducible quadratic" was paired with the reducible x² + 3x + 1 (discriminant 5 > 0) | Accepted: replaced with x² + 2; a separate note was added for 2022F-Q4 |
| 2 | Medium | The error example from the 2021 report is paraphrased incorrectly (the original is √(2 − sin²θ) ≠ √2 − sin θ) | Accepted |
| 3 | Medium | "Substitution is always tested in CF" is untrue (not tested in 2022), and there are 7-mark questions | Accepted |
| 4 | Medium | "Partial fractions are always tested every year" is untrue (not tested in 2017 or 2023) | Accepted |
| 5 | Medium | 2023A-Q17(c) is an increment formula question; 2022A-Q17 does not use dV/dh | Accepted: split and rewritten |
| 6 | Medium | "Absolute value is a separate 1 mark" is untrue; the absolute value is included in the antiderivative mark | Accepted |
| 7 | Low | The "correct notation" mark is awarded together with the limits; the area expression does not need π | Accepted |
| 8 | Low | 2016A-Q9 is an indefinite integral; for 2021F-Q3 the substitution must be chosen yourself | Accepted |
| 9 | Low | 3 questions are not categorised | Accepted |
| 10 | Low | The 4 in the cardioid is the product of two parts | Accepted |
| 11 | Low | The 2024 report says the numerator after finding a common denominator was written incorrectly, not that comparing coefficients was wrong | Accepted |

## 06 Rates of Change and Differential Equations (15 items: 15 accepted)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | Medium | The main solution in the key for 2017A-Q17(b) is to count periods, not ∫\|v\| | Accepted |
| 2 | High | The point of inflection in 2025A-Q16 is at the maximum slope (3, −1), not where the slope is 0 | Accepted |
| 3 | Medium | '10% growth per year' should be an instantaneous growth rate (dP/dt = 0.1P); otherwise the answer changes from 333 to about 412 | Accepted: editor verified both results |
| 4 | Low | For 2025A-Q15, x(0) is −1 | Accepted |
| 5 | Medium | The letter k refers to carrying capacity and the constant of proportionality in different questions, so it is easily confused | Accepted |
| 6 | Low | 'Initial value above k/2 is concave down throughout' needs P₀ < k added | Accepted |
| 7 | Low (doubtful) | The SHM criterion should allow for a shifted equilibrium point a = −n²(x − c) | Accepted |
| 8 | Low | The wording 'cannot differentiate directly with respect to t' is unclear | Accepted |
| 9 | Low | 2024A-Q12 does not give a direction; both ±A sin are awarded marks | Accepted |
| 10 | Medium | The marking panel reminder missed 2024 (logistic), 2017 (standard equation), and 2022 (absolute value) | Accepted |
| 11 | Low | The exact phrase 'integration statement' appears in only two years | Accepted |
| 12 | Low | 2016A-Q18 is a − bx; the two conditions come from different sources | Accepted |
| 13 | Low | 'keep only one independent variable' contradicts the shadow question; the past-paper list has incorrect inclusions and omissions | Accepted |
| 14 | Low | A vertical tangent only holds when the numerator ≠ 0 | Accepted |
| 15 | Low | 2018A-Q20 says 'do not' solve, not 'need not' | Accepted |

## 07 Statistical Inference (16 items: 16 accepted)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | 2022A-Q12(d) is 'the same sample duplicated', not two samples combined; this conflicts with the conclusion of 2019A-Q15(c) | Accepted: write the two cases separately |
| 2 | Medium (doubtful) | 'the key accepts both' is unsupported; the key only gives X̄ < T/n | Accepted; question-setting skill corrected accordingly |
| 3 | Medium | 'examined every year' is untrue (not examined in 2016, 2020) | Accepted |
| 4 | Medium | Missing counterexample 2025A-Q13(e) (many intervals not containing μ is the evidence) | Accepted |
| 5 | Low | 'citing the CLT' is not a standalone marking condition in the key | Accepted |
| 6 | Low | The calculation using 304.4 and 2.326 is inconsistent (should be 304.3) | Accepted: editor recalculated |
| 7 | Low | Rounding when back-solving for n: the key accepts both 2.576 and 2.58; add 2024A-Q14(f) | Accepted |
| 8 | Low | Missing the one-tailed and half-interval cases | Accepted |
| 9 | Low | 2024A-Q14(c) does not ask for n | Accepted |
| 10 | Low | 'the answer is unchanged' applies only to 2018A-Q12(c) | Accepted |
| 11 | Low | For the graphing question, the mark for labelling the probability region was omitted | Accepted |
| 12 | Low | The key's reason for 2024A-Q14(e) is that the sample sizes are different | Accepted |
| 13 | Low | Sample paper question not explained; sample paper A9 is also not referenced | Accepted |
| 14 | Low | 'definitely' should be 'very likely' | Accepted |
| 15 | Low | The precision table lacks context (μ = 80); s and σ are used interchangeably | Accepted |
| 16 | Low | 'n ≥ 30 applies' is an overgeneralisation; when the population is normal, any n works | Accepted |

---

**Summary (7 MAS documents)**: 95 comments in total (including 5 'doubtful' items), 94 accepted, 1 partially accepted, and 0 rejected. There were 8 high-severity items; all were revised after returning to the original paper text or recalculating.

---

## Classification corrections after user feedback (2026-10-09)

- User feedback: the 'Vectors' section contains unrelated differential equations questions. This was verified: 2017A-Q18 (carousel, cosine rule + implicit differentiation) and 2019A-Q18 (Ferris wheel, related rates + SHM proof) contain no vector content and were originally misclassified under vector calculus as 'circular motion'. They have been moved out and kept only in 'Rates of Change and Differential Equations'; the corresponding section in the notes has also been moved across. Vector calculus 14 → 12 questions.
- 2021A-Q19 (ski jump) gives the position vector r(t) and asks for the Cartesian path and landing angle; it is vector motion, so it is retained.
- A keyword review was carried out on all tags; MAS found no other misclassifications.
