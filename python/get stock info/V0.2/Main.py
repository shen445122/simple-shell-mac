#_*_ encoding:utf-8 _*_
from configparser import ConfigParser
import logging, os

import basefunc, importfunc, strategy

cf = ConfigParser()
cf.read("gsi.conf")

db_user = cf.get("db", "db_user")
db_pwd  = cf.get("db", "db_pwd")
db_host = cf.get("db", "db_host")
db_port = cf.get("db", "db_port")
db_name   = cf.get("db", "db_name")

data_dra = cf.get("info", "tops_file1")
data_hsc = cf.get("info", "tops_file2")
data_ydyl = cf.get("info", "tops_file3")

hsc_url = cf.get("url", "hscurl")
ydyl_url = cf.get("url", "ydylurl")

logfile = cf.get("log", "log_file")

logger = logging.getLogger('gsi')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(logfile)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(process)d] %(lineno)d: %(message)s", "%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)

engine_string = 'mysql+mysqlconnector://' + db_user + ':' + db_pwd + '@' + db_host + ':' + db_port + '/' + db_name

def main():
    #1 开盘日获取数据
    #importfunc.importDataDaily(logger, engine_string)

    #2 data_hsc data_dra data_ydyl
    #print("====="+"DRA"+"=====")
    #data_list = basefunc.changeFile2List(data_ydyl)
    #strategy.checkStrategy2(data_list, engine_string)

    #3 stock_hs300s_2016_08_01 stock_zz500s_2016_08_01
    #print("====="+"HS300"+"=====")
    #strategy.checkStrategy2(basefunc.getCodeFromSpecialKeyword('stock_hs300s_2016_08_01','date','2016', engine_string), engine_string)

    #4 'stock_concept_2017_2' 'c_name','雄安新区' 或 'stock_gsb_2017_1','name',''
    #print("====="+"XAXQ"+"=====")
    #strategy.checkStrategy2(basefunc.getCodeFromSpecialKeyword('stock_concept_2017_2', 'c_name', '雄安新区', engine_string), engine_string)
    #print("====="+"ALL"+"=====")
    #strategy.checkStrategy2(basefunc.getCodeFromSpecialKeyword('stock_gsb_2017_1','name',''), engine_string)

    #5
    #print("====="+"HIS"+"=====")
    #strategy.checkRollbackBest(mylist, 10, engine_string)
    #strategy.checkRollback(basefunc.getCodeFromSpecialKeyword('stock_concept_2017_2', 'c_name', '雄安新区', engine_string), engine_string)
    #strategy.checkRollbackBest(basefunc.getTitleInfo('stock_profit_2017_4', 'code', 'divi', 2, engine_string), 10, engine_string)
    #strategy.checkRollbackBest(basefunc.getCodeFromSpecialKeyword('stock_concept_2017_2', 'c_name', '雄安新区', engine_string), 10, engine_string)

    #tmp
    #print("20170616")
    
    #print('总收益:', basefunc.getrReturnFromDict({'600988': {'buy': 14.0, 'rate': 0.079000000000000001}, '002258': {'buy': 12.7, 'rate': 0.33700000000000002}}, 'stock_2017_09_29', 100000, engine_string))
    #print('总收益:', basefunc.getrReturnFromDict({'002859': {'buy': 86.55, 'rate': 0.14299999999999999}, '000990': {'buy': 18.38, 'rate': 0.41699999999999998}, '603626': {'buy': 66.13, 'rate': 0.14499999999999999}}, 'stock_2017_09_29', 100000, engine_string))
    #print('总收益:', basefunc.getrReturnFromDict({'601339': {'buy': 5.94, 'rate': 0.184}, '600551': {'buy': 14.81, 'rate': 0.033000000000000002}, '603658': {'buy': 43.98, 'rate': 0.20399999999999999}, '603388': {'buy': 39.9, 'rate': 0.28000000000000003}, '002370': {'buy': 29.43, 'rate': 0.29899999999999999}}, 'stock_2017_09_29', 100000, engine_string))
    #print('总收益:', basefunc.getrReturnFromDict({'300195': {'buy': 14.63, 'rate': 0.064000000000000001}, '002853': {'buy': 91.13, 'rate': 0.13}, '002852': {'buy': 68.74, 'rate': 0.38200000000000001}, '300457': {'buy': 75.24, 'rate': 0.185}, '600551': {'buy': 14.81, 'rate': 0.23999999999999999}}, 'stock_2017_09_29', 100000, engine_string))
    #print('总收益:', basefunc.getrReturnFromDict({'002138': {'buy': 20.18, 'rate': 0.058999999999999997}, '600545': {'buy': 10.73, 'rate': 0.056000000000000001}, '600988': {'buy': 14.0, 'rate': 0.22500000000000001}, '603960': {'buy': 29.27, 'rate': 0.32400000000000001}, '600551': {'buy': 14.81, 'rate': 0.33500000000000002}}, 'stock_2017_09_29', 100000, engine_string))
    #print('总收益:', basefunc.getrReturnFromDict(, '', 100000, engine_string))

if __name__ == '__main__':
    main()
