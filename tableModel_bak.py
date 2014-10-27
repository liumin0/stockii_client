# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtGui import QDialog
from PyQt4.QtSql import QSqlTableModel,  QSqlQuery
from PyQt4.QtCore import pyqtSignature,  QVariant,  QAbstractTableModel,  QModelIndex, QString
import os
import datetime

class MyModel(QAbstractTableModel):
    """
    Class documentation goes here.
    """
    db = None
    query = None
    def __init__(self, parent = None,  db=None):
        """
        Constructor
        """
        QAbstractTableModel.__init__(self, parent)
        if MyModel.db is None:
            if db is None:
                MyModel.db = QtSql.QSqlDatabase.addDatabase('QMYSQL') 
                #self.db.setHostName('42.121.137.80')           
                MyModel.db.setHostName('localhost')           
                MyModel.db.setDatabaseName('test')          
                MyModel.db.setUserName('root')           
                MyModel.db.setPassword('yjtxgtde')     
        #        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE");
        #        self.db.setDatabaseName('./stock.db'); 

                if not MyModel.db.open(): 
                    print 'can not open'
                    QtGui.QMessageBox.information(None,'result', "DB can not open")
                    exit(1)
            else:
                MyModel.db = db
        if MyModel.query is None:
            MyModel.query = QSqlQuery(MyModel.db)
        
        self.headers = [u"代码",u"名称",u"日期",u"涨幅",u"现价",u"日涨跌",u"买入价",u"卖出价",u"总量",u"现量",u"涨速",u"换手",u"今开",u"昨收",\
        u"市盈率",u"最高",u"最低",u"总金额",u"振幅",u"流通股本",u"笔涨跌",u"量比",u"均价",u"委比",u"内盘",u"外盘",u"内外比",u"委量差",u"买量一",\
        u"卖量一",u"买价一",u"卖价一",u"卖价二",u"卖量二",u"买价二",u"买量二",u"买价三",u"买量三",u"卖价三",u"卖量三",u"流通市值",u"多空平衡",\
        u"多头获利",u"多头止损",u"空头回补",u"空头止损",u"强弱度",u"活跃度",u"每笔均量",u"每笔换手",u"更新日期",u"总股本",u"最高价流通市值"\
        ,u"现价流通市值",u"最低价流通市值",u"均价流通市值",u"总市值"]
        #,u"上市日期"
        self.connect(self,  QtCore.SIGNAL("newQuery()"),  self.doNewQuery)
        self.customQuery = []
        self.newCustomQuery = []
        self.names={}
        self.scanConfig()
        self.datas=[]
        self.rCount = 0
        self.cCount = 0
        self.startD = datetime.date(2000, 1, 1)
        self.endD = datetime.date.today()
        self.id = '000001'

    def scanConfig(self):
        path = 'stock_basic_info.txt'
        if os.path.exists(path):
            f = open(path, 'rb')
            c = f.readlines()
            f.close()
            for line in c:
                splitL = line.strip().split()
                try:
                    self.names[splitL[0]] = splitL[1].decode('utf-8')
                except:
                    pass
                
    def setQuery(self):
        self.queryBasic(self.id,  self.startD,  self.endD)
        
    def queryBasic(self,  id,  start,  end):
        self.startD = start
        self.endD = end
        self.id = id
        filter = u"created >= '%s' and created <= '%s'" %(start,  end)
        if id:
            ids = id.split('|')
            if len(ids) > 1:
                filter = filter + u" and (stock_id = '%s'" %ids[0]
                for i in ids[1:]: 
                    i = i.strip()
                    filter = filter + u" or stock_id = '%s'" %i
                filter = filter + u')'
            else:    
                filter = filter + u" and stock_id = '%s'" %ids[0]
        sql = u"select * from stock_day_info where " + filter
        self.filter = filter
