"""Offline provider: canned replies per pipeline stage, for testing without an API key."""
import json, re

REPLIES = {
    "GENERATE": {"section": "CalcFree", "question": (
        "Let $f(x) = x^3 - 3x + 1$, graphed below. Entry costs \\$2.\n(a) Determine $f'(x)$. (1 mark)\n"
        "(b) Determine the coordinates of the stationary points of $f$ and state their nature. (4 marks)\n"
        "$$\\int_0^1 f(x)\\,dx = \\frac{1}{4}$$"),
        "figure": {"x": [-2.5, 2.5], "y": [-2, 4], "items": [
            {"curve": "x**3 - 3*x + 1", "label": "$y=f(x)$"}, {"point": [-1, 3], "label": "$A$"},
            {"point": [1, -1], "label": "$B$", "pos": "SE"}, {"fill": "x**3 - 3*x + 1", "from_x": 0, "to_x": 0.3}]},
        "parts": [{"label": "a", "marks": 1, "answer": "f′(x) = 3x² − 3", "value": "3*x**2 - 3"},
                  {"label": "b", "marks": 4, "answer": "(−1, 3) local maximum; (1, −1) local minimum", "value": "[-1, 1]"}]},
    "SOLVE": {"parts": [{"label": "a", "working": "power rule", "answer": "3x² − 3", "value": "3*x**2 - 3", "sympy": "diff(x**3 - 3*x + 1, x)"},
                        {"label": "b", "working": "3x² − 3 = 0 → x = ±1; f″(x) = 6x",
                         "answer": "max (−1, 3), min (1, −1)", "value": "[-1, 1]", "sympy": "solve(diff(x**3 - 3*x + 1, x), x)"}]},
    "VERIFY": {"parts": [{"label": "a", "agree": True, "correct_answer": "f′(x) = 3x² − 3", "note": ""},
                         {"label": "b", "agree": True, "correct_answer": "(−1, 3) local max; (1, −1) local min",
                          "note": ""}], "well_posed": True, "verdict": "pass", "feedback": ""},
    "MARKS": {"solution": "(a) f′(x) = 3x² − 3\n(b) f′(x) = 0 ⇒ x = ±1. f(−1) = 3, f(1) = −1. "
                          "f″(x) = 6x: f″(−1) = −6 < 0 so (−1, 3) is a local maximum; f″(1) = 6 > 0 so (1, −1) "
                          "is a local minimum.",
              "points": [{"label": "a", "text": "differentiates correctly"},
                         {"label": "b", "text": "equates f′(x) to zero"},
                         {"label": "b", "text": "solves for both x values"},
                         {"label": "b", "text": "determines both y coordinates"},
                         {"label": "b", "text": "justifies the nature of each point using f″ or a sign test"}]},
}


SKETCH = "\n(c) On the axes below, sketch the graph of $y = f(x)$, labelling the stationary points. (2 marks)"
CURVE = {"x": [-2.5, 2.5], "y": [-2, 4], "items": [{"curve": "x**3 - 3*x + 1"}, {"point": [-1, 3]}, {"point": [1, -1]}]}


def with_drawing(stage, reply):
    """The same canned question plus a drawing part (c), for prompts that require one."""
    reply = json.loads(json.dumps(reply))
    c = {"label": "c", "marks": 2}
    if stage == "GENERATE":
        reply["question"] += SKETCH
        reply["parts"].append({**c, "answer": "cubic through (−1, 3) and (1, −1)", "value": None})
    elif stage == "SOLVE":
        reply["parts"].append({"label": "c", "working": "sketch", "answer": "sketch", "value": None, "sympy": None})
    elif stage == "VERIFY":
        reply["parts"].append({"label": "c", "agree": True, "correct_answer": "cubic through (−1, 3), (1, −1)"})
    elif stage == "MARKS":
        reply["points"] += [{"label": "c", "text": "correct cubic shape"},
                            {"label": "c", "text": "stationary points labelled"}]
        reply["figures"] = {"c": CURVE}
    return reply


def setup(k):
    def chat(settings, system, user, timeout):
        stage = re.match(r"\[STAGE:(\w+)\]", system).group(1)
        if stage == "EXPLAIN":
            return "1. 这一问考什么\n（离线 mock 讲解）\n2. 你丢的分\n…\n3. 正确做法\n…\n4. 下次怎么避免\n…"
        reply = REPLIES.get(stage, {"ok": True})
        if "DRAWING PART REQUIRED" in user or "sketch the graph of $y = f(x)$" in user:
            reply = with_drawing(stage, reply)
        return "```json\n" + json.dumps(reply, ensure_ascii=False) + "\n```"

    k.get("llm.providers")["mock"] = chat
