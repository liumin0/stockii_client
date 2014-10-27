# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow, QFileDialog,  QProgressDialog , QMessageBox
from PyQt4.QtCore import pyqtSignature,  QString
from PyQt4 import QtSql
from Ui_StockUI import Ui_MainWindow
import platform
from queryModel  import MyQueryModel
from tableModel import MyModel
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
        self.model = MyModel(self)
        self.model.setQuery()
        self.tableView.myInit(self.model, 2)
        self.groupBox_2.setVisible(False)
        self.model2 = QtSql.QSqlQueryModel(self)
        self.tableView_2.setModel(self.model2)
            #self.tableWidget.show()       
        #self.tableView_2.setVisible(True)
    
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
#        print filter
        self.model.queryBasic(codes, startD, endD)
    
    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        option = 0
        startD = self.dateEdit_3.date().toPyDate()
        endD = self.dateEdit_4.date().toPyDate()
        self.selectedItem = {u'均价':'avg_price', u'总市值':'total_value', u'流通股本':'cir_of_cap_stock', \
                                    u'总股本':'total_stock', u'涨幅':'growth_ratio', u'换手':'turnover_ratio', \
                                    u'振幅':'amplitude_ratio', u'总金额':'total_money', u'量比':'volume_ratio'}[str(self.comboBox.currentText().toUtf8()).decode('utf-8')]
        #if self.radioButton_2.isChecked():
        if self.radioButton_2.isChecked():
            option = 1
        if option == 0:
            sql = u"select 代码,名称,max(%s) - min(%s) as %s差 from baseinfo where 日期='%s' or 日期='%s' group by 代码"\
                    %(self.selectedItem, self.selectedItem, self.selectedItem, startD, endD)
            sql = u"select stock_id, max(%s) - min(%s) as %s差 from stock_day_info where created ='%s' or created='%s' group by stock_id"\
                    %(self.selectedItem, self.selectedItem, self.comboBox.currentText(), startD, endD)
        else:
            sql = u"select stock_id, max(%s) - min(%s) as %s差 from stock_day_info where created >='%s' and created <='%s' group by stock_id"\
                    %(self.selectedItem, self.selectedItem, self.comboBox.currentText(), startD, endD)        
        
#        print sql
        
        self.model2.clear()
#        self.tableView_2.setFreezeNum(2)
        query = QtSql.QSqlQuery()
        query.exec_(sql)
        self.model2.setQuery(query)
        if self.groupBox_2.isHidden():
            self.groupBox_2.show()
    
    @pyqtSignature("")
    def on_action_triggered(self):
        """.
        Slot documentation goes here.
        """
        #self.model.clear()
        #self.model.setFilter(u"代码 = '000002'")
        #self.model.select()
        # TODO: not implemented yet
        #self.tableView_2.setFreezeNum(2)
        QMessageBox.warning(self,'warning', u"权限不够")
        #print str(self.model.data(self.model.index(1, 0)).toString().toUtf8())
        #raise NotImplementedError
    
    def doExport(self,  model):
#        print model.rowCount()
        if model.rowCount() < 1:
            QMessageBox.warning(self,'warning', "导出内容为空")
            return
        fileName = QFileDialog.getSaveFileName(self,self.tr('Save csv'),'',self.tr("*.csv"))
        if not fileName:
            return
        if platform.system() == 'Windows':
            fileName = str(fileName.toUtf8()).encode('gbk')
        content = ''
        for j in range(model.columnCount()):
            try:
                content += str(model.headerData(j,  QtCore.Qt.Horizontal).toString().toUtf8())+ ','
            except:
                content += str(model.headerData(j,  QtCore.Qt.Horizontal).toUtf8())+ ','
#        for j in range(model.columnCount()):
#            content += str(model2.headerData(j,  QtCore.Qt.Horizontal).toString().toUtf8())+ ','
        content = content[:-1] + '\r\n'
        progressDialog = QProgressDialog(u"正在导出 (%d/%d)" %(0,  model.rowCount()), u"取消", 0, model.rowCount(), self)
        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                try:
                    content += str(model.data(model.index(i, j)).toString().toUtf8())+ ','
                except:
                    content += str(model.data(model.index(i, j)).toUtf8())+ ','
#            for j in range(model2.columnCount()):
#                content += str(model2.data(model2.index(i, j)).toString().toUtf8())+ ','
            content = content[:-1] + '\r\n'
            if  progressDialog.wasCanceled():
                return
            progressDialog.setLabelText (u"正在导出 (%d/%d)" %(i+1,  model.rowCount()))
            progressDialog.setValue(i+1)
            
        if platform.system() == 'Windows':
            content = content.decode('utf-8').encode('gbk')
        f = open(fileName,  'wb')
        f.write(content)
        f.close()

    @pyqtSignature("")
    def on_action_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        model = self.model
        self.doExport(model)
        
    
    @pyqtSignature("")
    def on_action_3_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #dialog = Dialog()
        d = Dialog(self.tableView,  self)
        d.show()
    
    @pyqtSignature("")
    def on_action_4_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        model = self.model2
        self.doExport(model)
        #raise NotImplementedError
