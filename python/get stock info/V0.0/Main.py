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
    #strategy.checkRollback(basefunc.getCodeFromSpecialKeyword('stock_concept_2017_2', 'c_name', '雄安新区', engine_string), engine_string)
    strategy.checkRollbackBest(basefunc.getCodeFromSpecialKeyword('stock_concept_2017_2', 'c_name', '送转潜力', engine_string), 10, engine_string)

if __name__ == '__main__':
    main()
