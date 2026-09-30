# Data

No images are included in this repository. The corpus is public and is downloaded with

```bash
python data/download.py
```

| Dataset | Source | Version |
|---|---|---|
| Chest X-Ray Images (Pneumonia), Kermany et al. 2018: 5,216 train / 16 val / 624 test | [kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) | 2 |

The original release is at [data.mendeley.com/datasets/rscbjbr9sj/2](https://data.mendeley.com/datasets/rscbjbr9sj/2)
(CC BY 4.0). The images stay in the kagglehub cache; `data/paths.json` records where they are and is ignored by git.

Public Kaggle datasets can usually be downloaded without an account. If kagglehub asks for credentials, set the
`KAGGLE_USERNAME` and `KAGGLE_KEY` environment variables; never commit them.

`src/audit.py` writes the split lists to `results/splits/` (relative paths, labels and patient/study keys).
