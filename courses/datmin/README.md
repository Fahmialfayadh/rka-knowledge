# Data Mining (Datmin) — RKA

> Matkul Data Mining Semester 3 (4 SKS) — tahapan, praproses, class imbalance, ensemble, association, sequential, clustering, anomali. Diperlakukan setara dengan matkul lain: lokal + vendor copy KCV.

## Sumber
- **Lokal:** `materi/Rangkuman Data Mining Week 1.pdf` (kurasi Week 1)
- **Upstream:** [kcv-if/Modul-DM-RKA](https://github.com/kcv-if/Modul-DM-RKA) (`cfa1d6c` master)
- **Vendor raw:** `external/Modul-DM-RKA/` (preserve original, 7 modul)
- **Kurasi:** `courses/datmin/modul/` (copy terstruktur)

Lihat `external/ATTRIBUTION.md` & `external/Modul-DM-RKA/README.md` untuk CPMK & etika data.

## Struktur

```
materi/                          # lokal
└── Rangkuman Data Mining Week 1.pdf

modul/                           # dari Modul-DM-RKA (7 topik)
├── 0 - Panduan Instalasi.pdf
├── 1 - EDA/                     # Eksplorasi Data (ipynb + csv)
├── 2 - Preprocessing/           # Praproses Data
├── 3 - Ensemble/                # Ensemble & Class Imbalance
├── 4 - Association/             # Association Rule
├── 5 - Sequential/              # Sequential Pattern Analysis
├── 6 - Clustering/              # Clustering Advanced
└── 7 - Anomaly/                 # Deteksi Anomali
```

## CPMK (dari README upstream)
- Tahapan, karakteristik, eksplorasi & praproses data
- Class imbalance & ensemble
- Association rule & sequential pattern
- Clustering
- Deteksi anomali

## Daftar Modul (15 files)

| # | Folder | File | Deskripsi |
|---|---|---|---|
| 0 | `0 - Panduan Instalasi.pdf` | — | install Python, NumPy, Pandas, Sklearn, Colab |
| 1 | `1 - EDA/` | `1 - Eksplorasi Data.ipynb`, `pelanggan_toko_online.csv` | EDA |
| 2 | `2 - Preprocessing/` | `2 - Praproses Data.ipynb`, `2 - dataset-exercise.zip` | Praproses |
| 3 | `3 - Ensemble/` | `3 - Classification (Ensemble...).ipynb` | Ensemble & Imbalance |
| 4 | `4 - Association/` | `4 - Association Rule.ipynb` | Association |
| 5 | `5 - Sequential/` | `5 - Sequential Pattern Analysis.ipynb` | Sequential |
| 6 | `6 - Clustering/` | `6 - Clustering (Advance).ipynb`, `Dataset_Tugas.csv` | Clustering |
| 7 | `7 - Anomaly/` | `7 - Deteksi Anomali.ipynb` | Anomaly |

## Etika Data
Baca `external/Modul-DM-RKA/README.md` → Pernyataan Etika: gunakan dataset berlisensi/open-source, hindari dark web, patuhi PDP.

## Cara Pakai
1. Baca `materi/Rangkuman Data Mining Week 1.pdf` (lokal)
2. Lanjut `modul/1 - EDA/1 - Eksplorasi Data.ipynb` → `modul/7 - Anomaly/`
3. Install via `modul/0 - Panduan Instalasi.pdf`

## Sinkronisasi
```bash
./scripts/sync-external.sh
# update external/ & courses/datmin/modul/
```
