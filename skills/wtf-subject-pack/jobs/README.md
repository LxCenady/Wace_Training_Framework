# Pack-flow AI jobs — fixed specifications

Every step of the pack flow that needs a language model is one of these jobs. A job is fixed: the same
specification, the same input file shape, the same output file shape, the same checks — whoever runs it
(a Haiku subagent, DeepSeek through `tools/flowjobs.py run`, or you). `tools/flowjobs.py` writes the inputs,
checks the outputs and merges them; nothing a job writes reaches the bank without passing `check`.

| Job | Reads | Writes | Model | Per batch |
|---|---|---|---|---|
| [split](split.md) | a part whose key did not split into its printed marks | its awards | small | 15 parts |
| [label](label.md) | awards (key criterion + part stem) | skill, knowledge, operation per award | small | 40 awards |
| [atomise](atomise.md) | every label of one topic + the syllabus | patterns and knowledge atoms of the topic | strong | 1 topic |
| [assign](assign.md) | awards + the approved catalogue | pattern + knowledge codes per award | small | 40 awards |
| [review](review.md) | a 20% sample of assigned awards, blind | an independent assignment | small, other run | 40 awards |
| [notes](notes.md) | one topic's evidence pack | `methods_en/NN_Topic_Methods.md` | strong or small + review | 1 topic |
| [translate](translate.md) | an English notes file | the Chinese notes file | small | 1 file |

## Rules for every job

- **Run**: `python tools/flowjobs.py prompt <S> <job> <batch>` prints the exact prompt for one batch. Give it to the
  agent as it is. The agent reads this README, the job's file, and the input batch named in the prompt — nothing else
  is needed and nothing else may be edited.
- **Output** is one JSON file (or Markdown for notes/translate) at the path the prompt names. No other files, no
  edits to anything in the repository, no commits, no downloads. Valid JSON only: no comments, no trailing text.
- **Every input item gets exactly one output item**, with the same `id`, in any order. Never skip an item — when
  unsure, answer with a low `confidence` and say why in `note`.
- **Language**: English for every field unless the job says otherwise. Use the course's own terms (syllabus wording).
- **Copyright**: SCSA papers and keys are copyrighted. Output may quote at most a short phrase (≤ 8 words) of them.
  Describe what is asked and rewarded in your own words.
- **Confidence** is a number 0–1: 0.9+ the key leaves no doubt; 0.7–0.9 sure but another reading exists; below 0.7
  say what is unclear in `note`. `check` sends everything below 0.7 to review.
- **Report**: after writing the file, reply in Chinese, one short paragraph: the model you are (first line), items
  written, how many below 0.7, anything in the input that looked broken.
