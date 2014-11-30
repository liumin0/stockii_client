# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtGui import QDialog, QMessageBox
from PyQt4.QtSql import QSqlTableModel,  QSqlQuery
from PyQt4.QtCore import pyqtSignature,  QVariant,  QAbstractTableModel,  QModelIndex, QString,  SIGNAL
import os
import sys
import datetime
import json
from http import callRestAsync,  callRestSync
from log import log
from translate import translate
import myGlobal

class CustomModel(QAbstractTableModel):
    """
    自定义Model，用来存储需要再table中展示的数据
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QAbstractTableModel.__init__(self, parent)
        self.parent = parent;           #保存父类
        
        self.datas=[]                   #保存需要显示的数据
        self.rCount = 0                 #数据的行数
        self.cCount = 0                 #数据的列数
        self.totalCount = 0             #数据的总数(因为分页，不能一次展示所有的数据)
        self.totalPage = 0              #分页之后的总页数
        self.lastRowCount = 0           #因为返回的数据需要插入一些辅助数据，比如名称之类的，所有这个用来表示现有数据中已经执行过插入操作的行数
        self.restApi = ''               #保存访问的API
        self.args = {}                  #保存包括自己生成的所有参数
        self.qArgs = {}                 #保存来自外面的请求参数

        self.page = 1                   #当前显示的页
        self.pageSize = 200             #每页显示的行数
        self.connect(self,  SIGNAL("callBack(QVariant, QDialog*)"),  self.callBack) #异步通信的时候用到的回调函数
#        self.connect(self,  QtCore.SIGNAL("first()"),  self.first)
#        self.connect(self,  QtCore.SIGNAL("up()"),  self.up)
#        self.connect(self,  QtCore.SIGNAL("down()"),  self.down)
#        self.connect(self,  QtCore.SIGNAL("last()"),  self.last)

    def setPageSize(self,  pageSize):
        self.pageSize = pageSize
    
    def setHeader(self):
        """
        这个设置header的操作主要是为了保证header中的顺序，因为从服务器获取到的数据是json格式，解析之后得到的是
        dictionary，它原始的顺序就会丢失，这儿可以自定义header的顺序
        """
        self.headers = []
        if self.restApi == 'liststockdayinfo':
#            self.headers = [u"代码",u"名称",u"日期",u"涨幅",u"现价",u"日涨跌",u"买入价",u"卖出价",u"总量",u"现量",u"涨速",u"换手",u"今开",u"昨收",\
#            u"市盈率",u"最高",u"最低",u"总金额",u"振幅",u"流通股本",u"笔涨跌",u"量比",u"均价",u"委比",u"内盘",u"外盘",u"内外比",u"委量差",u"买量一",\
#            u"卖量一",u"买价一",u"卖价一",u"卖价二",u"卖量二",u"买价二",u"买量二",u"买价三",u"买量三",u"卖价三",u"卖量三",u"流通市值",u"多空平衡",\
#            u"多头获利",u"多头止损",u"空头回补",u"空头止损",u"强弱度",u"活跃度",u"每笔均量",u"每笔换手",u"更新日期",u"总股本",u"最高价流通市值"\
#            ,u"现价流通市值",u"最低价流通市值",u"均价流通市值",u"总市值"]
#            self.columnNames =  ["stock_id","stock_name","created","growth_ratio","current_price","daily_up_down","bought_price",\
#            "sold_price","total_deal_amount","last_deal_amount", "growth_speed","turnover_ratio","today_begin_price","ytd_end_price",\
#            "pe_ratio","max","min","total_money","amplitude_ratio","cir_of_cap_stock","upordown_per_deal","volume_ratio","avg_price",\
#            "DaPanWeiBi","sell","buy","sb_ratio","DaPanWeiCha","num1_buy","num1_sell","num1_buy_price","num1_sell_price","num2_buy",\
#            "num2_sell","num2_buy_price","num2_sell_price","num3_buy","num3_sell","num3_buy_price","num3_sell_price","circulation_value", \
#            "bbi_balance","bull_profit","bull_stop_losses","short_covering","bear_stop_losses","relative_strenth_index","activity",\
#            "num_per_deal","turn_per_deal","update_date","total_stock","max_circulation_value","current_circulation_value",\
#            "min_circulation_value","avg_circulation_value","total_value"]
            self.columnNames =  ["stockid",  "created"]
        elif self.restApi == 'listmonthsum' or self.restApi == 'listweeksum' or self.restApi == 'listdaysum':
            self.columnNames = ["stockid",  "created"]
        elif self.restApi == 'liststockdaysdiff':
            self.columnNames = ["stockid", "startvalue",  "endvalue", "maxdate", "maxvalue", "mindate", "minvalue"]
        elif self.restApi == 'listgrowthampdis':
            self.columnNames = ["stockid", "growthcount",  "ampcount",  "g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10","g11","g12","g13","g14","g15","g16","g17","g18","g19","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","a10","a11","a12","a13","a14","a15","a16","a17","a18","a19"]
        elif self.restApi == 'listndayssum':
            self.columnNames = ["stockid"]
            
    def setRestApi(self,  api):
        self.restApi = api
        #self.setHeader()
    
    def removeFilter(self):
        if 'filter' in self.args:
            self.args.pop('filter')   
        if 'filter' in self.qArgs:
            self.qArgs.pop('filter')  
            
    def setFilter(self, f):
        self.args['filter'] = f
        self.qArgs['filter'] = f
        
    def getArgs(self):
        return self.args
    
    def setRestArgs(self,  args):
        """
        设置访问restAPI的参数，设置时会跟以前的参数相比较，如果发现是同一个参数，不会再次请求。
        """
        args['response'] ='json'
#        log('srcArg',  self.qArgs)
#        log('newArg',  args)
        if self.restApi != 'listdaysum' and 'days' in self.args:
            self.args.pop('days')
        if self.restApi != 'listweeksum' and 'weeks' in self.args:
            self.args.pop('weeks')
        if self.qArgs == args:
            log('args is the same return')
            QMessageBox.warning(self.parent,'warning',  u'参数相同，无须重新查询')
            return
        else:
            for key in args:
                self.args[key] = args[key]
        self.qArgs = args.copy()
        if 'stockid' not in args and 'stockid' in self.args:
            self.args.pop('stockid')
        if 'sortname' not in args and 'sortname' in self.args:
            self.args.pop('sortname')   
        
        self.turnToPage(1)
    
    def callBack(self,  ret ,  load):
        """
        回调函数，用来关闭loading的界面和更新数据
        """
        ret = ret.toPyObject()
        if ret[0] == False:
            QMessageBox.warning(self.parent,'warning', str(ret[1]))
            if load is not None:
                load.close()
            return
        log("call Back")
        self.updateData(ret[1])
        if load is not None:
            load.close()
#        load.emit(SIGNAL("finished()"))
    
    def calcRowsInLimit(self,  col,  small,  big):
        """
        暂时没用到
        """
        log('calcRowsInLimit',  col,  small,  big)
        if (small is None and big is None):
            return []
        if small is not None and big is not None and small > big:
            return []
        hideRows = []
        for i in range(self.rCount):
            log(self.datas[i][col] )
            if (small is not None and self.datas[i][col] < small) or (big is not None and self.datas[i][col] > big) :
                hideRows.append(i)
        return hideRows[:]
    
    def turnToPage(self,  page):
        """
        跳转页面
        """
        if page < 1:
            QMessageBox.warning(self.parent,'warning', u'已经是第一页')
            return
        if page != 1 and page > self.totalPage:
            QMessageBox.warning(self.parent,'warning',  u'已经是尾页')
            return
        if self.restApi != '':
            self.args['page'] = page
            self.args['pagesize'] = self.pageSize;
            self.page = page
#            ret = callRestSync(self.restApi,  self.args)
#            self.updateData(ret[1])
            callRestAsync(self.parent, self.restApi,  self.args,  self)
            
    def showAll(self):
        """
        展示所有数据，这儿为了防止一次传输的数据量太大，做了一定的限制
        """
        if self.restApi != '' and self.totalCount != 0:
            if self.restApi == 'liststockdayinfo' and self.totalCount > 100000:
                QMessageBox.warning(self.parent,'warning', u'基础数据显示全部不能超过100000行')
                return
            elif self.restApi == 'listdaysum' or self.restApi == 'listweeksum' or self.restApi == 'listmonthsum' and self.totalCount > 200000:
                QMessageBox.warning(self.parent,'warning', u'n日和数据显示全部不能超过200000行')
                return
            self.args['page'] = 1
            self.args['pagesize'] = self.totalCount;
            self.page = 1
            callRestAsync(self.parent, self.restApi,  self.args,  self)
        else:
            QMessageBox.warning(self.parent,'warning', u'无数据')
            
    def first(self):
        """
        首页
        """
        self.turnToPage(1)
        pass
    def up(self):
        """
        上一页
        """
        self.turnToPage(self.page - 1)
    def down(self):
        """
        下一页
        """
        self.turnToPage(self.page + 1)
    def last(self):
        """
        尾页
        """
        self.turnToPage(self.totalPage)
    
    def findNearDate(self, curDate):
        for d in myGlobal.dealDays:
            if d >= curDate:
                return d
    def calcStartDate(self, curDate, delta, type):
        if curDate not in myGlobal.dealDays:
            log("======================================================")
            return curDate
        
        if type == 'day':
            startDate = myGlobal.dealDays[myGlobal.dealDays.index(curDate)-delta+1]#  curDate - datetime.timedelta(days = delta - 1)
        elif type == 'week':
            startDate = self.findNearDate(curDate - datetime.timedelta(days = 7 * (delta - 1) + curDate.weekday()))
        else:
            startDate = self.findNearDate(datetime.date(curDate.year, curDate.month, 1))
        
        return startDate
    
    def updateData(self,  rJson):
        """
        更新数据的函数，会根据API的不同，采用不同的解析方式。而且自定义列名，自定义数据显示的格式也都是在这个函数中
        """
        decodedJson = json.loads(rJson)
        
        try:
            if self.restApi == 'liststockdayinfo':
                response = decodedJson['liststockdayinforesponse']
                self.totalCount  = response['count']
                valuelist = response['stockdayinfo']
            elif self.restApi == 'listmonthsum':
                response = decodedJson['listmonthsumresponse']
                self.totalCount  = response['count']
                valuelist = response['monthsuminfo']
            elif self.restApi == 'listdaysum':
                response = decodedJson['listdaysumresponse']
                self.totalCount  = response['count']
                valuelist = response['daysuminfo']
            elif self.restApi == 'listweeksum':
                response = decodedJson['listweeksumresponse']
                self.totalCount  = response['count']
                valuelist = response['weeksuminfo']
            elif self.restApi == 'liststockdaysdiff':
                response = decodedJson['liststockdaysdiffresponse']
                self.totalCount  = response['count']
                valuelist = response['details']
            elif self.restApi == 'listgrowthampdis':
                response = decodedJson['listgrowthampdisresponse']
                self.totalCount  = response['count']
                valuelist = response['growthamp']
            elif self.restApi == 'listndayssum':
                response = decodedJson['listndayssumresponse']
                self.totalCount  = response['count']
                valuelist = response['stockndayssum']
            else:
                QMessageBox.warning(self.parent,'warning', u'查询异常')
                return
        except:
            
            QMessageBox.warning(self.parent,'warning', u'无查询结果')
            return
        
        log('count',  self.totalCount)
        if self.totalCount == 0:
            QMessageBox.warning(self.parent,'warning', u'无查询结果')
            return
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        
        
        
#            print valuelist
        if self.totalCount % self.args['pagesize'] == 0:
            self.totalPage = self.totalCount / self.args['pagesize']
        else:
            self.totalPage = self.totalCount / self.args['pagesize'] + 1
        
        headerSet = True
        log('pagesize', self.args['pagesize'], self.pageSize)
        log('page', self.args['page'])
        
        if self.args['page'] == 1:                  #只有在显示第一页的时候才会刷掉之前的数据(为了‘显示更多’按钮而做的设计)
            self.setHeader()
            del self.datas
            self.datas = []
            self.rCount = 0
            self.cCount = 0
            self.lastRowCount = 0
            headerSet = False
        try:
            for value in valuelist:
#                log(value)
                row = []
                countAppearedKey = []
                
                for key in self.columnNames[:]:
                    if key in countAppearedKey:         #columnNames中可能会出现重复的一些指标，这里防止重复的指标重复显示
                        continue
                    if key not in value:
                        self.columnNames.remove(key)
                        continue
                    if not headerSet:
                        self.headers.append(translate(key))
                    
                    
                    #分段API中需要显示百分比
                    if self.restApi == 'listgrowthampdis' and key != "stockid" and key != "stockname" and key != "growthcount" and key != "ampcount":
                        val = float(value[key])
                        tmpVal = value[key]
#                        log('row',  row)
                        if key.startswith('g'):
                            val /= float(row[1])
                        else:
                            val /= float(row[2])
                        
                        val *= 100
                        val = '%s,(%2.2f%%)' %(str(tmpVal), val)
                        row.append(val)
                        continue
                    
                    if key == 'maxdate' or key == 'mindate':
                        try:
                            tmpDate = datetime.datetime.strptime(value[key],"%Y-%m-%dT%H:%M:%S")
                        except:
                            tmpDate = datetime.datetime.strptime(value[key],"%Y-%m-%dT%H:%M:%S+0800")
                        
                        row.append(tmpDate.strftime("%Y-%m-%d") )
                    else:
                        tmpKey = key
                        if (self.restApi == 'liststockdaysdiff' and 'divide' in self.args['opt'] and key in myGlobal.reCalcTable) or (key not in myGlobal.reCalcTable and 'sum' not in key and \
                            key != 'startvalue' and key != 'endvalue' and key != 'maxvalue' and key != 'minvalue'):
                            row.append(value[key])
                        else:
                            if ('sum' in key and self.args['sumname'] not in myGlobal.reCalcTable) or ((key == 'startvalue' or key == 'endvalue' or key == 'maxvalue' or key == 'minvalue')\
                                and self.args['optname'] not in myGlobal.reCalcTable):
                                row.append(value[key])
                            else:
                                if 'sum' in key:
                                    tmpKey = self.args['sumname']
                                elif key == 'startvalue' or key == 'endvalue' or key == 'maxvalue' or key == 'minvalue':
                                    tmpKey = self.args['optname']
                                val = float(value[key])
                                val /= myGlobal.reCalcTable[tmpKey]
                                val = u'%4.4f' %val
                                row.append(val)
                             
                    countAppearedKey.append(key)

                if self.restApi == 'liststockdaysdiff' or self.restApi == 'listgrowthampdis' or self.restApi == 'listndayssum':
                    if not headerSet:
                        self.headers.insert(1,  u'开始时间')
                        self.headers.insert(2,  u'结束时间')
                    
                    row.insert(1,  str(self.args['starttime']))
                    row.insert(2,  str(self.args['endtime']))
                
                for key in value:
                    if key not in self.columnNames[:]:
                        tmpKey = key
                        if (self.restApi == 'liststockdaysdiff' and 'divide' in self.args['opt'] and key in myGlobal.reCalcTable) or (key not in myGlobal.reCalcTable and 'sum' not in key and \
                            key != 'startvalue' and key != 'endvalue' and key != 'maxvalue' and key != 'minvalue'):
                            row.append(value[key])
                        else:
                            if ('sum' in key and self.args['sumname'] not in myGlobal.reCalcTable) or ((key == 'startvalue' or key == 'endvalue' or key == 'maxvalue' or key == 'minvalue')\
                                and self.args['optname'] not in myGlobal.reCalcTable):
                                row.append(value[key])
                            else:
                                if 'sum' in key:
                                    tmpKey = self.args['sumname']
                                elif key == 'startvalue' or key == 'endvalue' or key == 'maxvalue' or key == 'minvalue':
                                    tmpKey = self.args['optname']
                                val = float(value[key])
                                val /= myGlobal.reCalcTable[tmpKey]
                                val = u'%4.4f' %val
                                row.append(val)
#                        if key == 'total_money':
#                            val = float(value[key])
#                            val /= 100000000
#                            val = u'%.4f亿' %val
#                            row.append(val)
#                        else:
                        if not headerSet:
                            unit = ''
                            if key in myGlobal.typeUnitTable:
                                unit = myGlobal.typeUnitTable[key]
                            if self.restApi == 'liststockdaysdiff':
                                opt = self.args['opt']
                                addName = ''
                                for i in self.parent.cmpMethNames:
                                    if self.parent.cmpMethNames[i] == opt:
                                        addName = i
                                if unit != '':
                                    self.headers.append(translate(key)+'('+unit+')'+'('+addName+')')
                                else:
                                    self.headers.append(translate(key)+'('+addName+')')
                            elif self.restApi == 'listndayssum':
                                if unit != '':
                                    self.headers.append(translate(key)+'('+unit+')'+u'(一段时间内的和)')
                                else:
                                    self.headers.append(translate(key)+u'(一段时间内的和)')
                            else:
                                if unit != '':
                                    self.headers.append(translate(key)+'('+unit+')')
                                else:
                                    if 'sum' in key and 'sumname' in self.args and self.args['sumname'] in myGlobal.typeUnitTable:
                                        self.headers.append(translate(key)+'('+myGlobal.typeUnitTable[self.args['sumname']]+')')
                                    else:
                                        self.headers.append(translate(key))
                            self.columnNames.append(key)
                
                
                if self.restApi != 'liststockdayinfo' and self.restApi != 'listgrowthampdis':
                    for k in range(1, len(row)):
                        try:
                            val = float(row[k])
                            val = u'%4.4f' %val
                        except:
                            val = row[k]
                        row[k] = val
                
                headerSet = True
                self.datas.append(row)   
            
            if self.restApi == 'listdaysum' or self.restApi == 'listweeksum' or self.restApi == 'listmonthsum':
                if u'开始日期' not in self.headers:
                    self.headers[1] = u'结束日期'
                    self.headers.insert(1,  u'开始日期')
                    self.columnNames.insert(1, 'created')
                
                for row in self.datas[self.lastRowCount:]:
                    try:
                        curDate = datetime.datetime.strptime(row[1],"%Y-%m-%dT%H:%M:%S")
                    except:
                        curDate = datetime.datetime.strptime(row[1],"%Y-%m-%dT%H:%M:%S+0800")
                    curDate = curDate.date()
                    startDate = curDate
                    if 'days' in self.args:
                        startDate = self.calcStartDate(curDate, self.args['days'], 'day')#datetime.timedelta(days = self.args['days'])
                    elif 'weeks' in self.args:
                        startDate = self.calcStartDate(curDate, self.args['weeks'], 'week')
#                        startDate -= datetime.timedelta(days = self.args['weeks'] * 7)
                    else:
                        startDate = self.calcStartDate(curDate, self.args['months'], 'month')
#                        startDate -= datetime.timedelta(days = 1)
                    
                    row[1] = curDate.strftime("%Y-%m-%d") 
                    row.insert(1,  startDate.strftime("%Y-%m-%d")  )
            
            if u'名称' not in self.headers:
                self.headers.insert(1,  u'名称')
                self.columnNames.insert(1, 'stockid')
            
#            log('self.columnNames', self.columnNames)
            
            for row in self.datas[self.lastRowCount:]:
                if str(row[0]) in myGlobal.id2name:
                    row.insert(1,  myGlobal.id2name[str(row[0])])
                else:
                    row.insert(1,  u'未知名称');
            
                        
        except:
            self.headers = []
            self.datas = []
            self.emit(QtCore.SIGNAL("layoutChanged()"))
            log('Something is wrong')
#            import traceback
#            traceback.print_exc()
            return
        self.rCount = len(self.datas)
        self.lastRowCount = self.rCount
        if self.rCount > 0:
            self.cCount = len(self.datas[0])
#            print self.rCount,  self.cCount
        self.emit(QtCore.SIGNAL("layoutChanged()"))
            
        
    
    def setHeaders(self, h):
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.headers = h[:]
        self.emit(QtCore.SIGNAL("layoutChanged()"))
    
    def setDatas(self, d):
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.datas = d[:]
        self.rCount = len(self.datas)
        if self.rCount > 0:
            self.cCount = len(self.datas[0])
        self.emit(QtCore.SIGNAL("layoutChanged()"))
    
    def rowCount(self, parent = QModelIndex()):
        return self.rCount
        
    def columnCount(self,  parent = QModelIndex()):
        return self.cCount
    
    def sort(self, col, order = QtCore.Qt.AscendingOrder):
        log(self.restApi, 'sort',  col)
        
        if self.restApi == 'liststockdaysdiff' or self.restApi == 'listgrowthampdis' or self.restApi == 'listndayssum':
            self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
            if self.rCount > 0:
                if col > 1:
                    try:
                        self.datas = sorted(self.datas, key=lambda t:float(t[col][:t[col].find(',')]),  reverse = (order != QtCore.Qt.AscendingOrder))
                    except:
                        self.datas = sorted(self.datas, key=lambda t:t[col],  reverse = (order != QtCore.Qt.AscendingOrder))
                else:
                    self.datas = sorted(self.datas, key=lambda t:t[col],  reverse = (order != QtCore.Qt.AscendingOrder))
                self.emit(QtCore.SIGNAL("layoutChanged()"))
        else:
        
#        if col == 0 or col == 1:
#            return
            args = self.args.copy()
            if col < len(self.columnNames):
                args['sortname'] = self.columnNames[col]
                
                
                if self.restApi == 'liststockdayinfo':
                    if (args['sortname'] not in [ 'growth_ratio', 'turnover_ratio', 'amplitude_ratio', 'avg_price', 'volume_ratio', 'total_money', 'stockid', 'created', 'name']):
                        QMessageBox.warning(self.parent,'warning', u'只有标成红色的指标可以排序')
                        return
                    
                    
                if order == QtCore.Qt.AscendingOrder:
                    args['asc'] = 'true'
                else:
                    args['asc'] = 'false'
                self.setRestArgs(args)

    
    def headerData (self, col , orientation, role = QtCore.Qt.DisplayRole):
        
        if col >= self.cCount and orientation==QtCore.Qt.Horizontal:
            return QVariant();
        if role == QtCore.Qt.ForegroundRole and orientation==QtCore.Qt.Horizontal and self.restApi == 'liststockdayinfo':
            if  col == self.columnNames.index('growth_ratio') or \
                col == self.columnNames.index('turnover_ratio') or \
                col == self.columnNames.index('amplitude_ratio') or \
                col == self.columnNames.index('volume_ratio') or \
                col == self.columnNames.index('avg_price') or \
                col == self.columnNames.index('total_money') or \
                col == self.columnNames.index('stockid') or \
                col == self.columnNames.index('created'):
                    return QVariant(QtGui.QColor(255,0,0));
        if(role==QtCore.Qt.DisplayRole and orientation==QtCore.Qt.Horizontal) :
            return QVariant(self.headers[col]);  
        return QAbstractTableModel.headerData(self, col,orientation,role)
        #,Qt.Orientation
    def data(self,  index,  role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.TextAlignmentRole:
            return QVariant(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        if not index.isValid():
            return QVariant();
        if index.row() > self.rCount or index.column() > self.cCount:
            return QVariant();
        if role == QtCore.Qt.DisplayRole:
            ret = self.datas[index.row()][index.column()]
            try:
#                if index.column() > 1:
#                    ret = float(ret)
                ret = str(ret)
            except:
                pass
            
            return ret
        else:
            return QVariant();
    
    #print names
if __name__ == "__main__":
    scanConfig()
    print 'Done'
