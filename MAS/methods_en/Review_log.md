# MAS Solution Approaches · Independent Review Record

**Review method**: Each handout is reviewed by an independent sub-agent. The reviewer did not take part in writing, works in a fresh context, and only reads without changing anything. Sources for verification include: the original "Specific behaviours" text in each question's marking key in `evidence/`, the full text of the 2016–2025 exam reports, the PDF pages of the original papers and keys, and independent verification using sympy/scipy/numpy.

**Handling principles**: The author reviews each review comment one by one. All high-severity comments are checked back against the original exam paper wording, and anything that can be verified by calculation has been recalculated. Items marked "doubtful" by the reviewer are changed only when evidence is found.

**Outcome categories**: Accepted = changed as suggested; Partly accepted = wording changed but the suggestion was not followed fully; Rejected = not changed, with reasons stated.

---

## 01 Complex numbers (12 items: 12 accepted)

| # | Severity | Issue | Resolution |
|---|---|---|---|
| 1 | High | Regular hexagon written incorrectly: in 2025F-Q7, z₀ is at the origin, the hexagon is not centred at O, and the product is 6r⁵, not r⁵ | Accepted: the author recalculated (moduli in order r, √3r, 2r, √3r, r) and corrected it; the question-setting skill was corrected at the same time |
| 2 | Medium-high | 2025A-Q19(b) omits the periodic solutions n = 3,4,5 + 12k | Accepted |
| 3 | Medium | Maximum argument: sin θ = r/d does not give the argument | Accepted |
| 4 | Medium | 2020A-Q10(b) ray endpoint i lies on the locus (filled point) | Accepted |
| 5 | Low | The shortest-distance formula holds only when the point lies outside the circle | Accepted |
| 6 | Low | "Always use polar form for multiplication and division" contradicts "use the conjugate for division" | Accepted |
| 7 | Low | Mismatch between report year and content (−z comes from the 2021 report) | Accepted |
| 8 | Low | The third-quadrant example is not the report's original wording; 5π/4 cannot be written either | Accepted |
| 9 | Low | Missing citation of 2022F-Q6; sample paper not specified | Accepted |
| 10 | Low | The "CF opener / CF hard question" labels do not match the cited CA questions | Accepted |
| 11 | Low | "iⁿ has period 4" is imprecise (n·iⁿ is not periodic) | Accepted |
| 12 | Low | When θ < 0, write clockwise by \|θ\| | Accepted |

## 02 Functions and graphs (16 items: 16 accepted)

| # | Severity | Issue | Resolution |
|---|---|---|---|
| 1 | High | In the reciprocal-function table, "f → ±∞ ⇒ horizontal asymptote y = 0" is wrong: a vertical asymptote of f corresponds to the open point (b, 0) of 1/f | Accepted: split into two rows |
| 2 | Medium | The table omits "horizontal asymptote y = c → y = 1/c" | Accepted |
| 3 | Medium | "Hole to hole" holds only when b ≠ 0 | Accepted |
| 4 | Medium | 2016A-Q12(b) is \|f(x)\| = d, not f(x) = d | Accepted |
| 5 | Medium | "Flat bottom of two V-shaped lines" is described incorrectly | Accepted: changed to the flat bottom of a sum of two absolute values; the author verified a = 3, k = 2 |
| 6 | Low | The integral of the W-shaped graph is one triangle, not two | Accepted |
| 7 | Medium | The sign of the inverse function should be determined by ran f⁻¹ = dom f | Accepted |
| 8 | Medium | When a square root is in the denominator, it must be > 0 (2025F-Q2(a)) | Accepted |
| 9 | Medium | "c > 0 guarantees no zeros" is not enough; a and c must have the same sign | Accepted |
| 10 | Low | "Turning point (if the question requires it)": 2017F-Q5 awarded marks even though it was not required | Accepted |
| 11 | Low (doubtful) | The invented example "c = 2 touches the x-axis" conflicts with the meaning of c in the actual exam question | Accepted: replaced with the original wording from the exam question |
| 12 | Low | "Most stable across the whole course" is an overgeneralisation (in 2018 it was instead listed as well answered) | Accepted |
| 13 | Low | "Do not use it" omits the 2019 report | Accepted |
| 14 | Low | The example ln\|x − 3\| does not come from the 2022 report | Accepted |
| 15 | Low | Missing citations for 2016F-Q8(b), 2022F-Q2(a) | Accepted |
| 16 | Low | "Intersection point unchanged" is vague wording | Accepted |

## 03 3D vectors and systems of linear equations (13 items: 13 accepted)

