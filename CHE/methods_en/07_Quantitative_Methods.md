# 07 Stoichiometry and Quantitative Analysis Problem-solving Approach

> Based on: the pattern definitions for QNT1–QNT8 in the CHE question-type catalogue `tools/catalogue_CHE.json`; evidence notes `evidence/che/notes/QNT.txt` (per-sub-question stems, marking key lines and report notes); index `evidence/che/notes/INDEX.md` (marks and number of sub-questions); data booklet `CHE/papers/<年>_CHE_DataBooklet.pdf`. The numerical constants are the same in the 2016–2025 booklets: R = 8.314 J K⁻¹ mol⁻¹, the volume of 1.00 mol of an ideal gas at 0.0 °C and 100.0 kPa is 22.71 L, Kw = 1.00 × 10⁻¹⁴, 0.0 °C = 273.15 K (the definition of STP is only stated explicitly from 2018 onwards). The data booklet only gives the periodic table (atomic masses), not molar mass M; M must be worked out yourself or is given in the question stem.
> Past exam question numbering convention: `2016S-Q26(a)` = 2016 Short answer (S), Question 26, part (a); `2016M-Q9` = 2016 Section One multiple choice (M), Question 9; `E` = Extended answer; `2018E-Q35` has no part letter and is a whole-question label (the whole question contains marks for multiple patterns at once). The original questions and marking files are kept locally; this article only paraphrases the key's marking points and does not copy the original text.
> Review status: draft (catalogue status draft_for_review), not independently reviewed.

## First, remember: where the marking panel repeatedly deducts marks

- **Every step is marked separately**: the key awards marks line by line for n (amount of substance), stoichiometric ratio, n, m/c/V, etc.; writing only the final number rarely earns marks. Every line must show the value and unit.
- **Significant figures and units are separate marks** (Pattern 7): several keys award a separate mark for the final answer, e.g. "correct to two significant figures", "mark for 3 sig figs".
- **Calculate first, then judge**: when the question asks you to judge, compare or evaluate (Patterns 2, 3, 7), the conclusion must be supported by calculated numbers; a conclusion alone earns no marks.
- **★ marker rule**: patterns ranked in the top quarter by INDEX marks are ★; QNT has 8 patterns in total, so the top two are taken: Pattern 1 (298 marks) and Pattern 3 (151 marks).
- **Limitations of report notes**: some REPORT fields in the notes are generic sentences copied from other sub-questions (e.g. "proved to be effective in discriminating…"); this article uses only notes clearly relevant to the sub-question.

---

## Pattern 1: Amount of substance, mass, concentration conversions and dilution ★

**Identify**: The question stem contains words such as mass, molar mass, concentration, volume of solution, dilute, g L⁻¹, mol L⁻¹, tonne, or gives several of M, m, c, V and asks for another. This is the most common basic calculation in QNT, and the first few steps of combined questions on titration, yield, gases, etc. usually also belong to it.

**Steps** (write each step on a separate line, with the value and unit)
1. Write the molar mass M: if it is given in the question stem, use it as is; otherwise calculate it from the periodic table atomic masses (the data booklet does not provide M).
2. Find n: for a solid or pure substance use n = m ÷ M; for a solution use n = c × V, where V must be in L.
3. Write unit conversions separately: mL → L (÷ 1000), tonne → g (× 10⁶), mg → g (÷ 1000), kg → g (× 1000).
4. Convert to the target substance using the stoichiometric ratio from the reaction equation, e.g. n(SO₂) = 8 × n(Fe₉Ni₉S₈) (the stoichiometric ratio in 2016E-Q39(a)).
5. Dilution questions: the n of the solute is unchanged before and after dilution; use n = c × V to find the n in the original solution, then divide by the new volume to find the new concentration.
6. Finally convert to the quantity and unit required by the question (g, g L⁻¹, mol L⁻¹); for significant figures see Pattern 7.

