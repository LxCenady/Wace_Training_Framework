# CHE Solution Notes Review Record

**Review method**: Eight sets of notes were drafted by three writing subagents (Haiku 5.5) based on the evidence packs in `evidence/che/notes/` (question stems of the past exam questions for each pattern, marking key mark-allocation lines, exam report comments); then two independent review subagents (Haiku 5.5, not involved in writing) checked item by item against the original papers, marking keys (rendering original images where text was missing), exam reports, and the data booklet, and corrected directly. A total of 86 corrections were made over the two rounds (13 high, 39 medium, 34 low); the "past exam questions" list for each pattern matches `tools/parttags_CHE.txt` item by item.

**Known issues with official materials (all noted neutrally in the notes)**: the key header marks for 2019E-Q40/Q41 do not match the paper; the key for 2019E-Q36(e)–(g) is a copyright placeholder image; 2023E-Q39's stem states that ethene hydration is endothermic (it is actually exothermic; the key accepts both); the key for 2023E-Q37(d) does not match the general prediction from Markovnikov's rule; the main text of the key for 2024E-Q36(c) uses 1:1, while the note uses 2:1; the key for 2025E-Q39 has a typographical error.

---

## Review A (01–04)

Review scope: the four files `01_Equilibrium`, `02_Acids_Bases`, `03_Redox_Electrochemistry`, `04_Organic_Structure` (within the editable range).
Review basis: `evidence/che/label_input/<年份>.json` (stem, key_text, marks); key pages were rendered and read with pymupdf using `key_regions`; exam reports `CHE/papers/<年份>_CHE_ExamReport.pdf`; data booklet `CHE/papers/2025_CHE_DataBooklet.pdf`; tags `tools/parttags_CHE.txt`.
Page numbers: key and report page numbers are 0-based (consistent with the evidence JSON). Severity: high = chemistry or key factual error, or opposite to the key; medium = missing key marking point, incorrect exam report attribution, incorrect data booklet attribution; low = wording precision or additional explanation.

## Check results (mechanical checks, re-run after edits)

- The "past exam questions" list in each pattern section matches parttags item by item: EQ 10 sections, AB 9 sections, RX 8 sections, ORG 9 sections, 36 sections in total, 0 inconsistencies.
- All past exam question references in the body (336 after de-duplication) exist in parttags_CHE.txt.
- Heading order unchanged: "## Pattern N:" occurs as 1–10, 1–9, 1–8, 1–9 in the four files respectively.
- The "(N marks)" immediately following references match the item marks in the evidence JSON; no inconsistencies.
- INDEX marks and ★ markers (EQ4, EQ5, EQ1; AB9, AB4, AB5; RX2, RX3; ORG4, ORG2) are consistent.
- The files no longer contain outdated statements such as "draft", "truncated", "key not entered", "key empty", and "only the answer entered in the evidence".

## 01_Equilibrium_Solution_Notes.md

