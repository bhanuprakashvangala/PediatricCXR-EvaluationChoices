# Evaluation Choices Shape Biomedical ML Claims

Data preparation and audit code for **Evaluation Choices Shape Biomedical ML Claims: A Pediatric Pneumonia Benchmark Case Study**
Bhanu Prakash Vangala, Sowmya Guda, Latha Peddi, Navya Vangala.
Under review at the [RCMLR Workshop](https://translatingmlresearch.github.io/RCMLR/) (Responsible Communication of Machine Learning Research in Biomedicine) at NeurIPS 2026.

The study measures how much a reported score on the Kermany pediatric chest X-ray benchmark moves with the split,
the backbone training, the decision threshold and where calibration is fitted. This repository has the data side of
the study: the split policy (exact-duplicate removal and a patient-disjoint validation split) and the near-duplicate
audit of the official test split. It runs on a CPU and needs no trained model.

## Layout

```
data/        download script for the Kermany corpus (no images are included)
src/         kermany.py            split policy: exact-duplicate removal, patient-disjoint validation split
             audit.py              split sizes, NCC near-duplicate audit, difference-hash check (Section 3, Appendix D)
             compare_to_paper.py   checks each number against the paper
             imaging.py            image loading, NCC and hashing helpers
scripts/     reproduce.py, the single entry point
results/     audit/            outputs of audit.py (CSV)
             splits/           train / validation / test lists written by audit.py (relative paths, labels, patient keys)
```

## Setup

```bash
git clone https://github.com/bhanuprakashvangala/PediatricCXR-EvaluationChoices.git
cd PediatricCXR-EvaluationChoices
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Reproduce

```bash
python scripts/reproduce.py
```

This downloads the corpus (about 2.4 GB, into the kagglehub cache), builds the splits, runs the audit and checks
every number against the paper. It takes about 5 minutes on a laptop CPU plus download time. See `data/README.md`
for the dataset source.

## Split policy

- Exact byte-level duplicates are removed from the released training and test sets (later copies dropped).
- The 16-image official validation set is not used.
- Images in the released training pool are grouped by the patient/study key in the file name (`person<id>` for
  pneumonia, `IM-<id>` for normal, ignoring the `NORMAL2-` prefix), and 15% of the groups of each class are drawn
  for validation with `numpy.random.default_rng(0)`.
- The official test split is otherwise left untouched.

## Results

All values below are recomputed by `scripts/reproduce.py` and equal the values in the paper
(`python src/compare_to_paper.py` checks all 7).

| | |
|---|---|
| Released training / test images | 5,216 / 624 |
| Exact duplicate copies in the released training / test sets | 26 / 6 |
| Train / validation / test images after the split policy | 4,420 / 770 / 618 |
| Pneumonia share of the official test split | 62.5% |
| Test images with a near-twin in training at NCC >= 0.98 / >= 0.95 | 0 / 14 |
| Test images flagged by a 64-bit difference hash at Hamming radius 5 | 93.3% |

The difference hash flags almost the whole test set even though no test image has a near-twin at NCC >= 0.98, which
is why the audit uses NCC.

## Citation

```bibtex
@misc{vangala2026evaluationchoicesshapebiomedical,
      title={Evaluation Choices Shape Biomedical ML Claims: A Pediatric Pneumonia Benchmark Case Study},
      author={Bhanu Prakash Vangala and Sowmya Guda and Latha Peddi and Navya Vangala},
      year={2026},
      eprint={2609.37848},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2609.37848},
}
```

## License

Code and split lists: MIT. The Kermany dataset is third-party (CC BY 4.0); see `data/README.md`.
