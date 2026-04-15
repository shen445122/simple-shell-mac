#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared Douban lookup helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
)
TIMEOUT = 15


@dataclass
class BookResult:
    title: str
    url: str
    rank: Optional[str]


class DoubanClient:
    def __init__(self) -> None:
        import requests

        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})

    def get_book(self, title: str) -> BookResult:
        title = title.strip()
        if not title:
            raise ValueError('Book title cannot be empty')

        suggest_url = 'https://book.douban.com/j/subject_suggest'
        response = self.session.get(suggest_url, params={'q': title}, timeout=TIMEOUT)
        response.raise_for_status()
        candidates = response.json()
        if not candidates:
            raise LookupError(f'No Douban result found for: {title}')

        url = candidates[0]['url']
        rank = self.get_rank(url)
        return BookResult(title=title, url=url, rank=rank)

    def get_rank(self, url: str) -> Optional[str]:
        from bs4 import BeautifulSoup

        response = self.session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        node = soup.select_one('#interest_sectl strong')
        rank = node.get_text(strip=True) if node else ''
        return rank or None
