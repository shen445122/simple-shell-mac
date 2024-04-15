#_*_ encoding:utf-8 _*_
import os,sys,time,datetime
import urllib.request
import mysql.connector
from configparser import ConfigParser
import tushare

cf = ConfigParser()
cf.read("m3.conf") 

user = cf.get("db", "db_user")
pwd  = cf.get("db", "db_pwd")
host = cf.get("db", "db_host")
port = cf.get("db", "db_port")
db   = cf.get("db", "db_db")

data_dragon = cf.get("info", "tops_file1")
data_hsc = cf.get("info", "tops_file2")

cnx = mysql.connector.connect(user=user, host=host, database=db)
cursor = cnx.cursor()

def getOpenday():
    todays_num = datetime.datetime.today().isoweekday()
    if todays_num < 4:
        revise_days = 5
    else:
        revise_days = 3
    return revise_days

def checkNumber():
    pass

def include_data(data_file):
    if os.path.exists(data_file):

        df = open(data_file)
        lines = df.readlines()
        myfile.close()

        for line in lines:
            stockIndex = line.split()
            stockNumber = stockIndex[0]
            stockName = stockIndex[1]
            date_3days_ago = (datetime.datetime.now()-datetime.timedelta(days=getOpenday())).strftime("%Y-%m-%d")

            stInfo = tushare.get_realtime_quotes(stockNumber) 
            stInfo_3days_ago = tushare.get_hist_data(stockNumber,start=date_3days_ago,end=date_3days_ago)

            stInfoNeed = stInfo[['code','name','open','price','high','low','time']]
            stInfoNeed_3days_ago = stInfo_3days_ago[['open','high','close','low']]

            stStr = stInfoNeed.to_json()
            stStr_3days_ago = stInfoNeed_3days_ago.to_json()

            stJson = eval(stStr)
            stJson_3days_ago = eval(stStr_3days_ago)

            price = float(stJson["price"]["0"])
            open_price = float(stJson["open"]["0"])
            low = float(stJson["low"]["0"])
            high = float(stJson["high"]["0"])
            code = str(stJson["code"]["0"])
            name = str(stJson["name"]["0"])

            try:
                open_price_3days_ago = float(stJson_3days_ago["open"][date_3days_ago])
            except KeyError as err:
                print("{} 没有三天前的数据:{}".format(name,err))
            

            if price > open_price:
                if ((open_price - low) / (price - open_price)) >= 1:
                    if (high - price + low) < open_price:
                        if open_price < open_price_3days_ago:
                            print(code,name)
                    

            #execute_sql(include_sql)



print("====="+"DRA"+"=====")
include_data(data_file1)
print("====="+"HSC"+"=====")
include_data(data_file2)
cnx.commit()
cursor.close()
cnx.close()
