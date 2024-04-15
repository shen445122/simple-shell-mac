#_*_ encoding:utf-8 _*_

import mysql.connector
import sys, os
from configparser import ConfigParser

cf = ConfigParser()
cf.read("m3.conf") 

user = cf.get("db", "db_user")
pwd  = cf.get("db", "db_pwd")
host = cf.get("db", "db_host")
port = cf.get("db", "db_port")
db   = cf.get("db", "db_db")

data_file = 'data.dat'

create_table_sql = "CREATE TABLE IF NOT EXISTS sttable ( \
            id int(10) AUTO_INCREMENT PRIMARY KEY, \
		    st_id char(6), \
		    buy float(10), \
		    sell_low float(10), \
		    sell_high float(10), \
		    day_low float(10), \
		    day_high float(10), \
		    now float(10), \
		    earn_rate float(10), \
		    buy_rate float(10), \
		    sell_rate float(10) ) \
		    CHARACTER SET utf8 " 

cnx = mysql.connector.connect(user=user, host=host, database=db)
cursor = cnx.cursor()

def create_table(create_table_sql):

    try:
        cursor.execute(create_table_sql)
    except mysql.connector.Error as err:
        print("create table 'sttable' failed.")
        print("Error: {}".format(err.msg))
        sys.exit()
 
def include_data(data_file):

    create_table(create_table_sql)

    if os.path.exists(data_file):
        myfile = open(data_file)
        lines = myfile.readlines()
        myfile.close()
        for line in lines:
            myset = line.split()
            sql = "INSERT INTO sttable (st_id, buy, sell_low, sell_high) VALUES ({}, {}, {}, {})".format(myset[0], myset[1], myset[2], myset[3])
            try:
                cursor.execute(sql)
            except mysql.connector.Error as err:
                print("insert table 'sttable' from file '{}' -- failed.".format(data_file))
                print("Error: {}".format(err.msg))
                sys.exit()

include_data(data_file)
cnx.commit()
cursor.close()
cnx.close()
