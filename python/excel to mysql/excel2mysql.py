#-*- coding: utf-8 -*-
import os,sys,datetime
import mysql.connector
import xlrd
from configparser import ConfigParser

cf = ConfigParser()
cf.read("my.conf")

username = cf.get("db", "db_user")
password  = cf.get("db", "db_pwd")
host = cf.get("db", "db_host")
port = cf.get("db", "db_port")
database   = cf.get("db", "db_db")
datapath = cf.get("data", "datapath")

def importDataHelper(username, database, datapath):
    try:
        conn = mysql.connector.connect(user=username, database=database, use_unicode=True)
    except mysql.connector.errors.ProgrammingError as e:
        print(e)
        return -1
    lists = getFilesList(datapath)
    nfiles = len(lists[0])
    cursor = conn.cursor()
    for file_idx in range(0, nfiles):
        file_path = lists[0][file_idx]
        print("processing file(%d/%d):[ %s ]"%(file_idx+1, nfiles, file_path))
        table_name = lists[1][file_idx]
        num = storeData(file_path, table_name, cursor)
        if num >= 0:
            print("[ %d ] data have been stored in TABLE:[ %s ]"%(num, table_name))
        conn.commit()
    cursor.close()
    conn.close()

'''
get files list in the dir, including the files in its sub-folders
the return list contain two elements, the first element is a file names list
and the second element is a table names list(will be used for creating tables in database),
'''
def getFilesList(dir):
    path_list = []
    table_list = []
    file_name_list = os.listdir(dir)
    for file_name in file_name_list:
        path = os.path.join(dir, file_name)
        if os.path.isdir(path):
            tmp_lists = getFilesList(path)
            path_list.extend(tmp_lists[0])
            table_list.extend(tmp_lists[1])
        else:
            path_list.append(path)
            file_name = file_name.split('.')[0] #remove .xls
            file_name = file_name.split('from')[0] #remove characters after 'from'
            file_name = file_name.strip()#remove redundant space at both ends
            file_name = file_name.replace(' ','_') #replace ' ' with '_'
            file_name = file_name.replace('-','_') #replace ' ' with '_'
            file_name = file_name.lower() #convert all characters to lowercase
            table_list.append(file_name)
    return [path_list, table_list]

def storeData(file_path, table_name, cursor):
    ret = 0
    file = xlrd.open_workbook(file_path)
    sheet = file.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols
    col_names = []
    for i in range(0, ncols):
        title = sheet.cell(0, i).value
        title = title.strip()
        title = title.strip(')')
        title = title.replace(' ','_')
        title = title.replace('(','_')
        title = title.lower()
        col_names.append(title)
    sql = 'create table '\
          +table_name+' ('

    for i in range(0, ncols):
        sql = sql + col_names[i] + ' varchar(150)'
        if i != ncols-1:
            sql += ','
    sql = sql + ')'
    try:
        cursor.execute(sql)
    except mysql.connector.errors.ProgrammingError as e:
        print(e)

    '''insert data'''
    #construct sql statement
    sql = 'insert into '+table_name+'('
    for i in range(0, ncols-1):
        sql = sql + col_names[i] + ', '
    sql = sql + col_names[ncols-1]
    sql += ') values ('
    sql = sql + '%s,'*(ncols-1)
    sql += '%s)'
    #get parameters
    parameter_list = []
    for row in range(2, nrows):
        for col in range(0, ncols):
            cell_type = sheet.cell_type(row, col)
            cell_value = sheet.cell_value(row, col)
            if cell_type == xlrd.XL_CELL_DATE:
                dt_tuple = xlrd.xldate_as_tuple(cell_value, file.datemode)
                meta_data = str(datetime.datetime(*dt_tuple))
            else:
                meta_data = sheet.cell(row, col).value
            parameter_list.append(meta_data)
        # cursor.execute(sql, parameter_list)
        try:
            cursor.execute(sql, parameter_list)
            parameter_list = []
            ret += 1
        except mysql.connector.errors.ProgrammingError as e:
            print(e)
            # return -1
    return ret



if __name__ == "__main__":
    importDataHelper(username, database, datapath)
