#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Combine images from ordered subfolders into one PDF.

Example:
    python combined_images.py --root 色轮眼 --output 色轮眼.pdf
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}


def natural_key(value: str):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', value)]


def iter_images(folder: Path):
    return sorted(
        [path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS and not path.name.startswith('.')],
        key=lambda path: natural_key(path.name),
    )


def combine_subdirectories(root: Path, output_file: Path, overwrite: bool = False) -> int:
    import fitz

    sub_dirs = sorted([path for path in root.iterdir() if path.is_dir() and not path.name.startswith('.')], key=lambda path: natural_key(path.name))
    if not sub_dirs:
        raise ValueError(f'No subdirectories found in {root}')
    if output_file.exists() and not overwrite:
        raise FileExistsError(f'{output_file} already exists, use --overwrite to replace it')

    output_file.parent.mkdir(parents=True, exist_ok=True)
    document = fitz.open()
    inserted = 0
    try:
        for sub_dir in sub_dirs:
            for image_path in iter_images(sub_dir):
                with fitz.open(image_path) as image_doc:
                    rect = image_doc[0].rect
                page = document.new_page(width=rect.width, height=rect.height)
                page.insert_image(rect, filename=str(image_path))
                inserted += 1
        if inserted == 0:
            raise ValueError(f'No supported image files found under {root}')
        document.save(output_file)
    finally:
        document.close()
    return inserted


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Combine images from subdirectories into one PDF.')
    parser.add_argument('--root', required=True, help='Main directory containing ordered image subdirectories.')
    parser.add_argument('--output', default=None, help='Output PDF path. Defaults to <root>.pdf')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output file if it already exists.')
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).expanduser().resolve()
    output = Path(args.output).expanduser().resolve() if args.output else root.with_suffix('.pdf')
    if not root.exists() or not root.is_dir():
        raise SystemExit(f'Root directory does not exist: {root}')

    count = combine_subdirectories(root, output, overwrite=args.overwrite)
    print(f'[OK] Wrote {output} with {count} image(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
