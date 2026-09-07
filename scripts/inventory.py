#!/usr/bin/env python3
"""Generate inventory for courses."""
import pathlib, os
root = pathlib.Path("/home/data/kuliah/rka-knowledge/courses")
for slug in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("_")):
    print(f"\n## {slug.name}")
    for f in sorted(slug.rglob("*")):
        if f.is_file():
            rel = f.relative_to(slug)
            size = f.stat().st_size
            print(f"  {rel} ({size//1024}KB)")
