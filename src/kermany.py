"""The Kermany chest X-ray corpus and the study's split policy.

Split policy (paper, Section 3):
  * exact byte-level duplicates are removed (later copies dropped) from the released training and
    test sets;
  * the 16-image official validation set is not used;
  * a patient-disjoint validation split is drawn from the released training pool: images are grouped
    by the patient/study key in the file name (person<id> for pneumonia, IM-<id> for normal, with the
    NORMAL2- prefix ignored) and 15% of the groups of each class go to validation;
  * the official test split is left untouched apart from exact-duplicate removal.

data/download.py writes data/paths.json with the local folder of the dataset.
"""
import json
import os
import re

import numpy as np

from imaging import list_images, md5

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PATHS_FILE = os.path.join(ROOT, "data", "paths.json")
CLASSES = ["NORMAL", "PNEUMONIA"]
VAL_FRACTION = 0.15
SEED = 0


def base_dir():
    if not os.path.exists(PATHS_FILE):
        raise SystemExit("data/paths.json not found: run `python data/download.py` first")
    with open(PATHS_FILE) as f:
        return os.path.join(json.load(f)["kermany"], "chest_xray")


def released(split):
    """Image paths of a released split (train | val | test), sorted."""
    return list_images(os.path.join(base_dir(), split))


def label(path):
    """1 for pneumonia, 0 for normal (from the class folder)."""
    return int(os.path.basename(os.path.dirname(path)) == "PNEUMONIA")


def group(path):
    """Patient/study key encoded in the file name."""
    name = os.path.basename(path)
    m = re.match(r"(person\d+)_", name)
    if m:
        return m.group(1)
    m = re.match(r"(?:NORMAL2-)?(IM-\d+)-", name)
    if m:
        return m.group(1)
    return name


def drop_exact_duplicates(paths):
    """(kept paths, number of dropped copies): keeps the first file of every MD5 class."""
    seen, kept = set(), []
    for p in paths:
        h = md5(p)
        if h not in seen:
            seen.add(h)
            kept.append(p)
    return kept, len(paths) - len(kept)


def study_split():
    """dict with train / val / test path lists and bookkeeping counts."""
    pool, dup_train = drop_exact_duplicates(released("train"))
    test, dup_test = drop_exact_duplicates(released("test"))
    rng = np.random.default_rng(SEED)
    val_groups = set()
    for c in [0, 1]:
        groups = sorted({group(p) for p in pool if label(p) == c})
        order = rng.permutation(len(groups))
        val_groups |= {groups[i] for i in order[: int(VAL_FRACTION * len(groups))]}
    train = [p for p in pool if group(p) not in val_groups]
    val = [p for p in pool if group(p) in val_groups]
    return dict(pool=pool, train=train, val=val, test=test, dup_train=dup_train, dup_test=dup_test,
                n_groups=len({group(p) for p in pool}), n_val_groups=len(val_groups))
