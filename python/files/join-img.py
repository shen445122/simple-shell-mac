#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert images from each child folder into a PDF.

Example:
    python join-img.py --root ./manga --output-dir ./pdfs
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}


def natural_key(value: str):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', value)]


def iter_image_files(folder: Path):
    return sorted(
        [path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS and not path.name.startswith('.')],
        key=lambda path: natural_key(path.name),
    )


def images_to_pdf(source_dir: Path, output_file: Path, overwrite: bool = False) -> int:
    import fitz

    images = iter_image_files(source_dir)
    if not images:
        raise ValueError(f'No supported image files found in {source_dir}')
    if output_file.exists() and not overwrite:
        raise FileExistsError(f'{output_file} already exists, use --overwrite to replace it')

    output_file.parent.mkdir(parents=True, exist_ok=True)
    document = fitz.open()
    try:
        for image_path in images:
            with fitz.open(image_path) as image_doc:
                pdf_bytes = image_doc.convert_to_pdf()
            with fitz.open('pdf', pdf_bytes) as image_pdf:
                document.insert_pdf(image_pdf)
        document.save(output_file)
    finally:
        document.close()
    return len(images)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Convert images in each child folder into one PDF per folder.')
    parser.add_argument('--root', default='.', help='Directory containing child folders with images.')
    parser.add_argument('--output-dir', default=None, help='Directory to store generated PDFs. Defaults to the root directory.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing PDF files.')
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else root

    if not root.exists() or not root.is_dir():
        raise SystemExit(f'Root directory does not exist: {root}')

    folders = sorted(
        [path for path in root.iterdir() if path.is_dir() and not path.name.startswith('.')],
        key=lambda path: natural_key(path.name),
    )
    if not folders:
        raise SystemExit(f'No child folders found under {root}')

    generated = 0
    for folder in folders:
        output_file = output_dir / f'{folder.name}.pdf'
        try:
            count = images_to_pdf(folder, output_file, overwrite=args.overwrite)
            generated += 1
            print(f'[OK] {folder.name} -> {output_file} ({count} images)')
        except ValueError as exc:
            print(f'[SKIP] {exc}')
    print(f'Generated {generated} PDF file(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
