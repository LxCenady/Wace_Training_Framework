# 03 Redox and Electrochemistry Problem-solving Approach

> Based on: `evidence/che/notes/RX.txt` (RX1–RX8, 91 sub-question annotations in total, listing the question stem, key and exam report for each sub-question), `tools/parttags_CHE.txt` (sub-question tags), `tools/catalogue_CHE.json` (pattern definitions), `evidence/che/notes/INDEX.md` (mark statistics). Resources available to students are taken from `CHE/papers/2025_CHE_DataBooklet.pdf`, with the 2016, 2019, 2022 and 2024 versions of the data booklet also spot-checked.
> Past-paper numbering format: `2024S-Q33(b)` = Question 33(b) in the 2024 Section Two (short answer); `2025E-Q40(a)` = Section Three (extended answer). `S` and `E` indicate paper type only.
> ★ markers: ranked by INDEX mark value, the top approximately one quarter are selected (for this topic's 8 patterns, the top 2): RX2 (80 marks), RX3 (51 marks).
> Review status: independent review completed (checked against past papers, key and exam reports); record at `CHE/methods/审校记录.md`.

## First, remember: where markers repeatedly deduct marks

- **Half-reactions must get both “correct species” and “correct balancing”**: the key marks each half-reaction separately (1 mark for correct species, 1 mark for correct balancing).
- **The overall reaction must actually cancel electrons**: add the two half-reactions only after their electron numbers are equal (written as “× 2” in the 2017S-Q27 key).
- **Observations must include colour and state**: the keys for 2020S-Q27, 2023S-Q30, 2024S-Q27 and similar questions all require the initial and final colours as well as the states of gases and solids.
- **Electrode names and electron flow**: the anode, cathode, positive and negative electrodes, and the directions of electron and ion flow must all be stated clearly (the 2019S-Q31(a) key requires both ion migration directions to be marked).
- **Exam report comments on this topic**: the 2021 report said the iron corrosion question (2021S-Q31) “answered well, with a mean of 70.4%”, placing it in a stable scoring range; the 2023 report said Question 37 (including the ionic equation in 2023E-Q37(e)(i)) “answered well in this section”. Both report comments are whole-section overviews; the evidence contains no finer pattern-level evaluation.

## What the data booklet provides (resources available to students in the exam)

- **Standard electrode potential table** (Standard Reduction Potentials at 25 °C, data booklet p. 8): gives a series of reduction half-reactions and their E° (starting with F₂ at +2.89 V, arranged in decreasing numerical order down to the half-reaction for K⁺). Students need to select two half-reactions from it.
- Colour table: Cu(s) is salmon pink, Cu²⁺ blue, Fe²⁺ pale green, Fe³⁺ pale brown, Cr³⁺ dark green, MnO₄⁻ purple, Cr₂O₇²⁻ orange, CrO₄²⁻ yellow, Cl₂(g) greenish-yellow, Br₂(ℓ) red, I₂(s) grey, I₂(g) purple; NO₂(g) is brown. The data booklet does not list the colours of Br₂(aq) or I₂(aq); for orange and brown in aqueous solution, follow the key (e.g. 2023S-Q30(c), 2024S-Q27(b)).
- Solubility rules: used to determine precipitates (e.g. Ag⁺ + Cl⁻ → AgCl(s)).
- The data booklet **does not** contain diagrams of electrolysis or cells; apparatus diagrams are usually given in the question stem.
- This time, only the E° table in the 2025 version was checked item by item (it includes half-reactions for metals such as Cr, Mg, Zn, Fe, Cu, Pb, Al and Li); other versions were only spot-checked for Kw and Ka.

---

## Pattern 1: Oxidation numbers and oxidising/reducing agents

**Identify**: “What is the oxidation number of … in …” “identify the atom that is oxidised and the atom that is reduced” “identify the species increasing in oxidation number” “use oxidation numbers to show that this is a redox reaction” “complete the table …”.

**Steps**
1. Apply oxidation number rules: elements in their elemental form are 0; a monatomic ion equals its charge; in compounds H is usually +1 and O is usually −2 (O is −1 in H₂O₂); the sum of the oxidation numbers of all atoms in a compound equals the overall charge.
2. First calculate the oxidation number of the atom asked for (not the whole compound) before and after the reaction. For example, Cl is +1 in Ca(OCl)₂ and −1 in HCl (2019S-Q28(a)).
3. Oxidation number increases → oxidised → the substance is the reducing agent; oxidation number decreases → reduced → the substance is the oxidising agent.
4. Write in a table or one sentence: which atom is oxidised, which atom is reduced, which species is the oxidising agent and which species is the reducing agent.

**Mark-earning points (typical wording in the key)**:
✓ 2019S-Q28(a) (2 marks): Cl is +1 in Ca(OCl)₂; Cl is −1 in HCl.
✓ 2020S-Q30(a) (2 marks): the atom oxidised is S; the atom reduced is H.
✓ 2021S-Q31(b) (2 marks): the oxidation number of Fe increases from +2 to +3; the oxidation number of O decreases from 0 to −2.
✓ 2024S-Q33(a) (3 marks): the species that increases in oxidation number (sulfur in SO₂); the species with the highest oxidation number (sulfur in SO₄²⁻); the oxidising agent (chlorine in ClO₃⁻).
✓ 2025E-Q40(b) (3 marks): the initial and final oxidation number of Se in each step, and whether that step is oxidation or reduction (e.g. −2 → +6, oxidation).

**Common errors (exam reports)**: The exam reports have no specific comment on this pattern. The following common errors are summarised from the key:
- Writing the compound instead of the atom asked for in the question.
- Writing O in H₂O₂ as −2, or omitting the sign of the oxidation number (+1 and −1 must be written).
- Confusing “the substance oxidised” with “the reducing agent” (the reducing agent is oxidised).
- 2021S-Q31(b) asks “show that this reaction is a redox reaction”; you must write the oxidation number changes for both atoms; writing only one cannot earn full marks.

**Past-paper questions**: 2019S-Q28(a), 2020S-Q30(a), 2021S-Q31(b), 2024S-Q33(a), 2025E-Q38(c)(ii), 2025E-Q40(b), 2019S-Q28(b)

---

## Pattern 2: Half-equations and balancing redox equations ★

**Identification**: “Write balanced half-equations for the oxidation and reduction reactions and a balanced overall redox equation” “state symbols are not required” “Write the balanced equation for the reaction …”. Common contexts: oxidation of alcohols or aldehydes by MnO₄⁻ or Cr₂O₇²⁻; halogens with SO₂; lactate ions with sulfate (2025S-Q33); fuel cell reactions; electrode reactions in electrorefining.

**Steps**
1. Mark the changes in oxidation number, identify the atoms oxidised and reduced, and write the reactants and products for the two half-reactions (correct species).
2. Balance the half-reactions:
   - first balance all atoms except O and H;
   - balance O with H₂O;
   - balance H with H⁺ (acidic conditions); if the question specifies basic conditions, use OH⁻ and H₂O;
   - balance charge with e⁻.
3. Make the number of electrons equal in the two half-reactions (multiply by coefficients), then add them.
4. Cancel common e⁻, H₂O, H⁺ (or OH⁻) on both sides, and check conservation of atoms and charge.
5. When the question specifies “acidic conditions”, OH⁻ must not appear in the overall reaction.

**Marking points (typical key wording)**:
✓ 2024S-Q33(b) (5 marks): reduction half-reaction MnO₄⁻(aq) + 8H⁺(aq) + 5e⁻ → Mn²⁺(aq) + 4H₂O(ℓ) (1 mark each for species and balancing); oxidation half-reaction CH₃OH(ℓ) + H₂O(ℓ) → HCOOH(aq) + 4H⁺(aq) + 4e⁻ (1 mark each for species and balancing); overall reaction 5CH₃OH(ℓ) + 4MnO₄⁻(aq) + 12H⁺(aq) → 5HCOOH(aq) + 4Mn²⁺(aq) + 11H₂O(ℓ) (1 mark each for species and balancing).
✓ 2025S-Q33 (6 marks): lactate oxidation half-reaction C₃H₅O₃⁻ + 2H₂O → C₂H₃O₂⁻ + HCO₃⁻ + 5H⁺ + 4e⁻ (correct after multiplying by 2); sulfate reduction half-reaction SO₄²⁻ + 10H⁺ + 8e⁻ → H₂S + 4H₂O; overall reaction 2C₃H₅O₃⁻ + SO₄²⁻ → 2C₂H₃O₂⁻ + 2HCO₃⁻ + H₂S.
✓ 2017S-Q27 (6 marks): oxidation half-reaction SCN⁻ + 4H₂O → SO₄²⁻ + HCN + 7H⁺ + 6e⁻; reduction half-reaction 4e⁻ + IO₃⁻ + 6H⁺ + Cl⁻ → ICl + 3H₂O; overall reaction (the key allows working to be omitted, but in the example the half-reactions must first be multiplied by coefficients ×2 and ×3 before adding).
✓ 2016S-Q27(b) (3 marks): organic product pentanoic acid (1 mark) and the balanced ionic equation (2 marks): Cr₂O₇²⁻ + 3C₅H₁₀O + 8H⁺ → 2Cr³⁺ + 3C₅H₁₀O₂ + 4H₂O.
✓ 2021S-Q31(a) (4 marks): oxidation half-reaction Fe(s) → Fe²⁺(aq) + 2e⁻; reduction half-reaction O₂(g) + 4H⁺(aq) + 4e⁻ → 2H₂O(ℓ); overall reaction 2Fe(s) + O₂(g) + 4H⁺(aq) → 2Fe²⁺(aq) + 2H₂O(ℓ).
✓ 2024E-Q39(d) (2 marks): anode Pb → Pb²⁺ + 2e⁻; cathode Cr³⁺ + 3e⁻ → Cr.

**Common errors (examiner reports)**: The 2023 report said Question 37 “was answered well in this section”, which included the ionic equation in 2023E-Q37(e)(i) (RX2 and ORG6, 3 marks). The following common errors are summarised from the key:
- Adding the two half-reactions directly when the numbers of electrons are unequal (coefficients must be multiplied first, e.g. “× 2” in 2017S-Q27).
- Using OH⁻ under acidic conditions, or placing H₂O and H⁺ incorrectly in a half-reaction.
- Writing electrons on the wrong side (e⁻ on the product side for an oxidation half-reaction and on the reactant side for a reduction half-reaction).
- Omitting the cancellation of H⁺ or H₂O in the overall reaction, leading to inconsistent species.
- The key for 2021S-Q31(a) accepts both overall reaction forms (H⁺ form and OH⁻/H₂O form); this must be consistent with the half-reactions written, and H⁺ cannot be used for one half and OH⁻ for the other.
- The key for 2019E-Q40 is marked as 22 marks, consistent with the sub-question marks in the question stem (a 9, b 4, c 3, d 6, total 22). 2019E-Q40(c) is a sub-question of this pattern (overall equation for the oxidation of Fe²⁺ by H₂O₂, 3 marks: 1 mark each for reactants, products and balancing).

**Past exam questions**: 2016E-Q40(a), 2016E-Q40(b), 2016S-Q27(b), 2017S-Q26(a)(ii), 2017S-Q27, 2017S-Q34(a), 2018S-Q28(a), 2018S-Q28(b), 2018S-Q30(d), 2019E-Q40(c), 2019S-Q28(b), 2020E-Q36(c), 2021S-Q27(b), 2021S-Q30(b), 2021S-Q31(a), 2022E-Q37(a), 2023E-Q37(e)(i), 2024E-Q39(d), 2024S-Q33(b), 2025E-Q40(c), 2025S-Q33

---

## Pattern 3: Redox reaction equations and observations ★

**Identification**: “Write balanced equations for any reactions occurring between the following substances and describe the observation(s)” “if there is no reaction, write ‘no reaction’” “describe the contents of the test tubes once any reactions are complete” “combustion of octane in limited oxygen”. Common contexts: metals with acids, metals with metal salt solutions, halogen displacement (Cl₂, Br₂, I₂), metals with halogen gases, incomplete combustion.

**Steps**
1. Determine whether a reaction occurs: use standard electrode potentials (Pattern 4) or metal reactivity (a more reactive metal displaces a less reactive ion); if there is no reaction, write ‘no reaction’ and ‘no visible reaction’ as required by the question (as in 2020S-Q27).
2. Write the equation: correct reactants and products, balanced, with state symbols (solid s, liquid ℓ, gas g, solution aq).
3. Describe observations (initial → final):
   - metal dissolves, solid disappears;
   - colourless, odourless bubbles form (effervescence);
   - solution colour change (use the data booklet colour table: Fe²⁺ pale green, Cu²⁺ blue, Br₂(aq) orange, I₂(aq) brown, Cl₂ yellow-green);
   - colour of the solid formed (Cu salmon pink, Ni or Ag, etc.).
4. Incomplete combustion: besides CO₂, there is also carbon black (black solid / soot) or colourless CO, and heat is released with an orange flame (2025S-Q26(b)).

**Marking points (typical key wording)**:
✓ 2024S-Q27(a) (4 marks): Mg(s) + 2H⁺(aq) → Mg²⁺(aq) + H₂(g) (1 mark each for species and balancing); observation: grey solid added to colourless solution, bubbles form, solid dissolves and disappears.
✓ 2024S-Q27(b) (4 marks): Br₂(ℓ) + 2I⁻(aq) → 2Br⁻(aq) + I₂(s) or I₂(aq) (1 mark each for species and balancing); observation: red liquid added to colourless solution, forming a grey precipitate or brown solution.
✓ 2024S-Q27(c) (4 marks): 2Al(s) + 3Ni²⁺(aq) → 2Al³⁺(aq) + 3Ni(s); observation: grey solid added to green solution, forming a black or silver precipitate, and the solution colour fades.
✓ 2023S-Q30(a) (4 marks): Fe(s) + Cu²⁺(aq) → Cu(s) + Fe²⁺(aq); observation: initially grey iron filings and blue solution; at the end, a salmon pink solid forms and the solution fades to pale green (the key requires both initial and final colours to be stated).
✓ 2023S-Q30(c) (4 marks): 2Br⁻(aq) + Cl₂(g) → Br₂(aq) + 2Cl⁻(aq); observation: yellow-green gas passed into colourless solution, forming an orange solution.
✓ 2025S-Q26(a) (5 marks): Cu(s) + Cl₂(g) → CuCl₂(s) (species, balancing, state symbols); observation: salmon pink solid with yellow-green gas, a green solid forms on the surface, and the yellow-green gas fades.
✓ 2025S-Q26(b) (5 marks): 2C₈H₁₈(g) + 17O₂(g) → 16CO(g) + 18H₂O(g); observation: heat released, flame (orange); and black solid (soot) or colourless gas mixture (choose one, must be consistent with the equation). If the equation only shows CO₂ and H₂O, the key gives a maximum of 4 marks.

**Common errors (examiner reports)**: The examiner reports contain no specific comment on this pattern. The following common errors are summarised from the key:
- Incorrect colours: in the data booklet, Cl₂(g) is yellow-green, Br₂(ℓ) is red, I₂(s) is grey, I₂(g) is purple; for aqueous solutions, orange and brown follow the key (e.g. orange solution in 2023S-Q30(c), brown solution in 2024S-Q27(b)).
- Omitting state symbols from the equation, or giving I₂ a state symbol that does not match the question requirements.
- Writing CuCl or another incorrect chemical formula can only receive partial marks even if balanced.
- Writing only “colour change” without the initial and final colours.
- Omitting soot or CO from the products of incomplete combustion and writing only CO₂.

**Past exam questions**: 2017S-Q26(a)(i), 2017S-Q26(c)(i), 2017S-Q26(c)(ii), 2019S-Q26(a), 2020S-Q27, 2022E-Q37(e), 2023S-Q30(a), 2023S-Q30(c), 2024S-Q27(a), 2024S-Q27(b), 2024S-Q27(c), 2025S-Q26(a), 2025S-Q26(b)

## Pattern 4: Standard electrode potentials: reaction tendency and cell voltage

**Recognise**: “calculate the EMF / potential difference of the cell” “predict whether the reaction will occur spontaneously” “identify the most suitable sacrificial anode using standard reduction potentials” “explain why the measured voltage is lower than the calculated value” “explain why water is not used as the solvent”.

**Steps**
1. From the E° table, find two half-reactions: the more positive E° is reduction (cathode), the more negative E° is oxidation (anode, reverse its half-reaction).
2. E°(cell) = E°(reduction, more positive) − E°(reduction, more negative), i.e. E°(cell) = E°(cathode) + E°(anode oxidation). Note the sign of E° for each half-reaction.
3. E°(cell) > 0 → reaction is spontaneous; E°(cell) < 0 → not spontaneous, requires an external voltage (key for 2024S-Q33(c): −1.38 V, not spontaneous).
4. To select the strongest oxidising agent: the oxidised species in the reduction half-reaction with the most positive E°; strongest reducing agent: the reduced species in the reduction half-reaction with the most negative E°.
5. If selecting a sacrificial anode, choose a metal with a more negative E° than iron (more easily oxidised), such as Zn, Mg, Cr, Mn, Al, and it must be electrically connected to the iron (2021S-Q31(d), 2023S-Q27(c)).
6. Reasons the measured voltage is lower than the calculated value: non-standard conditions (concentration, pressure, temperature), internal resistance, overvoltage, side reactions caused by impurities.
7. Water is not used as the solvent for lithium batteries because the E° of Li is −3.04 V; it reacts with water to release H₂ and energy, with a risk of explosion (2025S-Q27(c)).

**Marking points (typical key wording)**:
✓ 2017E-Q37(h) (1 mark): 1.23 + 0 = 1.23 V (acidic conditions); or 0.4 + 0.83 = 1.23 V (alkaline conditions).
✓ 2017S-Q34(c)(ii) (3 marks): From copper’s +0.34 V and the voltmeter reading, deduce the E° of the unknown metal, approximately −0.76 V; referring to the data booklet, Cr (−0.74 V) and Zn (−0.76 V) are both close; the key selects Zn on the basis that the unknown metal forms colourless and/or +2 ions, while the common ion of Cr is +3, which does not fit.
✓ 2020E-Q36(d) (2 marks): cell voltage +2.70 V (unit V must be written).
✓ 2021S-Q30(c) (2 marks): any two points, e.g. gas pressure higher than standard pressure, temperature not at 25 °C, some electrical energy converted to heat, voltage drop caused by resistance of components.
✓ 2021S-Q31(d) (2 marks): choose a metal with a more negative E° than iron (e.g. Zn), and state that its E° is more negative than that of iron.
✓ 2023S-Q27(c) (4 marks): sacrificial anode is more reactive than the protected metal; the metal can be one of Zn, Mg, Cr, Mn, Al; the two metals must be electrically connected; the E° of the anode is more negative than that of iron.
✓ 2024S-Q33(c) (4 marks): choose a species from the E° table (key examples: F⁻(aq), PbSO₄(s) or Cl₂(g)); write the voltage calculation (e.g. +1.51 V − 2.89 V = −1.38 V); state that the voltage is negative, so the reaction is not spontaneous.
✓ 2024E-Q39(e) (2 marks): any two points, e.g. concentration and temperature not under standard conditions, overvoltage, impurities, internal resistance (noted in key).
✓ 2025S-Q27(c) (2 marks): lithium reacts with water to release H₂, creating a risk of explosion due to pressure or heat release (any one).

**Common errors (examiner reports)**: The examiner reports do not provide specific comments on this pattern. The following common errors are summarised from the key:
- Writing E°(cell) as E°(reduction) − E°(oxidation), or writing the sign of E° for the oxidation half-reaction incorrectly.
- The calculated result has no unit (V must be written).
- Writing vague terms such as “temperature” as the reason for the measured voltage deviation, without stating the specific effect.
- Choosing a metal with a more positive E° than iron as the sacrificial anode (e.g. Cu, Ag, Sn).
- Forgetting to state that the voltage is negative and the reaction is not spontaneous in 2024S-Q33(c).

**Past exam questions**: 2017E-Q37(h), 2017E-Q37(i), 2017S-Q34(c)(ii), 2020E-Q36(d), 2021S-Q30(c), 2021S-Q31(d), 2023S-Q27(c), 2024E-Q39(b)(ii), 2024E-Q39(e), 2024S-Q33(c), 2025S-Q27(c)

---

## Pattern 5: Galvanic cell structure and working principles

**Recognise**: “galvanic cell” “label the anode, cathode, direction of electron flow and direction of ion flow” “write the electrode reactions” “describe the observations at the electrodes” “explain the function of the salt bridge” “why does a galvanic cell need a salt bridge”.

**Steps**
1. Determine the anode (oxidation occurs, electrons flow out) and cathode (reduction occurs, electrons flow in). In a galvanic cell, the anode is the negative electrode and the cathode is the positive electrode.
2. In the external circuit, electrons flow from the anode through the wire to the cathode; the current direction is opposite to the electron direction.
3. Ion migration in solution: in the salt bridge, anions move to the anode half-cell and cations move to the cathode half-cell (2020E-Q36(e)(ii): positive ions produced at the anode increase the positive charge in the anode half-cell, so anions enter the anode half-cell through the salt bridge).
4. Write electrode reactions: anode (metal dissolves) M → Mⁿ⁺ + ne⁻; cathode (ion reduction) Mⁿ⁺ + ne⁻ → M.
5. Describe electrode observations: the anode metal becomes thinner or dissolves, and the solution colour changes; a solid forms and deposits at the cathode (e.g. the blue colour of Cu²⁺ solution fades and the copper electrode increases in size, 2017S-Q34(b)).
6. Function of the salt bridge: maintain charge neutrality, complete the circuit, allow ion migration (prevent polarisation).
7. Cell diagram (cell notation) conventionally writes the anode first, then the cathode.

**Marking points (typical key wording)**:
✓ 2019S-Q31(a) (4 marks): label the anode and cathode, electron flow direction, ion flow direction (both cations and anions must be labelled), and the positive/negative signs of the two electrodes.
✓ 2017S-Q34(b) (2 marks): copper electrode increases in size or solid forms, solution fades and becomes lighter (must state the solution colour).
✓ 2020E-Q36(b) (1 mark): external circuit arrow from Mg to Cu/C.
✓ 2020E-Q36(e)(ii) (4 marks): anions enter the anode half-cell through the salt bridge; the reason is that positive ions are produced at the anode; cations enter the cathode half-cell through the salt bridge; the reason is that positive ions are removed at the cathode.
✓ 2020E-Q36(e)(i) (1 mark): salt bridge maintains charge neutrality, completes the circuit, allows ion movement, prevents polarisation (any one).
✓ 2021S-Q30(a) (4 marks): anode on the H₂ side, cathode on the O₂ side; electrons flow from the anode through the external circuit to the cathode; H⁺ flows from the anode through the electrolyte H₂SO₄(aq) to the cathode.
✓ 2016S-Q26(a) (4 marks): similarities between the two types of cells (e.g. both have an anode and cathode, electrons flow from the anode through the external circuit to the cathode, both are redox reactions, both require an electrolyte).

**Common errors (examiner reports)**: The examiner reports do not provide specific comments on this pattern. The following common errors are summarised from the key:
- Confusing electron flow direction with current direction.
- Reversing ion migration direction (salt bridge anions to the anode, cations to the cathode).
- Labelling only one ion’s migration (2019S-Q31(a) requires both ions to be labelled).
- Labelling the anode and cathode the wrong way round, or writing the anode as the “positive electrode” (in a galvanic cell the anode is negative).
- Observations only write “bubbles” or “solid forms”, without stating the change in solution colour.

**Past exam questions**: 2016S-Q26(a), 2016S-Q26(b), 2017E-Q37(f), 2017E-Q37(g), 2017S-Q34(b), 2019S-Q31(a), 2019S-Q31(b), 2020E-Q36(a), 2020E-Q36(b), 2020E-Q36(e)(i), 2020E-Q36(e)(ii), 2021S-Q30(a), 2023S-Q29

---

## Pattern 6: Electrolytic cells and electrolysis applications

**Identify**: "electrolytic cell" "an external power supply" "electroplating" "purify copper by electrolysis" "anode mud" "explain why the reaction is non-spontaneous" "label the diagram with the anode, cathode, cation and anion flow and electron flow".

**Steps**
1. An external power supply drives a non-spontaneous reaction: oxidation occurs at the anode (connected to the positive terminal of the power supply), and reduction occurs at the cathode (connected to the negative terminal). In an electrolytic cell, the anode is positive and the cathode is negative (opposite to a galvanic cell).
2. Electrolytic refining of copper: crude copper (containing impurities such as Zn, Fe, Ag and Au) is the anode, Cu → Cu²⁺ + 2e⁻; the electrolyte is CuSO₄(aq); pure copper is the cathode, Cu²⁺ + 2e⁻ → Cu.
3. Where impurities go: metals more reactive than copper (such as Zn and Fe) dissolve at the anode but do not deposit at the cathode, and remain in solution; metals less reactive than copper (Ag and Au) do not dissolve and deposit below the anode, forming anode mud.
4. Electroplating: the object to be plated is the cathode, and the electrolyte contains ions of the plating metal. In the apparatus in 2024E-Q39(c), the cathode is the object to be plated (plated with Cr), the anode is Pb, the key anode half-reaction is Pb → Pb²⁺ + 2e⁻, and the cathode half-reaction is Cr³⁺ + 3e⁻ → Cr (see Pattern 2).
5. Drawing: label the anode and cathode and the positive and negative terminals of the power supply; electrons flow from the anode through the external circuit to the positive terminal of the power supply, then from the negative terminal of the power supply to the cathode; cations move towards the cathode and anions move towards the anode.

**Marking points (typical wording in the key)**:
✓ 2016E-Q40(b) (10 marks): Outline the process; electrolytic cell diagram (including power supply, electron flow, anode as crude copper, cathode as pure copper); half-reactions at the anode and cathode; where impurities go (anode mud or dissolved metal ions).
✓ 2025E-Q40(a) (10 marks): anode (crude copper) and cathode (pure copper); anode reaction Cu(s) → Cu²⁺(aq) + 2e⁻; cathode reaction Cu²⁺(aq) + 2e⁻ → Cu(s); electrolyte is CuSO₄(aq); sites of oxidation and reduction; formation of anode mud; movement of ions and electrons; labelled diagram with power supply.
✓ 2022E-Q35(d) (3 marks): anode, cathode, cations flow to the cathode, anions flow to the anode, electrons flow to the cathode (three or more items).
✓ 2024E-Q39(c) (3 marks): label the anode and cathode, cation flow, electrons flow from the anode to the cathode.

**Common errors (exam report)**: The exam report makes no specific comment on this pattern. The following common errors are summarised from the key:
- Writing the anode of an electrolytic cell as the negative electrode (the anode of an electrolytic cell is connected to the positive terminal of the power supply).
- Getting the fate of impurities wrong: describing anode mud as a precipitate in solution, or saying Zn and Fe deposit at the cathode.
- Writing only the half-reactions and not the electrolyte (the key for 2025E-Q40(a) requires the electrolyte to be written).
- Drawing the electron direction or ion direction backwards.
- Not showing the position of the power supply.

**Past exam questions**: 2016E-Q40(b), 2016S-Q26(a), 2016S-Q26(b), 2019S-Q31(a), 2019S-Q31(b), 2022E-Q35(d), 2023S-Q29, 2024E-Q39(c), 2025E-Q40(a)

---

## Pattern 7: Practical batteries and fuel cells

**Identify**: "state whether the battery is primary, secondary or a fuel cell, and justify" "write the half-equation at the positively charged electrode during charging" "list two advantages / disadvantages of fuel cells" "explain the function of the electrolyte" "why is a fuel cell more environmentally friendly".

**Steps**
1. Classification: primary cell (non-rechargeable, e.g. dry cell); secondary cell (rechargeable, e.g. lead-acid battery, lithium-ion battery); fuel cell (reactants are continuously supplied from outside, and the electrodes themselves are not consumed).
2. During charging, oxidation occurs at the positive electrode (connected to the positive terminal of the external power supply); during discharging, reduction occurs at the positive electrode. Write the half-reaction for the electrode specified in the question (2025S-Q27(b): the positive electrode is LiCoO₂(s) → CoO₂(s) + Li⁺ + e⁻).
3. Hydrogen-oxygen fuel cell (acidic conditions): anode H₂ → 2H⁺ + 2e⁻, cathode O₂ + 4H⁺ + 4e⁻ → 2H₂O, overall reaction 2H₂ + O₂ → 2H₂O (2021S-Q30(b)).
4. Function of the electrolyte: allows ions to move between the two electrodes, maintains charge balance, and completes the circuit (2017E-Q37(g)).
5. Advantages (fuel cells compared with primary and secondary cells): reactants are continuously supplied, so they can operate continuously; no memory effect; electrodes are not consumed; high efficiency; stable voltage (2017E-Q37(e)).
6. Disadvantages and environmental performance: hydrogen must be stored under high pressure or at low temperature, and is flammable and explosive; producing hydrogen consumes energy and may release CO₂; platinum catalysts are expensive; limited lifespan (2025S-Q27(d)(ii)). Environmental advantages: the only product is water, it does not rely on fossil fuels, and it does not produce acid rain precursors such as SO₂ and NOₓ (2018S-Q28(c)).

**Marking points (typical wording in the key)**:
✓ 2025S-Q27(a) (2 marks): secondary cell (rechargeable), with a reason.
✓ 2025S-Q27(b) (1 mark): LiCoO₂(s) → CoO₂(s) + Li⁺ + e⁻ (i.e. equation 1).
✓ 2025S-Q27(di) (2 marks): A fuel cell is a galvanic cell with a continuous supply of reactants, so it can continuously generate electrical energy.
✓ 2025S-Q27(dii) (2 marks): Any two disadvantages, such as the bulky and costly high-pressure or low-temperature storage, flammability and explosiveness, greenhouse gas emissions from hydrogen production, expensive platinum catalysts, or low energy conversion efficiency.
✓ 2017E-Q37(e) (2 marks): Any two advantages, such as continuous operation, no memory effect, electrodes not consumed, or higher efficiency.
✓ 2018S-Q28(c) (2 marks): Any two statements with environmental advantages (as listed in the key): CO₂ is recycled rather than released into the atmosphere; raw materials can be obtained from the atmosphere, without relying on non-renewable fossil fuels and without drilling for oil; the product of a fuel cell is water, whereas the SO₂ and NOₓ emitted by internal combustion engines are major sources of acid rain.
✓ 2017E-Q37(g) (2 marks): The electrolyte allows ions to move; maintains charge neutrality; completes the circuit (any two).

**Common errors (exam report)**: The exam report makes no specific comment on this pattern. The following common errors are summarised from the key:
- Describing a fuel cell as "rechargeable".
- Treating "electrode consumption" as an advantage of fuel cells (it should be that the electrodes are not consumed).
- Mixing up the positive and negative electrode directions for charging and discharging (during charging, oxidation occurs at the positive electrode).
- Writing 2025S-Q27(b) as the reduction reaction for discharging.
- In environmental questions, writing only "no pollution" without specifically explaining the products or raw materials.

**Past exam questions**: 2017E-Q37(e), 2017E-Q37(f), 2017E-Q37(g), 2018S-Q28(c), 2023S-Q29, 2025S-Q27(a), 2025S-Q27(b), 2025S-Q27(d)(i), 2025S-Q27(d)(ii)

---

## Pattern 8: Corrosion and protection of iron

**Identify**: “explain why the steel pole rusts below ground but not above ground” “write the equations for the rusting process” “what is a sacrificial anode” “choose a metal for a sacrificial anode using standard reduction potentials” “explain how painting / oiling protects the iron” “chrome plating”.

**Steps**
1. Electrochemical process of corrosion: anode Fe(s) → Fe²⁺(aq) + 2e⁻; cathode O₂(g) + 2H₂O(ℓ) + 4e⁻ → 4OH⁻(aq) (neutral or alkaline) or O₂ + 4H⁺ + 4e⁻ → 2H₂O (acidic).
2. Subsequent reactions: Fe²⁺ is further oxidised to Fe³⁺, and hydroxides and Fe₂O₃·xH₂O (rust) are formed; in this step, the oxidation number of iron increases from +2 to +3, and the oxidation number of oxygen decreases from 0 to −2 (2021S-Q31(b)).
3. Difference between underground and above ground: underground soil provides water and ions (electrolyte), different parts of the iron can act as the anode and cathode respectively, and the iron itself conducts electrons; the soil may also be acidic (the key for 2024E-Q39(a) lists these points; choose any two).
4. Protection methods:
   - Isolation (painting, oiling or greasing): forms a barrier, preventing water and oxygen from contacting the iron; if the barrier is incomplete, rusting still occurs.
   - Sacrificial anode: a metal electrically connected to the iron and more reactive than iron (more negative E°); it is oxidised preferentially, protecting the iron (as the cathode).
   - Platings fall into two types: (1) Barrier platings (e.g. tin, nickel) are less reactive than iron and work by blocking water and oxygen; if the plating is damaged, the iron is electrically connected to the plating and becomes the anode, so rusting is actually accelerated. (2) Sacrificial platings (e.g. zinc) are more reactive than iron and are corroded first if damaged. The protection provided by chrome plating mostly comes from a dense surface oxide film (passivation); this is additional chemistry knowledge and is not in the key; Cr itself is more reactive than iron (see Pattern 4).
5. Definition of a sacrificial anode: a metal that is more easily oxidised than the metal being protected and is electrically connected to it; it is corroded preferentially (2021S-Q31(c)).

**Marking points (typical key wording)**:
✓ 2021S-Q31(a) (4 marks): oxidation and reduction half-reactions (species and balancing); overall reaction 2Fe + O₂ + 4H⁺ → 2Fe²⁺ + 2H₂O, or 2Fe + O₂ + 2H₂O → 2Fe(OH)₂ (either one; 1 mark each for species and balancing).
✓ 2021S-Q31(b) (2 marks): oxidation number of Fe increases from +2 to +3; oxidation number of O decreases from 0 to −2.
✓ 2021S-Q31(c) (1 mark): a sacrificial anode is a metal that is more easily oxidised than the metal being protected and is electrically connected to it.
✓ 2021S-Q31(d) (2 marks): choose one of Zn, Mg, Cr, Mn or Al (more negative than iron); state that its E° is more negative than that of iron (more easily oxidised).
✓ 2023S-Q27(b) (3 marks): oiling or greasing; forms a barrier; prevents water and oxygen from contacting the iron.
✓ 2023S-Q27(c) (4 marks): the anode is more reactive than the protected metal (cathode); the metal is one of Zn, Mg, Cr, Mn, Al; the two metals must be electrically connected; the anode E° is more negative than that of iron.
✓ 2024E-Q39(a) (5 marks): any two points, such as oxidation and reduction can occur at different sites, iron acts as an electron conductor, the soil may be acidic (refer to equations 1, 2, 3); alternatively, answer differential aeration (plenty of oxygen above ground, moisture retained below ground) or any other “any one” item from the key. At least one equation must be cited.
✓ 2024E-Q39(b)(i) (2 marks): painting forms a barrier, preventing water and oxygen; the barrier is incomplete (so rusting still occurs).
✓ 2024E-Q39(b)(ii) (3 marks): the wire acts as a conductor connecting the iron and the second metal; the second metal should be oxidised preferentially; because the method fails, the second metal is not more reactive than iron (e.g. less reactive than iron, or has a more positive E°).

**Common errors (exam reports)**: The 2021 report states that the iron corrosion question (2021S-Q31) had an average of 70.4%, and responses were relatively good; but the key for 2024E-Q39(b)(ii) states that if the chosen metal is less reactive than iron, protection fails, so students must clearly explain the reactivity relationship. The following common errors are summarised from the key:
- Choosing a metal less reactive than iron when selecting a sacrificial anode (e.g. Cu, Ag, Sn).
- Writing the protected iron as the anode (the protected iron is the cathode).
- Omitting “the two metals must be electrically connected”.
- For painting or oiling, writing only “prevents rust”, without explaining the role of the barrier, or without explaining why rusting still occurs when the barrier is incomplete (2024E-Q39(b)(i)).
- Mixing the OH⁻ and H⁺ forms of the overall reaction.

**Past exam questions**: 2021S-Q31(a), 2021S-Q31(c), 2021S-Q31(d), 2023S-Q27(b), 2023S-Q27(c), 2024E-Q39(a), 2024E-Q39(b)(i), 2024E-Q39(b)(ii)