| # | Severity | Location | Issue | Evidence | Correction |
|---|---|---|---|---|---|
| 1 | High | Pattern 4 Step 4 (colour question) | 2022S-Q26 direction of colour change written incorrectly: the text said the deep red of FeSCN²⁺ fades as the equilibrium shifts left, but in the key, adding FeCl₃ shifts it right and the colour becomes a deeper red; heating shifts it left to "more brown or orange"; adding water and adding Na₃PO₄ give a very pale brown | 2022 key p. 2 (rendered k2022S26_p2) | Rewritten to give the colour result of each of the four changes one by one according to the key |
| 2 | Medium | File header "Remember first" item 2 | Described the 2022 report as saying "sentences were truncated"; the original report says Question 26 (predicting equilibrium changes) was one of the best-answered questions in Section Two; the 2024 report's ocean acidification comment was also not truncated | Report 2022, early in Section Three; Report 2024, Section Two paragraph | Rewritten to match the report's intended meaning |
| 3 | Medium | File header "What the data booklet provides" colour table | Attributed the colours of Cl₂(aq), Br₂(aq), and I₂(aq) to the data booklet; the data booklet's coloured halogens table lists only Cl₂(g), Br₂(ℓ), I₂(g), and I₂(s) | Data booklet 2025 p. 5 (0-based 4, "Coloured halogens") | Removed the data booklet attribution and noted that aqueous colours should be based on the key (e.g. 2023S-Q30(c), 2024S-Q27(b)) |
| 4 | Medium | Pattern 1 common error | Recorded 39.5% as the mean for 2021E-Q37(aii) (3 marks); the report's 39.5% is for the whole of Question 37 (18 marks), and the report also notes that the calculation for this question required a non-standard method | Report 2021, Section Three paragraph; evidence JSON 2021E-Q37 total mark 18 | Changed to the whole-question basis and noted that it is not the separate mean for (aii) |
| 5 | Low | Pattern 3 marking point (2025S-Q30(a)) | Did not note that the key requires ¹⁵N to be explicitly written | 2025 key p. 6 (key note) | Added |
| 6 | Medium | Pattern 4 common error | Same as #2 (the claim that the 2022 report said "truncated" is incorrect) | Report 2022, early in Section Three | Rewritten as "Question 26 was best answered" |
| 7 | Low | Pattern 5 marking point (2025S-Q32(c)) | Only wrote "the forward reaction rate decreases", but did not give the direction of the equilibrium equation in the stem, so readers cannot tell which direction is the forward reaction | 2025 evidence JSON stem: 2CrO₄²⁻ + 2H⁺ ⇌ Cr₂O₇²⁻ + H₂O; key p. 8 | Added the equilibrium equation and noted the forward reaction direction |
| 8 | Low | Pattern 6 Step 2 | Described 2019S-Q34(c) (a non-equilibrium curve of CO₂ volume against time) as "the time taken to reach equilibrium is shortened" | 2019 key pp. 12–13 (the key only requires a steeper slope and the curve reaching the plateau earlier) | Changed to "reaches the plateau earlier" and noted that it is not a reversible equilibrium |
| 9 | Medium | Pattern 10 common error | Described the 2024 report's ocean acidification comment as "truncated"; the report actually lists 2024S-Q30 (explaining ocean acidification with equations) as one of the hardest questions in Section Two | Report 2024, Section Two paragraph | Rewritten to match the report's intended meaning |
| 10 | Medium | Pattern 10 common error (new) | The key for 2019E-Q36(e)–(g) is a copyright placeholder in the PDF, and the text previously had no note about this; the report confirms that (f) must use the equilibrium shift principle, and (g) must use collision theory and rate and must not be explained using the equilibrium shift principle; the two concentration conditions in (e) could not be verified | 2019 key p. 17 (rendered k2019E36_p17, (e)–(g) are placeholders); Report 2019 "Question 36(f)" paragraph | Added the report requirements and noted that (e) was not verified |
| 11 | Low | File header review status | The old status "draft, not yet independently reviewed" was outdated | — | Updated |

## 02_Acids_Bases_Problem-solving_Approach.md

