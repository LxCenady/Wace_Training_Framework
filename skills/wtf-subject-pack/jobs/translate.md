# Job: translate — Chinese notes from the English notes

Input: one `methods_en/NN_Topic_Methods.md`. Output: `methods/NN_Topic_解题思路.md`, the same content in Chinese
for a WACE student who studies in English (keep exam vocabulary usable).

- Same structure, line for line: `# ` title, the `>` lines, every `## Pattern N: title` becomes
  `## 题型 N：标题` with the same N, sections in the same order.
- Section labels: How often → **出现频率**, Recognise it → **识别**, Method → **步骤**, What the key rewards →
  **评分点**, Common errors → **易错点**, Past questions → **真题**.
- Keep in English, in brackets after the Chinese on first use per pattern: key exam terms and command words
  (e.g. 配平 (balance), 共轭酸碱对 (conjugate acid–base pair), 证明 (show that)).
- Do not translate: question references (2022 ER Q37(a)), formulas, chemical equations, units, code ids.
- Nothing added, nothing dropped. `check` compares the pattern numbers and the reference lists of both files.
