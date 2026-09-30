"""Split construction and leakage audit (Section 3 and Appendix D of the paper), CPU only.

  * exact duplicates in the released training and test sets, and the resulting split sizes;
  * the patient-disjoint validation split (written to results/splits/*.csv);
  * near-duplicate audit of the official test split against the training pool (NCC sweep);
  * the 64-bit difference-hash check the paper rejects (Hamming radius 5).

Writes results/audit/*.csv and results/splits/*.csv.   Run: python src/audit.py
"""
import csv
import os

import numpy as np

from imaging import best_match, dhash_bits, min_hamming, ncc_vectors, rel
from kermany import ROOT, base_dir, group, label, released, study_split

RES = os.environ.get("RESULTS_DIR", os.path.join(ROOT, "results"))
SWEEP = [0.90, 0.95, 0.98, 0.99, 0.995]


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def main():
    s = study_split()
    base = base_dir()
    for name in ["train", "val", "test"]:
        write_csv(os.path.join(RES, "splits", f"{name}.csv"), ["path", "label", "group"],
                  [[rel(p, base), label(p), group(p)] for p in s[name]])
    split_rows = [
        ["released train images", len(released("train"))],
        ["released test images", len(released("test"))],
        ["exact duplicate copies removed from train", s["dup_train"]],
        ["exact duplicate copies removed from test", s["dup_test"]],
        ["training pool after removal", len(s["pool"])],
        ["patient/study groups in training pool", s["n_groups"]],
        ["groups in validation split", s["n_val_groups"]],
        ["train images", len(s["train"])],
        ["validation images", len(s["val"])],
        ["test images", len(s["test"])],
        ["test positive rate (released)", round(np.mean([label(p) for p in released("test")]), 3)],
    ]
    write_csv(os.path.join(RES, "audit", "split_summary.csv"), ["quantity", "value"], split_rows)

    # near-duplicate audit: every released test image against the released training set
    tr, te = released("train"), released("test")
    best, _ = best_match(ncc_vectors(te), ncc_vectors(tr))
    write_csv(os.path.join(RES, "audit", "ncc_sweep.csv"), ["threshold", "n_test_flagged", "n_test"],
              [[t, int((best >= t).sum()), len(te)] for t in SWEEP])
    ham = min_hamming(dhash_bits(te), dhash_bits(tr))
    write_csv(os.path.join(RES, "audit", "dhash_radius5.csv"), ["n_test", "flagged", "flagged_pct"],
              [[len(te), int((ham <= 5).sum()), round(100 * (ham <= 5).mean(), 1)]])

    for name in ["split_summary", "ncc_sweep", "dhash_radius5"]:
        print(f"\n{name}.csv")
        with open(os.path.join(RES, "audit", f"{name}.csv")) as f:
            print(f.read().strip())


if __name__ == "__main__":
    main()
