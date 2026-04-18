# Python 脚本说明

这个目录主要放一些常用的小工具脚本，涵盖：
- 图片 / PDF 处理
- 豆瓣图书信息查询
- Excel 导入 MySQL
- 股票数据导入

## 目录结构

- `files/`
  - `join-img.py`：把每个子目录中的图片合并为一个 PDF
  - `combined_images.py`：把多个有序子目录中的图片合并成一个总 PDF
  - `join-pdf.py`：把每个子目录中的多个 PDF 合并为一个 PDF
  - `douban.py`：通过命令行传入书名，查询豆瓣图书链接和评分
  - `douban_by_list.py`：从文本文件读取书名列表，批量查询豆瓣图书链接和评分
  - `douban_common.py`：豆瓣查询的公共模块
- `excel to mysql/`
  - `excel2mysql.py`：将 `.xls` 文件导入 MySQL 表
  - `my.conf`：数据库和数据目录配置
- `get stock info/`
  - `Main.py`：根据股票代码导入股票数据

## 依赖安装

现在把依赖分成了 3 层：
- `requirements.txt`：默认入口，当前指向基础运行依赖
- `requirements-base.txt`：脚本运行所需的最小依赖集合
- `requirements-dev.txt`：开发 / 检查工具（在基础依赖之上增加 `pytest`、`ruff`）

常用安装方式：

```bash
# 默认安装入口
pip install -r python/requirements.txt

# 只安装基础运行依赖
pip install -r python/requirements-base.txt

# 安装开发依赖
pip install -r python/requirements-dev.txt
```

如果你只想手动安装，也可以直接执行：

```bash
pip install pymupdf PyPDF2 requests beautifulsoup4 lxml mysql-connector-python xlrd
```

依赖说明：
- `join-img.py` 和 `combined_images.py` 使用 PyMuPDF（导入名为 `fitz`）
- `join-pdf.py` 使用 `PyPDF2`
- 豆瓣脚本使用 `requests`、`beautifulsoup4`、`lxml`
- Excel 导入脚本使用 `mysql-connector-python` 和 `xlrd`
- 开发工具依赖在 `requirements-dev.txt` 中，当前包括 `pytest` 和 `ruff`

另外，仓库根目录新增了 `pyproject.toml`，也可以通过可选依赖安装：

```bash
pip install .[python-scripts]
pip install .[dev]
```

## 1. 每个图片子目录生成一个 PDF

脚本：

```bash
python3 python/files/join-img.py --root <目录> [--output-dir <输出目录>] [--overwrite]
```

功能：
- 扫描 `--root` 下的每个子目录
- 收集每个子目录中的图片文件
- 每个子目录生成一个对应的 PDF

支持的图片格式：
- `.jpg`
- `.jpeg`
- `.png`
- `.bmp`
- `.tif`
- `.tiff`
- `.webp`

示例：

```bash
python3 python/files/join-img.py --root ./manga --output-dir ./pdfs --overwrite
```

## 2. 多个有序子目录合并成一个总 PDF

脚本：

```bash
python3 python/files/combined_images.py --root <目录> [--output <输出文件.pdf>] [--overwrite]
```

功能：
- 扫描 `--root` 下的有序子目录
- 按顺序把所有图片合并进一个 PDF
- 适合漫画章节目录、扫描拆分目录等场景

示例：

```bash
python3 python/files/combined_images.py --root 色轮眼 --output 色轮眼.pdf --overwrite
```

## 3. 合并每个子目录中的 PDF

脚本：

```bash
python3 python/files/join-pdf.py --root <目录> [--output-dir <输出目录>] [--prefix <前缀>] [--overwrite]
```

功能：
- 扫描 `--root` 下的每个子目录
- 按自然顺序合并其中的 PDF 文件
- 可通过 `--prefix` 只合并指定前缀的 PDF

示例：

```bash
python3 python/files/join-pdf.py --root ./chapters --output-dir ./merged --overwrite
python3 python/files/join-pdf.py --root ./chapters --prefix chapter --overwrite
```

## 4. 命令行查询豆瓣图书信息

脚本：

```bash
python3 python/files/douban.py [书名1 书名2 ...]
```

默认会查询四大名著：
- 红楼梦
- 三国演义
- 水浒传
- 西游记

示例：

```bash
python3 python/files/douban.py 红楼梦 白夜行
```

输出格式：

```text
书名    评分    URL
```

## 5. 从文件列表批量查询豆瓣图书信息

脚本：

```bash
python3 python/files/douban_by_list.py --list-file <文件路径>
```

输入文件格式：
- 每行一个书名
- 建议使用 UTF-8 编码

示例：

```bash
python3 python/files/douban_by_list.py --list-file ./list
```

## 6. 导入 Excel `.xls` 到 MySQL

脚本：

```bash
python3 "python/excel to mysql/excel2mysql.py"
```

配置文件：

```bash
python/excel to mysql/my.conf
```

配置项示例：

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

行为说明：
- 递归扫描 `datapath` 下的 `.xls` 文件
- 根据文件名生成表名
- 根据第一行生成字段名
- 把后续数据行插入到 MySQL

注意：
- 目前只处理 `.xls`
- 表名和字段名会自动做安全清洗

## 7. 根据股票代码导入股票数据

脚本：

```bash
python3 "python/get stock info/Main.py" --code 600519
```

配置文件：

```bash
python/get stock info/conf/gsi.conf
```

行为说明：
- 从 `gsi.conf` 读取数据库和日志配置
- 根据传入的股票代码导入数据

## 快速示例

```bash
# 查看帮助
python3 python/files/join-img.py --help
python3 python/files/combined_images.py --help
python3 python/files/join-pdf.py --help
python3 python/files/douban.py --help
python3 python/files/douban_by_list.py --help
python3 "python/get stock info/Main.py" --help

# 图片 / PDF 工具
python3 python/files/join-img.py --root ./images --overwrite
python3 python/files/combined_images.py --root ./色轮眼 --overwrite
python3 python/files/join-pdf.py --root ./pdf_parts --overwrite

# 豆瓣工具
python3 python/files/douban.py 三体
python3 python/files/douban_by_list.py --list-file ./list
```
