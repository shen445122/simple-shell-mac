#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import .xls data files into MySQL tables.

Configuration is read from my.conf in the same directory.
"""

from __future__ import annotations

import datetime
import re
from configparser import ConfigParser
from pathlib import Path

import mysql.connector
import xlrd

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / 'my.conf'
IDENTIFIER_RE = re.compile(r'[^0-9a-zA-Z_]+')


def load_config(config_path: Path = CONFIG_PATH) -> ConfigParser:
    parser = ConfigParser()
    if not parser.read(config_path, encoding='utf-8'):
        raise FileNotFoundError(f'Config file not found: {config_path}')
    return parser


def sanitize_identifier(value: str) -> str:
    cleaned = IDENTIFIER_RE.sub('_', value.strip().lower())
    cleaned = re.sub(r'_+', '_', cleaned).strip('_')
    if not cleaned:
        cleaned = 'column'
    if cleaned[0].isdigit():
        cleaned = f'c_{cleaned}'
    return cleaned


def get_files_list(root: Path):
    path_list = []
    table_list = []
    for path in sorted(root.rglob('*.xls')):
        table_name = sanitize_identifier(path.stem.split('from')[0].replace('-', '_').replace(' ', '_'))
        path_list.append(path)
        table_list.append(table_name)
    return path_list, table_list


def workbook_cell_to_string(sheet, workbook, row: int, col: int) -> str:
    cell_type = sheet.cell_type(row, col)
    cell_value = sheet.cell_value(row, col)
    if cell_type == xlrd.XL_CELL_DATE:
        dt_tuple = xlrd.xldate_as_tuple(cell_value, workbook.datemode)
        return str(datetime.datetime(*dt_tuple))
    return str(cell_value).strip()


def store_data(file_path: Path, table_name: str, cursor) -> int:
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols
    if nrows == 0 or ncols == 0:
        return 0

    column_names = []
    seen = {}
    for index in range(ncols):
        name = sanitize_identifier(str(sheet.cell(0, index).value).strip().strip(')'))
        count = seen.get(name, 0)
        seen[name] = count + 1
        if count:
            name = f'{name}_{count + 1}'
        column_names.append(name)

    create_sql = 'CREATE TABLE IF NOT EXISTS `{}` ({})'.format(
        table_name,
        ', '.join(f'`{name}` VARCHAR(150)' for name in column_names),
    )
    cursor.execute(create_sql)

    insert_sql = 'INSERT INTO `{}` ({}) VALUES ({})'.format(
        table_name,
        ', '.join(f'`{name}`' for name in column_names),
        ', '.join(['%s'] * ncols),
    )

    inserted = 0
    for row in range(1, nrows):
        values = [workbook_cell_to_string(sheet, workbook, row, col) for col in range(ncols)]
        cursor.execute(insert_sql, values)
        inserted += 1
    return inserted


def import_data_helper() -> None:
    config = load_config()
    username = config.get('db', 'db_user')
    password = config.get('db', 'db_pwd')
    host = config.get('db', 'db_host')
    port = config.getint('db', 'db_port')
    database = config.get('db', 'db_db')
    data_path = Path(config.get('data', 'datapath')).expanduser().resolve()

    files, tables = get_files_list(data_path)
    if not files:
        print(f'No .xls files found under {data_path}')
        return

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        port=port,
        database=database,
        use_unicode=True,
    )
    try:
        cursor = connection.cursor()
        try:
            for index, file_path in enumerate(files, start=1):
                table_name = tables[index - 1]
                print(f'processing file({index}/{len(files)}): [ {file_path} ]')
                count = store_data(file_path, table_name, cursor)
                print(f'[ {count} ] rows stored in TABLE: [ {table_name} ]')
                connection.commit()
        finally:
            cursor.close()
    finally:
        connection.close()


if __name__ == '__main__':
    import_data_helper()
