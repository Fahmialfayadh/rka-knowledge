# Panduan Konversi PPT → PDF

## Tool
- **LibreOffice 24.2.7.2** (`soffice --headless --convert-to pdf`)
- Tested OK: `.ppsx` (KK 2026_1_Pengantar KK), `*.pptx`, legacy `.ppt` 2005 (probstat Uji Parameter 1 Populasi), `.docx` (PAA Portofolio 22M)

## Cara
```bash
./scripts/convert_ppt_to_pdf.sh
# atau manual:
soffice --headless --convert-to pdf --outdir /tmp/out "path/file.pptx"
mv /tmp/out/file.pdf courses/<slug>/slides/pdf/<kebab>.pdf
```

## Mapping yang Dipakai (17 file)

| Source | Dest (slug baru) |
|---|---|
| `KK/ASSET_MATERI/2026_1_Pengantar KK S1 RKA.ppsx` | `kecerdasan-komputasional/2026-1-pengantar-kk-s1-rka.pdf` |
| `kka/07. Adversarial Search.pptx` | `konsep-kecerdasan-artifisial/07-adversarial-search.pdf` |
| `kka/12. First Order Logic.pptx` | `konsep-kecerdasan-artifisial/12-first-order-logic.pdf` |
| `kka/FP_KKA_PPT.pptx` | `konsep-kecerdasan-artifisial/fp-kka-ppt.pdf` |
| `kka/asset_ppt/04. Informed Search.pptx` | `konsep-kecerdasan-artifisial/04-informed-search.pdf` |
| `kka/finalproject/WAR/KelasN_ProgresFP_Kelompok10.pptx` | `konsep-kecerdasan-artifisial/kelasn-progres-fp-kelompok10.pdf` |
| `PAA/Portofolio ... .docx` | `perancangan-dan-analisis-algoritma/portofolio-perancangan-dan-analisis-algoritma.pdf` |
| `probstat/ppt/Uji Parameter 1 Populasi.ppt` | `probabilitas-dan-statistika/uji-parameter-1-populasi.pdf` |
| `probstat/ppt/Uji Hipotesis...ppsx` | `probabilitas-dan-statistika/uji-hipotesis-parameter-2-populasi.pdf` |
| `probstat/ppt/one-way ANOVA.ppt` | `probabilitas-dan-statistika/one-way-anova.pdf` |
| `tegrf/M5 - Tree and Spanning.pptx` | `teori-graf/m5-tree-and-spanning.pdf` |
| `tegrf/Presentasi_Analisis_Narasi.pptx` | `teori-graf/presentasi-analisis-narasi.pdf` |
| `tegrf/finalproject/Analisis-ini-membahas...pptx` | `teori-graf/analisis-pola-penyebaran-narasi-politik-x-kelompok6.pdf` |
| `tegrf/.../Cokelat ...Seminar Proposal...pptx` | `teori-graf/cokelat-dan-krem-seminar-proposal.pdf` |
| `tegrf/.../Proposal_Graf_Narasi...pptx` | `teori-graf/proposal-graf-narasi-politik-twitterx-kelompok6.pdf` |
| `tegrf/.../vision_board_1.0 ... .pptx` | `teori-graf/vision-board-1-0.pdf` |
| `tegrf/.../vision_board_1.0_final.pptx` | `teori-graf/vision-board-1-0-final.pdf` |

> Semua dest di `courses/<slug>/slides/pdf/` dengan slug baru (nama lengkap).

## Legacy .PPT
`probstat/ppt/Uji Parameter 1 Populasi.ppt` adalah `Composite Document File V2` (Office 2003, Author Diana Purwitasari, 2005). `soffice` sanggup convert → 772K PDF (OK). Jika layout rusak: cek dengan `pandoc` atau pakai hasil convert yang sudah ada, jangan keep `.ppt`.

## Dedup
- `kka/asset_ppt/07. Adversarial Search.pptx` duplikat `kka/07...pptx` → convert 1x.
- `ppt_fp_tegraf/Presentasi_Analisis_Narasi.pptx.pptx` & `*.pptx.pdf` → hanya sumber `.pptx` (sama dengan `tegrf/Presentasi_Analisis_Narasi.pptx`).
- `tegrf/narasi-x-pilpres-ig.pptx` vs `.pptx.pptx` duplikat → skip (sudah terwakili).
- `tegrf/data/DE-sample-X-capres2024 (2)/` & `__MACOSX/` → skip.

## Verifikasi
```bash
find courses -path "*/slides/pdf/*.pdf" -exec ls -lh {} \;
find courses -name "*.pptx" | wc -l  # harus 0 (pdf-only)
```

Hasil: **17 success, 0 fail** (2026-09-07).