| # | Severity | Location | Issue | Evidence | Correction |
|---|---|---|---|---|---|
| 1 | High | Pattern 1 common errors (circling bases) | 2023S-Q26(c) is written as "both bases must be circled"; the key lists three B-L bases: H₂O, NO₂⁻, HCOO⁻ | 2023 key p. 2 (key text within render range) | Change to three and note that all must be circled for full marks |
| 2 | High | Pattern 2 Step 2 (stepwise ionisation of polyprotic acids) | The before/after relationship is reversed: the product of the second step should be the reactant of the first step, not "the product of the second step is the reactant of the first step" | Chemistry rules; 2018S-Q27(a) key p. 4 | Correct it, and use H₂PO₄⁻ as an example |
| 3 | High | Pattern 6 Step 6 (polyprotic acid equivalence points) | Says H₃PO₄ has two equivalence points; actually it has three, and the third is outside the phenolphthalein colour-change range. The original mixes in the H₂SO₃ context | 2018S-Q27(d) key pp. 4–5 (mentions the third equivalence point) | Write separately: H₂SO₃ has two, H₃PO₄ has three |
| 4 | High | Pattern 8 Step 3 (titration curves) | Says H₂SO₄ shows two sharp jumps, contrary to the 2019S-Q35(a)(ii) key: the key says H₂SO₄ is a strong acid and the curve has only one plateau and one endpoint | 2019 key pp. 14–15 | Change to H₂SO₃ has two sharp jumps, H₂SO₄ has one |
| 5 | Medium | File header "First remember" point 2 | The 2023 report is written as listing 2023S-Q26 as the hardest question; the report itself says Q26 was best answered, and the hardest questions were Q28 (buffers) and Q32 (intermolecular forces and solubility) | Report 2023 Section Two paragraph | Rewrite |
| 6 | Medium | File header colour table | Attributes the colour of Cu(OH)₂ to the Data Booklet; the Data Booklet solids table has no Cu(OH)₂ | Data Booklet 2025 p. 5 (solids table) | Delete the attribution; instead list CuO black and CuCO₃ green, and note that the question stem or key takes precedence |
| 7 | Medium | Pattern 1 common errors | Same as #5 (incorrect attribution to the 2023 report) | Report 2023 | Rewrite |
| 8 | Medium | Pattern 2 common errors | Same as #5 (incorrect attribution to the 2023 report) | Report 2023 | Rewrite |
| 9 | Medium | Pattern 2 marking points | 2020S-Q31(a) is missing marking points; the key page is a boxed diagram and the text is garbled | 2020 key p. 8 (render k2020S31_p8: three-step equilibrium, 1 mark per box, 3 marks total) | Add the three-step equilibrium equations and 1 mark per blank |
| 10 | Medium | Pattern 4 common errors | Says the 2024 report's Q32 (buffer applications) "the preceding text is truncated and cannot be confirmed"; the report lists Q32 as one of the hardest questions in Section Two | Report 2024 Section Two paragraph | Rewrite to match the report's intended meaning |
| 11 | Low | Pattern 4 Step 6 | "The closer to 1:1, the better" is attributed to 2024S-Q32(e); the key only requires listing two factors, and the 1:1 statement is supplementary chemistry knowledge | 2024 key p. 8 | Note it as supplementary chemistry knowledge, not in the key |
| 12 | Low | Pattern 4 marking points (2025S-Q29(b)) | Missing the fifth key point: pH rises slightly | 2025 key p. 5 | Add |
| 13 | Medium | Pattern 6 marking points (2018S-Q27(d)) | Says "only the answer is recorded in the evidence; the reason is not recorded"; in fact the key has five marking points, equation requirements and a methyl orange alternative | 2018 key pp. 4–5 | Add the five points, equation and alternative condition |
| 14 | Medium | Pattern 6 marking points (2020E-Q37(d)) | Does not note the key's "no hydrolysis equations: maximum 4 marks" | 2020 key pp. 19–20 | Add |
| 15 | Medium | Pattern 6 common errors | Only writes "too low"; for Error II the key accepts "too small", or "unchanged" when accompanied by the reason "first equivalence point reached, calculation needs correction"; the statement "indicator pH 4.5" has no basis in the key | 2019 key p. 15 (two options for Error II) | Rewrite |
| 16 | Medium | Pattern 7 marking points (2019S-Q35(b)) | Only writes "too small", missing the key's accepted "unchanged" option, and the per-item marking is not stated | 2019 key p. 15 | Change to per-item wording for Error I and Error II |
| 17 | Medium | Pattern 8 marking points (2019S-Q35(a)(ii)) | Says the key for this part is not recorded; in fact the key has two reason formats (initial pH; one or two equivalence points) | 2019 key pp. 14–15 | Add the key's two reason formats and the 1 mark for (a)(i) |
| 18 | Low | File header review status | Same as 01 #11 | — | Update |

## 03_Redox_Electrochemistry_Problem-solving_Approach.md

