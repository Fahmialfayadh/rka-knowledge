# Contributing — RKA Knowledge

## Prinsip
- **Hanya pembelajaran:** Tidak ada script/tooling selain tugas.
- **Kebab-case & nama lengkap:** `aljabar-linear` bukan `alin`, `kecerdasan-komputasional` bukan `kk`, `konsep-kecerdasan-artifisial` bukan `kka`, dll.
- **Flat:** `courses/<slug>/` tanpa `semester/` (14 mata kuliah).
- **No junk:** Jangan commit `.venv/`, `__pycache__/`, `.godot/`, `__MACOSX/`.
- **LFS:** `*.pdf, *.zip, *.mp4, *.m4a` otomatis LFS.

## Menambah Mata Kuliah
```bash
mkdir -p courses/<slug-baru>/{materi,slides/pdf,praktikum}
# tulis README.md
```

## Commit
```
feat(course): add e.g., struktur-data tugas baru
```

## Validasi
```bash
find courses -name "*.pptx" | wc -l  # harus 0
```

## Akses
Repo **private — limited**.
