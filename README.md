# RKA Knowledge — ITS

> Kurasi materi Rekayasa Kecerdasan Artifisial (RKA), Departemen Teknik Informatika ITS — terstruktur, PDF-only, enak dibaca, siap dikembangkan.

[![Courses](https://img.shields.io/badge/courses-14-blue)](#daftar-matkul)
[![External](https://img.shields.io/badge/external-2-green)](#modul-eksternal-vendor-copy)
[![PDF-only](https://img.shields.io/badge/slides-PDF--only-orange)](#kebijakan-pdf-only)
[![LFS](https://img.shields.io/badge/git--lfs-enabled-lightgrey)](#git-lfs)
[![Private](https://img.shields.io/badge/access-private--limited-red)](#akses)

Repo ini mengumpulkan **14 matkul + assets** dari `/home/data/kuliah/rka` plus **2 modul KCV** sebagai vendor copy. Semua slide PPT/PPSX/PPTX/DOCX sudah di-convert ke **PDF** (`courses/*/slides/pdf/`) — tidak menyimpan original PPT (backup tetap di source).

## Struktur

```
rka-knowledge/
├── README.md
├── CONTRIBUTING.md
├── docs/panduan-konversi.md
├── external/{Modul-ML-RKA,Modul-DM-RKA,ATTRIBUTION.md}
├── scripts/{convert_ppt_to_pdf.sh,sync-external.sh,inventory.py}
└── courses/
    ├── alin/            # Aljabar Linear — notebooks
    ├── basisdata/       # Basis Data — studenttracker (Django)
    ├── bluecamp/        # Bluecamp Day 2 — studi literatur sitasi
    ├── dasprog/         # Dasar Pemrograman — 5 tugas
    ├── datmin/          # Data Mining — rangkuman Week 1
    ├── kalkulus-2/      # Kalkulus 2 — 11 modul + images
    ├── kk/              # Kecerdasan Komputasional — Logical Agents (Wumpus)
    ├── kka/             # KKA — search, adversarial, CSP, fuzzy, WAR project
    ├── matdis/          # Matematika Diskrit — risiko stroke (Flask)
    ├── paa/             # PAA — portofolio (docx→pdf)
    ├── probstat/        # Probstat — uji hipotesis + tabel Z/T/F
    ├── strukdat/        # Struktur Data — BST/BFS/DFS, queue/stack, media
    ├── tegrf/           # Teori Graf — HeFDN, M5 Tree, narasi politik X, data capres2024
    └── _template/
```

Tiap `courses/<slug>/` baku:
```
courses/<slug>/
├── README.md
├── slides/pdf/          # PDF hasil konvert (kebab-case)
├── materi/              # modul, paper, rangkuman
├── praktikum/ | tugas/ | projects/
└── assets/
```

## Daftar Matkul

| # | Slug | Nama | Ringkasan | Slides PDF |
|---|---|---|---|---|
| 1 | `alin` | Aljabar Linear | `women-s-shoes-prices-analysis.ipynb` (15M) | — |
| 2 | `basisdata` | Basis Data | `projects/studenttracker` (Django `manage.py`, `tracker/models.py`) | — |
| 3 | `bluecamp` | Bluecamp | `materi/studiliteratur.md` — APA vs Harvard, Ibid/Op.cit, Mendeley | — |
| 4 | `dasprog` | Dasar Pemrograman | `tugas/{tugas_backtracking,floodnfill,search,sorting,textfile}` (32 py, 12 png bukti) | — |
| 5 | `datmin` | Data Mining | `materi/Rangkuman Data Mining Week 1.pdf` | ✓ |
| 6 | `kalkulus-2` | Kalkulus 2 | `modul/01-11` + `images/` + `polar.md/volue.md` | — |
| 7 | `kk` | Kecerdasan Komputasional | `praktikum/Modul-Praktikum-KK-RKA-25` (Wumpus, 4 ipynb, `2026_2_Logical Agents_a.pdf`) | [`kk/slides/pdf/2026-1-pengantar-kk-s1-rka.pdf`](courses/kk/slides/pdf/2026-1-pengantar-kk-s1-rka.pdf) |
| 8 | `kka` | KKA | `praktikum/uninformed-informed-search`, `local-adversarial-csp`, `materi/asset-ppt` (CS P, Fuzzy, EAS), `projects/WAR` (Godot+Python, `WARID_KEL-10.zip`) | [`kka/slides/pdf/`](courses/kka/slides/pdf/) (5 pdf) |
| 9 | `matdis` | Matematika Diskrit | `projects/risiko-stroke` (Flask `app.py`, `templates/`, `pdf_generator.py`) | — |
| 10 | `paa` | PAA | Portofolio 22M `docx→pdf` | [`paa/slides/pdf/portofolio-perancangan-dan-analisis-algoritma.pdf`](courses/paa/slides/pdf/portofolio-perancangan-dan-analisis-algoritma.pdf) |
| 11 | `probstat` | Probabilitas & Statistika | `slides/pdf/{uji-parameter-1-populasi,uji-hipotesis-2-populasi,one-way-anova}`, `tabel/{F0-05,T,Z}` | ✓ 3 pdf |
| 12 | `strukdat` | Struktur Data | `tugas/{sandbox,tugas1-4}`, `assets/audio1053355768.m4a` 33M, `tugas2/media` (95M) | — |
| 13 | `tegrf` | Teori Graf | `materi/{FP_Tegraf.py,HeFDN_Analysis.pdf,viewer.html}`, `docs/` (7 md), `data/DE-sample-X-capres2024`, `praktikum/{modul2,terminologigraf}` | [`tegrf/slides/pdf/`](courses/tegrf/slides/pdf/) (7 pdf) |
| 14 | `bluecamp` | — | sudah di atas | — |

Detail per-course: buka `courses/<slug>/README.md`.

## Modul Eksternal (Vendor Copy)

Bukan submodule — snapshot self-contained di `external/`:

| Modul | Source | Commit | Isi |
|---|---|---|---|
| **Modul-ML-RKA** | [kcv-if/Modul-ML-RKA](https://github.com/kcv-if/Modul-ML-RKA) | `46e0089` main | Supervised (Linear/Poly/Ridge-Lasso/Logistic/KNN/SVM/SVR/DecisionTree/ANN/NaiveBayes), Unsupervised (KMeans/Hierarchical/DBSCAN/BIRCH), DL (ANN/CNN), RL, Deployment |
| **Modul-DM-RKA** | [kcv-if/Modul-DM-RKA](https://github.com/kcv-if/Modul-DM-RKA) | `cfa1d6c` master | Data Mining: EDA, Preprocessing, Ensemble & Class Imbalance, Association, Sequential, Clustering, Anomaly |

Lihat `external/ATTRIBUTION.md`. Sync: `./scripts/sync-external.sh`.

## Kebijakan PDF-only

- Semua `*.pptx/*.ppt/*.ppsx/*.docx` di-convert via `soffice --headless --convert-to pdf` (LibreOffice 24.2.7.2).
- Hasil di `courses/*/slides/pdf/<kebab>.pdf` (contoh: `07. Adversarial Search.pptx` → `07-adversarial-search.pdf`).
- **Original PPT tidak di-commit** — backup tetap di `/home/data/kuliah/rka` (source).
- Dedup: `kka/asset_ppt/07. Adversarial` duplikat root → 1 pdf; `ppt_fp_tegraf/*.pptx.pptx` & `*.pptx.pdf` → 1 pdf; `tegrf/data/... (2)` & `__MACOSX` dibuang.
- 17 PDF hasil konvert terverifikasi (0 fail).

List PDF:
```
kk/slides/pdf/2026-1-pengantar-kk-s1-rka.pdf (2.0M)
kka/slides/pdf/04-informed-search.pdf (1.5M)
kka/slides/pdf/07-adversarial-search.pdf (2.0M)
kka/slides/pdf/12-first-order-logic.pdf (1.3M)
kka/slides/pdf/fp-kka-ppt.pdf (2.8M)
kka/slides/pdf/kelasn-progres-fp-kelompok10.pdf (6.6M)
paa/slides/pdf/portofolio-perancangan-dan-analisis-algoritma.pdf (1.8M)
probstat/slides/pdf/uji-parameter-1-populasi.pdf (772K) — legacy .ppt 2005
probstat/slides/pdf/uji-hipotesis-parameter-2-populasi.pdf (23M)
probstat/slides/pdf/one-way-anova.pdf (1.2M)
tegrf/slides/pdf/m5-tree-and-spanning.pdf (1.4M)
tegrf/slides/pdf/presentasi-analisis-narasi.pdf (807K)
tegrf/slides/pdf/analisis-pola-penyebaran-narasi-politik-x-kelompok6.pdf (52K)
tegrf/slides/pdf/cokelat-dan-krem-seminar-proposal.pdf (2.9M)
tegrf/slides/pdf/proposal-graf-narasi-politik-twitterx-kelompok6.pdf (779K)
tegrf/slides/pdf/vision-board-1-0.pdf (5.7M)
tegrf/slides/pdf/vision-board-1-0-final.pdf (4.0M)
```

## Quick Start

```bash
git clone <url> rka-knowledge
cd rka-knowledge
# tidak perlu --recurse-submodules (vendor copy)
# optional: re-run konversi
./scripts/convert_ppt_to_pdf.sh
# sync external snapshot
./scripts/sync-external.sh
```

## Git LFS

```
*.pdf *.zip *.mp4 *.m4a *.mp3 *.odb *.png *.jpg filter=lfs
```

File >50M wajib LFS: `WARID_KEL-10.zip` (54M), `strukdat/tugas2/media` (95M), `probstat uji-hipotesis` 23M, dll.

## Akses

**Private — limited** (“public terbatas”): repo GitHub private, invite collaborator manual. Tidak publish ke org `kcv-if`. Bagi akses: `gh api repos/<owner>/rka-knowledge/collaborators/<user> -X PUT`.

## Kontribusi

Lihat [`CONTRIBUTING.md`](CONTRIBUTING.md). Penamaan file kebab-case, tidak ada `PAA` kapital, tidak commit `.venv/.godot/__pycache__`.

## Lisensi

Konten kurasi internal untuk kuliah RKA. Modul external mengikuti lisensi upstream (lihat `external/*/README.md`). Hubungi KCV untuk lisensi spesifik.

---

*Generated 2026-09-07 — source `/home/data/kuliah/rka` (304M, 14 matkul).*
