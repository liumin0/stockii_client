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
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QAbstractTableModel.__init__(self, parent)
        self.parent = parent;
        
        #,u"上市日期"
        self.datas=[]
        self.rCount = 0
        self.cCount = 0
        self.totalCount = 0
        self.totalPage = 0
        self.restApi = ''
        self.args = {} #保存包括自己生成的所有参数
        self.qArgs = {} #保存来自外面的请求参数

        self.page = 1
        self.pageSize = 200
        self.connect(self,  SIGNAL("callBack(QVariant, QDialog*)"),  self.callBack)
#        self.connect(self,  QtCore.SIGNAL("first()"),  self.first)
#        self.connect(self,  QtCore.SIGNAL("up()"),  self.up)
#        self.connect(self,  QtCore.SIGNAL("down()"),  self.down)
#        self.connect(self,  QtCore.SIGNAL("last()"),  self.last)
    def setPageSize(self,  pageSize):
        self.pageSize = pageSize
    
    def setHeader(self):
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
        
    def setRestArgs(self,  args):
        args['response'] ='json'
#        log('srcArg',  self.qArgs)
#        log('newArg',  args)
        if self.restApi != 'listdaysum' and 'days' in self.args:
            self.args.pop('days')
        if self.restApi != 'listweeksum' and 'weeks' in self.args:
            self.args.pop('weeks')
        if self.qArgs == args:
            log('args is the same return')
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
            
            
    def first(self):
        self.turnToPage(1)
        pass
    def up(self):
        self.turnToPage(self.page - 1)
    def down(self):
        self.turnToPage(self.page + 1)
    def last(self):
        self.turnToPage(self.totalPage)
    
    def updateData(self,  rJson):
        
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
        self.setHeader()
        
        
#            print valuelist
        if self.totalCount % self.pageSize == 0:
            self.totalPage = self.totalCount / self.pageSize
        else:
            self.totalPage = self.totalCount / self.pageSize + 1
            
        del self.datas
        self.datas = []
        self.rCount = 0
        self.cCount = 0
        headerSet = False
        try:
            for value in valuelist:
#                log(value)
                row = []
                for key in self.columnNames[:]:
                    if key not in value:
                        self.columnNames.remove(key)
                        continue
                    if not headerSet:
                        self.headers.append(translate(key))
                    
                    if self.restApi == 'listgrowthampdis' and key != "stockid" and key != "stockname" and key != "growthcount" and key != "ampcount":
                        val = float(value[key])
                        tmpVal = value[key]
                        log('row',  row)
                        if key.startswith('g'):
                            val /= float(row[1])
                        else:
                            val /= float(row[2])
                        
                        val *= 100
                        val = '%s(%.2f%%)' %(str(tmpVal), val)
                        row.append(val)
                        continue
                    
                    if key == 'total_money':
                        
                        val = float(value[key])
                        val /= 100000000
                        val = u'%.4f亿' %val
                        row.append(val)
                    else:
                        row.append(value[key])
                    
                    
                

                if self.restApi == 'liststockdaysdiff' or self.restApi == 'listgrowthampdis' or self.restApi == 'listndayssum':
                    if not headerSet:
                        self.headers.insert(1,  u'开始时间')
                        self.headers.insert(2,  u'结束时间')
                    row.insert(1,  str(self.args['starttime']))
                    row.insert(2,  str(self.args['endtime']))
                
                for key in value:
                    if key not in self.columnNames[:]:
                        if key == 'total_money':
                            val = float(value[key])
                            val /= 100000000
                            val = u'%.4f亿' %val
                            row.append(val)
                        else:
                            row.append(value[key])   
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
#                log(row)
                self.datas.append(row)   
            
            if self.restApi == 'listdaysum' or self.restApi == 'listweeksum' or self.restApi == 'listmonthsum':
                self.headers[1] = u'结束日期'
                self.headers.insert(1,  u'开始日期')
                self.columnNames.insert(1, 'created')
                
#                log(self.args)
#                log(self.qArgs)
                for row in self.datas:
                    try:
                        curDate = datetime.datetime.strptime(row[1],"%Y-%m-%dT%H:%M:%S")
                    except:
                        curDate = datetime.datetime.strptime(row[1],"%Y-%m-%dT%H:%M:%S+0800")
                    startDate = curDate
                    if 'days' in self.args:
                        startDate -= datetime.timedelta(days = self.args['days'])
                    elif 'weeks' in self.args:
                        startDate -= datetime.timedelta(days = self.args['weeks'] * 7)
                    else:
                        startDate = datetime.datetime(curDate.year, curDate.month, 1)
                        startDate -= datetime.timedelta(days = 1)
                    
                    row.insert(1,  startDate.strftime("%Y-%m-%dT%H:%M:%S")  )
            
            self.headers.insert(1,  u'名称')
            self.columnNames.insert(1, 'stockid')    
            for row in self.datas:
                
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
                        self.datas = sorted(self.datas, key=lambda t:float(t[col][:t[col].find('(')]),  reverse = (order != QtCore.Qt.AscendingOrder))
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
