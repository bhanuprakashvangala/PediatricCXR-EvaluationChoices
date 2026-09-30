"""Download the corpus, build the splits, run the duplicate audit and compare with the paper.

    python scripts/reproduce.py

About 5 minutes on a laptop CPU, plus download time.
"""
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run(*args):
    print(f"\n$ python {' '.join(args)}", flush=True)
    subprocess.run([sys.executable, *args], check=True, cwd=ROOT)


def main():
    run("data/download.py")
    run("src/audit.py")
    run("src/compare_to_paper.py")


if __name__ == "__main__":
    main()
