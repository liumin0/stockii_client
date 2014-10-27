# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow, QFileDialog,  QProgressDialog 
from PyQt4.QtCore import pyqtSignature,  QString
from PyQt4 import QtSql
from Ui_StockUI import Ui_MainWindow
import platform
from queryModel  import MyQueryModel
from dialog import Dialog

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
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
        self.db.setHostName('localhost')           
        self.db.setDatabaseName('test')          
        self.db.setUserName('root')           
        self.db.setPassword('yjtxgtde')     
        if not self.db.open(): 
            QtGui.QMessageBox.information(self,'result', "not opened")
            exit(1)
        else:
            self.model = QtSql.QSqlTableModel(self, self.db)
            self.model.setTable('baseinfo')
            self.model.setFilter(u"代码 = '000001'")
            self.tableView.myInit(self.model, 2)
            
            #self.tableView.setModel(self.model)
            self.model2 = QtSql.QSqlTableModel(self, self.db)
            self.model2.setTable('suminfo')
            self.model2.setFilter(u"代码 = '000001'")
            self.tableView_2.myInit(self.model2, 1)
            
            self.filter = ''
            #self.tableWidget.show()       
        #self.tableView_3.setVisible(False)
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        startD = self.dateEdit.date().toPyDate()
        endD = self.dateEdit_2.date().toPyDate()
        codes = str(self.lineEdit.text().toUtf8())
        #name = str(self.lineEdit_2.text().toUtf8())
        
        #self.model.setTable('baseinfo')
        filter = u"日期 >= '%s' and 日期 <= '%s'" %(startD,  endD)
        if codes:
            ids = codes.split('|')
            if len(ids) > 1:
                filter = filter + u" and (代码 = '%s'" %ids[0]
                for id in ids[1:]: 
                    id = id.strip()
                    filter = filter + u" or 代码 = '%s'" %id
                filter = filter + u')'
            else:    
                filter = filter + u" and 代码 = '%s'" %ids[0]
        #filter += ' limit 2000'
        
        self.filter = filter
        print filter
        #if name:
         #   filter = filter + u"and 名称 like '%%%s%%'" %name.decode('utf-8')
        
        self.model.setFilter(filter)
        self.model.select()
        self.model2.setFilter(filter)
        self.model2.select()
    
    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        option = 0
        startD = self.dateEdit.date().toPyDate()
        endD = self.dateEdit_2.date().toPyDate()
        self.selectedItem = self.comboBox.currentText()
        #if self.radioButton_2.isChecked():
        #    option = 1
        if option == 0:
            sql = u"select 代码,名称,max(%s) - min(%s) as %s差 from baseinfo where 日期='%s' or 日期='%s' group by 代码" %(self.selectedItem, self.selectedItem, self.selectedItem, startD, endD)
            
        else:
            sql = u"select 代码,名称,max(%s) - min(%s) as %s最大差 from baseinfo where 日期>='%s' and 日期<='%s' group by 代码" %(self.selectedItem, self.selectedItem, self.selectedItem, startD, endD)
        print sql
        
        self.model2.clear()
        self.tableView_2.setFreezeNum(2)
        query = QtSql.QSqlQuery(self.db)
        query.exec_(sql)
        self.model2.setQuery(query)
    
    @pyqtSignature("")
    def on_action_triggered(self):
        """.
        Slot documentation goes here.
        """
        self.model.clear()
        #self.model.setFilter(u"代码 = '000002'")
        #self.model.select()
        # TODO: not implemented yet
        #self.tableView_2.setFreezeNum(2)
        print str(self.model.data(self.model.index(1, 0)).toString().toUtf8())
        #raise NotImplementedError
    
    @pyqtSignature("")
    def on_action_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.model.rowCount < 1:
            QtGui.QMessageBox.warning(self,'warning', "Nothing could be export")
            return
        fileName = QFileDialog.getSaveFileName(self,self.tr('Save csv'),'',self.tr("*.csv"))
        if platform.system() == 'Windows':
            fileName = str(fileName.toUtf8()).encode('gbk')
        content = ''
        for j in range(self.model.columnCount()):
            content += str(self.model.headerData(j,  QtCore.Qt.Horizontal).toString().toUtf8())+ ','
        for j in range(self.model.columnCount()):
            content += str(self.model2.headerData(j,  QtCore.Qt.Horizontal).toString().toUtf8())+ ','
        content = content[:-1] + '\r\n'
        progressDialog = QProgressDialog(u"正在导出 (%d/%d)" %(0,  self.model.rowCount()), u"取消", 0, self.model.rowCount(), self)
        for i in range(self.model.rowCount()):
            for j in range(self.model.columnCount()):
                content += str(self.model.data(self.model.index(i, j)).toString().toUtf8())+ ','
            for j in range(self.model2.columnCount()):
                content += str(self.model2.data(self.model2.index(i, j)).toString().toUtf8())+ ','
            content = content[:-1] + '\r\n'
            if  progressDialog.wasCanceled():
                return
            progressDialog.setLabelText (u"正在导出 (%d/%d)" %(i+1,  self.model.rowCount()))
            progressDialog.setValue(i+1)
            
        if platform.system() == 'Windows':
            content = content.decode('utf-8').encode('gbk')
        f = open(fileName,  'wb')
        f.write(content)
        f.close()
    
    @pyqtSignature("")
    def on_action_3_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #dialog = Dialog()
        raise NotImplementedError
