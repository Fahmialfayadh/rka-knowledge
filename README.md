# RKA Knowledge — ITS

> Materi Rekayasa Kecerdasan Artifisial (RKA), Departemen Teknik Informatika ITS.

## Struktur

```
rka-knowledge/
├── README.md
├── CONTRIBUTING.md
└── courses/
    ├── aljabar-linear/
    ├── basis-data/
    ├── bluecamp/
    ├── dasar-pemrograman/
    ├── data-mining/
    ├── kalkulus-2/
    ├── kecerdasan-komputasional/
    ├── konsep-kecerdasan-artifisial/
    ├── machine-learning/
    ├── matematika-diskrit/
    ├── perancangan-dan-analisis-algoritma/
    ├── probabilitas-dan-statistika/
    ├── struktur-data/
    └── teori-graf/
```

Tiap `courses/<slug>/`:

```
courses/<slug>/
├── README.md
├── slides/pdf/
├── materi/ | modul/
├── tugas/ | praktikum/ | projects/
└── assets/
```

## Daftar Mata Kuliah

| # | Slug | Nama | Isi |
|---|---|---|---|
| 1 | `aljabar-linear` | Aljabar Linear | `notebooks/women-s-shoes-prices-analysis.ipynb` |
| 2 | `basis-data` | Basis Data | `projects/studenttracker` (Django) |
| 3 | `bluecamp` | Bluecamp — Studi Literatur | `materi/studiliteratur.md` (APA, Harvard, MLA, Mendeley) |
| 4 | `dasar-pemrograman` | Dasar Pemrograman | `tugas/` (backtracking, flood-fill, search, sorting, text-file) |
| 5 | `data-mining` | Data Mining | `materi/` + `modul/0-7` (EDA, preprocessing, ensemble, association, sequential, clustering, anomali) |
| 6 | `machine-learning` | Machine Learning | `materi/` (supervised, unsupervised, deep learning, reinforcement learning, deployment) |
| 7 | `kalkulus-2` | Kalkulus 2 | `materi/` + `modul/01-11` + `images/` |
| 8 | `kecerdasan-komputasional` | Kecerdasan Komputasional | `materi/` + `praktikum/` (Wumpus World, logical agents) + `slides/pdf/` |
| 9 | `konsep-kecerdasan-artifisial` | Konsep Kecerdasan Artifisial | `materi/` + `praktikum/` + `projects/WAR` + `tugas/` + `slides/pdf/` |
| 10 | `matematika-diskrit` | Matematika Diskrit | `projects/risiko-stroke` (Flask) |
| 11 | `perancangan-dan-analisis-algoritma` | Perancangan dan Analisis Algoritma | `slides/pdf/portofolio-perancangan-dan-analisis-algoritma.pdf` |
| 12 | `probabilitas-dan-statistika` | Probabilitas dan Statistika | `materi/` (uji hipotesis, ANOVA) + `slides/pdf/` + `tabel/` |
| 13 | `struktur-data` | Struktur Data | `tugas/` (sandbox, tugas1-4) + `assets/` |
| 14 | `teori-graf` | Teori Graf | `materi/` + `docs/` + `data/` + `praktikum/` + `projects/finalproject` + `slides/pdf/` |

Detail: `courses/<slug>/README.md`.

## Penggunaan

```bash
git clone <url> rka-knowledge
cd rka-knowledge
# Buka courses/<slug>/README.md
```

## Kontribusi

Lihat [`CONTRIBUTING.md`](CONTRIBUTING.md).
