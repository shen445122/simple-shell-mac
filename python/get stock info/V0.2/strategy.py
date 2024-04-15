
# =============================
# 验证策略1 ： 挑选出具有金针探底，且当天开盘价格小于前某一天开盘价格的股票
def checkStrategy(code_list, engine_string):
    import basefunc

    list_stocks = []
    for table in basefunc.showTables(engine_string):
        if 'stock_201' in table:
            list_stocks.append(table)
    date_last = list_stocks[len(list_stocks)-1]
    date_days_ago = list_stocks[len(list_stocks)-4]
    table_today = date_last
    table_days_ago = date_days_ago

    for code in code_list:
        try:
            stInfo = basefunc.getStockInfo(table_today, code, engine_string)
            stInfo_days_ago = basefunc.getStockInfo(table_days_ago, code, engine_string)
            open_today = stInfo['open']
            trade_today = stInfo['trade']
            low_today = stInfo['low']
            high_today = stInfo['high']
            open_days_ago = stInfo_days_ago['open']

            if trade_today > open_today:
                if ((open_today - low_today) / (trade_today - open_today)) >= 3:
                    if (high_today - trade_today + low_today) < open_today:
                        if open_today < open_days_ago:
                            print("%s [%s]" %(stInfo['code'], stInfo['name']))

        except UnboundLocalError as e:
            print('[Error] Can not find any infomation by code: %s: %s '%(code, e))


# 验证策略2：挑选出前4天里面有3天下跌，且当天开盘价小于前4天第一天开盘价格的股票
def checkStrategy2(code_list, engine_string):
    import basefunc

    list_stocks = []
    for table in basefunc.showTables(engine_string):
        if 'stock_201' in table:
            list_stocks.append(table)

    for code in code_list:
        try:
            open_list, trade_list, low_list, high_list = [], [], [], []
            for table in list_stocks[-5:] :
                stInfo = basefunc.getStockInfo(table, code, engine_string)
                open_tmp = stInfo['open']
                trade_tmp = stInfo['trade']
                low_tmp = stInfo['low']
                high_tmp = stInfo['high']
                open_list.append(open_tmp)
                trade_list.append(trade_tmp)
                low_list.append(low_tmp)
                high_list.append(high_tmp)

            if open_list == [0,0,0,0,0]:
                pass
                #print("[Warn] the stock had stop:%s[%s]" %(stInfo['code'],stInfo['name']))

            checklist = [trade_list[x] - open_list[x]  for x in range(0,len(open_list)-1)]

            if basefunc.checkListDiff(checklist, 0, 0, 3):
                open_today = open_list[-1]
                trade_today = trade_list[-1]
                low_today = low_list[-1]
                high_today = high_list[-1]
                if trade_today > open_today:
                    if ((open_today - low_today) / (trade_today - open_today)) >= 2:
                        if (high_today - trade_today + low_today) < open_today:
                            if open_today < open_list[0]:
                                print("%s [%s]"%(stInfo['code'],stInfo['name']))

        except UnboundLocalError as e:
            pass #print('[Error] Can not find any infomation by code: %s' %(code))



