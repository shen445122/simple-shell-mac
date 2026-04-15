#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge PDFs from each child folder into a single PDF.

Example:
    python join-pdf.py --root ./chapters --prefix chapter --output-dir ./merged
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def natural_key(value: str):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', value)]


def iter_pdfs(folder: Path, prefix: str = ''):
    pdfs = [
        path for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() == '.pdf' and not path.name.startswith('.') and (not prefix or path.name.startswith(prefix))
    ]
    return sorted(pdfs, key=lambda path: natural_key(path.name))


def merge_pdfs(source_dir: Path, output_file: Path, prefix: str = '', overwrite: bool = False) -> int:
    from PyPDF2 import PdfMerger

    pdfs = iter_pdfs(source_dir, prefix=prefix)
    if not pdfs:
        raise ValueError(f'No PDF files found in {source_dir}')
    if output_file.exists() and not overwrite:
        raise FileExistsError(f'{output_file} already exists, use --overwrite to replace it')

    output_file.parent.mkdir(parents=True, exist_ok=True)
    merger = PdfMerger()
    try:
        for pdf_path in pdfs:
            merger.append(str(pdf_path))
        with output_file.open('wb') as handle:
            merger.write(handle)
    finally:
        merger.close()
    return len(pdfs)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Merge PDFs in each child folder.')
    parser.add_argument('--root', default='.', help='Directory containing child folders with PDFs.')
    parser.add_argument('--output-dir', default=None, help='Directory to store merged PDFs. Defaults to the root directory.')
    parser.add_argument('--prefix', default='', help='Only merge PDF files whose names start with this prefix.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing output files.')
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else root
    if not root.exists() or not root.is_dir():
        raise SystemExit(f'Root directory does not exist: {root}')

    folders = sorted([path for path in root.iterdir() if path.is_dir() and not path.name.startswith('.')], key=lambda path: natural_key(path.name))
    if not folders:
        raise SystemExit(f'No child folders found under {root}')

    generated = 0
    for folder in folders:
        output_name = f'{folder.name}.pdf' if not args.prefix else f'{folder.name}_{args.prefix}.pdf'
        output_file = output_dir / output_name
        try:
            count = merge_pdfs(folder, output_file, prefix=args.prefix, overwrite=args.overwrite)
            generated += 1
            print(f'[OK] {folder.name} -> {output_file} ({count} PDFs)')
        except ValueError as exc:
            print(f'[SKIP] {exc}')
    print(f'Generated {generated} merged PDF file(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
