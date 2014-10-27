# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt4 import QtCore
from PyQt4.QtGui import QDialog, QListWidgetItem,  QMessageBox
from PyQt4.QtCore import pyqtSignature

from Ui_dialog import Ui_Dialog

class TableSetting(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    ret = {}
    def __init__(self, tableView,  parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        del TableSetting.ret
        TableSetting.ret = None
        self.setWindowTitle(u"自定义列表")
        self.tableView = tableView
        headers=self.tableView.model().headers
        for i in range(len(headers)):
            newItem = QListWidgetItem();
            newItem.setText(headers[i]);
            
            if self.tableView.isColumnHidden(i):
                newItem.setCheckState(QtCore.Qt.Unchecked)
            else:
                newItem.setCheckState(QtCore.Qt.Checked)
            self.listWidget.insertItem(i, newItem)
            if i < 2:
                newItem.setHidden(True)
        items = [str(i) for i in range(self.listWidget.count())]
        for item in items:
            self.comboBox_3.addItem(item)
        self.comboBox_3.setCurrentIndex(self.tableView.freezeNum)        
        
        self.groupBox.setVisible(False)
#        self.names = {  u'涨幅':'growth',\
#                            u'换手':'turn',\
#                            u'振幅':'amp',\
#                            u'总金额':'total',\
#                            u'量比':'vol'}
#        for key in self.names:
#            self.comboBox_2.addItem(key)
#        
#        self.customName = ''
#        self.customType = 'D'
#        self.customNum = 1
#        self.addCol = False
#        self.on_radioButton_clicked()
    
    @classmethod 
    def getSetting(clazz, tableView,  parent = None):
        dialog = clazz(tableView,  parent)
        dialog.exec_()
        return TableSetting.ret
        
        
    @pyqtSignature("int")
    def on_checkBox_stateChanged(self, state):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet

        for i in range(self.listWidget.count()):
            if i < 2:
                continue
            self.listWidget.item(i).setCheckState(state)

    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
#        if self.addCol:
#            self.tableView.model().doNewQuery()
        hideColumns = []
        for i in range(self.listWidget.count()):
            
            if not self.listWidget.item(i).checkState():
                hideColumns.append(i)
                self.tableView.hideColumn(i)
        self.tableView.setFreezeNum(self.comboBox_3.currentText().toInt()[0])
        TableSetting.ret = {'freezeNum':self.comboBox_3.currentText().toInt()[0],  'hideColumns':hideColumns}
        #self.tableView.model().emit(QtCore.SIGNAL("newQuery()"))
        
        self.close()
        #raise NotImplementedError
    
    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.close()
        #raise NotImplementedError
    
#    @pyqtSignature("")
#    def on_radioButton_clicked(self):
#        """
#        Slot documentation goes here.
#        """
#        # TODO: not implemented yet
#        self.customType = 'D'
#        self.comboBox.clear()
#        items = [str(i) for i in range(3, 31)]
#        for item in items:
#            self.comboBox.addItem(item)
#        #raise NotImplementedError
#    
#    @pyqtSignature("")
#    def on_radioButton_2_clicked(self):
#        """
#        Slot documentation goes here.
#        """
#        # TODO: not implemented yet
#        self.customType = 'W'
#        self.comboBox.clear()
#        items = [str(i) for i in range(1, 7)]
#        for item in items:
#            self.comboBox.addItem(item)
#        #raise NotImplementedError
#    
#    @pyqtSignature("")
#    def on_radioButton_3_clicked(self):
#        """
#        Slot documentation goes here.
#        """
#        # TODO: not implemented yet
#        self.customType = 'M'
#        self.comboBox.clear()
#        self.comboBox.addItem('1')
#        #raise NotImplementedError
#    
#    @pyqtSignature("")
#    def on_pushButton_3_clicked(self):
#        """
#        Slot documentation goes here.
#        """
#        # TODO: not implemented yet
#        self.customNum = self.comboBox.currentText().toInt()[0]
#        self.customName = self.names[str(self.comboBox_2.currentText().toUtf8()).decode('utf-8')]
##        print self.customType
##        print self.customNum
##        print self.customName
#        addHeaderName = self.comboBox_2.currentText()+'%d%s'%(self.customNum, self.customType)
#        if addHeaderName in self.tableView.model().headers:
#            QMessageBox.warning(self,'Warning', u"%s 已经存在" %(addHeaderName))
#            return
#        self.tableView.model().headers.append(addHeaderName)
#        self.tableView.model().newCustomQuery.append({'type':self.customType, 'num':self.customNum,  'name':self.customName})
#        newItem = QListWidgetItem();
#        newItem.setText(addHeaderName);
#        newItem.setCheckState(QtCore.Qt.Checked)
#        self.listWidget.insertItem(self.listWidget.count(), newItem)
#        self.listWidget.scrollToItem(newItem)
#        self.addCol = True

        #raise NotImplementedError
