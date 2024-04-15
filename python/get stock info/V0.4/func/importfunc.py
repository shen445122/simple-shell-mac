# 【调用其他函数】将特定股票代码的数据导入数据库
def importDataByCode(code, logger, engine_string):
    from func import basefunc
    import datetime
    import tushare as ts
    from sqlalchemy import create_engine

    runtime = datetime.datetime.today().isoweekday()
    if runtime :#<= 6:
        table_name = 'stock_' + code + '_' + datetime.datetime.now().strftime('%Y_%m_%d')

        if basefunc.showTables(engine_string) == None :
            gta = ts.get_hist_data(code)
            engine = create_engine(engine_string)
            logger.info('save data to mysql : %s' %table_name)
            #gta.to_excel("/Users/shen.szr/Downloads/code.xlsx")
            #gta.to_sql(table_name, engine, index=False, index_label="date")
        elif table_name in basefunc.showTables(engine_string):
            logger.warning('table alread exit : %s' %table_name)
        else:
            gta = ts.get_hist_data(code, ktype='W')
            engine = create_engine(engine_string)
            logger.info('save data to mysql : %s' %table_name)

            excelfile = "/Users/shen.szr/Downloads/" + code + ".xlsx"
            gta.to_excel(excelfile)
            gta.to_sql(table_name, engine, if_exists='replace', dtypes={'date':VARCHAR(200)})

# 【调用其他函数】将每天的数据导入数据库
def importDataDaily(logger, engine_string):
    from func import basefunc
    import datetime
    import tushare as ts
    from sqlalchemy import create_engine

    runtime = datetime.datetime.today().isoweekday()
    if runtime :#<= 6:
        table_name = 'stock_' + datetime.datetime.now().strftime('%Y_%m_%d')
        print(table_name)

        if basefunc.showTables(engine_string) == None :
            gta = ts.get_today_all()
            engine = create_engine(engine_string)
            logger.info('save data to mysql : %s' %table_name)
            gta.to_sql(table_name, engine)
        elif table_name in basefunc.showTables(engine_string):
            logger.warning('table alread exit : %s' %table_name)
        else:
            gta = ts.get_today_all()
            engine = create_engine(engine_string)
            logger.info('save data to mysql : %s' %table_name)
            gta.to_sql(table_name, engine)

# 将每季度的数据导入数据库,1月，4月，7月，10月的第一天可以执行
def importDataMonth(logger, engine_string):
    import datetime
    import tushare as ts
    from sqlalchemy import create_engine

    engine = create_engine(engine_string)

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')

    #分配预案
    tpd = ts.profit_data(year=year,top=1000)
    #概念板块
    #gccd = ts.get_concept_classified()

    for (power,power_string) in [(tpd,'tpd')]:
    #for (power,power_string) in [(gccd,'gccd')]:
        table_name = 'stock_' + power_string + '_' + year + '_' + month
        power = power.reset_index()
        logger.info('save data to mysql : %s' %table_name)
        power.to_sql(table_name,engine)

# 将每季度的数据导入数据库,1月，4月，7月，10月的第一天可以执行
def importDataQuarter(engine_string):
    import datetime
    import tushare as ts
    from sqlalchemy import create_engine

    engine = create_engine(engine_string)

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    if month in ['01','02','03']:
        quarter = 1
    elif month in ['04','05','06']:
        quarter = 2
    elif month in ['07','08','09']:
        quarter = 3
    elif month in ['10','11','12']:
        quarter = 4

    #股票基本面
    #gsb = ts.get_stock_basics()
    #地域板块
    #gicd = ts.get_industry_classified()
    #业绩报告
    #grd = ts.get_report_data(year,quarter)
    #盈利能力
    #gpd = ts.get_profit_data(year,quarter)
    #营运能力
    #god = ts.get_operation_data(year,quarter)
    #成长能力
    #ggd = ts.get_growth_data(year,quarter)
    #偿债能力
    #gdd = ts.get_debtpaying_data(year,quarter)
    #现金能力
    #gcd = ts.get_cashflow_data(year,quarter)


    #for (power,power_string) in [(gsb,'gsb'),(grd,'grd'),(gpd,'gpd'),(god,'god'),(ggd,'ggd'),(gdd,'gdd'),(gcd,'gcd'),(gccd,'gccd'),(gicd,'gicd'),(tpd,'tpd')]:
    #    table_name = 'stock_' + power_string + '_' + year + '_' + quarter
    #    power = power.reset_index()
    #    power.to_sql(table_name,engine)

# 将每年的数据导入数据库,每年的1月1日的第一天可以执行
def importDataYear(engine_string):
    import datetime
    import tushare as ts
    from sqlalchemy import create_engine

    engine = create_engine(engine_string)

    #沪深300指数
    ghs300 = ts.get_hs300s()
    #中证500指数
    gzz500 = ts.get_zz500s()
    #行业分类
    gic = ts.get_industry_classified()
    #概念分类
    gcc = ts.get_concept_classified()

    table_name_hs300s = 'stock_hs300s_' + datetime.datetime.now().strftime('%Y_%m_%d')
    table_name_zz500s = 'stock_zz500s_' + datetime.datetime.now().strftime('%Y_%m_%d')
    table_name_gic = 'stock_gic_' + datetime.datetime.now().strftime('%Y_%m_%d')
    table_name_gcc = 'stock_gcc_' + datetime.datetime.now().strftime('%Y_%m_%d')

    ghs300.to_sql(table_name_hs300s,engine)
    gzz500.to_sql(table_name_zz500s,engine)
    gic.to_sql(table_name_gic,engine)
    gcc.to_sql(table_name_gic,engine)

