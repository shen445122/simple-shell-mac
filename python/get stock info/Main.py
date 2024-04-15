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

logfile = cf.get("log", "log_file")

logger = logging.getLogger('gsi')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(logfile)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(process)d] %(lineno)d: %(message)s", "%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)

engine_string = 'mysql+mysqlconnector://' + db_user + ':' + db_pwd + '@' + db_host + ':' + db_port + '/' + db_name

def main():
    code = "600519"
    importfunc.importDataByCode(code, logger, engine_string)

    #strategy.checkStrategy(basefunc.changeFile2List(data_new), engine_string)



if __name__ == '__main__':
    main()



