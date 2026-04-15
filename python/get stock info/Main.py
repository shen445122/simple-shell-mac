#!/usr/bin/env python3
# _*_ encoding:utf-8 _*_

from __future__ import annotations

import argparse
import logging
from configparser import ConfigParser
from pathlib import Path

from func import importfunc

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / 'conf' / 'gsi.conf'
LOGGER_NAME = 'gsi'


def load_config(config_path: Path = CONFIG_PATH) -> ConfigParser:
    parser = ConfigParser()
    if not parser.read(config_path, encoding='utf-8'):
        raise FileNotFoundError(f'Config file not found: {config_path}')
    return parser


def build_engine_string(config: ConfigParser) -> str:
    return 'mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{name}'.format(
        user=config.get('db', 'db_user'),
        pwd=config.get('db', 'db_pwd'),
        host=config.get('db', 'db_host'),
        port=config.get('db', 'db_port'),
        name=config.get('db', 'db_name'),
    )


def configure_logger(log_file: str) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(process)d] %(lineno)d: %(message)s',
        '%Y-%m-%d %H:%M:%S',
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Import stock data by code.')
    parser.add_argument('--code', default='600519', help='Stock code to import.')
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config()
    logger = configure_logger(config.get('log', 'log_file'))
    engine_string = build_engine_string(config)
    importfunc.importDataByCode(args.code, logger, engine_string)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
