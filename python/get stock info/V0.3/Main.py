#_*_ encoding:utf-8 _*_
from configparser import ConfigParser
import logging, os

from func import basefunc, importfunc, strategy

cf = ConfigParser()
cf.read("conf/gsi.conf")

db_user = cf.get("db", "db_user")
db_pwd  = cf.get("db", "db_pwd")
db_host = cf.get("db", "db_host")
db_port = cf.get("db", "db_port")
db_name   = cf.get("db", "db_name")

data_dra = cf.get("info", "tops_file1")
data_hsc = cf.get("info", "tops_file2")
data_ydyl = cf.get("info", "tops_file3")
data_new = cf.get("info", "tops_file4")
strategyRB = cf.get("info", "strategyRB")

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
    importfunc.importDataDaily(logger, engine_string)
    #importfunc.importDataMonth(logger, engine_string)

    #2
    #strategy.checkRollbackBest(basefunc.getTitleInfo('stock_tpd_2018_01', 'code', 'divi', 2, engine_string), 10, engine_string)

    #print(basefunc.getCodeFromSpecialKeyword('stock_gccd_2018_01', 'c_name', '次新', engine_string))
    #strategy.checkRollbackBest(basefunc.getTitleInfo('stock_tpd_2018_01', 'code', 'divi', 2, engine_string), 10, engine_string)
    strategy.checkStrategy(basefunc.changeFile2List(data_new), engine_string)

    #2.1
    #strategy.checkRollbackBestAcception(strategyRB, '', engine_string)


if __name__ == '__main__':
    main()



