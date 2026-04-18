# simple-shell-mac

一个收集 shell 与 Python 小工具脚本的仓库，主要用于日常自动化、文件处理和数据导入。

## 目录说明

- `shell/`：shell 脚本
- `python/`：Python 工具脚本

## Python 脚本文档

Python 目录下脚本的详细说明、依赖安装方式和使用示例见：

- [python/README.md](python/README.md)

## 快速开始

```bash
git clone git@github.com:shen445122/simple-shell-mac.git
cd simple-shell-mac
```

如果你要使用 Python 脚本，建议先安装依赖：

```bash
# 基础运行依赖
pip install -r python/requirements.txt

# 或者显式安装基础依赖文件
pip install -r python/requirements-base.txt

# 如果需要开发 / 检查工具
pip install -r python/requirements-dev.txt
```

也可以直接使用 `pyproject.toml` 里的可选依赖：

```bash
pip install .[python-scripts]
pip install .[dev]
```
