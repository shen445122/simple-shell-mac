#_*_ encoding:utf-8 _*_
import os,sys,time
import urllib.request
import json
import mysql.connector
from configparser import ConfigParser
import tushare

## http request header
send_headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'hq.sinajs.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

## config
cf = ConfigParser()
cf.read("m3.conf") 
user = cf.get("db", "db_user")
pwd  = cf.get("db", "db_pwd")
host = cf.get("db", "db_host")
port = cf.get("db", "db_port")
db   = cf.get("db", "db_db")
data_file = cf.get("info", "data_file")
table = "sttable"

## connect mysql
cnx = mysql.connector.connect(user=user, host=host, database=db)
cursor = cnx.cursor()

def select_best(table):
    select_sql_line = "SELECT id, st_id, buy, sell_low, sell_high, now, earn_rate, buy_rate FROM {}".format(table)
    try:
        cursor.execute(select_sql_line)
        for (id, st_id, buy, sell_low, sell_high, now, earn_rate, buy_rate) in cursor:
            if buy_rate < 0:
                print("ID:{}  st_id:{}  earn_rate:{} buy_rate:{}".format(id, st_id, earn_rate, buy_rate))
    except mysql.connector.Error as err:
        print("query table 'sttable' failed.")
        print("Error: {}".format(err.msg))
        sys.exit()

def get_st_id(table):
    select_sql_line = "SELECT id, buy, st_id, sell_low FROM {}".format(table)
    st_id_list = []
    try:
        cursor.execute(select_sql_line)
        for (id, buy, st_id, sell_low) in cursor:
            st_id_list.append((buy, st_id, sell_low))
        return st_id_list
    except mysql.connector.Error as err:
        print("query table failed.")
        print("Error: {}".format(err.msg))
        sys.exit()

def update_data(id_list):
    for buy, st_id, sell_low in id_list:
        buy = float(buy)
        sell_low = float(sell_low)
        try:
            stInfo = tushare.get_realtime_quotes(st_id) 
            stInfoNeed = stInfo[['code','price','bid','ask','high','low','time']]
            stStr = stInfoNeed.to_json()
            stJson = eval(stStr)
        except:
            print("Error: {}".format("something error"))

        now = float(stJson["price"]["0"])
        day_low = float(stJson["low"]["0"])
        day_high = float(stJson["high"]["0"])
        earn_rate = (sell_low - buy) / buy * 100
        buy_rate = (now - buy) / buy * 100
        sell_rate = ((now - buy) / (sell_low - buy)) * 100
        sql = "UPDATE {} SET now={},day_low={},day_high={},earn_rate={},buy_rate={},sell_rate={} WHERE st_id={}".format(table, now, day_low, day_high, earn_rate, buy_rate, sell_rate, st_id)
        try:
            cursor.execute(sql)
        except:
            print("insert table 'sttable' from file '{}' -- failed.".format(data_file))
            print("Error: {}".format(err.msg))
            sys.exit()

def create_table_time():
    try:
        id_set = []
        st_id_sql = ""
        st_col = ""
        st_value = ""
        
        select_sql_line = "SELECT id, st_id, buy, sell_low, sell_high, now, earn_rate, buy_rate, sell_rate FROM sttable"
        cursor.execute(select_sql_line)
        for (id, st_id, buy, sell_low, sell_high, now, earn_rate, buy_rate, sell_rate) in cursor:
            if buy_rate:
                id_set.append((st_id,buy_rate))
        for st_id,buy_rate in id_set:
            st_id_sql = st_id_sql + "st_{} float(10),".format(st_id)

        st_id_sql = st_id_sql[0:-1]
        create_table_sql_time = "CREATE TABLE IF NOT EXISTS sttable_time ( \
                                 Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
                                 {} ) \
                                 CHARACTER SET utf8".format(st_id_sql)
        for st_id,buy_rate in id_set:
            st_col = st_col + "st_{},".format(st_id)
            st_value = st_value + "{},".format(buy_rate)
        st_col = st_col[0:-1]
        st_value = st_value[0:-1]
        insert_data_sql =  "INSERT INTO sttable_time ({}) VALUES ({})".format(st_col,st_value)
        cursor.execute(create_table_sql_time)
        cursor.execute(insert_data_sql)
        
    except mysql.connector.Error as err:
        print("query table 'sttable_time' failed.")
        print("Error: {}".format(err.msg))
        sys.exit()

def select_sql():
    select_sql_line = "SELECT id, st_id, buy, sell_low, sell_high, now, earn_rate, buy_rate, sell_rate FROM sttable"
    try:
        cursor.execute(select_sql_line)
        for (id, st_id, buy, sell_low, sell_high, now, earn_rate, buy_rate, sell_rate) in cursor:
            if buy_rate:
                if buy_rate < 0:
                    print("ID:{}  st_id:{}  earn_rate:{} buy_rate:{} sell_rate:{}".format(id, st_id, earn_rate, buy_rate, sell_rate))
    except mysql.connector.Error as err:
        print("query table 'sttable' failed.")
        print("Error: {}".format(err.msg))
        sys.exit()

id_list = get_st_id(table)
update_data(id_list)
create_table_time()
select_sql()

cnx.commit()
cursor.close()
cnx.close()
