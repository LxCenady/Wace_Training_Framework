# QNT · Stoichiometry and quantitative analysis 计量与定量分析 (Units 3–4; assumed Year 11 skills)

Bank: `CHE/questions.json` (entries whose tags include QNT). 44 of 150 bank questions touch QNT; QNT carries 21.9% of tagged marks, the largest share of any topic. Tags: `tools/parttags_CHE.txt`. Catalogue: `tools/catalogue_CHE.json` (QNT1–QNT8). Key PDFs: `CHE/papers/<year>_CHE_MarkingKey.pdf`.

## Scope
- Moles, mass, concentration and dilution (n = m/M; c = n/V; C₁V₁ = C₂V₂).
- Limiting reagent and theoretical yield.
- Percentage yield, purity and percentage composition.
- Titration calculations: concordant titres, average, aliquot-to-flask scaling, back titration, mass or concentration of the analyte.
- Empirical and molecular formulae from combustion or mass-composition data, using molar mass.
- Gas calculations: PV = nRT and the molar volume at standard conditions; the data booklet gives the constants and the conditions.
- Significant figures and units: required in final answers; examiners check them.
- Gravimetric analysis: precipitation, filtration, washing, drying to constant mass, weighing and calculation.

## How SCSA asks it
- Multi-step calculations in an ER context: a titration of a product, a percentage of the active ingredient, a yield from a reaction (QNT1–QNT4), often in the same question as an observation or equation.
- Empirical formula from mass data, then molecular formula with a given molar mass (QNT5); ER only.
- Gas volume or moles from PV = nRT (QNT6), often in a short SA part.
- Significant figures and units are scored in their own marks in many keys (QNT7). Expect them in every calculation.
- Gravimetric analysis is rare (QNT8, one tagged part).

## Patterns

| code | pattern (bank) | parts / questions | median marks (range) | notes |
|---|---|---|---|---|
| QNT1 | Moles, mass, concentration and dilution | 48 / 34 | 6 (2–16) | the base skill; scored as a separate step in many keys |
| QNT2 | Limiting reagent and theoretical yield | 11 / 9 | 7 (1–9) | compare mole ratios from the balanced equation |
| QNT3 | Percentage yield, purity and composition | 24 / 21 | 6 (3–16) | actual over theoretical × 100; purity or mass percentage of a component |
| QNT4 | Titration calculations | 20 / 13 | 5.5 (1–12) | discard outliers, average concordant titres, scale by the aliquot ratio |
| QNT5 | Empirical and molecular formulae | 14 / 10 | 10 (2–16) | moles from mass, smallest whole-number ratio, molar mass to molecular formula |
| QNT6 | Gas calculations | 11 / 11 | 6 (2–16) | PV = nRT; molar volume at stated conditions |
| QNT7 | Significant figures and units | 10 / 10 | 6.5 (1–9) | separate marks for units and for significant figures in the final answer |
| QNT8 | Gravimetric analysis | 1 / 1 | 6 (6–6) | precipitate mass to analyte mass by mole ratio |

## Method in brief
- **QNT1.** n = m/M; c = n/V; for a dilution, C₁V₁ = C₂V₂. Keep the unit in every line. Convert mL to L before using c in mol L⁻¹.
- **QNT2.** Moles of each reactant divided by its coefficient; the smallest is the limiting reagent. Theoretical yield from the limiting reagent's moles and the product's ratio.
- **QNT3.** Percentage yield = actual / theoretical × 100. Purity = mass of pure component / mass of sample × 100. State which mass is which.
- **QNT4.** Discard a titre that is not concordant (use the tolerance the question states, or state the rule you used), average the rest, then n(analyte) = n(titrant) × (ratio from the equation) × (flask volume / aliquot volume). A back titration uses the excess reagent first. Check the mole ratio from the equation.
- **QNT5.** Convert each element's mass to moles; divide by the smallest; multiply to get whole numbers; the empirical formula mass × n = molar mass gives the molecular formula.
- **QNT6.** PV = nRT, with SI units (Pa, m³, K). At standard conditions, the molar volume from the data booklet. Keep the temperature in K.
- **QNT7.** Final numerical answers: state units; round to the significant figures the least precise datum allows (usually two or three in these data), and say which datum fixed it.
- **QNT8.** Mass of precipitate → moles of precipitate → moles of analyte by the equation's ratio → mass of analyte. Note the filtration and drying steps if asked.

## Traps (examiners' reports and key notes)
- Numbers without labels: the examiners' reports name bare numbers, with no statement of what they represent or how they were found, as a common error. Label every number (moles of X, volume of Y).
- Units and significant figures: the reports ask for final answers in standard units and to an appropriate number of significant figures unless the question says otherwise. Students often lose these marks in an otherwise correct answer.
- Aliquot scaling: the titration result is for the aliquot, not the whole solution. Multiply by the flask volume divided by the aliquot volume.
- Mole ratio: use the balanced equation's coefficients; do not use masses or volumes as the ratio.
- Gas constant: use SI units. A pressure in kPa must be converted before PV = nRT.
- Percent composition: the mass of the component over the mass of the whole sample, not over the mass of the pure compound.
- Keys often accept alternative methods (for example percentage composition for an empirical formula) and say so; do not require one method.

## Generator notes
- Give every number with its unit and its meaning. Choose data so each step is exact or rounds cleanly.
- QNT1–QNT4 are the building blocks of the ER questions; build a multi-step ER question from two or three of these, with one observation or equation part.
- Titration data: 3–4 trials; include one non-concordant trial if the question asks the student to decide which to use (only with a stated rule; see the 2025 caveat in `SKILL.md`).
- Empirical formula questions: give masses to two decimal places and a molar mass for the molecular formula step.
- Verify: every calculation recomputed with `fractions` or `decimal` at the stated precision; sig figs of each answer checked against the least precise datum; units on each final answer; mole ratio from the equation; aliquot scaling.
