# -*- coding: utf-8 -*-

"""
Module implementing ChooseId.
"""
import sys
from PyQt4 import QtSql,  QtGui
from PyQt4.QtSql import QSqlQuery
from log import log
import json
import math
from log import DEBUG

class myurllib():
    db = None
    query = None
    def __init__(self):
        if myurllib.db is None:
            self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')   
    #        self.db.setHostName('42.121.137.80')  
#            self.db.setHostName('192.168.1.220')    
#            self.db.setDatabaseName('test')          
#            self.db.setUserName('testuser')             
#            self.db.setPassword('123456')  

#            self.db.setHostName('192.168.1.114')    
#            self.db.setDatabaseName('stock')          
#            self.db.setUserName('user')             
#            self.db.setPassword('123456')  
            
            self.db.setHostName('localhost') 
            self.db.setDatabaseName('stock')          
            self.db.setUserName('root')             
            self.db.setPassword('root')  
#            self.db.setHostName('192.168.1.104')        
            
    #        self.db.setUserName('anyoneling2')         
    #        self.db.setPassword('yjtxgtde') 
            if not self.db.open(): 
                log('DB can not open')
                QtGui.QMessageBox.information(None, 'result', "DB can not open")
                sys.exit(1)
        
            self.query = QSqlQuery(self.db)
            myurllib.db = self.db
            myurllib.query = self.query
        else:
            self.db = myurllib.db
            self.query = myurllib.query 
    
    def parseInnerFilter(self,  innerFilterType):
        ret = None
        condition = ''
        tableFilter = ''
        try:
            flag, type = innerFilterType.split('#')
            clz, switchType, subType = type.split('_')
            log('innerFilterType', switchType, subType)
            if switchType == '0':
                condition = { 
                 '0': u' and z.today_begin_price=z.current_price and z.max=z.min and z.current_price=z.max',     #开盘=收盘=最高=最低
                }[subType]
            elif switchType == '1':
                condition = {
                 '0': u' and z.amplitude_ratio<2',                                       #振幅 < 2%
                 '1': u' and amplitude_ratio=0'                                          #振幅 = 0
                }[subType]
            elif switchType == '2':
                condition = {
                 '0': u' and z.sold_price=0 and z.growth_ratio>4.9',                        #u'卖价 = 0, 涨幅 > 4.9%'
                 '1': u' and z.bought_price=0 and z.growth_ratio<-4.9'                      #u'买价 = 0, 涨幅 < -4.9%'
                }[subType]
            elif switchType == '3':
                condition = {
                 '0': u' and z.total_money<99990000',                                    #u'总金额 < 0.9999亿'
                 '1': u' and z.total_money<199990000 and z.total_money>100000000',       #u'总金额 1 ~ 1.9999亿'
                 '2': u' and z.total_money<499990000 and z.total_money>200000000',       #u'总金额 2 ~ 4.9999亿'
                 '3': u' and z.total_money>=500000000',                                  #u'总金额 >= 5亿', 
                 '4': u' and z.total_money>900000000',                                   #u'总金额 >  9亿', 
                 '5': u' and z.total_money<1500000000',                                  #u'总金额 >  15亿'
                 '6': u' and z.total_money>2000000000',                                  #u'总金额 >  20亿'
                 '7': u' and z.total_money>2500000000',                                  #u'总金额 >  25亿'
                 '8': u' and z.total_money>3000000000',                                  #u'总金额 >  30亿'
                 '9': u' and z.total_money>4000000000'                                   #u'总金额 >  40亿'  
                }[subType]
            elif switchType == '4':
                condition = {
                 '0': u' and z.turnover_ratio<0.9999',                                    #u'换手率 < 0.9999%'
                 '1': u' and z.turnover_ratio<2.9999 and z.turnover_ratio>=1',            #u'换手率 1% ~ 2.9999%'
                 '2': u' and z.turnover_ratio<4.9999 and z.turnover_ratio>=3',            #u'换手率 3% ~ 4.9999%'
                 '3': u' and z.turnover_ratio<6.9999 and z.turnover_ratio>=5',            #u'换手率 5% ~ 6.9999%'
                 '4': u' and z.turnover_ratio<9.9999 and z.turnover_ratio>=7',            #u'换手率 7% ~ 9.9999%'
                 '5': u' and z.turnover_ratio>=10',                                       #u'换手率 >= 10%'
                 '6': u' and z.turnover_ratio>15',                                        #u'换手率 > 15%'
                 '7': u' and z.turnover_ratio>20',                                        #u'换手率 > 20%'
                 '8': u' and z.turnover_ratio>25',                                        #u'换手率 > 25%'
                 '9': u' and z.turnover_ratio>30',                                        #u'换手率 > 30%'
                 '10': u' and z.turnover_ratio>35',                                       #u'换手率 > 35%'
                 '11': u' and z.turnover_ratio>40',                                       #u'换手率 > 40%'
                 '12': u' and z.turnover_ratio>45',                                       #u'换手率 > 45%'
                 '13': u' and z.turnover_ratio>50',                                       #u'换手率 > 50%'
                 '14': u' and z.turnover_ratio>60',                                       #u'换手率 > 60%'
                }[subType]
            elif switchType == '5':
                subTypeL = subType.split('.')
                subType = subTypeL[0]
                condition = {
                 '0': u' and MONTH(z.created)<4',                                         #u'第 1 季度'
                 '1': u' and MONTH(z.created)<7 and MONTH(z.created)>=4',                 #u'第 2 季度'
                 '2': u' and MONTH(z.created)<10 and MONTH(z.created)>=7',                #u'第 3 季度'
                 '3': u' and MONTH(z.created)<=12 and MONTH(z.created)>=10',              #u'第 4 季度'
                 '4': u' and MONTH(z.created)=1',                                         #u'1 月'
                 '5': u' and MONTH(z.created)=2',                                         #u'2 月'
                 '6': u' and MONTH(z.created)=3',                                         #u'3 月'
                 '7': u' and MONTH(z.created)=4',                                         #u'4 月'
                 '8': u' and MONTH(z.created)=5',                                         #u'5 月'
                 '9': u' and MONTH(z.created)=6',                                         #u'6 月'
                 '10': u' and MONTH(z.created)=7',                                        #u'7 月'
                 '11': u' and MONTH(z.created)=8',                                        #u'8 月'
                 '12': u' and MONTH(z.created)=9',                                        #u'9 月'
                 '13': u' and MONTH(z.created)=10',                                       #u'10 月'
                 '14': u' and MONTH(z.created)=11',                                       #u'11 月'
                 '14': u' and MONTH(z.created)=12',                                       #u'12 月'
                }[subType]
            elif switchType == '5':
                condition = ''
            else:
                log('Unkown filter')
                
            if flag == 'FLAG_UP':
                tableFilter = u' and y.ty_minus>0' 
            else:
                tableFilter = u' and y.yt_minus>0' 
        except:
            log('Exception')
        
        return tableFilter, condition
        
    def request(self, api,  args):
        log('APINAME', api)
        try:
            if api == 'liststockclassfication':
                sql = 'SELECT stock_basic_info.stock_id,stock_basic_info.stock_name,industry_info.industry_name,area_info.area_name FROM stock_basic_info, stock_classification LEFT JOIN industry_info ON stock_classification.industry_id=industry_info.industry_id LEFT JOIN area_info ON stock_classification.area_id = area_info.area_id where stock_basic_info.stock_id=stock_classification.stock_id'
                self.query.exec_(sql)
                ret = {'liststockclassficationresponse':{}}
                ret['liststockclassficationresponse']['stockclassification'] = []
                count = 0
                while self.query.next():
                    row = {}
                    row['stockid'] = str(self.query.value(0).toString().toUtf8())
                    row['stockname'] = str(self.query.value(1).toString().toUtf8())
                    row['industryname'] = str(self.query.value(2).toString().toUtf8())
                    row['areaname'] = str(self.query.value(3).toString().toUtf8())
                    ret['liststockclassficationresponse']['stockclassification'].append(row)
                    count += 1
                ret['liststockclassficationresponse']['count'] = count
                self.query.clear()
    #            log('ret',  ret)
                return json.dumps(ret)
                
            elif api == 'liststockdayinfo':
                startD = args['starttime']
                endD = args['endtime']
                ids = None
                
                if 'stockid' in args:
                    ids = args['stockid']
                filter = 'z.created >= "%s" and z.created <= "%s"' %(startD,  endD)
                if ids is not None:
                    filter += " and z.stock_id in (%s)" %ids 
                
                innerFilterType = None
                if 'filter' in args:
                    innerFilterType = args['filter']
                    tableFilter, condition = self.parseInnerFilter(innerFilterType)
                    filter += ' and y.stock_id=z.stock_id and y.created=z.created %s %s' %(tableFilter, condition)
                    countSql = 'select count(*) from stock_day_info z, twodaysdifference y where ' + filter
                else:
                    countSql = 'select count(*) from stock_day_info z where ' + filter

                log('countSql',  countSql)
                self.query.exec_(countSql)
                self.query.next()
                ret = {'liststockdayinforesponse':{}}
                ret['liststockdayinforesponse']['count'] = int(self.query.value(0).toString().toUtf8())
                ret['liststockdayinforesponse']['stockdayinfo'] = []
                log('count', ret['liststockdayinforesponse']['count'] )
                self.query.clear()
                
                sql = 'SELECT z.* FROM stock_day_info z'
    #            sql = 'select stock_basic_info.stock_name, stock_day_info.* from stock_basic_info,stock_day_info where stock_basic_info.stock_id = stock_day_info.stock_id'
                if innerFilterType is not None:
                    sql += ', twodaysdifference y'
                    
                sql += ' where ' + filter
                if 'sortname' in args:
                    sortName = args['sortname']
                    ############
                    if sortName == 'name' or sortName == 'stockname':
                        sortName = 'stock_name'
                    elif sortName == 'stockid':
                        sortName = 'stock_id'
                    ############    
                    
                    if 'asc' in args and args['asc'] == 'false':
                        sql += ' order by %s desc' %sortName
                    else:
                        sql += ' order by %s asc' %sortName
                
                if 'page' in args and 'pagesize' in args:
                    sql += ' limit %d,%d' %((int(args['page']) - 1)*int(args['pagesize']),  int(args['pagesize']))
                
                log('sql',  sql)
                self.query.exec_(sql)
                
                count = 0
                while self.query.next():
                    row = {}
                    cCount = 0
                    row['stockid'] = str(self.query.value(cCount + 1).toString().toUtf8())
                    row['growth_ratio'] = str(self.query.value(cCount + 2).toString().toUtf8())
                    row['current_price'] = str(self.query.value(cCount + 3).toString().toUtf8())
                    row['daily_up_down'] = str(self.query.value(cCount + 4).toString().toUtf8())
                    row['bought_price'] = str(self.query.value(cCount + 5).toString().toUtf8())
                    row['sold_price'] = str(self.query.value(cCount + 6).toString().toUtf8())
                    row['total_deal_amount'] = str(self.query.value(cCount + 7).toString().toUtf8())
                    row['last_deal_amount'] = str(self.query.value(cCount + 8).toString().toUtf8())
                    row['growth_speed'] = str(self.query.value(cCount + 9).toString().toUtf8())
                    row['turnover_ratio'] = str(self.query.value(cCount + 10).toString().toUtf8())
                    row['today_begin_price'] = str(self.query.value(cCount + 11).toString().toUtf8())
                    row['ytd_end_price'] = str(self.query.value(cCount + 12).toString().toUtf8())
                    row['pe_ratio'] = str(self.query.value(cCount + 13).toString().toUtf8())
                    row['max'] = str(self.query.value(cCount + 14).toString().toUtf8())
                    row['min'] = str(self.query.value(cCount + 15).toString().toUtf8())
                    row['total_money'] = str(self.query.value(cCount + 16).toString().toUtf8())
                    row['amplitude_ratio'] = str(self.query.value(cCount + 17).toString().toUtf8())
                    row['cir_of_cap_stock'] = str(self.query.value(cCount + 18).toString().toUtf8())
                    row['upordown_per_deal'] = str(self.query.value(cCount + 19).toString().toUtf8())
                    row['volume_ratio'] = str(self.query.value(cCount + 20).toString().toUtf8())
                    row['avg_price'] = str(self.query.value(cCount + 21).toString().toUtf8())
                    row['DaPanWeiBi'] = str(self.query.value(cCount + 22).toString().toUtf8())
                    row['sell'] = str(self.query.value(cCount + 23).toString().toUtf8())
                    row['buy'] = str(self.query.value(cCount + 24).toString().toUtf8())
                    row['sb_ratio'] = str(self.query.value(cCount + 25).toString().toUtf8())
                    row['DaPanWeiCha'] = str(self.query.value(cCount + 26).toString().toUtf8())
                    row['num1_buy'] = str(self.query.value(cCount + 27).toString().toUtf8())
                    row['num1_sell'] = str(self.query.value(cCount + 28).toString().toUtf8())
                    row['num1_buy_price'] = str(self.query.value(cCount + 29).toString().toUtf8())
                    row['num1_sell_price'] = str(self.query.value(cCount + 30).toString().toUtf8())
                    row['num2_buy'] = str(self.query.value(cCount + 31).toString().toUtf8())
                    row['num2_sell'] = str(self.query.value(cCount + 32).toString().toUtf8())
                    row['num2_buy_price'] = str(self.query.value(cCount + 33).toString().toUtf8())
                    row['num2_sell_price'] = str(self.query.value(cCount + 34).toString().toUtf8())
                    row['num3_buy'] = str(self.query.value(cCount + 35).toString().toUtf8())
                    row['num3_sell'] = str(self.query.value(cCount + 36).toString().toUtf8())
                    row['num3_buy_price'] = str(self.query.value(cCount + 37).toString().toUtf8())
                    row['num3_sell_price'] = str(self.query.value(cCount + 38).toString().toUtf8())
                    row['circulation_value'] = str(self.query.value(cCount + 39).toString().toUtf8())
    #                if u'亿'.encode('utf-8') in row['circulation_value']:
    #                    log("======================")
    #                    row['circulation_value'] = row['circulation_value'].replace(u'亿'.encode('utf-8'), '')
                    row['bbi_balance'] = str(self.query.value(cCount + 40).toString().toUtf8())
                    row['bull_profit'] = str(self.query.value(cCount + 41).toString().toUtf8())
                    row['bull_stop_losses'] = str(self.query.value(cCount + 42).toString().toUtf8())
                    row['short_covering'] = str(self.query.value(cCount + 43).toString().toUtf8())
                    row['bear_stop_losses'] = str(self.query.value(cCount + 44).toString().toUtf8())
                    row['relative_strength_index'] = str(self.query.value(cCount + 45).toString().toUtf8())
                    row['activity'] = str(self.query.value(cCount + 46).toString().toUtf8())
                    row['num_per_deal'] = str(self.query.value(cCount + 47).toString().toUtf8())
                    row['turn_per_deal'] = str(self.query.value(cCount + 48).toString().toUtf8())
                    row['update_date'] = str(self.query.value(cCount + 49).toString().toUtf8())
                    row['total_stock'] = str(self.query.value(cCount + 50).toString().toUtf8())
                    row['max_circulation_value'] = str(self.query.value(cCount + 51).toString().toUtf8())
                    row['current_circulation_value'] = str(self.query.value(cCount + 52).toString().toUtf8())
                    row['min_circulation_value'] = str(self.query.value(cCount + 53).toString().toUtf8())
                    row['avg_circulation_value'] = str(self.query.value(cCount + 54).toString().toUtf8())
                    row['total_value'] = str(self.query.value(cCount + 55).toString().toUtf8())
                    row['created'] = str(self.query.value(cCount + 56).toString().toUtf8())
                    ret['liststockdayinforesponse']['stockdayinfo'].append(row)
                self.query.clear()
    #            log('ret',  ret)
                return json.dumps(ret)
            elif api == 'listdaysum' or api == 'listmonthsum' or api == 'listweeksum':
                pass
                startD = args['starttime']
                endD = args['endtime']
                ids = None
                if 'stockid' in args:
                    ids = args['stockid']
                sumType = args['sumType']
                sumName = args['sumname']
                tableName = ''
                num = 1

                if api == 'listdaysum':
                    num = args['days']
                    if sumType == 'all':
                        tableName = '%s_sum' %sumName
                    else:
                        tableName = '%s_%s_sum' %(sumType, sumName)
                elif api == 'listmonthsum':
                    num = args['months']
                    if sumType == 'all':
                        tableName = '%s_month_sum' %sumName
                    else:
                        tableName = '%s_%s_month_sum' %(sumType, sumName)
                elif api == 'listweeksum':
                    num = args['weeks']
                    if sumType == 'all':
                        tableName = '%s_week_sum' %sumName
                    else:
                        tableName = '%s_%s_week_sum' %(sumType, sumName)
                log('tableName',  tableName)
                filter = 'x.created >= "%s" and x.created <= "%s"' %(startD,  endD)
                if ids is not None:
                    filter += " and x.stock_id in (%s)" %ids 
                
                innerFilterType = None
                if 'filter' in args:
                    innerFilterType = args['filter']
                    tableFilter, condition = self.parseInnerFilter(innerFilterType)
                    filter += ' and x.stock_id=y.stock_id and x.created=y.created and y.stock_id=z.stock_id and y.created=z.created %s %s' %(tableFilter, condition)
                    countSql = 'select count(*) from %s x, stock_day_info z, twodaysdifference y where ' %tableName + filter
                else:
                    countSql = 'select count(*) from %s x where ' %tableName + filter
                    
                log('countSql',  countSql)
                self.query.exec_(countSql)
                self.query.next()
                response = None
                if api == 'listdaysum':
                    ret = {'listdaysumresponse':{}}
                    ret['listdaysumresponse']['count'] = int(self.query.value(0).toString().toUtf8())
                    ret['listdaysumresponse']['daysuminfo'] = []
                    response = ret['listdaysumresponse']['daysuminfo']
                    columnNum = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten',\
                              11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen',16:'sixteen',17:'seventeen',18:'eighteen',\
                              19:'nineteen',20:'twenty',21:'twenty1',22:'twenty2',23:'twenty3',24:'twenty4',25:'twenty5',26:'twenty7',\
                              27:'twenty7',28:'twenty8',29:'twenty9',30:'thirty'}[int(num)]
                    columnName = columnNum + '_sum'
                    retColumnName = columnNum + 'sum'
                elif api == 'listmonthsum':
                    ret = {'listmonthsumresponse':{}}
                    ret['listmonthsumresponse']['count'] = int(self.query.value(0).toString().toUtf8())
                    ret['listmonthsumresponse']['monthsuminfo'] = []
                    response = ret['listmonthsumresponse']['monthsuminfo'] 
                    columnNum = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten',\
                              11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen',16:'sixteen',17:'seventeen',18:'eighteen',\
                              19:'nineteen',20:'twenty',21:'twenty1',22:'twenty2',23:'twenty3',24:'twenty4',25:'twenty5',26:'twenty7',\
                              27:'twenty7',28:'twenty8',29:'twenty9',30:'thirty'}[int(num)]
                    columnName = columnNum + '_month_sum'
                    retColumnName = columnNum + 'monthsum'
                elif api == 'listweeksum':
                    ret = {'listweeksumresponse':{}}
                    ret['listweeksumresponse']['count'] = int(self.query.value(0).toString().toUtf8())
                    ret['listweeksumresponse']['weeksuminfo'] = []
                    response = ret['listweeksumresponse']['weeksuminfo'] 
                    columnNum = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten',\
                              11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen',16:'sixteen',17:'seventeen',18:'eighteen',\
                              19:'nineteen',20:'twenty',21:'twenty1',22:'twenty2',23:'twenty3',24:'twenty4',25:'twenty5',26:'twenty7',\
                              27:'twenty7',28:'twenty8',29:'twenty9',30:'thirty'}[int(num)]
                    columnName = columnNum + '_week_sum'
                    retColumnName = columnNum + 'weeksum'
                
    #            log('count', ret['liststockdayinforesponse']['count'] )
                self.query.clear()
                
                
                if innerFilterType is not None:
                    sql = 'select x.stock_id,x.created,x.%s from %s x, stock_day_info z, twodaysdifference y where ' %(columnName, tableName) + filter
                else:
                    sql = 'select x.stock_id,x.created,x.%s from %s x where ' %(columnName, tableName) + filter
                        
                if 'sortname' in args:
                    sortName = args['sortname']
                    ############命名规则跟数据库不一致，需要重新映射
                    if sortName == 'name' or sortName == 'stockname':
                        sortName = 'stock_name'
                    elif sortName == 'stockid':
                        sortName = 'stock_id'
                    sortName = sortName.replace('week',  '_week')
                    sortName = sortName.replace('month',  '_month')
                    sortName = sortName.replace('sum',  '_sum')
                    ############    
                    
                    if 'asc' in args and args['asc'] == 'false':
                        sql += ' order by %s desc' %sortName
                    else:
                        sql += ' order by %s asc' %sortName
                
                if 'page' in args and 'pagesize' in args:
                    sql += ' limit %d,%d' %((int(args['page']) - 1)*int(args['pagesize']),  int(args['pagesize']))
                
                log('sql',  sql)
                self.query.exec_(sql)
                colCount = self.query.record().count()
                while self.query.next():
                    row = {}
                    row['stockid'] = str(self.query.value(0).toString().toUtf8())
                    row['created'] = str(self.query.value(1).toString().toUtf8())
                    row[retColumnName] = str(self.query.value(2).toString().toUtf8())
                    response.append(row)
                
                self.query.clear()
                #log('ret',  ret)
                return json.dumps(ret)
            
            elif api == 'liststockdaysdiff':
                startD = args['starttime']
                endD = args['endtime']
                ids = None
                if 'stockid' in args:
                    ids = args['stockid']
                optName = args['optname']
                opt = args['opt']
                filter = None
                if ids is not None:
                    filter = "stock_id in (%s)" %ids 
                
                
                ret = {'liststockdaysdiffresponse':{}}
                ret['liststockdaysdiffresponse']['details'] = []

                sortName = None
                if 'sortname' in args:
                    sortName = args['sortname']
                    if sortName == 'name' or sortName == 'stockname':
                        sortName = 'stock_name'
                    elif sortName == 'stockid':
                        sortName = 'stock_id'
                
                if opt == 'plus' or opt == 'minus' or opt == 'divide':
                    optType = {'plus':'+', 'minus':'-', 'divide':'/'}[opt]
                    sql = 'select a.stock_id as stock_id, a.%s, b.%s, b.%s%sa.%s as op from (select stock_id,%s from stock_day_info where created = "%s") a,\
                        (select stock_id,%s from stock_day_info where created = "%s") b where a.stock_id = b.stock_id'\
                        %(optName, optName, optName, optType, optName, optName, startD, optName, endD)
                    if filter is not None:
                        sql += ' and a.' + filter
                    if sortName != 'stock_id':
                        sortName = 'op'
                elif opt == 'maxmin':
                    sql = 'select stock_day_info.stock_id, max(stock_day_info.%s), min(stock_day_info.%s), max(stock_day_info.%s) - min(stock_day_info.%s) as maxmin from stock_day_info \
                        where stock_day_info.created >="%s" and stock_day_info.created <="%s" and %s > 0' %(optName,  optName,  optName, optName, startD, endD, optName)
                    if filter is not None:
                        sql += ' and stock_day_info.' + filter
                    sql += ' group by stock_day_info.stock_id'
                    if sortName != 'stock_id':
                        sortName = 'maxmin'   
                elif opt == 'maxmindivide':
                    sql = 'select stock_day_info.stock_id, max(stock_day_info.%s), min(stock_day_info.%s), max(stock_day_info.%s) / min(stock_day_info.%s) as maxmin from stock_day_info \
                        where stock_day_info.created >="%s" and stock_day_info.created <="%s" and %s > 0' %(optName,  optName,  optName, optName, startD, endD, optName)
                    if filter is not None:
                        sql += ' and stock_day_info.' + filter
                    sql += ' group by stock_day_info.stock_id'
                    if sortName != 'stock_id':
                        sortName = 'maxmindivide'  
                elif opt == 'sum':
                    sql = 'select stock_day_info.stock_id as stock_id as stock_name,sum(stock_day_info.%s) as s from stock_day_info \
                        where stock_day_info.created >="%s" and stock_day_info.created <="%s"' %(optName, startD,  endD)
                    if filter is not None:
                        sql += ' and stock_day_info.' + filter
                    sql += ' group by stock_day_info.stock_id'
                    if sortName != 'stock_id':
                        sortName = 's'   
                    
    #            if 'asc' in args and args['asc'] == 'false':
    #                sql += ' order by %s desc' %sortName
    #            else:
    #                sql += ' order by %s asc' %sortName
    #            
    #            if 'page' in args and 'pagesize' in args:
    #                sql += ' limit %d,%d' %((int(args['page']) - 1)*int(args['pagesize']),  int(args['pagesize']))
                
                log('sql',  sql)
                self.query.exec_(sql)
                count = 0
                while self.query.next():
                    row = {}
                    
                    row['stockid'] = str(self.query.value(0).toString().toUtf8())
                    if opt == 'plus' or opt == 'minus' or opt == 'divide':
                        row['startvalue'] = str(self.query.value(1).toString().toUtf8())
                        row['endvalue'] = str(self.query.value(2).toString().toUtf8())
                        row[optName] = str(self.query.value(3).toString().toUtf8())
                    elif opt == 'maxmin' or opt == 'maxmindivide':
                        row['maxvalue'] = str(self.query.value(1).toString().toUtf8())
                        row['minvalue'] = str(self.query.value(2).toString().toUtf8())
                        row[optName] = str(self.query.value(3).toString().toUtf8())
                        row['maxdate']  = ''
                        row['mindate']  = ''
                        if (optName == 'current_price' or optName == 'volume_ratio' or optName == 'amplitude_ratio' or optName == 'turnover_ratio' or optName == 'total_money') and float(row['minvalue']) == 0:
                            continue
                    else:
                        row[optName] = str(self.query.value(1).toString().toUtf8())
                    ret['liststockdaysdiffresponse']['details'].append(row)
                    count += 1
                ret['liststockdaysdiffresponse']['count'] = count
                self.query.clear()
                
                if opt == 'maxmin' or opt == 'maxmindivide':
    #                sql = 'select a.stock_id,a.created from stock_day_info as a, (select stock_id, max(%s) as ma from stock_day_info where stock_day_info.created >="%s" and stock_day_info.created <="%s" GROUP BY stock_id) as c where a.stock_id = c.stock_id and c.ma = a.%s and a.created >= "%s" and a.created <= "%s"' %(optName, startD, endD, optName, startD, endD)
                    sql = 'select a.stock_id, a.created from (select stock_id, created, %s from stock_day_info where created >="%s" and created <="%s" and %s > 0 order by %s desc) as a' %(optName, startD, endD, optName, optName)
     
                    if filter is not None:
                        sql += ' where a.' + filter
                    sql += ' group by a.stock_id'
                    log('sql',  sql)
                    self.query.exec_(sql)
                    log('[*]',  'query finished',  count)
                    i = 0
                    while self.query.next():
    #                    while i < count:
    #                        
                        if ret['liststockdaysdiffresponse']['details'][i]['stockid'] == str(self.query.value(0).toString().toUtf8()):
                            if ret['liststockdaysdiffresponse']['details'][i]['maxdate'] == '':
                                ret['liststockdaysdiffresponse']['details'][i]['maxdate'] = str(self.query.value(1).toString().toUtf8())
                            i += 1
                        
                        if i >= count:
                            break
                    self.query.clear()
                    log('[*]',  'scan ')
    #                sql = 'select a.stock_id,a.created from stock_day_info as a, (select stock_id, min(%s) as ma from stock_day_info where stock_day_info.created >="%s" and stock_day_info.created <="%s" GROUP BY stock_id) as c where a.stock_id = c.stock_id and c.ma = a.%s and a.created >= "%s" and a.created <= "%s"' %(optName, startD, endD, optName, startD, endD)
                    sql = 'select a.stock_id, a.created from (select stock_id, created, %s from stock_day_info where created >="%s" and created <="%s" and %s > 0 order by %s asc) as a' %(optName, startD, endD, optName, optName)

                    
                    if filter is not None:
                        sql += ' where a.' + filter
                    
                    sql += ' group by a.stock_id'
                    log('sql',  sql)
                    self.query.exec_(sql)
                    i = 0
                    while self.query.next():
    #                    while i < count:
                        if ret['liststockdaysdiffresponse']['details'][i]['stockid'] == str(self.query.value(0).toString().toUtf8()):
                            if ret['liststockdaysdiffresponse']['details'][i]['mindate']  == '':
                                ret['liststockdaysdiffresponse']['details'][i]['mindate'] = str(self.query.value(1).toString().toUtf8())
                            i += 1
                        if i >= count:
                            break
                    self.query.clear()
    #            log('ret',  ret)
                return json.dumps(ret)
            elif api == 'listndayssum':
                startD = args['starttime']
                endD = args['endtime']
                ids = None
                if 'stockid' in args:
                    ids = args['stockid']
                optName = args['sumname']

                filter = None
                if ids is not None:
                    filter = "stock_id in (%s)" %ids 
                ret = {'listndayssumresponse':{}}
                ret['listndayssumresponse']['stockndayssum'] = []
    #            countSql = 'select count(*) from stock_day_info'
    #            if filter is not None:
    #                countSql += ' where ' + filter
    #            log('countSql',  countSql)
    #            self.query.exec_(countSql)
    #            self.query.next()
    #            ret['liststockdaysdiffresponse']['count'] = int(self.query.value(0).toString().toUtf8())
    #            self.query.clear()
                sortName = None
                if 'sortname' in args:
                    sortName = args['sortname']
                    if sortName == 'name' or sortName == 'stockname':
                        sortName = 'stock_name'
                    elif sortName == 'stockid':
                        sortName = 'stock_id'
                        
                sql = 'select stock_day_info.stock_id as stock_id,sum(stock_day_info.%s) as s from stock_day_info \
                    where stock_day_info.created >="%s" and stock_day_info.created <="%s"' %(optName, startD,  endD)
                if filter is not None:
                    sql += ' and stock_day_info.' + filter
                sql += ' group by stock_day_info.stock_id'
                if sortName != 'stock_id':
                    sortName = 's'   
                
                log('sql',  sql)
                self.query.exec_(sql)
                count = 0
                while self.query.next():
                    row = {}
                    count += 1
                    row['stockid'] = str(self.query.value(0).toString().toUtf8())
                    row[optName] = str(self.query.value(1).toString().toUtf8())
                    ret['listndayssumresponse']['stockndayssum'].append(row)
                ret['listndayssumresponse']['count'] = count
                self.query.clear()
                
    #            log('ret',  ret)
                return json.dumps(ret)
            
            elif api == 'listgrowthampdis':
                ids = None
                if 'stockid' in args:
                    ids = args['stockid']
                filter = None
                startD = args['starttime']
                endD = args['endtime']
                if ids is not None:
                    filter = "stock_id in (%s)" %ids 
                
                sql = 'select stock_day_info.stock_id, count(stock_day_info.growth_ratio), count(stock_day_info.amplitude_ratio)'
                sql = self.appendCountSql(sql, 'growth_ratio', None,  -9)
                sql = self.appendCountSql(sql, 'growth_ratio', -9,  -8)
                sql = self.appendCountSql(sql, 'growth_ratio', -8,  -7)
                sql = self.appendCountSql(sql, 'growth_ratio', -7,  -6)
                sql = self.appendCountSql(sql, 'growth_ratio', -6,  -5)
                sql = self.appendCountSql(sql, 'growth_ratio', -5,  -4)
                sql = self.appendCountSql(sql, 'growth_ratio', -4,  -3)
                sql = self.appendCountSql(sql, 'growth_ratio', -3,  -2)
                sql = self.appendCountSql(sql, 'growth_ratio', -2,  -1)
                sql = self.appendCountSql(sql, 'growth_ratio', -1,  0)
                sql = self.appendCountSql(sql, 'growth_ratio', 0,  1)
                sql = self.appendCountSql(sql, 'growth_ratio', 1,  2)
                sql = self.appendCountSql(sql, 'growth_ratio', 2,  3)
                sql = self.appendCountSql(sql, 'growth_ratio', 3,  4)
                sql = self.appendCountSql(sql, 'growth_ratio', 4,  5)
                sql = self.appendCountSql(sql, 'growth_ratio', 5,  6)
                sql = self.appendCountSql(sql, 'growth_ratio', 6,  7)
                sql = self.appendCountSql(sql, 'growth_ratio', 7,  8)
                sql = self.appendCountSql(sql, 'growth_ratio', 8,  9)
                sql = self.appendCountSql(sql, 'growth_ratio', 9,  None)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 0,  1)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 1,  2)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 2,  3)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 3,  4)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 4,  5)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 5,  6)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 6,  7)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 7,  8)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 8,  9)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 9,  10)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 10,  11)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 11,  12)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 12,  13)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 13,  14)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 14,  15)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 15,  16)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 16,  17)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 17,  18)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 18,  19)
                sql = self.appendCountSql(sql, 'amplitude_ratio', 19, None)

                if filter is not None:
                    filter = ' from stock_day_info where stock_day_info.' + filter + ' and stock_day_info.created >= "%s" and stock_day_info.created <= "%s"' %(startD,  endD)
                else:
                    filter = ' from stock_day_info where stock_day_info.created >= "%s" and stock_day_info.created <= "%s"' %(startD,  endD)
                sql += filter
                sql +=' group by stock_day_info.stock_id'
                log('sql',  sql)
                self.query.exec_(sql)
                ret = {'listgrowthampdisresponse':{}}
                ret['listgrowthampdisresponse']['growthamp'] = []
                count = 0
                while self.query.next():
                    row = {}
                    tmp = 0
                    row['stockid'] = str(self.query.value(0).toString().toUtf8())
                    row['growthcount']  = int(self.query.value(1).toString().toUtf8())
                    row['ampcount']  = int(self.query.value(2).toString().toUtf8())
                    tmp = 3
                    row['g0'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g1'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g2'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g3'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g4'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g5'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g6'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g7'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g8'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g9'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g10'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g11'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g12'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g13'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g14'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g15'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g16'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g17'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g18'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['g19'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a0'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a1'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a2'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a3'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a4'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a5'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a6'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a7'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a8'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a9'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a10'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a11'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a12'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a13'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a14'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a15'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a16'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a17'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a18'] = str(self.query.value(tmp).toString().toUtf8())
                    tmp += 1
                    row['a19'] = str(self.query.value(tmp).toString().toUtf8())

                    ret['listgrowthampdisresponse']['growthamp'].append(row)
                    count += 1
                ret['listgrowthampdisresponse']['count'] = count
                self.query.clear()
                return json.dumps(ret)   
            elif api == 'listdealdays':
                sql = 'select distinct created from stock_day_info ORDER BY created asc'
                self.query.exec_(sql)
                ret = {'listdealdaysresponse':{}}
                ret['listdealdaysresponse']['dealdays'] = []
                count = 0
                while self.query.next():
                    row = {}
                    row['date'] = str(self.query.value(0).toString().toUtf8())
                    ret['listdealdaysresponse']['dealdays'].append(row)
                    count += 1
                ret['listdealdaysresponse']['count'] = count
                self.query.clear()
    #            log('ret',  ret)
                return json.dumps(ret)
            elif api == 'listcrossinfo':
                startD = args['starttime']
                endD = args['endtime']
                weight = args['weight']
                optname = args['optname']
                
                sql = 'SELECT stock_id, created , %s \
                                        FROM stock_day_info \
                                        WHERE created = "%s" OR created = "%s" \
                                        ORDER BY stock_id , created' %( optname, startD, endD)
                self.query.exec_(sql)
                startEndDict = {}
                while self.query.next():
                    stockId = str(self.query.value(0).toString().toUtf8())
                    if stockId not in startEndDict:
                        startEndDict[stockId] = [str(self.query.value(2).toString().toUtf8())]
                    else:
                        startEndDict[stockId] += [str(self.query.value(2).toString().toUtf8())]
                
                self.query.clear()
                log(startEndDict)
                sql = 'SELECT stock_id,avg(%s) FROM stock_day_info WHERE created BETWEEN "%s" AND "%s" GROUP BY stock_id HAVING COUNT(created) >= 30' %(optname, startD, endD)
                self.query.exec_(sql)
                positiveList = []
                negativeList = []
                defaultList = []
                while self.query.next():
                    stockId = str(self.query.value(0).toString().toUtf8())
                    avg = str(self.query.value(1).toString().toUtf8())
                    if stockId in startEndDict and len(startEndDict[stockId]) == 2:
                        tempItem = DataItem(startEndDict[stockId][0], startEndDict[stockId][1], stockId, avg, weight)
                        if tempItem.difference >= 0 :
                            positiveList.append( tempItem )
                        else :
                            negativeList.append( tempItem )
                self.query.clear()
                log(positiveList)
                positiveList.sort( key = sortKey )
                negativeList.sort( key = sortKey )
                if len( positiveList ) > 100 :
                    defaultList += positiveList[-100:]
                    defaultList.sort( key = sortKey )
                    del positiveList[100:]
                else :
                    defaultList += positiveList[:]
                    defaultList.sort( key = sortKey )
                if len( negativeList ) > 100 :
                    del negativeList[:-100]
                if len( defaultList ) > 100 :
                    del defaultList[:-100]
                    
                ret = {'listcrossinforesponse':{}}
                ret['listcrossinforesponse']['crossinfo'] = []
                count = 0
                border = min( 100 , len( positiveList ) )
                for i in range( 0 , border ) :
                    row = {}
                    row['stockid'] = positiveList[i].stockId
                    row['startdate'] = str(startD)
                    row['startvalue'] = positiveList[i].startPrice
                    row['enddate'] = str(endD)
                    row['endvalue'] = positiveList[i].endPrice
                    row['avg'] = positiveList[i].avg
                    row['difference'] = positiveList[i].difference
                    row['crosstype'] = 'positive'
                    ret['listcrossinforesponse']['crossinfo'].append(row)
                    count += 1
                border = max( 0 , len( defaultList ) - 100 )
                for i in range( border , len( defaultList ) )[::-1] :
                    row = {}
                    row['stockid'] = defaultList[i].stockId
                    row['startdate'] = str(startD)
                    row['startvalue'] = defaultList[i].startPrice
                    row['enddate'] = str(endD)
                    row['endvalue'] = defaultList[i].endPrice
                    row['avg'] = defaultList[i].avg
                    row['difference'] = defaultList[i].difference
                    row['crosstype'] = 'default'
                    ret['listcrossinforesponse']['crossinfo'].append(row)
                    count += 1
                border = max( 0 , len( negativeList ) - 100 )
                for i in range( border , len( negativeList ) )[::-1] :
                    row = {}
                    row['stockid'] = negativeList[i].stockId
                    row['startdate'] = str(startD)
                    row['startvalue'] = negativeList[i].startPrice
                    row['enddate'] = str(endD)
                    row['endvalue'] = negativeList[i].endPrice
                    row['avg'] = negativeList[i].avg
                    row['difference'] = negativeList[i].difference
                    row['crosstype'] = 'negative'
                    ret['listcrossinforesponse']['crossinfo'].append(row)
                    count += 1
                ret['listcrossinforesponse']['count'] = count
#                log('ret',  ret)
                return json.dumps(ret)
            else:
                return json.dumps('')
                pass
        except:
            if DEBUG:
                import traceback
                traceback.print_exc()
            return json.dumps('')
#           

    
    def appendCountSql(self, sql, name, left, right):
        if left == None:
            sql += ', count(stock_day_info.%s < %d or null)' %(name, right)
        elif right == None:
            sql += ', count(stock_day_info.%s >= %d or null)' %(name, left)
        else:     
            sql += ', count(stock_day_info.%s >= %d and stock_day_info.%s < %d or null)' %(name, left, name, right)
        return sql
    
    
    def reuseQuery(self, filter, name, container, target, left= None,  right=None):
        if left == None:
            sql = 'select stock_day_info.stock_id, stock_basic_info.stock_name, count(stock_day_info.%s < %d or null) as num from stock_day_info,stock_basic_info where stock_day_info.stock_id = stock_basic_info.stock_id' %(name, right)
        elif right == None:
            sql = 'select stock_day_info.stock_id, stock_basic_info.stock_name, count(stock_day_info.%s >= %d or null) as num from stock_day_info,stock_basic_info where stock_day_info.stock_id = stock_basic_info.stock_id' %(name, left)
        else:    
            sql = 'select stock_day_info.stock_id, stock_basic_info.stock_name, count(stock_day_info.%s >= %d and stock_day_info.%s < %d or null) as num from stock_day_info,stock_basic_info where stock_day_info.stock_id = stock_basic_info.stock_id' %(name, left, name, right)
        

        sql += filter
            
        sql +=' group by stock_day_info.stock_id'
            
        log('sql', sql)
        self.query.exec_(sql)
        i = 0
        while self.query.next():
            container[i][target] = str(self.query.value(2).toString().toUtf8())
            if target.startswith('growth'):
                container[i]['growthCount'] += int(self.query.value(2).toString().toUtf8())
            else:
                container[i]['ampCount'] += int(self.query.value(2).toString().toUtf8())
            i += 1
        self.query.clear()
class DataItem :
    def __init__( self, start_price, end_price, stock_id, avg ,weight):
        avg = float(avg)
        weight = float(weight)
        self.startPrice = float(start_price)
        self.endPrice = float(end_price)
        self.stockId = stock_id
        self.avg = round( avg , 2 )
        value1 = math.log( self.startPrice / avg , 1 + weight )
        value2 = math.log( self.endPrice / avg , 1 + weight )
        if value1 > 0 :
            n1 = math.ceil( value1 )
        else :
            n1 = math.floor( value1 )
        if value2 > 0 :
            n2 = math.ceil( value2 )
        else :
            n2 = math.floor( value2 )
        self.difference = n2 - n1

def sortKey( x ) :
    return -x.difference
        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    urllib = myurllib()
#    urllib.request('listStockDayInfo', {'stockid':'000001',  'starttime':'2000-01-01',  'endtime':'2014-01-01',  'sortname':'bull_profit'})
#    urllib.request('listdaysum', {'starttime':'2000-01-01',  'endtime':'2014-01-01',  'sumType':'all',  'sumname':'avg_price',  'days':'3',  'page':'1',  'pagesize':1000,  'sortname':'threeSum'})
#    urllib.request('liststockdaysdiff', {'starttime':'2000-01-01',  'stockid':'000001, 000002, 000006', 'endtime':'2014-01-01',  'optname':'growth_ratio',  'opt':'maxmin','page':'1',  'pagesize':1000,  'sortname':'growth_ratio'})
#    urllib.request('listgrowthampdis', {'starttime':'2012-10-01',  'endtime':'2012-11-01',  'stockid':'000001'})
#    urllib.request('listDealDays', '')
    urllib.request('listcrossinfo', {'starttime':'2012-12-10',  'endtime':'2013-12-10', 'weight':'2', 'crossType':'ytd_end_price'})
    sys.exit(app.exec_())
