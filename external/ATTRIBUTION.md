# Attribution — External Modules (Vendor Copy)

This directory contains vendor-copied snapshots of external repositories curated by **KCV - Laboratorium Kecerdasan Cerdas Visual, Departemen Teknik Informatika ITS**.

> **Policy:** Vendor copy (snapshot), not git submodule — self-contained, no `--recurse-submodules` needed. Update manually via `scripts/sync-external.sh`.

## Modul-ML-RKA
- **Source:** https://github.com/kcv-if/Modul-ML-RKA
- **Branch:** `main`
- **Snapshot commit:** `46e0089` — "add knn image" (2026-09-07)
- **Path:** `external/Modul-ML-RKA/`
- **Contents:** 163 commits, covers Supervised Learning (Linear/Polynomial/Ridge-Lasso/Logistic/KNN/SVM/SVR/DecisionTree/ANN/NaiveBayes), Unsupervised (K-Means/Hierarchical/DBSCAN/BIRCH), Deep Learning (ANN/CNN), Reinforcement Learning, Deployment.
- **License:** As per upstream (see upstream README). Include original LICENSE if provided.
- **Update:** `git clone --depth 1 https://github.com/kcv-if/Modul-ML-RKA /tmp/Modul-ML-RKA && rsync -av --exclude=".git" /tmp/Modul-ML-RKA/ external/Modul-ML-RKA/`

## Modul-DM-RKA
- **Source:** https://github.com/kcv-if/Modul-DM-RKA
- **Branch:** `master`
- **Snapshot commit:** `cfa1d6c` — "chore(modul-1): sisakan hanya dataset yang dipakai notebook" (2026-09-07)
- **Path:** `external/Modul-DM-RKA/`
- **Contents:** 37 commits, covers Praktikum Data Mining — EDA, Preprocessing, Ensemble & Class Imbalance, Association Rule, Sequential Pattern, Clustering, Anomaly Detection.
- **License:** As per upstream.
- **Update:** `git clone --depth 1 https://github.com/kcv-if/Modul-DM-RKA /tmp/Modul-DM-RKA && rsync -av --exclude=".git" /tmp/Modul-DM-RKA/ external/Modul-DM-RKA/`

## How to Sync
```bash
./scripts/sync-external.sh
# or manually:
git clone --depth 1 https://github.com/kcv-if/Modul-ML-RKA /tmp/Modul-ML-RKA
rsync -av --delete --exclude=".git" /tmp/Modul-ML-RKA/ external/Modul-ML-RKA/
git clone --depth 1 https://github.com/kcv-if/Modul-DM-RKA /tmp/Modul-DM-RKA
rsync -av --delete --exclude=".git" /tmp/Modul-DM-RKA/ external/Modul-DM-RKA/
# record new hash in this file
```

Keep this file updated with the latest snapshot hash after each sync.