| # | Severity | Issue | Resolution |
|---|---|---|---|
| 1 | High | Laser reflection direction written incorrectly: adding in the S→B direction gives a vector parallel to the mirror; it should be the sum of the unit vectors B→S and B→R, or d̂_out − d̂_in ∥ n | Accepted: the author used numpy to verify d̂_out − d̂_in = (0, 0.23, 0.46) ∥ (0, 1, 2) |
| 2 | High | 2024A-Q16(c) is the shortest distance between two lines (two independent parameters); 2017A-Q14 is solving an inequality to find duration; the two were conflated | Accepted: split into two types |
| 3 | Medium | "CF is examined every year" is false (not examined in 2017 or 2019; in 2021 it was in CA) | Accepted |
| 4 | Medium | "Named five years in a row" does not match the reports; 2024 is missing | Accepted |
| 5 | Medium | "Must write in parametric form" is an overgeneralisation; the key accepts representation by a relationship between variables | Accepted |
| 6 | Medium | "Wavy lines, dot product, cross product" is not the original report wording | Accepted: marked as author's suggestion |
| 7 | Low-medium | The point-to-plane distance formula is not on the formula sheet | Accepted |
| 8 | Low | "Many people have never seen it" is an exaggerated paraphrase | Accepted |
| 9 | Low | The line-plane angle formula is missing an absolute value, and is inconsistent | Accepted |
| 10 | Low | The geometric interpretation table omits "three planes coincide"; 2021A-Q14 requires both points to be written | Accepted |
| 11 | Low | The letters a and d are each used for two different things | Accepted |
| 12 | Low | "CA final question" does not match 2018F-Q8 | Accepted |
| 13 | Low (doubtful) | Sample paper question not specified | Accepted |

## 04 Vector calculus and motion (12 items: 11 accepted, 1 partly accepted)

| # | Severity | Issue | Resolution |
|---|---|---|---|
| 1 | High | 2019A-Q13(d) is not a parabola; it is a figure-of-eight shape | Accepted |
| 2 | High | All three examples of restrictions on values do not match the key (2024A-Q18 requires x ≥ 2 and y ≥ 0) | Accepted: replaced with the original key wording |
| 3 | Medium | "One loop = 0 to 2π" is an overgeneralisation (2017A-Q15 is 6π, 2019A-Q13 is 4π) | Accepted |
| 4 | Medium | 2021A-Q19 has no wind and no launch angle, but has lift | Accepted: split into two models |
| 5 | Medium | "Uniform velocity" should be "constant speed" | Accepted |
| 6 | Medium | The descent angle 90° − φ gives a negative value (φ = 143.3°) | Accepted: changed to \|90° − φ\|; the author verified 53.3° |
| 7 | Low | "Three marking points" is an overgeneralisation | Accepted |
| 8 | Low | Height is relative to the centre; 100 m above the ground corresponds to y = 20 | Accepted |
| 9 | Low | The order of subtraction has no source or rule given | Accepted |
| 10 | Low | In 2024A-Q16(c), both speed and departure time can be adjusted | Accepted |
| 11 | Low | Eliminating the parameter omits the type "x is linear in t" (named in the 2018 report) | Accepted |
| 12 | Low (doubtful) | SHM in 2019A-Q18(d) is not mentioned | Partly accepted: added a cross-reference; the method is in the differential equations handout |

## 05 Integration techniques and applications (11 items: 11 accepted)

| # | Severity | Issue | Resolution |
|---|---|---|---|
| 1 | Medium | "Irreducible quadratic" was paired with the reducible x² + 3x + 1 (discriminant 5 > 0) | Accepted: replaced with x² + 2; a separate note was added for 2022F-Q4 |
| 2 | Medium | The error example from the 2021 report is paraphrased incorrectly (the original is √(2 − sin²θ) ≠ √2 − sin θ) | Accepted |
| 3 | Medium | "Substitution is CF every year" is false (not examined in 2022), and there are 7-mark questions | Accepted |
| 4 | Medium | "Partial fractions are examined every year" is false (not examined in 2017 or 2023) | Accepted |
| 5 | Medium | 2023A-Q17(c) is an increment formula question; 2022A-Q17 does not use dV/dh | Accepted: split and rewritten |
| 6 | Medium | "The absolute value gets 1 mark on its own" is false; the absolute value is included in the antiderivative mark | Accepted |
| 7 | Low | The "correct notation" mark is awarded together with the limits; the area expression does not need π | Accepted |
| 8 | Low | 2016A-Q9 is an indefinite integral; in 2021F-Q3 the substitution must be chosen | Accepted |
| 9 | Low | 3 questions were not classified | Accepted |
| 10 | Low | The 4 in the cardioid comes from multiplying two parts | Accepted |
| 11 | Low | The 2024 report says the numerator after finding a common denominator was written incorrectly, not that comparing coefficients was wrong | Accepted |