| # | Severity | Location | Issue | Evidence | Correction |
|---|---|---|---|---|---|
| 1 | High | Pattern 3 marking points (2023S-Q30(a)) | The grey solid is written as a product; actually the grey is the reactant iron filings, the product is salmon-pink copper, and the solution fades to pale green | 2023 key p. 6 (observations for Fe + Cu²⁺) | Change to write the starting and final colours separately |
| 2 | High | Pattern 8 Step 4 (coating) | Says "use an unreactive metal coating (e.g. chromium)"; in the Data Booklet E° table, Cr³⁺ + 3e⁻ lies below Fe²⁺, and the key also lists Cr as a metal more negative than iron that can act as a sacrificial anode, so the two contradict each other | Data Booklet 2025 p. 8 (0-indexed 7); 2021 key pp. 8–9; 2023 key p. 3 (Cr listed as an acceptable sacrificial anode) | Change to two types of coating: barrier and sacrificial; chromium passivation is supplementary knowledge |
| 3 | Medium | File header colour table | Br₂(aq) orange and I₂(aq) brown are attributed to the Data Booklet; the Data Booklet only lists Br₂(ℓ) red, I₂(s) grey, I₂(g) purple, and also adds Cr³⁺ dark green | Data Booklet 2025 p. 5 | Correct it, noting that aqueous solution colours are based on the key |
| 4 | Medium | Pattern 3 common errors (colours) | Same as #3: attributes the colours of Br₂(aq) and I₂(aq) to the Data Booklet | Data Booklet 2025 p. 5; 2023 key pp. 6–7 (orange Br₂ solution); 2024 key pp. 3–4 (brown I₂ solution) | Change to separate Data Booklet colours and key colours |
| 5 | Medium | Pattern 4 marking points (2017S-Q34(c)(ii)) | Writes "choose Zn (or Cr)"; the key chooses Zn, because the unknown metal forms colourless and/or +2 ions, and Cr is +3 and does not fit | 2017 key p. 12 | Change to choosing Zn with the key's reason, and explain that Cr is excluded |
| 6 | Medium | Pattern 2 common errors (2019E-Q40) | Says the 2019E-Q40 key title and mark total are inconsistent and could not be verified this time; in fact the key is 22 marks, consistent with the part marks (a 9, b 4, c 3, d 6) | 2019 evidence JSON 2019E-Q40 breakdown; 2019 key pp. 27–28 | Delete the incorrect statement, add the mark breakdown for (c) |
| 7 | Low | Pattern 2 marking points (2017S-Q27) | The statement "no working required" is too absolute; in the key example, half-reactions are multiplied by ×2, ×3 and then added | 2017 key p. 4 | Add coefficient handling |
| 8 | Low | Pattern 3 marking points (2025S-Q26(b)) | Does not note that when the equation only writes CO₂ and H₂O, the key gives a maximum of 4 marks | 2025 key p. 2 (note) | Add |
| 9 | Low | Pattern 5 marking points (2021S-Q30(a)) | Only writes "label anode and cathode, electron flow and H⁺ flow", without giving their positions and directions | 2021 key p. 7 (render k2021S30_p7) | Add anode on the H₂ side, cathode on the O₂ side, and the directions of electrons and H⁺ |
| 10 | Low | Pattern 8 marking points (2024E-Q39(a)) | Does not list the key's differential aeration etc. "any one item", nor note that at least one equation must be cited | 2024 key p. 22 | Add |
| 11 | Low | File header review status | Same as 01 #11 | — | Update |

## 04_Organic_Structure_Solution_Approaches.md

