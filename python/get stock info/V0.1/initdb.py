#_*_ encoding:utf-8 _*_Main
import os,sys,time,datetime
from configparser import ConfigParser

cf = ConfigParser()
cf.read("m3.conf") 

db_user = cf.get("db", "db_user")
db_pwd  = cf.get("db", "db_pwd")
db_host = cf.get("db", "db_host")
db_port = cf.get("db", "db_port")
db_db   = cf.get("db", "db_db")

table_name = "stock_" + time.strftime("%Y%m%d", time.localtime())
create_table_sql = "CREATE TABLE IF NOT EXISTS {} ( \
            id int(10) AUTO_INCREMENT PRIMARY KEY, \
		    name char(6), \
		    open_price float(10), \
		    price float(10), \
		    higt float(10), \
		    low float(10), \
		    threedaysago float(10) \
		    CHARACTER SET utf8 ".format(table_name))

def execute_sql(sql):
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print("[1] create table failed.")
        print("Error: {}".format(err.msg))
        sys.exit(1)

cnx = mysql.connector.connect(user=db_user, host=db_host, database=db_db)
cursor = cnx.cursor()

#execute_sql(create_table_sql)