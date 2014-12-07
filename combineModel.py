# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtGui import QDialog
from PyQt4.QtSql import QSqlTableModel,  QSqlQuery
from PyQt4.QtCore import pyqtSignature,  QVariant,  QAbstractTableModel,  QModelIndex, QString
from customModel import CustomModel
import os
import sys
import datetime
from log import log

class CombineModel(CustomModel):
    """
    Class documentation goes here.
    """

    def appendModel(self, model, filter = None):
        if filter is not None and len(filter) == 0:
            return
        appendDatas = model.datas
        appendHeaders = model.headers
        
        mapList = {}
        for i in range(len(appendDatas)):
            mapList[appendDatas[i][0]] = i
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        
        if self.rCount == 0:
            self.headers = appendHeaders[:]
            if filter is not None:
                for i in filter:
                    self.datas.append(appendDatas[i][:])
            else:
                for line in appendDatas:
                    self.datas.append(line[:])
        else:
            self.headers += appendHeaders[:]
            for line in self.datas[:]:
                if line[0] in mapList and (filter is None or mapList[line[0]] in filter):
                    line += appendDatas[mapList[line[0]]][:]
                else:
                    self.datas.pop(self.datas.index(line))
        
        self.rCount = len(self.datas)
        if self.rCount > 0:
            self.cCount = len(self.datas[0])
        self.emit(QtCore.SIGNAL("layoutChanged()"))
    
    def clear(self):
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        del self.datas
        del self.headers
        self.headers = []
        self.datas = []
        self.rCount = 0
        self.cCount = 0
        self.emit(QtCore.SIGNAL("layoutChanged()"))
        
