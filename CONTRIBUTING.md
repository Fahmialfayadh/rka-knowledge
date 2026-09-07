# Contributing — RKA Knowledge

## Prinsip
- **PDF-only:** Jangan commit `*.pptx/*.ppt/*.ppsx/*.docx`. Convert dulu via `./scripts/convert_ppt_to_pdf.sh` (LibreOffice headless). Original simpan di source backup, tidak di repo.
- **Kebab-case:** `07. Adversarial Search.pptx` → `07-adversarial-search.pdf`. Tidak ada spasi, huruf kecil, no `PAA` kapital.
- **Flat:** `courses/<slug>/` tanpa `semester/`. Slug: `alin, basisdata, bluecamp, dasprog, datmin, kalkulus-2, kk, kka, machine-learning, matdis, paa, probstat, strukdat, tegrf` (15).
- **ML/DM first-class:** `external/Modul-ML-RKA` → `courses/machine-learning/materi/`, `external/Modul-DM-RKA` → `courses/datmin/modul/` (sync via `scripts/sync-external.sh`).
- **No junk:** Jangan commit `.venv/`, `venv-ppt/`, `__pycache__/`, `.godot/`, `__MACOSX/`, `*.lck`, `*.pyc`, `instance/stroke.db`.
- **LFS:** `*.pdf, *.zip, *.mp4, *.m4a` otomatis LFS (`.gitattributes`).

## Menambah Matkul
```bash
mkdir -p courses/<slug>/{materi,slides/pdf,praktikum}
# copy & convert
./scripts/convert_ppt_to_pdf.sh
# tulis courses/<slug>/README.md pakai template docs/_template/README.md
```

## Update External
```bash
./scripts/sync-external.sh
# cat external/ATTRIBUTION.md — update hash
```

## Commit
```
feat(course): add kka EAS 2024 pdf
fix(slides): re-convert probstat legacy ppt
docs: update courses/tegra README
```

## Validasi Sebelum Push
```bash
find courses -name "*.pptx" -o -name "*.ppt" | wc -l  # harus 0
find . -type d -name ".venv" | wc -l  # 0
git lfs ls-files | head
./scripts/inventory.py | head -n 50
```

## Akses
Repo **private — limited**. Minta invite ke owner via `gh api repos/<owner>/rka-knowledge/collaborators/<username> -X PUT --field permission=push`.
