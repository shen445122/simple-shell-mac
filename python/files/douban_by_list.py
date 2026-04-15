#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lookup Douban book links and ratings from a text file list."""

from __future__ import annotations

import argparse
from pathlib import Path

from douban_common import DoubanClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Lookup Douban book URLs and ratings from a file list.')
    parser.add_argument('--list-file', default='./list', help='Path to a text file containing one book title per line.')
    return parser


def main() -> int:
    args = build_parser().parse_args()
    list_path = Path(args.list_file).expanduser().resolve()
    if not list_path.exists():
        raise SystemExit(f'List file does not exist: {list_path}')

    client = DoubanClient()
    for line in list_path.read_text(encoding='utf-8').splitlines():
        title = line.strip()
        if not title:
            continue
        try:
            result = client.get_book(title)
            print(f'{result.title}\t{result.rank or "暂无评分"}\t{result.url}')
        except Exception as exc:
            print(f'[ERROR] {title}: {exc}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
