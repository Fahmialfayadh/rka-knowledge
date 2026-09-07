# Machine Learning (ML) — RKA

> Kurikulum ML RKA — vendor copy dari [kcv-if/Modul-ML-RKA](https://github.com/kcv-if/Modul-ML-RKA) (`46e0089` main), diperlakukan setara dengan matkul lain (bukan sekadar `external/`).

## Sumber
- **Upstream:** https://github.com/kcv-if/Modul-ML-RKA
- **Snapshot:** `46e0089` — "add knn image" (2026-09-07)
- **Vendor raw:** `external/Modul-ML-RKA/` (preserve original)
- **Kurasi:** `courses/machine-learning/materi/` (copy terstruktur, siap baca)

Lihat `external/ATTRIBUTION.md` untuk lisensi.

## Struktur

```
materi/
├── Supervised Learning/   # Linear/Polynomial/Ridge-Lasso/Logistic/KNN/SVM/SVR/DecisionTree/ANN/NaiveBayes
├── Unsupervised Learning/ # K-Means/Hierarchical/DBSCAN/BIRCH
├── Deep Learning/         # ANN/CNN
├── Reinforcement Learning/ # RL.md
└── Deployment/            # deployment.md
```

## Daftar Materi (24 files)

**Supervised Learning**
- `Supervised Learning/LinearRegression.md`, `PolynomialRegression.md`, `LassoRidgeRegression.md`
- `LogisticRegression.md`, `KNN.md`, `SVM.md`, `SVR.md`, `DecisionTreeClassifier.md`, `DecisionTreeRegressor.md`, `ANN.md`, `NaiveBayes/NaiveBayes.md`

**Unsupervised Learning**
- `Unsupervised Learning/K-Means.md`, `Hierarchical.md`, `DBSCAN.md`, `BIRCH.md`

**Deep Learning**
- `Deep Learning/ANN.md`, `CNN.md`

**RL & Deployment**
- `Reinforcement Learning/RL.md`, `Deployment/deployment.md`

## Cara Pakai
Buka `materi/<Topik>/README.md` lalu lanjut ke `*.md` per algoritma. Tiap modul berisi penjelasan konseptual + implementasi Python + contoh kasus.

## Sinkronisasi
```bash
./scripts/sync-external.sh
# otomatis update external/ dan courses/machine-learning/materi/
```