**Marking points (typical wording in the key)**:
- Converting mass to amount of substance is marked separately, and M must be accurate (the key for 2016E-Q39(a) awards a separate mark for "accurate M and calculation").
- Volume or concentration conversion (mL → L) is marked (the line n(Na₂CO₃) = c × 0.0164 in 2016E-Q42(a)).
- The stoichiometric ratio is marked separately (the 1 : 8 ratio line in 2016E-Q39(a), the Sb₂S₃ : Sb ratio line in 2017E-Q36(a)).
- The final value and unit each earn 1 mark.

**Common errors**:
- Forgetting mL → L: the keys for 2016E-Q42(a) and 2016E-Q42(c) both write the mL → L conversion separately in n = c × V or c = n ÷ V.
- Breaking the unit chain: 2018E-Q36(c) first calculates the amount in mg (698 506 000 mg), then converts to g (698 506 g), and only then calculates n; skipping mg → g makes the later number wrong by three orders of magnitude.
- Tonne conversion: 2024E-Q40(a) first converts 2245 tonne to 2.245 × 10⁹ g, then calculates n(Ni).
- Volume after dilution: in 2016E-Q42(f), a 100 mL sample is diluted to 250 mL; the key first calculates n(H⁺) in 250 mL, then divides by the original sample's 0.100 L; omitting this step means the original sample concentration cannot be obtained.
- MC question 2016M-Q9 tests mole ratios for a polyprotic acid: each mole of a diprotic acid supplies 2 mol H⁺, so 0.5 mol neutralises 1 mol NaOH.

**Past questions**: 2016M-Q9, 2016E-Q39(a), 2016E-Q42(a), 2016E-Q42(f), 2017S-Q29(a), 2017S-Q29(b), 2017S-Q33(c), 2017E-Q36(a), 2017E-Q36(b), 2017E-Q37(b), 2017E-Q37(c), 2018S-Q29(b), 2018E-Q35, 2018E-Q36(c), 2018E-Q40(a), 2018E-Q40(c), 2019S-Q30(b), 2019S-Q32, 2019E-Q38(d), 2019E-Q39(c), 2019E-Q40(a), 2019E-Q40(b), 2019E-Q40(d), 2020E-Q39(a), 2020E-Q39(b), 2022E-Q34, 2022E-Q35(c), 2022E-Q37(f), 2022E-Q38(a), 2023E-Q35(b), 2023E-Q36(b), 2023E-Q37(a), 2023E-Q37(b), 2023E-Q38(a), 2023E-Q38(b), 2024S-Q34, 2024E-Q36(c), 2024E-Q38(a), 2024E-Q38(b), 2024E-Q40(a), 2024E-Q40(b), 2024E-Q40(c), 2025E-Q35(d), 2025E-Q36(a), 2025E-Q36(b), 2025E-Q37(a), 2025E-Q38(d), 2025E-Q39, 2025E-Q40(d)

---

## Pattern 2: Limiting reagent and theoretical yield

**Identify**: The question stem contains words such as limiting reagent, in excess, sufficient, enough, would … dissolve completely, remaining, or asks you to judge whether the reagent added is sufficient.

**Steps**
1. Write the balanced reaction equation and read off the stoichiometric ratio (H⁺ : OH⁻ = 1 : 1; each mole of Ca(OH)₂ or Ba(OH)₂ provides 2 mol OH⁻).
2. Calculate n for each of the two reactants separately, writing each on its own line.
3. Compare: use the stoichiometric ratio to convert the n of one reactant to the amount needed of the other, or compare n ÷ stoichiometric coefficient; the smaller ratio is the limiting reagent.
4. Write the reason for the judgement (state which substance has the smaller n or ratio, and explain that it determines the upper limit of the reaction).
5. Calculate the product or remaining amount from the limiting reagent: remaining amount = initial n − n reacted; when finding concentration, use the total volume after mixing.

