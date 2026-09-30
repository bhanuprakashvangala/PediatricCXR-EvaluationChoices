"""Download the Kermany pediatric chest X-ray corpus with kagglehub and record where it is.

    pip install kagglehub
    python data/download.py

Public Kaggle datasets can usually be fetched without an account; if Kaggle asks for credentials,
set KAGGLE_USERNAME and KAGGLE_KEY (see https://github.com/Kaggle/kagglehub). The images stay in the
kagglehub cache (about 2.4 GB); only data/paths.json is written here.
"""
import json
import os

import kagglehub

HERE = os.path.dirname(os.path.abspath(__file__))
# Kermany et al. (2018), Kaggle mirror: train/val/test = 5,216/16/624
HANDLE = "paultimothymooney/chest-xray-pneumonia/versions/2"


def main():
    path = kagglehub.dataset_download(HANDLE)
    print(f"kermany {HANDLE} -> {path}")
    with open(os.path.join(HERE, "paths.json"), "w") as f:
        json.dump({"kermany": path}, f, indent=1)
    print("wrote data/paths.json")


if __name__ == "__main__":
    main()
