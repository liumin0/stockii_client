# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtGui import QDialog
from PyQt4.QtSql import QSqlQueryModel,  QSqlQuery
from PyQt4.QtCore import pyqtSignature,  QVariant,  QAbstractTableModel,  QModelIndex


class MyQueryModel(QSqlQueryModel):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QSqlQueryModel.__init__(self, parent)
        self.data = []
        self.rCount = 0
        self.cCount = 0
        
        
    def ouput(self,  filePath):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                print self.data(self.index(i, j)).toString().toUtf8(),
            print ''
    
    def rowCount(self, parent = QModelIndex()):
        return self.rCount
        
    def columnCount(self,  parent = QModelIndex()):
        return self.cCount
    
    def setQuery(self,  str,  db=None):
        if db == None:
            self.query = QSqlQuery(str)
        else:
            self.query = str
        QSqlQueryModel.setQuery(self,  str)
        del self.data
        self.data = []
        self.rCount = QSqlQueryModel.rowCount(self)
        if self.rCount > 10000:
            self.rCount = 10000
        self.cCount = QSqlQueryModel.columnCount(self)
        for i in range(self.rCount ):
            row = []
            for j in range(self.cCount):
                row.append(QSqlQueryModel.data(self, QSqlQueryModel.index(self, i, j)))
            self.data.append(row)
        self.clear()
        print self.rowCount(), self.columnCount()
#    def rowCount(self, parent = QModelIndex()):
#        return self.rCount
#        
#    def columnCount(self,  parent = QModelIndex()):
#        return self.cCount
#    
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
    

    
    def data(self,  index,  role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QVariant();
        if index.row() > self.rCount or index.column() > self.cCount:
            return QVariant();
        if role == QtCore.Qt.DisplayRole:
            return self.datas[index.row()][index.column()]
        else:
            return QVariant();
