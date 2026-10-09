"""Rebuild every derived file from the papers. One job: run the pipeline steps in order.

papers -> questions.json -> topic PDFs + question banks -> wace.db (methods notes and tags are hand-written inputs)
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["segment.py", "build_docs.py", "build_bank.py", "build_db.py"]

if __name__ == "__main__":
    subjects = sys.argv[1:] or ["MAM", "MAS"]
    for step in STEPS:
        print(f"== {step}", flush=True)
        args = [] if step == "build_db.py" else subjects
        subprocess.run([sys.executable, os.path.join(HERE, step), *args], check=True)
