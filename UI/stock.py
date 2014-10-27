 # -*- coding: utf-8 -*-

"""
Module implementing Form.
"""

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignature

from Ui_stock import Ui_Form
from PyQt4 import QtSql
from PyQt4.QtSql import *
from tableModel import MyModel
from queryModel  import MyQueryModel
from myTableWidget import FreezeTableWidget
from dialog import Dialog
class Form(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        
        
        self.selectedItem = ''
        self.items = [ u'均价',\
                            u'总市值',\
                            u'流通股本',\
                            u'总股本',\
                            u'涨幅',\
                            u'换手',\
                            u'振幅',\
                            u'总金额',\
                            u'量比']
        for item in self.items:
            self.comboBox.addItem(item)
        
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL') 
        #self.db.setHostName('42.121.137.80')           
        self.db.setHostName('localhost')           
        self.db.setDatabaseName('test')          
        self.db.setUserName('root')           
        self.db.setPassword('yjtxgtde')     
#        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE");
#        self.db.setDatabaseName('./stock.db'); 

        if not self.db.open(): 
            QtGui.QMessageBox.information(self,'result', "not opened")
            exit(1)
        else:
            #self.model = MyQueryModel(self)
            self.model = MyModel(self, self.db)
            #self.model.setHeaderData(0, 1, "xxxxxxxxxxxx")
            self.model.setQuery()
            self.tableView.myInit(self.model, 2)
            #self.tableView_2.setModel(self.model)
           #self.tableView.setModel(self.model)
            self.model2 = QtSql.QSqlTableModel(self, self.db)
            self.model2.setTable('suminfo')
            self.tableView_2.setModel(self.model2)
#            self.filter = ''
            #self.tableWidget.show()       
        self.tableView_3.setVisible(False)
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        d = Dialog(self.tableView,  self)
        d.show()
#        startD = self.dateEdit.date().toPyDate()
#        endD = self.dateEdit_2.date().toPyDate()
#        codes = str(self.lineEdit.text().toUtf8())
#        #name = str(self.lineEdit_2.text().toUtf8())
#        
#        #self.model.setTable('baseinfo')
#        filter = u"日期 >= '%s' and 日期 <= '%s'" %(startD,  endD)
#        if codes:
#            ids = codes.split('|')
#            if len(ids) > 1:
#                filter = filter + u" and (代码 = '%s'" %ids[0]
#                for id in ids[1:]: 
#                    id = id.strip()
#                    filter = filter + u" or 代码 = '%s'" %id
#                filter = filter + u')'
#            else:    
#                filter = filter + u" and 代码 = '%s'" %ids[0]
#        self.filter = filter
#            
#        #if name:
#         #   filter = filter + u"and 名称 like '%%%s%%'" %name.decode('utf-8')
#        
#        self.model.setFilter(filter)
#        self.model.select()
#        self.model2.setFilter(filter)
#        self.model2.select()

    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        #self.tableView.setFreezeNum(1)
        self.model.setQuery()
#        self.tableView_2.setVisible(False)
#        self.tableView_3.setVisible(True)
#        option = 0
#        startD = self.dateEdit_3.date().toPyDate()
#        endD = self.dateEdit_4.date().toPyDate()
#        if self.radioButton_2.isChecked():
#            option = 1
#        if option == 0:
#            sql = u"select 代码,名称,max(%s) - min(%s) as %s差 from baseinfo where 日期='%s' or 日期='%s' group by 代码" %(self.selectedItem, self.selectedItem, self.selectedItem, startD, endD)
#            
#        else:
#            sql = u"select 代码,名称,max(%s) - min(%s) as %s最大差 from baseinfo where 日期>='%s' and 日期<='%s' group by 代码" %(self.selectedItem, self.selectedItem, self.selectedItem, startD, endD)
#        print sql
#        #self.model2.setTable('baseinfo')
#        model = QtSql.QSqlTableModel(self, self.db)
#        query = QtSql.QSqlQuery(self.db)
#        query.exec_(sql)
#        self.tableView_3.setModel(model)
#        model.setQuery(query)

    @pyqtSignature("")
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
#        self.tableView_2.setVisible(True)
#        self.tableView_3.setVisible(False)
#        #self.model2.setTable('suminfo')
#        self.model2.setFilter(self.filter)
#        #self.tableView_2.setModel(self.model2)
#        self.model2.select()
        for i in range(self.model.rowCount()):
            for j in range(self.model.columnCount()):
                print self.model.data(self.model.index(i, j)).toString().toUtf8(), 
            print ''
        print 'output'
        
    @pyqtSignature("QString")
    def on_comboBox_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        
        self.selectedItem = str(p0.toUtf8()).decode('utf-8')
        #raise NotImplementedError

import sys
from PyQt4 import QtGui

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Form()
    ui.show()
    sys.exit(app.exec_())