**Marking points (typical wording in the key)**:
- The equation or stoichiometric ratio is worth 1 mark on its own (2017S-Q29(a) requires the stoichiometric ratio to be written).
- The two n values are 1 mark each.
- The judgement conclusion and reason are marked: the key requires the conclusion to include an explanatory statement; a conclusion alone earns no marks; the limiting judgement in 2024E-Q40(c) (comparing the two n values and giving a reason) is worth 1–3 marks, with the rest for calculating n and the amount of substance of NO.
- The remaining amount or follow-on quantity (2017S-Q29(b) 3 marks: remaining n, total volume and concentration are 1 mark each).
- Sufficiency judgement (2019E-Q40(b), 2020E-Q39(c)): write the "required n" and the "added n" side by side, then compare.

**Common errors**:
- Forgetting that Ca(OH)₂ or Ba(OH)₂ contains two OH⁻: the keys for 2019S-Q32 and 2024S-Q34 both write n(OH⁻) = 2 × c × V.
- Comparing the wrong direction: 2021E-Q37(c) should compare the required Mn (= ½ × n(LiCoO₂)) with the actual Mn, not compare the masses of LiCoO₂ and Mn.
- Denominator for the remaining concentration: 2017S-Q29(b) uses the total volume after mixing, 0.0445 L, not the volume of one of the solutions.
- Limiting reagent and remaining species in neutralisation questions: 2019S-Q32 first determines that H⁺ is limiting, then uses the remaining OH⁻ to find the pH (12.1).
- 2023E-Q38(a): the key uses the 1 : 2 : 1 stoichiometric ratio to determine that Cl₂ is limiting and the other two reactants are in excess, then uses n(Fe(OH)₃) = 2 × n(Cl₂) to find the yield.
- 2018E-Q37(d) is a conceptual question: hydrochloric acid is in excess to make all the Ga₂O₃ react and increase the yield; no calculation is needed.

**Past questions**: 2017S-Q29(a), 2017S-Q29(b), 2018E-Q37(d), 2019S-Q32, 2019E-Q40(a), 2019E-Q40(b), 2020E-Q39(c), 2021E-Q37(c), 2023E-Q38(a), 2024S-Q34, 2024E-Q40(c)

## Pattern 3: Yield, purity and percentage content ★

**Identify**: The question stem contains percentage yield, efficiency, purity, % by mass, impure, contains x% by mass, assuming the reactions go to completion, or gives the "efficiency/yield of a step".

**Steps**
1. First calculate the theoretical amount: n or m for complete reaction, converted using the stoichiometric ratio.
2. When the actual amount is given: percentage yield = actual yield ÷ theoretical yield × 100%.
3. When efficiency e% is given: if the amount of reactant required is asked for, then reactant amount = theoretical amount required × 100 ÷ e; if the actual amount obtained is known, then theoretical amount = actual amount × 100 ÷ e. The direction is determined by the question; do not mechanically multiply by e%.
4. Purity or mass fraction: mass of pure substance ÷ mass of sample × 100%; when the sample mass is not consistent with the amount specified in the question (whole tablet, whole bottle, 250 mL solution), convert using the scale factor.
5. If the question requires judging whether a statement is true, write the calculated value, comparison basis and conclusion (for format, see Pattern 7).

**Marking points (typical wording in the key)**:
- Theoretical amount (n or m) 1 mark.
- Efficiency or yield conversion 1 mark (the key for 2022E-Q35(c) uses 100 ÷ 89.5 to reflect the efficiency).
- Purity or content 1 mark (the keys for 2018E-Q40(c) and 2020E-Q37(c) both first calculate the pure substance in the sample, then convert to a percentage).
- Final answer with units 1 mark.
- Examples: 2018E-Q40(a) 4 marks, n(aspirin) = n(salicylic acid) → theoretical mass → 85.5%; 2024E-Q40(b) 4 marks, theoretical n(Ni(CO)₄) = n(Ni) → 67.6%; 2025E-Q35(d) 6 marks, deduce carboxylate from calcium ion loss, then calculate 7.32%.