## 06 Rates of Change and Differential Equations (15 items: 15 adopted)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | Medium | The key's main solution for 2017A-Q17(b) is counting periods, not ∫\|v\| | Adopted |
| 2 | High | The inflection point in 2025A-Q16 is at the maximum slope (3, −1), not where the slope is 0 | Adopted |
| 3 | Medium | "10% growth per year" should be an instantaneous growth rate (dP/dt = 0.1P); otherwise the answer changes from 333 to about 412 | Adopted: editor verified both results |
| 4 | Low | x(0) in 2025A-Q15 is −1 | Adopted |
| 5 | Medium | The letter k refers to carrying capacity and the proportionality constant in different questions, and is easily confused | Adopted |
| 6 | Low | "Initial value above k/2 is concave down throughout" needs P₀ < k added | Adopted |
| 7 | Low (uncertain) | SHM criterion should allow for a shifted equilibrium point a = −n²(x − c) | Adopted |
| 8 | Low | "Cannot differentiate directly with respect to t" is unclear | Adopted |
| 9 | Low | 2024A-Q12 did not give a direction; both ±A sin are awarded marks | Adopted |
| 10 | Medium | Marking-key reminder omitted 2024 (logistic), 2017 (standard equation), 2022 (absolute value) | Adopted |
| 11 | Low | The exact wording "integration statement" appears in only two years | Adopted |
| 12 | Low | 2016A-Q18 is a − bx; the two conditions come from different sources | Adopted |
| 13 | Low | "Keep only one independent variable" contradicts the shadow question; the past paper list has incorrect inclusions and omissions | Adopted |
| 14 | Low | A vertical tangent only holds when the numerator ≠ 0 | Adopted |
| 15 | Low | 2018A-Q20 is "do not" solve, not "need not" | Adopted |

## 07 Statistical Inference (16 items: 16 adopted)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | 2022A-Q12(d) is "the same sample duplicated", not two samples combined, and conflicts with the conclusion of 2019A-Q15(c) | Adopted: the two cases written separately |
| 2 | Medium (uncertain) | "key accepts both" has no basis; key only gives X̄ < T/n | Adopted; question-setting skill corrected accordingly |
| 3 | Medium | "Examined every year" is untrue (not examined in 2016, 2020) | Adopted |
| 4 | Medium | Missed the counterexample 2025A-Q13(e) (many intervals not containing μ are evidence) | Adopted |
| 5 | Low | "Citing CLT" is not a separate scoring condition in the key | Adopted |
| 6 | Low | The calculation for 304.4 with 2.326 is inconsistent (should be 304.3) | Adopted: editor recalculated |
| 7 | Low | Rounding when back-solving for n: the key accepts both 2.576 and 2.58 differences; add 2024A-Q14(f) | Adopted |
| 8 | Low | Missed the one-tailed and half-interval cases | Adopted |
| 9 | Low | 2024A-Q14(c) does not ask for n | Adopted |
| 10 | Low | "The answer does not change" only applies to 2018A-Q12(c) | Adopted |
| 11 | Low | The graphing question missed the mark for indicating the probability region | Adopted |
| 12 | Low | The key reason for 2024A-Q14(e) is different sample sizes | Adopted |
| 13 | Low | Sample paper question not explained, and sample paper A9 not cited | Adopted |
| 14 | Low | "Definitely" should be "very likely" | Adopted |
| 15 | Low | Precision table lacks context (μ = 80); s and σ used interchangeably | Adopted |
| 16 | Low | "n ≥ 30 applies" is an overgeneralisation; for a normal population any n works | Adopted |

---

**Summary (7 MAS documents)**: 95 comments in total (including 5 "uncertain"), 94 adopted, 1 partially adopted, 0 rejected. 8 high-severity items, all revised after returning to the original paper text or recalculating.


---

## Classification corrections after user feedback (2026-10-09)

- User feedback: "Vectors" contained unrelated differential equation questions. Verified true: 2017A-Q18 (carousel, cosine rule + implicit differentiation) and 2019A-Q18 (Ferris wheel, related rates + SHM proof) contain no vector content; they were originally misclassified as vector calculus under "circular motion". Removed; kept only in "Rates of Change and Differential Equations"; the corresponding section in the notes was moved across as well. Vector calculus 14 → 12 questions.
- 2021A-Q19 (ski jump) gives the position vector r(t) in the question and asks for the Cartesian path and landing angle; this is vector motion and is retained.
- Keyword review of all tags; MAS found no other misclassifications.
