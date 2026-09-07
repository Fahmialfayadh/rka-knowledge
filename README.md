# RKA Knowledge — ITS

> Kurasi materi Rekayasa Kecerdasan Artifisial (RKA), Departemen Teknik Informatika ITS — terstruktur, PDF-only, enak dibaca, siap dikembangkan.

[![Courses](https://img.shields.io/badge/courses-14-blue)](#daftar-mata-kuliah)
[![PDF-only](https://img.shields.io/badge/slides-PDF--only-orange)](#kebijakan-pdf-only)
[![LFS](https://img.shields.io/badge/git--lfs-enabled-lightgrey)](#git-lfs)
[![Private](https://img.shields.io/badge/access-private--limited-red)](#akses)

Repo ini mengumpulkan **14 mata kuliah** dari `/home/data/kuliah/rka` (termasuk Data Mining & Machine Learning dari KCV). Semua slide PPT/PPSX/PPTX/DOCX sudah di-convert ke **PDF** (`courses/*/slides/pdf/`) — hanya pembelajaran.

## Struktur

```
rka-knowledge/
├── README.md
├── CONTRIBUTING.md
└── courses/                          # 14 mata kuliah, hanya pembelajaran (tanpa docs/scripts/external)
    ├── aljabar-linear/               # Aljabar Linear
    ├── basis-data/                   # Basis Data
    ├── bluecamp/                     # Bluecamp Day 2 — Studi Literatur
    ├── dasar-pemrograman/            # Dasar Pemrograman
    ├── data-mining/                  # Data Mining (lokal + Modul-DM-RKA)
    ├── kalkulus-2/                   # Kalkulus 2
    ├── kecerdasan-komputasional/     # Kecerdasan Komputasional
    ├── konsep-kecerdasan-artifisial/ # Konsep Kecerdasan Artifisial
    ├── machine-learning/             # Machine Learning (dari Modul-ML-RKA)
    ├── matematika-diskrit/           # Matematika Diskrit
    ├── perancangan-dan-analisis-algoritma/ # Perancangan dan Analisis Algoritma
    ├── probabilitas-dan-statistika/  # Probabilitas dan Statistika
    ├── struktur-data/                # Struktur Data
    └── teori-graf/                   # Teori Graf
```

> **Desain:** `courses/data-mining` & `courses/machine-learning` sudah dikurasi dari KCV — sejajar dengan mata kuliah lain.

Tiap `courses/<slug>/` baku:

```
courses/<slug>/
├── README.md
├── slides/pdf/          # PDF hasil konvert (kebab-case) — hanya jika ada slide
├── materi/              # modul lokal (pdf/md)
├── modul/               # khusus kalkulus / data-mining / machine-learning (dari external)
├── praktikum/ | tugas/ | projects/
└── assets/              # hanya jika ada media (tidak ada empty folder)
```

> Empty folder sudah di-prune — repo tidak menyimpan `assets/` kosong.

## Daftar Mata Kuliah (14)

| # | Slug | Nama | Ringkasan | Slides PDF |
|---|---|---|---|---|
| 1 | `aljabar-linear` | Aljabar Linear | `notebooks/women-s-shoes-prices-analysis.ipynb` (15M) | — |
| 2 | `basis-data` | Basis Data | `projects/studenttracker` (Django `manage.py`, `tracker/models.py`) | — |
| 3 | `bluecamp` | Bluecamp — Studi Literatur | `materi/studiliteratur.md` — APA vs Harvard, Ibid./Op.cit., Mendeley | — |
| 4 | `dasar-pemrograman` | Dasar Pemrograman | `tugas/{tugas_backtracking,floodnfill,search,sorting,textfile}` (32 py, 12 png bukti) | — |
| 5 | `data-mining` | Data Mining | `materi/Rangkuman Week 1.pdf` + `modul/0-7` (EDA → Anomaly, 15 files dari `external/Modul-DM-RKA`) | ✓ pdf lokal |
| 6 | `machine-learning` | Machine Learning | `materi/Supervised (11), Unsupervised (4), Deep Learning (2), RL, Deployment` — 24 files dari `external/Modul-ML-RKA` | — |
| 7 | `kalkulus-2` | Kalkulus 2 | `materi/{polar.md,volue.md}` + `modul/01-11` + `images/` (20 png) | — |
| 8 | `kecerdasan-komputasional` | Kecerdasan Komputasional | `praktikum/Modul-Praktikum-KK-RKA-25` (Wumpus, 4 ipynb, `2026_2_Logical Agents_a.pdf`) | [`kecerdasan-komputasional/slides/pdf/2026-1-pengantar-kk-s1-rka.pdf`](courses/kecerdasan-komputasional/slides/pdf/2026-1-pengantar-kk-s1-rka.pdf) |
| 9 | `konsep-kecerdasan-artifisial` | Konsep Kecerdasan Artifisial | `praktikum/uninformed-informed-search`, `local-adversarial-csp`, `materi/asset-ppt` (CSP, Fuzzy, EAS), `projects/WAR` (Godot+Python, `WARID_KEL-10.zip`) | [`konsep-kecerdasan-artifisial/slides/pdf/`](courses/konsep-kecerdasan-artifisial/slides/pdf/) (5 pdf) |
| 10 | `matematika-diskrit` | Matematika Diskrit | `projects/risiko-stroke` (Flask `app.py`, `templates/`, `pdf_generator.py`) | — |
| 11 | `perancangan-dan-analisis-algoritma` | Perancangan dan Analisis Algoritma | Portofolio `docx→pdf` | [`perancangan-dan-analisis-algoritma/slides/pdf/portofolio-perancangan-dan-analisis-algoritma.pdf`](courses/perancangan-dan-analisis-algoritma/slides/pdf/portofolio-perancangan-dan-analisis-algoritma.pdf) |
| 12 | `probabilitas-dan-statistika` | Probabilitas dan Statistika | `slides/pdf/{uji-parameter-1-populasi,uji-hipotesis-2-populasi,one-way-anova}`, `tabel/{F0-05,T,Z}` | ✓ 3 pdf |
| 13 | `struktur-data` | Struktur Data | `tugas/{sandbox,tugas1-4}`, `assets/audio1053355768.m4a` 33M, `tugas2/media` (95M) | — |
| 14 | `teori-graf` | Teori Graf | `materi/{FP_Tegraf.py,HeFDN_Analysis.pdf}`, `docs/` (7 md), `data/DE-sample-X-capres2024`, `praktikum/{modul2,terminologigraf}` | [`teori-graf/slides/pdf/`](courses/teori-graf/slides/pdf/) (7 pdf) |

Detail per-course: buka `courses/<slug>/README.md`.

## Alur Folder — Kenapa Begini?

- **Flat `courses/` (tanpa semester)** — enak discan, tidak perlu tebak semester.
- **Nama lengkap:** `aljabar-linear` bukan `alin`, `kecerdasan-komputasional` bukan `kk`, dst. Semua slug kebab-case.
- **Hanya pembelajaran:** Tidak ada `scripts/`/`docs/`/`external/` — sudah di-gitignore.

## Kebijakan PDF-only

- Semua `*.pptx/*.ppt/*.ppsx/*.docx` di-convert via `soffice --headless --convert-to pdf` (LibreOffice 24.2.7.2).
- Hasil di `courses/*/slides/pdf/<kebab>.pdf` (contoh: `07. Adversarial Search.pptx` → `07-adversarial-search.pdf`).
- **Original PPT tidak di-commit** — backup tetap di `/home/data/kuliah/rka` (source).
- Dedup: `kka/asset_ppt/07. Adversarial` duplikat root → 1 pdf; `ppt_fp_tegraf/*.pptx.pptx` & `*.pptx.pdf` → 1 pdf; `tegrf/data/... (2)` & `__MACOSX` dibuang.
- 17 PDF hasil konvert terverifikasi (0 fail).

List PDF:
```
kecerdasan-komputasional/slides/pdf/2026-1-pengantar-kk-s1-rka.pdf (2.0M)
konsep-kecerdasan-artifisial/slides/pdf/04-informed-search.pdf (1.5M)
konsep-kecerdasan-artifisial/slides/pdf/07-adversarial-search.pdf (2.0M)
konsep-kecerdasan-artifisial/slides/pdf/12-first-order-logic.pdf (1.3M)
konsep-kecerdasan-artifisial/slides/pdf/fp-kka-ppt.pdf (2.8M)
konsep-kecerdasan-artifisial/slides/pdf/kelasn-progres-fp-kelompok10.pdf (6.6M)
perancangan-dan-analisis-algoritma/slides/pdf/portofolio-perancangan-dan-analisis-algoritma.pdf (1.8M)
probabilitas-dan-statistika/slides/pdf/uji-parameter-1-populasi.pdf (772K) — legacy .ppt 2005
probabilitas-dan-statistika/slides/pdf/uji-hipotesis-parameter-2-populasi.pdf (23M)
probabilitas-dan-statistika/slides/pdf/one-way-anova.pdf (1.2M)
teori-graf/slides/pdf/m5-tree-and-spanning.pdf (1.4M)
teori-graf/slides/pdf/presentasi-analisis-narasi.pdf (807K)
teori-graf/slides/pdf/analisis-pola-penyebaran-narasi-politik-x-kelompok6.pdf (52K)
teori-graf/slides/pdf/cokelat-dan-krem-seminar-proposal.pdf (2.9M)
teori-graf/slides/pdf/proposal-graf-narasi-politik-twitterx-kelompok6.pdf (779K)
teori-graf/slides/pdf/vision-board-1-0.pdf (5.7M)
teori-graf/slides/pdf/vision-board-1-0-final.pdf (4.0M)
```

## Quick Start

```bash
git clone <url> rka-knowledge
cd rka-knowledge
# Buka courses/<slug>/README.md
```

## Git LFS

```
*.pdf *.zip *.mp4 *.m4a *.mp3 *.odb *.png *.jpg filter=lfs
```

File >50M wajib LFS: `WARID_KEL-10.zip` (54M), `struktur-data/tugas2/media` (95M), `probabilitas-dan-statistika uji-hipotesis` 23M, dll.

## Akses

**Private — limited** (“public terbatas”): repo GitHub private, invite collaborator manual. Tidak publish ke org `kcv-if`. Bagi akses: `gh api repos/<owner>/rka-knowledge/collaborators/<user> -X PUT`.

## Kontribusi

Lihat [`CONTRIBUTING.md`](CONTRIBUTING.md). Penamaan file kebab-case, tidak commit `.venv/.godot/__pycache__`.

## Lisensi

Konten kurasi internal untuk kuliah RKA.

---

*Generated 2026-09-07 — source `/home/data/kuliah/rka` (304M → curated 14 mata kuliah).*