**Common errors**:
- Efficiency direction reversed: 2022E-Q35(c) asks "how much iron oxide is needed", and the key uses ÷ 0.895 (i.e. × 100/89.5), not × 0.895.
- Sample and solution volume mismatch: in 2018E-Q40(c), a 3.55 g sample is made up to 250 mL, and 20.00 mL is titrated, so the scale factor is 250 ÷ 20; in 2020E-Q37(c), it is made up to 250.0 mL and 10.00 mL is taken, so scale by 25.
- Purity basis: 2024E-Q40(a) first calculates the pure Ni mass from 95.7% purity, then converts to NiO; 2245 tonne cannot be treated directly as pure Ni.
- Wrong percentage denominator: the denominator in 2024E-Q40(b) is the theoretical yield (1.516 × 10⁹ g), not the actual yield.
- Claim true/false question (2022S-Q31(b)): the key first calculates the "water that should be absorbed" (3.97 g × 180 = 715 g), then multiplies by 97.4% to get 696 g, compares this with the measured 691 g, and concludes claim not true; the two numbers compared must be on the same basis.

**Past questions**: 2016E-Q39(a), 2017S-Q33(c), 2017E-Q36(a), 2017E-Q37(c), 2018E-Q35, 2018E-Q40(a), 2018E-Q40(c), 2019S-Q30(b), 2019E-Q38(d), 2019E-Q40(d), 2020E-Q37(c), 2020E-Q39(b), 2021E-Q37(d), 2022S-Q31(b), 2022E-Q34, 2022E-Q35(c), 2022E-Q37(f), 2023E-Q35(b), 2024E-Q40(a), 2024E-Q40(b), 2024E-Q40(c), 2025E-Q35(d), 2025E-Q37(a), 2025E-Q40(d)

---

## Pattern 4: Titration calculations

**Identify**: The question stem contains titration, titre, burette readings, aliquot, average titre, standardised, back titration, neutralise, indicator, or gives titration data to find concentration, mass or percentage content.

**Steps**
1. Calculate the titre from the readings: titre = final reading − initial reading, list row by row.
2. Judge consistency: the usual criterion for concordant titres is a difference of no more than 0.10 mL; remove clearly deviating outliers (rough, incorrect endpoint judgement), then take the arithmetic mean, keeping to 0.01 mL.
3. Write the stoichiometric ratio for the titration reaction (HCl : NaOH = 1 : 1; Na₂CO₃ : HCl = 1 : 2; H₃PO₄ : NaOH = 1 : 3; nicotine : CH₃COOH = 1 : 2, etc.).
4. n(standard solution) = c × V, with V in L, using the average volume.
5. n(unknown aliquot) = n(standard solution) × stoichiometric ratio.
6. Scale up to the original solution or original sample: × (total volume ÷ volume taken), e.g. 250.0 ÷ 25.00 = 10.
7. Convert to the concentration, mass or percentage content required by the question.
8. Back titration: first calculate the total n of excess reagent added, then titrate the remaining amount with standard solution, n(reacted) = n(total) − n(remaining).

**Marking points (typical wording in the key)**:
- Average titre 1 mark or 2 marks (outliers must be removed; the key for 2024E-Q36(b) notes: completing the table only earns at most 1 mark, and an average that includes the outlier earns only partial marks).
- n(standard solution) 1 mark.
- Stoichiometric ratio 1 mark.
- Scale factor 1 mark.
- Final concentration, mass or percentage content and units 1 mark.

