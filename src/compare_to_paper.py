"""Compare the audit outputs in results/audit/ with the values printed in the paper.

    python src/compare_to_paper.py
"""
import csv
import os
import sys

from kermany import ROOT

AUD = os.path.join(os.environ.get("RESULTS_DIR", os.path.join(ROOT, "results")), "audit")


def get(name, key_col, key, col):
    path = os.path.join(AUD, name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        for r in csv.DictReader(f):
            if r[key_col] == key:
                return r[col]
    return None


def checks():
    S, N = "split_summary.csv", "ncc_sweep.csv"
    q = lambda k: get(S, "quantity", k, "value")  # noqa: E731
    return [
        ("released train / test images", "5216 / 624", f"{q('released train images')} / {q('released test images')}", None),
        ("exact duplicate copies in released train / test", "26 / 6",
         f"{q('exact duplicate copies removed from train')} / {q('exact duplicate copies removed from test')}", None),
        ("train / validation / test images", "4420 / 770 / 618",
         f"{q('train images')} / {q('validation images')} / {q('test images')}", None),
        ("official test positive rate", "0.625", q("test positive rate (released)"), 0.0005),
        ("test images with NCC >= 0.98 twin in train", "0", get(N, "threshold", "0.98", "n_test_flagged"), 0),
        ("test images with NCC >= 0.95 twin in train", "14", get(N, "threshold", "0.95", "n_test_flagged"), 0),
        ("dHash radius 5 flags test, %", "93", get("dhash_radius5.csv", "n_test", "624", "flagged_pct"), 0.5),
    ]


def main():
    print(f"{'claim':52s} | {'paper':18s} | {'reproduced':18s} | match")
    print("-" * 104)
    n_run = n_ok = 0
    for claim, paper, got, tol in checks():
        if got is None or "None" in str(got):
            status, got = "not run", "-"
        else:
            n_run += 1
            ok = got == paper if tol is None else abs(float(got) - float(paper)) <= tol
            n_ok += ok
            status = "yes" if ok else "no"
        print(f"{claim:52s} | {paper:18s} | {str(got):18s} | {status}")
    print(f"\n{n_ok}/{n_run} values match the paper.")
    if n_ok < n_run:
        sys.exit(1)


if __name__ == "__main__":
    main()
