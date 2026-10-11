"""External tag proposals using the user's configured llm.chat and a shared, maintained tagging skill."""
import json
from pathlib import Path


def classify(chat, skill, catalogue, question, answer, language="zh"):
    if not question.strip() or not answer.strip():
        raise ValueError("AI 标注需要题目和答案文字；扫描件请先补充文字")
    system = "[STAGE:EXTERNAL_TAG]\n" + skill + "\nReturn the reason in " + ("English." if language == "en" else "Chinese.")
    payload = json.dumps(dict(catalogue=catalogue, question=question, answer=answer), ensure_ascii=False)
    response = chat(system, payload).strip()
    if response.startswith("```"):
        response = "\n".join(response.splitlines()[1:-1])
    try:
        result = json.loads(response)
    except (ValueError, TypeError) as exc:
        raise ValueError("AI 标注回复不是有效的 JSON") from exc
    allowed = {row["code"] for row in catalogue}
    if (not isinstance(result, dict) or not isinstance(result.get("tags"), list)
            or any(not isinstance(tag, str) or tag not in allowed for tag in result["tags"])
            or not isinstance(result.get("reason"), str) or not result["reason"].strip()
            or type(result.get("uncertain")) is not bool):
        raise ValueError("AI 标注回复的标签或理由无效")
    result["tags"] = sorted(set(result["tags"]))
    if not result["tags"] and not result["uncertain"]:
        raise ValueError("没有匹配题型时必须注明不确定")
    return result


def setup(k):
    def propose(qid):
        store = k.get("external.store")()
        q = store.question(qid)
        catalogue = [dict(code=code, title=title, method=method) for code, title, method in
            k.get("store").q("SELECT code,title,method FROM patterns WHERE code LIKE ? ORDER BY topic,n", q["subject"] + ".%")]
        path = Path(k.root) / "skills" / "wace-external-tagging" / "SKILL.md"
        skill = path.read_text(encoding="utf-8")
        answer = k.get("external.pdf.text")(store.asset(q["answer"]), q["answer_regions"])
        # Manual answer transcription supports scan-only PDFs; the crop remains the source of truth.
        answer = q.get("answer_text") or answer
        return classify(k.get("llm.chat"), skill, catalogue, q["stem"], answer, k.get("config").get("language", "zh"))

    k.provide("external.tag.propose", propose)
