"""English edition. One job: translate the Chinese content and UI strings with the configured model (DeepSeek
by default — cheap), caching every chunk so re-runs cost nothing.

  python tools/translate.py docs     methods notes + review logs + cheat sheets -> *_en / methods_en
  python tools/translate.py ui       CJK runs in app/ code (+ ones seen at run time) -> app/i18n/en.json

Docs keep Markdown, tables, LaTeX, code, numbers and question references; "## 题型 N：title" becomes
"## Pattern N: title" so tools/build_db.py can read the English notes too.
"""
import glob, hashlib, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app")
CACHE = os.path.join(ROOT, "tools", "i18n_cache.json")
CJK = re.compile(r"[㐀-鿿　-〿＀-￯“”‘’·★☆]+")
HAS_CJK = re.compile(r"[㐀-鿿]")
PUNCT = {"：": ": ", "，": ", ", "。": ". ", "；": "; ", "（": " (", "）": ") ", "、": ", ", "「": "“", "」": "”",
         "？": "? ", "！": "! ", "·": "·", "—": "—", "…": "…", "“": "“", "”": "”"}

DOC_PROMPT = (
    "Translate this Chinese study note for Year 12 students of WACE Mathematics (Western Australia) into clear, "
    "concise Australian English. Keep exactly as they are: the Markdown structure (headings, lists, tables, "
    "blockquotes), all LaTeX and maths, code spans, numbers, question references such as 2024A-Q12(c) or 2016S F4, "
    "★ markers, and English terms already present. Translate a heading '题型 N：title' as 'Pattern N: title'. "
    "Do not add or drop content, do not comment. Output only the translated Markdown.")
UI_PROMPT = (
    "You translate the Chinese user-interface text of a maths study app for WACE students into short, natural English "
    "UI text. Each item is a Chinese fragment cut out of a longer string (shown as context); numbers and names are "
    "inserted around it at run time, so translate only the fragment, keep its leading/trailing role (e.g. '共' -> "
    "'total', '分' -> 'marks'), no quotes. Glossary: 题型 = pattern, 知识点 = topic, 知识图谱 = knowledge tree, "
    "错题本 = mistake book, 得分点 = mark points, 评分标准 = marking key, 真题/真卷 = past paper. "
    "Reply with ONE JSON object mapping each id to its English text.")


def kernel():
    sys.path.insert(0, APP)
    from kernel import Kernel
    k = Kernel(ROOT)
    k.load(["config", "llm", "llm_openai", "llm_anthropic", "llm_mock"])
    return k


def load_cache():
    return json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}


def chunks(md, limit=4500):
    """Split at '## ' headings into pieces of at most ~limit characters."""
    out, cur = [], ""
    for block in re.split(r"(?m)^(?=## )", md):
        if cur and len(cur) + len(block) > limit:
            out.append(cur)
            cur = ""
        cur += block
    if cur:
        out.append(cur)
    return out


def docs(k):
    chat, cache = k.get("llm.chat"), load_cache()
    jobs = []
    for src in sorted(glob.glob(os.path.join(ROOT, "M??", "methods", "*.md"))):
        name = os.path.basename(src).replace("_解题思路", "_Methods").replace("审校记录", "Review_log")
        jobs.append((src, os.path.join(os.path.dirname(os.path.dirname(src)), "methods_en", name)))
    for src in sorted(glob.glob(os.path.join(ROOT, "cheatsheet", "*_CheatSheet.md"))):
        jobs.append((src, src[:-3] + "_EN.md"))
    pieces = [(dst, i, c) for src, dst in jobs for i, c in enumerate(chunks(open(src, encoding="utf-8").read()))]
    todo = [c for _, _, c in pieces if hashlib.sha1(c.encode()).hexdigest() not in cache and HAS_CJK.search(c)]
    print(f"{len(jobs)} files, {len(pieces)} chunks, {len(todo)} to translate")

    def one(c):
        out = chat(DOC_PROMPT, c).strip()
        out = re.sub(r"^```(?:markdown)?\n|\n```$", "", out)  # some models wrap the reply in a code fence
        return hashlib.sha1(c.encode()).hexdigest(), out

    with ThreadPoolExecutor(8) as pool:
        for n, (h, out) in enumerate(pool.map(one, todo), 1):
            cache[h] = out
            if n % 5 == 0 or n == len(todo):
                json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
                print(f"  {n}/{len(todo)}", flush=True)
    by_file = {}
    for dst, i, c in pieces:
        by_file.setdefault(dst, []).append(cache.get(hashlib.sha1(c.encode()).hexdigest(), c))
    for dst, parts in by_file.items():
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        text = "\n".join(p.rstrip("\n") + "\n" for p in parts)
        open(dst, "w", encoding="utf-8").write(text)
        left = len(HAS_CJK.findall(text))
        print(f"{os.path.relpath(dst, ROOT)}  ({left} CJK characters left)")


def ui_runs():
    """{fragment: context line} from app code, plus fragments recorded at run time (i18n/missing.txt)."""
    runs = {}
    for f in sorted(glob.glob(os.path.join(APP, "**", "*.py"), recursive=True)) + [os.path.join(APP, "setup.txt")]:
        for line in open(f, encoding="utf-8"):
            if line.lstrip().startswith("#"):
                continue
            for m in CJK.finditer(line):
                if HAS_CJK.search(m.group(0)):
                    runs.setdefault(m.group(0), line.strip()[:160])
    missing = os.path.join(APP, "i18n", "missing.txt")
    if os.path.exists(missing):
        for line in open(missing, encoding="utf-8"):
            run, _, ctx = line.rstrip("\n").partition("\t")
            if run:
                runs.setdefault(run, ctx)
    return runs


def ui(k):
    chat = k.get("llm.chat")
    path = os.path.join(APP, "i18n", "en.json")
    table = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    todo = [(r, c) for r, c in ui_runs().items() if r not in table]
    print(f"{len(todo)} UI fragments to translate")
    batches = [todo[i:i + 60] for i in range(0, len(todo), 60)]

    def one(batch):
        items = [{"id": str(i), "text": r, "context": c} for i, (r, c) in enumerate(batch)]
        reply = chat(UI_PROMPT, json.dumps(items, ensure_ascii=False))
        got = json.loads(reply[reply.index("{"): reply.rindex("}") + 1])
        return {r: str(got[str(i)]).strip() for i, (r, _) in enumerate(batch) if str(i) in got}

    with ThreadPoolExecutor(6) as pool:
        for got in pool.map(one, batches):
            table.update(got)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(dict(sorted(table.items())), open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    missing = os.path.join(APP, "i18n", "missing.txt")
    if os.path.exists(missing):
        os.remove(missing)
    print(f"{len(table)} entries in {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    what = sys.argv[1:] or ["docs", "ui"]
    k = kernel()
    for w in what:
        {"docs": docs, "ui": ui}[w](k)