# 回测策略：20日均线与50日均线交叉方式选股
def checkStrategy2050(code_list):

    import tushare as ts
    import numpy as np
    import pandas as pd
    import sys, datetime

    for code in code_list:
        print("********%s********"%code)
        #1 Year, Month, Day = '2014', '01', '01'
        #1 start = Year + '-' + Month + '-' + Day
        #1 end = datetime.datetime.now().strftime('%Y-%m-%d')
        bussiness = ts.get_k_data(code) #1 , start, end)
        bussiness["20d"] = np.round(bussiness["close"].rolling(window = 20, center = False).mean(), 2)
        bussiness["50d"] = np.round(bussiness["close"].rolling(window = 50, center = False).mean(), 2)
        bussiness["20d-50d"] = bussiness["20d"] - bussiness["50d"]

        bussiness['Regime'] = np.where(bussiness['20d-50d'] > 0, 1, 0)
        bussiness['Regime'] = np.where(bussiness['20d-50d'] < 0, -1, bussiness['Regime'])

        #print(bussiness['Regime'].value_counts())
        # to ensure that all trades close out
        index_last = bussiness.index.tolist().pop()
        regime_orig = bussiness.ix[index_last, 'Regime']
        bussiness.ix[index_last, 'Regime'] = -1
        bussiness['Signal'] = np.sign(bussiness['Regime'] - bussiness['Regime'].shift(1))
        # Restore original regime data
        bussiness.ix[index_last, 'Regime'] = regime_orig

        bussiness_signals = pd.concat([
            pd.DataFrame({
                "Date": bussiness.loc[bussiness["Signal"] == 1, "date"],
                "Price": bussiness.loc[bussiness["Signal"] == 1, "close"],
                "Regime": bussiness.loc[bussiness["Signal"] == 1, "Regime"],
                "Signal": "Buy"
            }),
            pd.DataFrame({
                "Date": bussiness.loc[bussiness["Signal"] == -1, "date"],
                "Price": bussiness.loc[bussiness["Signal"] == -1, "close"],
                "Regime": bussiness.loc[bussiness["Signal"] == -1, "Regime"],
                "Signal": "Sell"
            }),
        ])

        bussiness_signals.sort_index(inplace = True)
        #gzmt_signals.ix[-1, "Signal"] = "Buy"
        #print(bussiness_signals)

        bussiness_long_profits = pd.DataFrame({
            "Price": bussiness_signals.loc[(bussiness_signals["Signal"] == "Buy") & (bussiness_signals["Regime"] == 1), "Price"],
            "Profit": pd.Series((bussiness_signals["Price"] - bussiness_signals["Price"].shift(1))/bussiness_signals["Price"].shift(1)*100).loc[
                bussiness_signals.loc[(bussiness_signals["Signal"].shift(1) == "Buy") & (bussiness_signals["Regime"].shift(1) == 1)].index
            ].tolist(),
            "End Date": bussiness_signals.loc[(bussiness_signals["Signal"].shift(1) == "Buy") & (bussiness_signals["Regime"].shift(1) == 1), 'Date'].tolist(),
            "Start Date":bussiness_signals.loc[(bussiness_signals["Signal"] == "Buy") & (bussiness_signals["Regime"] == 1), "Date"]
        })

        print(bussiness_long_profits)
        for pro in bussiness_long_profits['Profit'].tolist():
            cash = 100000
            cash = (cash * (100 + pro))/100
        print(cash)
        import time
        time.sleep(1)
        #sys.exit(4)

# 回测策略
def checkRollback(code_list, engine_string):
    import basefunc

    list_stocks = []
    for table in basefunc.showTables(engine_string):
        if 'stock_201' in table:
            list_stocks.append(table)

    for code in code_list:
        try:
            open_list, trade_list, low_list, high_list = [], [], [], []
            first_day = 45
            handle_day = 2
            first_day, buy_day, sell_day = first_day, first_day+5, first_day+handle_day+5
            for table in list_stocks[first_day:buy_day] :
                stInfo = basefunc.getStockInfo(table, code, engine_string)
                open_tmp = stInfo['open']
                trade_tmp = stInfo['trade']
                low_tmp = stInfo['low']
                high_tmp = stInfo['high']
                open_list.append(open_tmp)
                trade_list.append(trade_tmp)
                low_list.append(low_tmp)
                high_list.append(high_tmp)

            if open_list == [0,0,0,0,0]:
                pass #print("[Warn] the stock had stop:%s[%s]" %(stInfo['code'],stInfo['name']))

            checklist = [trade_list[x] - open_list[x]  for x in range(0,len(open_list)-1)]

            if basefunc.checkListDiff(checklist, 0, 0, 3):
                open_today = open_list[-1]
                trade_today = trade_list[-1]
                low_today = low_list[-1]
                high_today = high_list[-1]
                if trade_today > open_today:
                    if ((open_today - low_today) / (trade_today - open_today)) >= 2:
                        if (high_today - trade_today + low_today) < open_today:
                            if open_today < open_list[0]:
                                trade_last = basefunc.getStockInfo(list_stocks[sell_day], code, engine_string)['trade']
                                trade_last_diff = (trade_last - trade_today)/trade_today * 100
                                print("%s [%s] last[%f]"%(stInfo['code'], stInfo['name'], trade_last_diff))

        except UnboundLocalError as e:
            pass #print('[Error] Can not find any infomation by code: %s' %(code))