**Common errors**:
- Outlier handling: the key for 2025E-Q38(d) removes 18.85 mL and takes the average of 17.42, 17.59 and 17.55, which is 17.52 mL; these three values differ by 0.17 mL, exceeding the usual 0.10 mL reference criterion (the key itself also does not fully satisfy this criterion, so follow the key's method). Students should state the reason for removal; they cannot just write "take the average".
- 2020E-Q37(a): the rough value 21.10 mL is not included in the average; 19.40 mL deviates from the others by about 0.7 mL; the key takes the average of 20.05, 20.15 and 20.10, which is 20.10 mL.
- 2020E-Q37(c): the key's main method is 3 NaOH : 1 H₃PO₄, giving 19.1% (3 significant figures); a note gives another method using 2 : 1, giving 28.7%, and states that this treatment is beyond the course requirements and students do not need to know it.
- 2019E-Q39(a): the readings in the key's sample table are 19.47, 19.44, 20.34 and 19.39 mL. 20.34 mL deviates the most; the key's average 0.01943 L (19.43 mL) is consistent with the average of the three values after removing 20.34.
- 2024E-Q36(b): including the outlier in the average gives 13.81 mL (the key's "includes outlier" row); after removing it, the average is 13.74 mL; including the outlier earns only partial marks.
- 2016E-Q42(f) working back to the original sample: two scale-ups for dilution and sampling, n(H⁺) × 10, then divide by the original sample volume 0.100 L.
- Back titration (2024E-Q36(c)): n(OH⁻) reacted = n(OH⁻) added − n(H⁺) titrated; both n values must be shown. In this question, the total n for 5 tablets must be divided by 5 to obtain the n for one tablet (see Pattern 1 for unit and ratio conversions).
- **Known issue with the official key (2024E-Q36(c))**: the main text of the key calculates using OH⁻ : aspirin = 1 : 1, giving 305 mg/tablet; the key's note says "if a 2:1 ratio is used, m = 152 mg". The two results differ by a factor of two, so the key is internally inconsistent. Aspirin contains one carboxyl group; if OH⁻ consumed by hydrolysis of the ester group is also included, the ratio may be 2 : 1. When answering, students should state the stoichiometric ratio used and the basis for it.
- MC question 2018M-Q13 asks which titre to use: discard clearly anomalous readings (such as 19.23 mL) before averaging, rather than averaging all of them.

**Past questions**: 2016E-Q42(a), 2016E-Q42(c), 2016E-Q42(e), 2016E-Q42(f), 2017E-Q37(c), 2018M-Q13, 2018E-Q40(c), 2019E-Q39(a), 2019E-Q39(c), 2020E-Q37(a), 2020E-Q37(b), 2020E-Q37(c), 2021E-Q35(c), 2021E-Q36(a), 2022E-Q34, 2022E-Q38(a), 2023E-Q36(b), 2024E-Q36(b), 2024E-Q36(c), 2024E-Q38(b), 2025E-Q38(d)

---

## Pattern 5: Empirical and Molecular Formulas

**Identify**: The question contains empirical formula, molecular formula, combusted, produced … of carbon dioxide and water, % by mass, molar mass, determine the formula.

**Steps** (one line per element, the last line being the ratio)
1. C: n(C) = n(CO₂) = m(CO₂) ÷ 44.01; m(C) = n × 12.01.
2. H: n(H) = 2 × n(H₂O); m(H) = n × 1.008.
3. N: n(N) from the n(H⁺) of the acid used in the neutralisation (e.g. n(N) = n(H⁺) in 2024E-Q38(a)), or from the mass of NO₂ (2016E-Q38(c) uses NO₂, M = 46.01).
4. S and halogens: S from n(H₂SO₄) (2020E-Q38(a)); halogens converted from the precipitate mass (e.g. n(I) = 2 × n(PbI₂), 2018E-Q35).
5. O: if the sample mass is known, O is found by difference: m(O) = sample mass − Σ m(other elements), then n(O) = m ÷ 16.00.
6. Ratio: each n ÷ the smallest n. If this gives half-integers such as 1.5 or 2.5, multiply by 2 to make them whole numbers (2024E-Q38(a): the O ratio is 2.5, and after multiplying by 2 the result is C₂₁H₂₈N₂O₅).
7. Molecular formula: from n(sample) = PV ÷ RT (kPa, L, K) get M = m ÷ n; then find the whole-number multiple M ÷ empirical formula mass, and multiply the empirical formula by it (2017E-Q38(c), 2021E-Q36(b)).

**Scoring points (typical key wording)**:
- Each element's n or m is marked separately (the 9-mark key for 2016E-Q38(c) awards marks element by element).
- Ratio and empirical formula 1–2 marks (the "Mole ratio" line and the final empirical formula in 2021E-Q36(a)).
- The multiplier relationship for the molecular formula (the "MFM / EFM × EF" line in 2017E-Q38(c)).

**Common errors**:
- Not multiplying by 2 when the ratio is a half-integer: in 2024E-Q38(a), both 10.5 and 2.5 must be multiplied by 2.
- Forgetting to × 2 for H: n(H) = 2 × n(H₂O); the key for 2016E-Q38(c) lists this line separately.
- Source of nitrogen: 2016E-Q38(c) gets n(N) from NO₂, 2021E-Q36(a) gets n(N) from the back-titration of ammonia; the two must not be mixed up.
- Units in the difference method: when the O in the sample is found by difference, all masses must be converted to g.
- Rounding the ratio: the ratio in 2022E-Q34 (e.g. 4.25 ÷ 0.328 ≈ 13) is a near-integer result, so state why it is rounded.
- Multiplier for the molecular formula: 2017E-Q38(b) gives M ≈ 194 g mol⁻¹, about 2 times the empirical formula mass of 97.1; the key for 2017E-Q38(c) uses this to write the molecular formula, so the multiplier must be stated explicitly.

**Past questions**: 2016E-Q38(c), 2017E-Q38(a), 2017E-Q38(c), 2018E-Q35, 2019S-Q30(b), 2020E-Q38(a), 2020E-Q38(b), 2021E-Q36(a), 2021E-Q36(b), 2022E-Q34, 2023E-Q37(a), 2023E-Q37(b), 2024E-Q38(a), 2025E-Q39

---

## Pattern 6: Gas Calculations

**Identify**: The question contains gas, vapourised, occupy … L, at … kPa and … °C, STP, volume of … at … °C and … kPa, or uses gas data to find the molar mass of a volatile compound.

**Steps**
1. Convert to consistent units: pressure in kPa; volume in L (mL ÷ 1000); temperature in K, K = °C + 273.15 (16.0 °C is 289.15 K).
2. Non-standard conditions: n = PV ÷ RT, R = 8.314 (kPa · L · K⁻¹ · mol⁻¹, equivalent to the J K⁻¹ mol⁻¹ in the data booklet).
3. Standard conditions (STP, 0.0 °C, 100.0 kPa): n = V ÷ 22.71. The data booklet's STP pressure is 100.0 kPa, not 101.3 kPa.
4. Use n to find the required quantity: V = nRT ÷ P (2016E-Q39(a)), M = m ÷ n (2017E-Q38(b)), or to find the molecular formula (2021E-Q36(b)).
5. Round to significant figures as in Pattern 7.

**Scoring points (typical key wording)**: Correct temperature conversion (K); expression and value for n; final volume, molar mass or molecular formula with units. When combined with other patterns, each step is marked separately: in the 7 marks for 2016E-Q39(a), the ideal gas equation and the temperature conversion each have their own line.

**Common errors**:
- Not converting °C: the key for 2016E-Q39(a) explicitly includes the temperature conversion in the marks (300.0 °C → 573.15 K).
- Treating STP at 100 kPa as 101.3 kPa: 22.71 L is the molar volume at 100.0 kPa and 0.0 °C.
- Volume units: the 100.0 mL in 2017E-Q38(b) must first be converted to 0.100 L.
- 2024E-Q40(c): volume of NO = n(NO) × 22.71 = 2.57 L; n(NO) must first be found from the limiting HNO₃ (links with Pattern 2).
- 2023E-Q37(b): 150 °C converts to 423.15 K, n = (1.42 × 205) ÷ (8.314 × 423.15).
- 2020E-Q38(b): 637 mL converts to 0.637 L, 40 °C converts to 313.15 K, key gives n = 0.0367 mol.

**Past questions**: 2016E-Q39(a), 2016E-Q42(g), 2017E-Q36(b), 2017E-Q38(b), 2018E-Q35, 2020E-Q38(b), 2021E-Q36(b), 2023E-Q35(b), 2023E-Q37(b), 2024E-Q40(c), 2025E-Q39

---

## Pattern 7: Significant Figures and Units

**Identify**: The question contains appropriate number of significant figures, correct to …, give your answer to …, express in g L⁻¹, reading to the appropriate accuracy, to 2 decimal places.

**Steps**
1. Find the data in the question with the fewest significant figures (e.g. 2.2 tonne is 2 s.f., 5.0 L is 2 s.f., 105 kPa is 3 s.f.). If the question specifies otherwise, follow the question.
2. Keep intermediate results to 3 or more significant figures, without rounding; only round the final answer.
3. Compare with the way the key rounds (keys for the same pattern are not fully consistent): 2016E-Q39(a) uses 2 s.f. (2.8 × 10⁵ L); 2017E-Q36(b) uses 3 s.f. (4.67 × 10⁶ L); 2019E-Q40(a) uses 2 s.f. (1.4 g L⁻¹, the key notes two significant figures); 2020E-Q37(c) uses 3 s.f. (19.1%); 2021E-Q37(d) uses 3 s.f. (6.74%); 2022E-Q35(c) uses 3 s.f. (1.07 × 10⁶ g); 2023E-Q35(b) uses 4 s.f. (7.621 × 10⁸ L); 2018E-Q36(c) requires 4 s.f. (6.792 × 10⁵ g, the data 0.5310 and 0.09100 being 4 s.f.).
4. Readings: instrument readings must be given to a reasonable precision (2017S-Q34(ci): the voltmeter reading must be kept to two decimal places, about 1.09 V).
5. Units: write the unit after the value, converted to the unit the question requires (g, g L⁻¹, mol L⁻¹, L, kPa); percentages are written with %.
6. pH: write the decimal places as in the key (2019S-Q32 gives 12.1, 2024S-Q34 gives 12.9, 2016E-Q42(f) gives 5.20). Keys are not consistent, so follow the question and the reporting requirements.

**Scoring points (typical key wording)**: Significant figures are marked separately for 1 mark (2016E-Q39(a), 2017E-Q36(b), 2018E-Q36(c) and 2022E-Q35(c) each have a separate line); correct units (e.g. g L⁻¹, 2019E-Q40(a)).

**Common errors**:
- Rounding too early: in 2016E-Q42(f), the pH from 6.30 × 10⁻⁶ is 5.20; if [H⁺] is first rounded to 6.3 × 10⁻⁶ (two s.f.), the last digit is affected.
- Significant figures not matching the data: writing the voltage reading as 1.1 V does not meet the two-decimal-place requirement (2017S-Q34(ci)).
- Unit chain: mixing tonne, kg, g and mg gives a wrong value, and even correct significant figures won't earn the marks (2018E-Q36(c)).
- Rounding requirements are not consistent: different keys round differently, so answer according to what the question explicitly requires.

**Past questions**: 2016E-Q39(a), 2017S-Q34(c)(i), 2017E-Q36(b), 2018E-Q36(c), 2019E-Q40(a), 2020E-Q37(c), 2021E-Q37(d), 2022E-Q35(c), 2023E-Q35(b), 2025E-Q37(a)

---

## Pattern 8: Gravimetric Analysis by Precipitation

**Identify**: The question contains precipitate, filter, wash, dry, weigh, gravimetric, excess silver nitrate (or another precipitating agent), and asks you to determine the mass of an ion by weighing the precipitate.

**Steps** (in the key's order)
1. Add excess precipitating agent (e.g. AgNO₃) so the ion being tested (Cl⁻) precipitates completely.
2. Filter to separate the precipitate.
3. Wash the precipitate to remove soluble impurities.
4. Dry the precipitate to constant mass.
5. Weigh the precipitate and convert its mass to the mass of the ion being tested (n(AgCl) = n(Cl⁻)).
6. Write the precipitation equation: Ag⁺(aq) + Cl⁻(aq) → AgCl(s).

**Scoring points (typical key wording)**: 2019S-Q30(a) is worth 6 marks in total, including the description of adding excess precipitating agent (1–2 marks), 1 mark each for filtering, washing, drying and weighing, and 1 mark for the precipitation equation.

**Common errors**: Not writing "excess"; only writing weigh without drying to constant mass; omitting the equation; treating the precipitate mass directly as the mass of the ion being tested.
(Evidence note: only 1 sub-question in this pattern, so the evidence base is weak.)

**Past questions**: 2019S-Q30(a)
