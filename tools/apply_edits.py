"""Apply exact (old -> new) replacements to a file; fail loudly if any old text is missing."""
import json, sys
path, edits = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
t = open(path, encoding="utf-8").read()
for old, new in edits:
    assert t.count(old) == 1, f"not unique/missing: {old[:60]}"
    t = t.replace(old, new)
open(path, "w", encoding="utf-8").write(t)
print(path, len(edits), "edits")
