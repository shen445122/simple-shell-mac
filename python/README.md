# Python Scripts

This directory contains a few small utility scripts for file processing, Douban lookups, Excel-to-MySQL import, and stock data import.

## Structure

- `files/`
  - `join-img.py`: convert images inside each child folder into one PDF per folder
  - `combined_images.py`: combine images from ordered subfolders into a single PDF
  - `join-pdf.py`: merge PDFs inside each child folder into one PDF per folder
  - `douban.py`: look up Douban book URLs and ratings from command-line titles
  - `douban_by_list.py`: look up Douban book URLs and ratings from a text file list
  - `douban_common.py`: shared Douban helper module
- `excel to mysql/`
  - `excel2mysql.py`: import `.xls` files into MySQL tables
  - `my.conf`: database and data path config
- `get stock info/`
  - `Main.py`: import stock data by stock code

## Requirements

Some scripts need third-party packages.

Suggested install:

```bash
pip install pymupdf PyPDF2 requests beautifulsoup4 lxml mysql-connector-python xlrd
```

Notes:
- `join-img.py` and `combined_images.py` use PyMuPDF (`fitz`)
- `join-pdf.py` uses `PyPDF2`
- Douban scripts use `requests`, `beautifulsoup4`, `lxml`
- Excel import uses `mysql-connector-python` and `xlrd`

## 1. Image folder -> one PDF per folder

Script:

```bash
python3 python/files/join-img.py --root <directory> [--output-dir <dir>] [--overwrite]
```

What it does:
- scans each child folder under `--root`
- collects supported images in each child folder
- creates one PDF for each child folder

Supported image formats:
- `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tif`, `.tiff`, `.webp`

Example:

```bash
python3 python/files/join-img.py --root ./manga --output-dir ./pdfs --overwrite
```

## 2. Ordered subfolders -> one combined PDF

Script:

```bash
python3 python/files/combined_images.py --root <directory> [--output <file.pdf>] [--overwrite]
```

What it does:
- scans ordered subfolders under `--root`
- appends all supported images into one single PDF
- useful for manga/comic chapter folders or split scan folders

Example:

```bash
python3 python/files/combined_images.py --root 色轮眼 --output 色轮眼.pdf --overwrite
```

## 3. Merge PDFs inside each child folder

Script:

```bash
python3 python/files/join-pdf.py --root <directory> [--output-dir <dir>] [--prefix <prefix>] [--overwrite]
```

What it does:
- scans each child folder under `--root`
- merges PDF files in natural filename order
- optionally filters input files by `--prefix`

Example:

```bash
python3 python/files/join-pdf.py --root ./chapters --output-dir ./merged --overwrite
python3 python/files/join-pdf.py --root ./chapters --prefix chapter --overwrite
```

## 4. Douban lookup from CLI titles

Script:

```bash
python3 python/files/douban.py [title1 title2 ...]
```

Default titles:
- 红楼梦
- 三国演义
- 水浒传
- 西游记

Example:

```bash
python3 python/files/douban.py 红楼梦 白夜行
```

Output format:

```text
书名    评分    URL
```

## 5. Douban lookup from a file list

Script:

```bash
python3 python/files/douban_by_list.py --list-file <path>
```

Input file format:
- one book title per line
- UTF-8 recommended

Example:

```bash
python3 python/files/douban_by_list.py --list-file ./list
```

## 6. Import Excel `.xls` files into MySQL

Script:

```bash
python3 "python/excel to mysql/excel2mysql.py"
```

Configuration file:

```bash
python/excel to mysql/my.conf
```

Expected config sections:

```ini
[db]
db_user = your_user
db_pwd = your_password
db_host = 127.0.0.1
db_port = 3306
db_db = your_database

[data]
datapath = /path/to/xls/files
```

Behavior:
- recursively scans `datapath` for `.xls`
- creates tables from file names
- creates columns from the first row
- inserts the remaining rows into MySQL

Notes:
- only `.xls` is currently handled
- table and column names are sanitized automatically

## 7. Import stock data by code

Script:

```bash
python3 "python/get stock info/Main.py" --code 600519
```

Configuration file:

```bash
python/get stock info/conf/gsi.conf
```

Behavior:
- reads DB/log config from `gsi.conf`
- imports stock data for the given code

## Quick examples

```bash
# Show help
python3 python/files/join-img.py --help
python3 python/files/combined_images.py --help
python3 python/files/join-pdf.py --help
python3 python/files/douban.py --help
python3 python/files/douban_by_list.py --help
python3 "python/get stock info/Main.py" --help

# Image tools
python3 python/files/join-img.py --root ./images --overwrite
python3 python/files/combined_images.py --root ./色轮眼 --overwrite
python3 python/files/join-pdf.py --root ./pdf_parts --overwrite

# Douban tools
python3 python/files/douban.py 三体
python3 python/files/douban_by_list.py --list-file ./list
```