| # | Severity | Location | Issue | Evidence | Change |
|---|---|---|---|---|---|
| 1 | High | Pattern 2 common error (2019S-Q33) | States that the key for 2019S-Q33 is empty; the key is actually complete (12 marks): pent-2-ene with Br₂(aq) → 2,3-dibromopentane, ethanal → ethanoic acid, butanoic acid + Na₂CO₃ → sodium butanoate (marks allocated separately for each row's structure, product and name) | 2019 key p. 11 (0-based); evidence JSON 2019S-Q33 | Write out the key content and mark allocations |
| 2 | High | Pattern 5 common error (2023E-Q37(d)) | The key lists hydration of but-1-ene (pent-1-ene) as producing a primary alcohol, inconsistent with the general prediction of Markovnikov's rule (terminal H adds to the terminal carbon, mainly secondary alcohol); the original text says "needs to be checked against the original paper" but gives no conclusion. Changed to a neutral description: answering according to the key can earn marks, not used as a general rule | 2023 question (d) (3 marks) and key pp. 14–17; Markovnikov's rule (chemical rule) | Neutral description of the difference between the key and Markovnikov's rule, and note that anti-Markovnikov addition requires another pathway |
| 3 | Medium | Pattern 1 step 4 | Writes the structure for 2017E-Q40(f) as a "cysteine-like structure"; it is actually cysteic acid (contains a sulfonic acid group and an amino group) | 2017 key pp. 26–28 (cysteic acid structure) | Change to cysteic acid |
| 4 | Medium | Pattern 3 common error (2023E-Q37(c)) | States that the key gives only one each of but-1-ene and pent-1-ene; the key actually gives but-1-ene, cis/trans-but-2-ene (the C₅H₁₀ version is pent-1-ene, cis/trans-pent-2-ene) | 2023 key pp. 14–17 | Correction |
| 5 | Medium | Pattern 3 and Pattern 5 common errors (report) | The 2023 report's "answered well" refers to Question 37 as a whole; the file writes it as separate comments for (c) and (d); the 2025 report states 2025S-Q34 is one of the best-answered questions in Section Two, but the file writes "not listed as one of the hardest questions", which is inaccurate | Report 2023 Section Three paragraph; Report 2025 Section Two paragraph | Correct to the report's original meaning |
| 6 | Low | File header review status | Old status "labelled as draft, this file has not been independently reviewed" is outdated | — | Update |

## Unresolved or Unverified Items

1. 2019E-Q36(e): the two required concentration conditions; the key in the PDF is a copyright placeholder and could not be verified. The file only notes "unverified".
2. 2019E-Q36(f), (g): the key is also a placeholder; only the 2019 report confirms the answering method ((f) uses equilibrium shift principles; (g) uses collision theory and rate); specific mark points could not be verified.
3. 2023E-Q37(d): the key is inconsistent with the general prediction of Markovnikov's rule; the original paper's intent cannot be determined from the evidence. The file has a neutral description; answering according to the key can earn marks.
4. Observation (not changed, within label review scope): the 2021 report lists 2021E-Q38 (application of collision theory and chemical equilibrium, mean 35.5%) as a difficult question, but in parttags this question is tagged SYN2, not the EQ series.
5. Sub-questions not checked item-by-item against the key (relevant points were spot-checked, but this is not the basis for this pass): complete mark allocations for 2020S-Q32(e), 2022S-Q27(d), 2021E-Q34(d)–(e), 2020S-Q28(b)(i), 2023E-Q39(b)(i), 2025E-Q36(a)–(b), and 2025E-Q35(a)(c).

## Summary

| File | High | Medium | Low | Total |
|---|---|---|---|---|
| 01_Equilibrium | 1 | 6 | 4 | 11 |
| 02_Acids_Bases | 4 | 11 | 3 | 18 |
| 03_Redox_Electrochemistry | 2 | 4 | 5 | 11 |
| 04_Organic_Structure | 2 | 3 | 1 | 6 |
| Total | 9 | 24 | 13 | 46 |

---

## Review B (05–08 and Cheat Sheet)

> Scope: four solution approach files for `05_Polymers_Proteins`, `06_Chemical_Synthesis`, `07_Quantitative`, `08_Science_Inquiry` (`CHE/methods/`), plus `cheatsheet/CHE_CheatSheet.md` and `CHE_CheatSheet_EN.md`.
> Basis: question text and key text in `evidence/che/label_input/<年>.json`; for sub-questions with missing or garbled key text (2025S-Q28(a), 2025E-Q40(d), 2023E-Q35(b)), the key regions were rendered with pymupdf (dpi 110) and read item by item; exam reports `CHE/papers/<年>_CHE_ExamReport.pdf`; data booklet `CHE/papers/2025_CHE_DataBooklet.pdf` (also checked against 2016, 2018).
> Page numbers: key page numbers in the table below are all PDF 1-based page numbers (key_regions in label_input are 0-based and have been converted).
> Severity: High = chemical factual error or incorrect scoring rule that would mislead answers; Medium = mark value, mark allocation, report citation, or inconsistency with the key; Low = mark range wording, supplementary notes, Chinese–English consistency and formatting.

## 1. 05 Polymers and Proteins (PRO)

| # | Severity | Location | Issue | Evidence (paper / key page / report) | Correction |
|---|---|---|---|---|---|
| 1 | High | Pattern 2 common error, item 1 | States "writing an ester bond as C–O gives only 1 mark" | 2020S-Q28(a) key note "Incorrect or missing ester links is a major error, allocate 0 marks" (2020 MarkingKey p.6); 2018S-Q30(a) same note (2018 p.10) | Change to: incorrect or missing ester links is a major error, 0 marks for that part; minor errors such as missing H or end-group capping deduct 1 mark |
| 2 | High | Pattern 4 mark allocation | Writes "2 marks each for low pH and high pH, requires drawing all H" as applying to both 2018E-Q39(c) and 2020E-Q35(f) | 2018E-Q39(c): low and high pH 2 marks each, minor errors 1 mark each, question requires "Show all hydrogen atoms" (2018 p.26–27); 2020E-Q35(f): total 2 marks, acidic and basic 1 mark each, incorrectly drawn amino acid max 1 mark (2020 p.15–16) | Write the mark values and rules for the two questions separately |
| 3 | High | Pattern 4 common error | States that 2020E-Q35(f) question requires "show all hydrogen atoms" | 2020E-Q35(f) question only says "drawing the structural formula of leucine", with no requirement for all H | Keep only 2018E-Q39(c) |
| 4 | Medium | Marking group item 1 (2021 performance) | "2021 report says Question 34 was best", omits the tied Questions 35 and 36 | 2021 ExamReport, Section Three: "best in Questions 34 (polymers/proteins), 35 (titration calculations) and 36 (empirical formula)" | Change to the three questions tied |
| 5 | Medium | Pattern 3 mark allocation | 2019E-Q38(a) "2 marks per choice" | key: 1–2 marks per choice, total 4 marks (2019 p.23–25) | Change to 1–2 marks (total 4 marks) |
| 6 | Medium | Pattern 6 mark allocation | 2022S-Q29(bii) (tertiary structure) says "2 marks" | key: definition 1 mark, formation 1–2 marks, total 3 marks (2022 p.7–8) | Change to total 3 marks (definition 1 mark, formation 1–2 marks) |
| 7 | Medium | Pattern 2 common error (2025S-Q28(a)) | States the key is blank, "must refer to the original paper", monomer can only be inferred | key diagram has been rendered and read (2025 p.5): monomer is 3-hydroxybutanoic acid HO–CH(CH₃)–CH₂–COOH, total 2 marks, minor errors 1 mark | State the key diagram and mark allocation |
| 8 | Low | Pattern 5 mark allocation | The 1 mark for full names in 2019E-Q41(a) is not stated | key: all 5 correct 2 marks, at least 3 in correct order 1 mark, full names 1 mark (2019 p.30–31) | Add "full names earn an additional 1 mark" |
| 9 | Low | Pattern 7 common error (new) | Does not mention the report's issue with anthropomorphic wording | 2024 ExamReport general advice: "Discourage students from using terms such as 'sensitive' … enzymes sensitive to pH" | Add one item |
| 10 | Low | Pattern 5 common error (new) | Does not mention the report's issue with drawing peptide bonds | 2018 ExamReport, Section Three: "struggled with … drawing peptide links" | Add one item |

## 2. 06 Chemical Synthesis (SYN)

| # | Severity | Location | Issue | Evidence | Correction |
|---|---|---|---|---|---|
| 11 | Medium | Marking panel item 3 (soap structure comparison) | states that the 2024 report lists 2024S-Q31 as an assessed point | 2024 ExamReport, Section Two: "Candidates performed best on Question 31 (structures of soaps and detergents and micelles)" | Change to "the question candidates performed best on in Section Two" |
| 12 | Medium | Pattern 1 marking points | 2021E-Q39(a) "4 marks per synthesis step: reactants, products, balancing, catalyst" | key: in the ethene hydration step, the 4 marks are for reactants, products, acid catalyst and H₂O(g), with no marks for balancing; in the biodiesel step, they are for reactants, products, balancing and lipase (2021 p.22–23) | List the breakdown separately for the two steps |
| 13 | Medium | Pattern 4 marking points | 2024E-Q37(ai) says "missing reactants and products 2 marks each, balancing 1 mark" | key: reactants and products combined 1–2 marks, balancing 1 mark, total 3 marks (2024 p.17) | Change to 1–2 marks + 1 mark for balancing |
| 14 | Low | Pattern 2 marking points | 2017S-Q30(b) breakdown "rate and yield 2 marks each, compromise explanation counted separately" | key: identifies compromise conditions 1, rate 1–2, yield 1–2, reason for compromise 1, total 6 marks (2017 p.7–8) | Rewrite as mark ranges for the breakdown |
| 15 | Low | Pattern 2 marking points | 2023E-Q35(a) mark allocation written as fixed "2 / 3 / 3 marks" | key: catalyst 1–2, temperature 1–3, pressure 1–3, total 8 marks (2023 p.12) | Change to ranges |
| 16 | Low | Pattern 4 marking points (2024S-Q31(b)) | W and X written as "water molecules" and "oil/grease", but the diagram does not label them as such | key only gives positions: W outside micelle, X inside micelle, Y inside micelle (dispersion force position), Z hydrophilic head group (2024 p.7–8) | Remove the identity inference; write only positions |
| 17 | Low | Pattern 5 marking points (2024E-Q37(aii)) | reactants and products "2 marks each" | key: reactants and products 1–2 marks each, catalyst 1 mark, balancing 1 mark, total 4 marks (2024 p.17) | Change to 1–2 marks |

## 3. 07 Quantitative (QNT)

| # | Severity | Location | Issue | Evidence | Correction |
|---|---|---|---|---|---|
| 18 | Medium | Pattern 4 common errors (new item) | 2020E-Q37(c) only gives 19.1%, without explaining that the key has another solution method | 2020 MarkingKey p.20: main method 3 NaOH : 1 H₃PO₄ gives 19.1%; a note gives a 2 : 1 method giving 28.7%, and states that it is beyond the course requirements | Add both methods and the explanation |
| 19 | Low | Pattern 2 marking points | 2024E-Q40(c) "calculation of n, comparison and conclusion total 3 marks" | key: limiting reagent determination 1–3 marks, calculation of n counted separately (2024 p.26–27) | Change to limiting reagent determination 1–3 marks |
| 20 | Low | Pattern 4 common errors (outliers) | describes 0.10 mL as a "commonly used criterion", but does not explain that the key itself uses 17.42, 17.59, 17.55 (differing by 0.17 mL) | 2025 MarkingKey p.19–20 (2025E-Q38(d)) | State that 0.10 mL is a reference; follow the key's approach, and require the reason for exclusion to be stated |
| 21 | Low | Pattern 4 common errors (2019E-Q39(a)) | the label "(calculated by the editor)" is inappropriate | the 2019 key example table directly gives four readings (2019 p.26) | Change to "the readings in the key's example table" |
| 22 | Low | Pattern 7 marking points | omits the rounding requirement for 2023E-Q35(b) | key: 7.621 × 10⁸ L, 4 significant figures (2023 p.12) | Add |

## 4. 08 Scientific Inquiry (INQ)

| # | Severity | Location | Issue | Evidence | Correction |
|---|---|---|---|---|---|
| 23 | Medium | Marking panel item 3 and Pattern 4 step 1 | states that all five elements are marked, including the title | 2019S-Q34(a) key: "No marks have been allocated for a title" (2019 p.13); for titles being marked, see 2021E-Q39(c) (2021 p.22–23), 2022S-Q27(b) (2022 p.4–5) | Change to "titles are marked depending on the question; they are not marked in 2019S-Q34(a)" |
| 24 | Medium | Pattern 7 marking points (2025E-Q38(d)) | "average titre (3 marks)" breakdown does not match | key total 7 marks: titre values 1, average 1, n(OH⁻) 1, stoichiometric ratio 1, mass 1, concentration 1, conclusion 1 (2025 p.19–20) | Change to the correct breakdown |
| 25 | Low | Pattern 3 marking points (2022E-Q39(d)) | fixed volume written as "2 marks" | key: fixed volume 1–2 marks (2022 p.21–22) | Change to 1–2 marks |
| 26 | Low | Pattern 2 marking points (2022E-Q39(c)) | "total 2 marks, requiring two different controlled variables" written as fixed | key: controlled variables 1–2 marks (2022 p.21) | Change to 1–2 marks |

## 5. Cheat Sheet (Chinese) `cheatsheet/CHE_CheatSheet.md`

| # | Severity | Location | Issue | Evidence | Correction |
|---|---|---|---|---|---|
| 27 | High | Section 4 ORG3 cis-trans isomerism conditions | says "two different groups attached to the same carbon of the double bond"; the condition is incorrect | Basic organic chemistry: each carbon of the double bond is attached to two different groups; the English version in the same section says "two different groups on each C of the C=C" | Change to "each carbon at the two ends of the double bond is attached to two different groups" |
| 28 | Medium | Section 2 AB3 | "zwitterion: NaHCO₃ …" term is misused (zwitterion in Section 5 specifically refers to the amino acid H₃N⁺–R–COO⁻) | Conflicts with the terminology in Section 5 PRO4 | Change to "amphiprotic substance (can both donate and accept H⁺)" |
| 29 | Medium | Section 2 AB9 | "Ag⁺ + I⁻ yellow (AgI)" | 2025 Data Booklet "Colours of selected substances": silver iodide = pale yellow | Change to "pale yellow" |
| 30 | Medium | Section 6 SYN5 | "NaOH/KOH fast and cheap, lipase catalysis mild but slow and expensive"; "slow and expensive" has no basis in the key and is contrary to the industrial preference in the 2020 key | 2020E-Q40(f) key: NaOH cheap, fast, high yield; lipase mild conditions, low energy consumption, no soap formation, reusable | Rewrite the comparison points for the two catalysts according to the key |
| 31 | Low | Section 3 RX4 | E°'s "1.00 mol L⁻¹, 100 kPa" is written as if it were Data Booklet content | 2025 Data Booklet only says "at 25 °C" | Note that 1.00 mol L⁻¹ and 100 kPa are textbook standard conditions |
| 32 | Low | Section 5 PRO6 denaturation | missing the two factors heavy metal ions and organic solvents (present in the English version) | English version, same section | Add; make Chinese and English consistent |
| 33 | Low | Section 6 SYN1 fermentation | missing "batch" (present in the English version) | English version, same section | Add; make Chinese and English consistent |
| 34 | Low | Layout (Section 8 INQ7 and gas tests) | exceeds 3 pages after additions | `tools/render_cheat.py` output | Delete the "models improve with evidence" item that duplicates AB1, condense "gas tests" and one phenomenon description, with no factual deletions; re-render to 3 pages |

## 6. Cheat Sheet (English) `cheatsheet/CHE_CheatSheet_EN.md`

| # | Severity | Location | Issue | Evidence | Correction |
|---|---|---|---|---|---|
| 35 | Medium | 2 AB9 | "Ag⁺ + I⁻ yellow" does not match the Data Booklet's pale yellow | 2025 Data Booklet | Change to pale yellow; write AgBr as pale yellow |
| 36 | Low | 2 AB9 | "Cu(OH)₂ pale blue" is inconsistent with the Chinese version's "blue" | Chinese version, same section | Standardise as blue |
| 37 | Medium | 6 SYN5 | "NaOH/KOH fast; lipase mild but slow" does not match the 2020 key | 2020E-Q40(f) key | Rewrite according to the key (same as #30) |
| 38 | Low | 3 RX4 | E° conditions wording does not match the Data Booklet | 2025 Data Booklet | Note as textbook standard conditions (same as #31) |
| 39 | Low | 3 RX3 | missing the colour change for Cl₂(aq) + KBr(aq) (present in the Chinese version) | Chinese version, same section | Add; make Chinese and English consistent |
| 40 | Low | Layout (3 RX7 and 8 INQ7) | additions consistent with the Chinese version cause page overflow | render output | Delete the "Models change …" item that duplicates AB1, condense gas tests, re-render to 3 pages |

## 7. Summary

| File | High | Medium | Low | Total |
|---|---|---|---|---|
| 05 PRO Solution Guide | 3 | 4 | 3 | 10 |
| 06 SYN Solution Guide | 0 | 3 | 4 | 7 |
| 07 QNT Solution Guide | 0 | 1 | 4 | 5 |
| 08 INQ Solution Guide | 0 | 2 | 2 | 4 |
| CHE_CheatSheet.md (Chinese) | 1 | 3 | 4 | 8 |
| CHE_CheatSheet_EN.md (English) | 0 | 2 | 4 | 6 |
| **Total** | **4** | **15** | **21** | **40** |

## 8. Verification

- The past-paper question list was cross-checked against `tools/parttags_CHE.txt` (the script compared each question and recorded the results in the scratchpad): 05's PRO1–PRO7 total 89 items, 06's SYN1–SYN5 total 43 items, 07's QNT1–QNT8 total 139 items, and 08's INQ1–INQ7 total 38 items; all correspond one-to-one, with no missing items, no extra items and no duplicates. This is consistent with the sub-question counts in `evidence/che/notes/INDEX.md` (PRO 89, SYN 43).
- Pattern headings: 05 has 7 (Patterns 1–7), 06 has 5 (Patterns 1–5), 07 has 8 (Patterns 1–8), and 08 has 7 (Patterns 1–7); the count, numbering and order are all unchanged; the ★ markers are consistent with the mark-value ordering in INDEX (PRO6, PRO4; SYN4; QNT1, QNT3; INQ7).
- Cheat sheet page count: `CHE_CheatSheet.pdf` and `CHE_CheatSheet_EN.pdf` were both re-rendered to 3 pages.
- Copyright: all changes are paraphrases; no SCSA original paragraphs were copied; the quoted phrases are only terms from the key (such as "ends are not terminated", etc.).

## 9. Unresolved or noteworthy matters

1. The official key for 2024E-Q36(c) is internally inconsistent (1 : 1 gives 305 mg; the annotation 2 : 1 gives 152 mg). The note records this faithfully; the official intent could not be determined, so the original explanation is retained.
2. The key for 2020E-Q37(c) gives both 3 : 1 and 2 : 1 solution methods; a supplementary explanation has now been added in 07; the key itself notes that 2 : 1 is beyond the course requirements.
3. In the 05 note, for the PMMA key diagram in 2019E-Q38(c), the arrangement of the groups on either side of the main chain is not fully consistent with the chemical structure (the methyl and ester groups are attached to the same main-chain carbon); the note follows the chemical structure description, and the key diagram was not copied verbatim or changed.
4. Nonpolar classification of tryptophan (Trp) in the 05 note: the key for 2022S-Q29(e) lists 8 nonpolar amino acids and does not include Trp. The note states that this was judged independently based on structure, and no change was made.
5. The 2025 ExamReport was not checked item by item; typographical errors in the key for 2025E-Q39, such as "0.02299" should be "0.02999", were not cited in the note for their numerical values, and no change was made.
6. Note content not checked: general conclusions in the reports not involving PRO, SYN, QNT or INQ (such as the overall average marks in the 2016–2019 reports) were not checked one by one, because the note does not cite them.
