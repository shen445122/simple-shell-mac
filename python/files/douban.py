#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lookup Douban book links and ratings from command-line titles."""

from __future__ import annotations

import argparse

from douban_common import DoubanClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Lookup Douban book URLs and ratings.')
    parser.add_argument('titles', nargs='*', help='Book titles to query. Defaults to the four classics.')
    return parser


def main() -> int:
    args = build_parser().parse_args()
    titles = args.titles or ['红楼梦', '三国演义', '水浒传', '西游记']
    client = DoubanClient()
    for title in titles:
        try:
            result = client.get_book(title)
            print(f'{result.title}\t{result.rank or "暂无评分"}\t{result.url}')
        except Exception as exc:
            print(f'[ERROR] {title}: {exc}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