#        print sql
        self.query.exec_(sql);
        self.rCount = 0
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        del self.datas
        self.datas=[]
        endCol = self.query.record().indexOf("total_value");
        while self.query.next():
            self.cCount = 0
            self.datas.append([])
            while self.cCount <= endCol:
                #print self.query.value(self.cCount).typeName()
                self.datas[self.rCount].append(self.query.value(self.cCount))
                if self.cCount == 0:
                    try:
                        self.datas[self.rCount].append(QVariant(self.names[str(self.query.value(self.cCount).toByteArray())]))
                    except:
                        self.datas[self.rCount].append(QVariant("#Unknown#"))
                self.cCount+=1
            self.rCount += 1
        self.query.clear()
        self.emit(QtCore.SIGNAL("layoutChanged()"))
        self.queryCustom()
        
        #self.cCount += 1
        #print self.datas
    def queryCustom(self):
        self.newCustomQuery = self.customQuery[:]
        self.doNewQuery()
        
    def doNewQuery(self):
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        for line in self.newCustomQuery:
            if line['type'] == 'D':
                columnName = '_sum'
                if int(line['num']) < 10:
                    targetTable = 'unit_days_sum'
                elif int(line['num']) < 20:
                    targetTable = 'ten_days_sum'
                else:
                    targetTable = 'twenty_days_sum'
            elif line['type'] == 'W':
                targetTable = 'week_sum'
                columnName = '_week_sum'
            else:
                targetTable = 'month_sum'
                columnName = '_month_sum'
            columnName = {1:'one',2:'two',3:'tri',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten',\
                          11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen',16:'sixteen',17:'seventeen',18:'eighteen',\
                          19:'nineteen',20:'twenty',21:'twenty1',22:'twenty2',23:'twenty3',24:'twenty4',25:'twenty5',26:'twenty7',\
                          27:'twenty7',28:'twenty8',29:'twenty9',30:'thirty'}[line['num']] +columnName
            columnName += '_'+line['name']
            sql = u"select stock_id,created,%s from %s where "%(columnName, targetTable) + self.filter
            print sql
            self.query.exec_(sql)
            self.cCount += 1
            count = 0
            findId = False
            findDate = False
            findIndex = 0
            while self.query.next():
#                print self.query.value(0).toString(), self.query.value(1).toString(), self.query.value(2).toString()
                if not findDate:
                    for i in range(self.rCount):
                        if not findId and self.datas[i][0].toString() == self.query.value(0).toString():
                            findId = True
                        if findId and self.datas[i][2].toString() == self.query.value(1).toString():
                            findDate = True
                            findIndex = i
                            break
                        else:
                            continue
                if not findDate:
                    break
                for i in range(findIndex):
                    self.datas[i].append(QVariant(0))
                self.datas[findIndex+count].append(self.query.value(2))
                count += 1
            self.query.clear()
        self.emit(QtCore.SIGNAL("layoutChanged()"))
        for q in self.newCustomQuery:
                self.customQuery.append(q)
        del self.newCustomQuery
        self.newCustomQuery = []
        print 'Done'
    
    def rowCount(self, parent = QModelIndex()):
        return self.rCount
        
    def columnCount(self,  parent = QModelIndex()):
        return self.cCount+1
    
    def sort(self, col, order = QtCore.Qt.AscendingOrder):
#        print 'sort'
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        if self.rCount > 0:
            typeName = self.datas[0][col].typeName();
            if typeName== 'QString' or typeName == 'QDateTime' or typeName == 'QDate':
                self.datas = sorted(self.datas, key=lambda t:t[col].toString(),  reverse = (order != QtCore.Qt.AscendingOrder))
            else:
                self.datas = sorted(self.datas, key=lambda t:t[col].toDouble(),  reverse = (order != QtCore.Qt.AscendingOrder))
            self.emit(QtCore.SIGNAL("layoutChanged()"))
    
    def headerData (self, col , orientation, role):
        if(role==QtCore.Qt.DisplayRole and orientation==QtCore.Qt.Horizontal) :
            return self.headers[col];  
        return QAbstractTableModel.headerData(self, col,orientation,role)
        #,Qt.Orientation
    def data(self,  index,  role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QVariant();
        if index.row() > self.rCount or index.column() > self.cCount:
            return QVariant();
        if role == QtCore.Qt.DisplayRole:
            if index.column() > 1:
                return self.datas[index.row()][index.column()].toString()
            else:
                return self.datas[index.row()][index.column()]
        else:
            return QVariant();
    
    #print names
if __name__ == "__main__":
    scanConfig()
    print 'Done'
