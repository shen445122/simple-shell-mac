#_*_ encoding:utf-8 _*_

import os,sys,time,datetime
import mysql.connector

from configparser import ConfigParser
from sqlalchemy import create_engine

import tushare as ts

cf = ConfigParser()
cf.read("gsi.conf") 

db_user = cf.get("db", "db_user")
db_pwd  = cf.get("db", "db_pwd")
db_host = cf.get("db", "db_host")
db_port = cf.get("db", "db_port")
db_name   = cf.get("db", "db_name")

engine_string = 'mysql+mysqlconnector://' + db_user + ':@' + db_host + ':' + db_port + '/' + db_name
engine = create_engine(engine_string)


def loopToImportData():
	year = 2017
	for quarter in range(1,5):
		#股票基本面
		#print(get_stock_basics)
		#gsb = ts.get_stock_basics()
		#业绩报告
		print('业绩报告:%d-%d \n' %(year,quarter))
		grd = ts.get_report_data(year,quarter)
		#盈利能力
		print('盈利能力:%d-%d \n' %(year,quarter))
		gpd = ts.get_profit_data(year,quarter)
		#营运能力
		print('营运能力:%d-%d \n' %(year,quarter))
		god = ts.get_operation_data(year,quarter)
		#成长能力
		print('成长能力:%d-%d \n' %(year,quarter))
		ggd = ts.get_growth_data(year,quarter)
		#偿债能力
		print('偿债能力:%d-%d \n' %(year,quarter))
		gdd = ts.get_debtpaying_data(year,quarter)
		#现金能力
		print('现金能力:%d-%d \n' %(year,quarter))
		gcd = ts.get_cashflow_data(year,quarter)

		for (power,power_string) in [(grd,'grd'),(gpd,'gpd'),(god,'god'),(ggd,'ggd'),(gdd,'gdd'),(gcd,'gcd')]:
			table_name = 'stock_' + power_string + '_' + str(year) + '_' + str(quarter)
			power = power.reset_index()
			power.to_sql(table_name,engine)

# 获取三天前的开盘修正时间
def getOpenday():
    todays_num = datetime.datetime.today().isoweekday()
    if todays_num < 4 or todays_num == 7:
        revise_days = 5
    elif todays_num == 6:
        revise_days = 4
    else:
        revise_days = 3
    return revise_days





