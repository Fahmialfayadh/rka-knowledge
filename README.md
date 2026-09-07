# RKA Knowledge — ITS

> Kurasi materi Rekayasa Kecerdasan Artifisial (RKA), Departemen Teknik Informatika ITS — terstruktur, PDF-only, enak dibaca, siap dikembangkan.

[![Courses](https://img.shields.io/badge/courses-15-blue)](#daftar-matkul)
[![PDF-only](https://img.shields.io/badge/slides-PDF--only-orange)](#kebijakan-pdf-only)
[![LFS](https://img.shields.io/badge/git--lfs-enabled-lightgrey)](#git-lfs)
[![Private](https://img.shields.io/badge/access-private--limited-red)](#akses)

Repo ini mengumpulkan **15 matkul + assets** dari `/home/data/kuliah/rka` plus **2 modul KCV sebagai matkul first-class** (bukan sekadar `external/`). Semua slide PPT/PPSX/PPTX/DOCX sudah di-convert ke **PDF** (`courses/*/slides/pdf/`) — tidak menyimpan original PPT (backup tetap di source).

## Struktur

```
rka-knowledge/
├── README.md
├── CONTRIBUTING.md
├── docs/{panduan-konversi.md,_template/}
├── external/{Modul-ML-RKA,Modul-DM-RKA,ATTRIBUTION.md}  # vendor raw (preserve upstream)
├── scripts/{convert_ppt_to_pdf.sh,sync-external.sh,inventory.py}
└── courses/                     # 15 first-class, flat (ga per semester)
    ├── alin/                    # Aljabar Linear
    ├── basisdata/               # Basis Data
    ├── bluecamp/                # Bluecamp Day 2
    ├── dasprog/                 # Dasar Pemrograman
    ├── data-mining/  -> datmin/ # Data Mining (lokal + Modul-DM-RKA)
    ├── datmin/                  # alias ke data-mining (keep slang, isi penuh)
    ├── kalkulus-2/              # Kalkulus 2
    ├── kk/                      # Kecerdasan Komputasional
    ├── kka/                     # KKA
    ├── machine-learning/        # Machine Learning (dari Modul-ML-RKA)
    ├── matdis/                  # Matematika Diskrit
    ├── paa/                     # PAA
    ├── probstat/                # Probstat
    ├── strukdat/                # Struktur Data
    └── tegrf/                   # Teori Graf
```

> **Desain:** `external/` menyimpan snapshot mentah upstream (untuk attribution & sync). `courses/datmin` & `courses/machine-learning` adalah **kurasi first-class** yang berisi copy terstruktur dari `external/` — jadi ML/DM diperlakukan **sama** seperti matkul lain, tidak terpisah.

Tiap `courses/<slug>/` baku:

```
courses/<slug>/
├── README.md
├── slides/pdf/          # PDF hasil konvert (kebab-case) — hanya jika ada slide
├── materi/              # modul lokal (pdf/md)
├── modul/               # khusus kalkulus/datmin/machine-learning (dari external)
├── praktikum/ | tugas/ | projects/
└── assets/              # hanya jika ada media (tidak ada empty folder)
```

> Empty folder sudah di-prune — repo tidak menyimpan `assets/` kosong.

## Daftar Matkul (15)

| # | Slug | Nama | Ringkasan | Slides PDF |
|---|---|---|---|---|
| 1 | `alin` | Aljabar Linear | `notebooks/women-s-shoes-prices-analysis.ipynb` (15M) | — |
| 2 | `basisdata` | Basis Data | `projects/studenttracker` (Django `manage.py`, `tracker/models.py`) | — |
| 3 | `bluecamp` | Bluecamp | `materi/studiliteratur.md` — APA vs Harvard, Ibid/Op.cit, Mendeley | — |
| 4 | `dasprog` | Dasar Pemrograman | `tugas/{tugas_backtracking,floodnfill,search,sorting,textfile}` (32 py, 12 png bukti) | — |
| 5 | `datmin` | **Data Mining** | `materi/Rangkuman Week1.pdf` + `modul/0-7` (EDA→Anomaly, 15 files dari `external/Modul-DM-RKA`) | ✓ pdf lokal |
| 6 | `machine-learning` | **Machine Learning** | `materi/Supervised(11), Unsupervised(4), Deep Learning(2), RL, Deployment` — 24 files dari `external/Modul-ML-RKA` | — |
| 7 | `kalkulus-2` | Kalkulus 2 | `materi/{polar.md,volue.md}` + `modul/01-11` + `images/` (20 png) | — |
| 8 | `kk` | Kecerdasan Komputasional | `praktikum/Modul-Praktikum-KK-RKA-25` (Wumpus, 4 ipynb, `2026_2_Logical Agents_a.pdf`) | [`kk/slides/pdf/2026-1-pengantar-kk-s1-rka.pdf`](courses/kk/slides/pdf/2026-1-pengantar-kk-s1-rka.pdf) |
| 9 | `kka` | KKA | `praktikum/uninformed-informed-search`, `local-adversarial-csp`, `materi/asset-ppt` (CSP, Fuzzy, EAS), `projects/WAR` (Godot+Python, `WARID_KEL-10.zip`) | [`kka/slides/pdf/`](courses/kka/slides/pdf/) (5 pdf) |
| 10 | `matdis` | Matematika Diskrit | `projects/risiko-stroke` (Flask `app.py`, `templates/`, `pdf_generator.py`) | — |
| 11 | `paa` | PAA | Portofolio `docx→pdf` | [`paa/slides/pdf/portofolio-perancangan-dan-analisis-algoritma.pdf`](courses/paa/slides/pdf/portofolio-perancangan-dan-analisis-algoritma.pdf) |
| 12 | `probstat` | Probabilitas & Statistika | `slides/pdf/{uji-parameter-1-populasi,uji-hipotesis-2-populasi,one-way-anova}`, `tabel/{F0-05,T,Z}` | ✓ 3 pdf |
| 13 | `strukdat` | Struktur Data | `tugas/{sandbox,tugas1-4}`, `assets/audio1053355768.m4a` 33M, `tugas2/media` (95M) | — |
| 14 | `tegrf` | Teori Graf | `materi/{FP_Tegraf.py,HeFDN_Analysis.pdf,viewer.html}`, `docs/` (7 md), `data/DE-sample-X-capres2024`, `praktikum/{modul2,terminologigraf}` | [`tegrf/slides/pdf/`](courses/tegrf/slides/pdf/) (7 pdf) |
| 15 | *(external)* | Vendor Raw | `external/Modul-ML-RKA` + `external/Modul-DM-RKA` — preserve upstream, sync via `scripts/sync-external.sh`; lihat `external/ATTRIBUTION.md` | — |

Detail per-course: buka `courses/<slug>/README.md`.

## Alur Folder — Kenapa Begini?

- **Flat `courses/` (ga per semester)** sesuai request — enak discan, tidak perlu tebak semester. Urutan di tabel adalah navigasi utama.
- **ML & DM jadi first-class** (`courses/machine-learning`, `courses/datmin/modul`) — tidak lagi “external doang”. `external/` tetap ada sebagai **arsip vendor mentah** (untuk audit & `sync-external.sh`), tapi yang dibaca sehari-hari adalah `courses/`.
- **Tidak ada empty folder** — `assets/`, `slides/`, `materi/` kosong sudah dihapus (git tidak track empty dir; mengurangi noise).
- **Kalkulus-2 dirapikan:** `polar.md`/`volue.md` → `materi/`, `modul/` tetap 11 md + `images/`, `slides/` dihapus (tidak ada slide), `assets/` dihapus.
- **`_template` pindah** dari `courses/_template` → `docs/_template` (tidak mengotori listing matkul).

## Modul KCV — Treat Sama

Dua modul KCV sekarang **simetris**:

```
external/Modul-ML-RKA  ──copy──►  courses/machine-learning/materi/
external/Modul-DM-RKA  ──copy──►  courses/datmin/modul/
local datmin Assets/  ────────►  courses/datmin/materi/Rangkuman...pdf
```

- `courses/datmin` = `materi/` (lokal) + `modul/` (7 topik KCV)
- `courses/machine-learning` = `materi/` (5 topik KCV: Supervised/Unsupervised/DL/RL/Deployment)

Update upstream: `./scripts/sync-external.sh` otomatis update `external/` + `courses/*/materi|modul/`. Commit hash tercatat di `external/ATTRIBUTION.md`.

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
# tidak perlu --recurse-submodules (vendor copy, tapi sudah di courses/)
# optional: re-run konversi
./scripts/convert_ppt_to_pdf.sh
# sync external + courses
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

Lihat [`CONTRIBUTING.md`](CONTRIBUTING.md). Penamaan file kebab-case, tidak commit `.venv/.godot/__pycache__`.

## Lisensi

Konten kurasi internal untuk kuliah RKA. Modul external mengikuti lisensi upstream (lihat `external/*/README.md`). Hubungi KCV untuk lisensi spesifik.

---

*Generated 2026-09-07 — source `/home/data/kuliah/rka` (304M → curated 15 courses).*
