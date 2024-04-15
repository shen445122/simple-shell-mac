#_*_ encoding:utf-8 _*_
# 补全股票代码(6位股票代码)
# input: int or string
# output: string
def getSixDigitalStockCode(code):
    strZero = ''
    for i in range(len(str(code)), 6):
        strZero += '0'
    return strZero + str(code)

# 检查列表中大于或小于某个值的数据有多少个
# input: 列表，compara：1为大于（默认），0为小于，norm_num：基准数值，count：满足条件的有多少个
# output：符合条件的个数与给定相同返回true，否则返回false
def checkListDiff(list=[], compara=1, norm_num=0, count=1):
    result_list = []
    max_length = len(list)
    if count <= max_length:
        if compara == 0:
            for n in list:
                if n < norm_num:
                    result_list.append(n)
            if len(result_list) == count:
                return True
            else:
                return False
        if compara == 1:
            for n in list:
                if n > norm_num:
                    result_list.append(n)
            if len(result_list) == count:
                return True
            else:
                return False
    else:
        print("[Error] argument count too big!")

# 从指定的数据表中获取单个股票的信息
# input: table name , code like 000001
def getStockInfo(table, code, engine_string):
    import pandas as pd
    import sys
    from sqlalchemy import create_engine
    try:
        sql = "select * from %s where code='%s'" % (table, code)
        engine = create_engine(engine_string)
        df = pd.read_sql_query(sql, engine)
        se = df.ix[0]
        return se
    except Exception as e:
        pass

# 从指定的数据表中获取某一列数据
# input: table name , code like 000001
def getTitleInfo(table, title, order, orderby, engine_string):
    import pandas as pd
    from sqlalchemy import create_engine
    try:
        if order:
            if orderby == 0 :
                sql = "select %s from %s" % (title, table)
            elif orderby == 1:
                sql = "select %s from %s order by %s asc" % (title, table, order)
            elif orderby == 2:
                sql = "select %s from %s order by %s desc" % (title, table, order)

        engine = create_engine(engine_string)
        df = pd.read_sql_query(sql, engine)
        se = df[title].tolist()
    except Exception as e:
        print(e)
    return se

# 从指定数据表中查找股票名称的代码
# input: table name, name like '金运激光'
# output：打印股票代码到终端
def getCodeFromName(table, name, engine_string):
    import pandas as pd
    from sqlalchemy import create_engine
    try:
        sql = "select * from %s where name='%s'" % (table, name)
        engine = create_engine(engine_string)
        df = pd.read_sql_query(sql, engine)
        se = df.ix[0]
        print(se['code'])
    except Exception as e:
        pass
    #return se['code']

# 【调用其他函数】从指定数据表中查找股票名称的代码
# input: table name, file include name like '金运激光'，一行一个
# output：打印股票代码到终端
def getCodeFromNameFile(table, file, engine_string):
    try:
        for name in open(file):
            name = name.strip()
            getCodeFromName(table, name, engine_string)
    except Exception as e:
        print('Can not find infomation by name : %s' %name )

# 从指定数据库表中的某一列查找包含关键字那一行的代码
# input：数据库表名称，某一列的名称，某一列的关键字（默认为空）
# output:返回符合条件的股票代码code列表
def getCodeFromSpecialKeyword(table, row_name, row_keyword, engine_string):
    import pandas as pd
    from sqlalchemy import create_engine
    import sys
    try:
        code_list = []
        sql = "select code from {} where {} like '%{}%'".format(table, row_name, row_keyword)
        engine = create_engine(engine_string)
        df = pd.read_sql_query(sql, engine)
        se = df.ix[0]
        df_dict = df.to_dict()['code']
        for v in df_dict.values():
            code_list.append(v)
        return code_list
    except Exception as e:
        pass

# 【需要联网访问】 访问给定url并获取网页中出现的股票代码
# input:网页地址
# output:返回一个含有股票代码的list
def createCodeFromUrl(url):
    import requests
    import bs4
    respons = requests.get(url)
    list_code = []
    soup = bs4.BeautifulSoup(respons.text,'lxml')
    list_original = [i.string for i in soup.select('td a[href]')]
    for data_original in list_original:
        if data_original.isdigit():
            list_code.append(data_original)
    return list_code


# 列出数据库的所有表,返回一个列表
def showTables(engine_string):
    import pandas as pd
    from sqlalchemy import create_engine
    try:
        df_list = []
        sql = "show tables"
        engine = create_engine(engine_string)
        df = pd.read_sql_query(sql, engine)
        df_dict = df.to_dict()['Tables_in_stock']
        for v in df_dict.values():
            df_list.append(v)
        return df_list
    except Exception as e:
        pass

# 将一份列表文件转换为列表，列表文件每行仅有一列
def changeFile2List(file):
    import os
    if os.path.isfile(file):
        index_list = []
        for stock_index in open(file):
            stock_index = stock_index.strip()
            index_list.append(stock_index)
    return index_list

def getrReturnFromDict(dict_stocks, table, cash, engine_string):
    returnlist = []
    returnsum = 0
    for code in dict_stocks:
        price_buy = dict_stocks[code]['buy']
        price_rate = dict_stocks[code]['rate']
        if not table:
            list_stocks = []
            for table_db in showTables(engine_string):
                if 'stock_201' in table_db:
                    list_stocks.append(table_db)
                    table = list_stocks[len(list_stocks)-1]
        stInfo = getStockInfo(table, code, engine_string)
        getreturn = (stInfo['trade'] - price_buy) / price_buy * price_rate * cash
        rangereturn = (stInfo['trade'] - price_buy) / price_buy * 100
        returnlist.append(getreturn)
        print('%s[%s]: Buy:%.2f, Sell:%.2f, Rate:%.3f, Range:%.3f%%, Return:%d' %(stInfo['name'], code, price_buy, stInfo['trade'], price_rate, rangereturn, getreturn))
    for ret in returnlist:
        returnsum = returnsum + ret

    return returnsum