# 最优风险资产组合
def checkRollbackBest(codes, number_of_assets, engine_string):
    import basefunc,sys
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt   
    import tushare as ts
    import scipy.optimize as sco
    import scipy.interpolate as scii

    
    # 备用的股票代码数量，用于防止有些股票时间太短被弃掉，建议number_of_assets的50%
    backupcode = 20
    # 策略数据获取最长时间的百分比，用于筛选掉小于标准开盘时间范围的股票
    stddaterate = 0.3
    # 获取股票数量的范围，最大值为1，相当于获取股票列表数量的前100%,总数值为2000
    codeslenrate = 1
    #
    stdtable = 'stock_2017_09_29'
    stdcloses = []
    # 策略数据获取开始时间，结束时间
    start_day = '2016-09-01'
    end_day = '2017-09-29'
    check_day = ''
    # 选择A股最长寿的股票作为时间参考
    standard = '600601'
    cash = 100000
    code_list = []
    names_show = []
    codes_show = []
    code_blacklist = []
    datas = {}

    for ind in (np.random.random(number_of_assets + backupcode) * ((len(codes) - 1)*codeslenrate)):
        ind = int(ind)
        code_list.append(codes[ind])

    stddf = ts.get_k_data(standard, start_day, end_day) #前复权
    stdopendays = len(stddf['close'].tolist())

    for code in code_list:
        df = pd.DataFrame()
        df = ts.get_k_data(code, start_day, end_day) #前复权
        # 筛选掉开盘时间过短的股票
        if len(df['close'].tolist()) < (stdopendays * stddaterate):
            #print('time too short:%s,%s,%s' %(code, len(df['close'].tolist()), stdopendays * stddaterate))
            continue

        df.index = df['date'].tolist()
        data_simple = df['close']
        try:
            stInfo = basefunc.getStockInfo(stdtable, code, engine_string)
            stdcloses.append(stInfo['trade'])
            names_show.append(stInfo['name'])
            codes_show.append(stInfo['code'])
            data_simple.name = code
            datas[code] = data_simple
            #print(stInfo['code'], stInfo['name'], stInfo['trade'])
        except TypeError:
            #print('empty info:%s' %code)
            continue
        #print(len(datas))
        if len(datas) == number_of_assets:
            break

    data = pd.DataFrame(datas)
    # 将无效数据用前一次或是后一次有效数据填充
    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')
    global rets
    rets = np.log(data / data.shift(1))

    # 计算年化收益率
    year_ret = rets.mean() * 252
    print('年化收益率:\n', year_ret)
    #计算协方差矩阵
    #year_volatility = rets.cov() * 252

    #生成number_of_assets个随机数
    weights = np.random.random(number_of_assets)
    #将随机数归一化，每一份就是权重，权重之和为1
    weights /= np.sum(weights)

    #min_func_sharpe = -(basefunc.statistics(weights, rets)[2])
    #为权重初始值 [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1] ， 'SLSQP' 为Sequential Least Squares Programming方法。
    noa = number_of_assets * [1. / number_of_assets,]

    #即每个权重需要在0到1之间。边界条件为：
    bnds = tuple((0, 1) for x in range(number_of_assets))

    #即权重之和为1。约束条件为：
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}) 

    #我们之前引入了优化算法包 import scipy.optimize as sco ，使用其中的最小化优化算法 sco.minimize 。
    opts = sco.minimize(min_func_sharpe, noa , method='SLSQP',  bounds=bnds, constraints=cons)

    #结果 opts['x'] 即为最大夏普率的投资组合的权重分配。精确到小数点后三位，结果为：
    optsr3 = opts['x'].round(3)
    print('最大夏普率的投资组合的权重分配:', optsr3)

    #可以获得最大夏普率的投资组合的收益率、波动率和夏普率。结果为：
    stoptsr3 = statistics(opts['x']).round(3)
    print('最大夏普率的投资组合的收益率、波动率和夏普率:', stoptsr3)

    if stoptsr3[1] > 0.35:
        print('风险较大，终止计算')
        #sys.exit(1)
    elif stoptsr3[0] < 0.5:
        print('收益较小，终止计算')
        #sys.exit(1)

    allbenifit = 0
    allavebenifit = 0
    rates = []
    returninfo = {}

    for rate in opts['x'].round(3):
        rates.append(rate)
    for i in range(number_of_assets):
        returninfosub = {}
        name = names_show[i]
        code = codes_show[i]
        buy = data[-1:][code].tolist()
        for buy_only in buy:
            buy = buy_only
        sell = stdcloses[i]
        rate = rates[i]
        benifit = (sell - buy) / buy * rate * cash
        avebenifit = (sell - buy) / buy * cash * (1 / number_of_assets)
        benifitrate = (sell - buy) / buy
        allbenifit = allbenifit + benifit
        allavebenifit = allavebenifit + avebenifit
        print('%s[%s]: 买入价:%f, 卖出价:%f, 收益率:%f, 配额:%f, 配额收益:%f, 无差收益:%f' %( name, code, buy, sell, benifitrate, rate, benifit, avebenifit))

        if rate > 0:
            returninfosub['buy'] = buy
            returninfosub['rate'] = rate
            returninfo[code] = returninfosub

    print('配额策略总收益:%f' % allbenifit)
    print('无差策略总收益:%f' % allavebenifit)
    print('收益数据:%s' % returninfo)

#### checkRollbackBest附属函数
#我们现在再描述一下某个投资组合。这个投资组合是这样的一个函数，即输入权重分配，输出该组合的收益率、波动率和夏普率。函数定义如下：
def statistics(weights):
    import numpy as np
    weights = np.array(weights)
    pret = np.sum(rets.mean() * weights) * 252
    pvol = np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))
    return np.array([pret, pvol, pret / pvol])

def min_func_sharpe(weights):
    return -statistics(weights)[2]
