# -*- coding: utf-8 -*-

"""
Module implementing ChooseId.
"""

from PyQt4.QtGui import QDialog, QTableWidgetItem,  QMessageBox
from PyQt4.QtCore import pyqtSignature

from Ui_chooseid import Ui_Dialog
import os
import myGlobal

class ChooseId(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    ret = []
    
    def __init__(self, parent,  groupNames,  groupName = None):
        """
        
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.names = myGlobal.id2name.keys()
#        self.scanConfig()
        self.groups = groupNames
        self.orgName = groupName
        if groupName is not None: 
            self.choosedId = self.groups[groupName]
            self.isCreate = False
        else:
            self.choosedId = []
            self.isCreate = True
        if groupName == None:
            tmpName = u'新建分组%d'
            i = 1
            if self.groups is not None:
                while((tmpName %i) in self.groups):
                    i += 1
            groupName = tmpName %i
        
        self.lineEdit.setText(groupName)
            
        del ChooseId.ret
        ChooseId.ret = None
        self.tableWidget_2.setHorizontalHeaderLabels([u'代码',u'名称'])  
        self.initTable(self.tableWidget,  self.names)
        self.initTable(self.tableWidget_2,  self.choosedId)
        if self.tableWidget_2.rowCount() == 0 :
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            
    def initTable(self,  table,  ids):
        table.setHorizontalHeaderLabels([u'代码',u'名称'])  
        count = 0
        ids.sort()
        for i in ids:
            try:
                self.tableAddRow(table,  i,  myGlobal.id2name[i])
            except:
                ids.remove(i)
    
    def tableAddRow(self,  table,  id,  name):
        if table == self.tableWidget_2:
            if self.tableWidget_2.rowCount() == 0 :
                
                self.pushButton_4.setEnabled(True)
        
        curRow = table.rowCount()
        #print curRow, id,  name
        table.insertRow(curRow)
        newItem = QTableWidgetItem(id)
        table.setItem(curRow, 0, newItem)  
        newItem = QTableWidgetItem(name)
        table.setItem(curRow, 1,  newItem)  
        
    @classmethod 
    def getIds(clazz, parent,  groupNames,  groupName = None):
        dialog = clazz(parent,  groupNames,  groupName)
        dialog.exec_()
        return ChooseId.ret
    
    
    #添加按钮
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        selectedItems = self.tableWidget.selectedItems()
        self.tableWidget_2.setSortingEnabled(False)
        for item in selectedItems:
            if item.column() == 0:
                id = str(item.text().toUtf8())
                if id not in self.choosedId:
                    self.choosedId.append(id)
#                    self.choosedId[id] = self.names[id]
                    self.tableAddRow(self.tableWidget_2,  id,  myGlobal.id2name[id])
        
        self.tableWidget_2.setSortingEnabled(True)
        #raise NotImplementedError
    
    #全部添加按钮
    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        ids = self.names
        ids.sort()
        self.tableWidget_2.setSortingEnabled(False)
        for id in ids:
            if id not in self.choosedId:
                self.choosedId.append(id)
#                self.choosedId[id] = self.names[id]
                self.tableAddRow(self.tableWidget_2,  id,  myGlobal.id2name[id])
        
        self.tableWidget_2.setSortingEnabled(True)
        #raise NotImplementedError
    
    #删除按钮
    @pyqtSignature("")
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        selectedItems = self.tableWidget_2.selectedItems()
        tobeRemove = []
        for item in selectedItems:
            if item.column() == 0 and item.row() not in tobeRemove:
                id = str(item.text().toUtf8())
                if id in self.choosedId:
                    self.choosedId.remove(id)
                tobeRemove.append(item.row())
        tobeRemove.sort(reverse=True)
        for row in tobeRemove:
            self.tableWidget_2.removeRow(row)

        if self.tableWidget_2.rowCount() == 0 :
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
    
    #全部删除按钮
    @pyqtSignature("")
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        while self.tableWidget_2.rowCount() > 0:
            self.tableWidget_2.removeRow(0)
        del self.choosedId
        self.choosedId = []
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
    
    @pyqtSignature("")
    def on_tableWidget_2_itemSelectionChanged(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        if len(self.tableWidget_2.selectedItems()) > 0:
            self.pushButton_3.setEnabled(True)
        else:
            self.pushButton_3.setEnabled(False)
        
    @pyqtSignature("")
    def on_pushButton_5_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        groupName = str(self.lineEdit.text().toUtf8()).decode('utf-8')
        if groupName is None or groupName == '':
            QMessageBox.warning(self.parent,'warning', u'组名不能为空')
            return
        
        #print groupName
        if self.orgName != groupName and  groupName in self.groups:
            QMessageBox.warning(self.parent,'warning', u'%s 已经存在' %groupName)#
            return
        
        if len(self.choosedId) == 0:
            QMessageBox.warning(self.parent,'warning', u'已选列表为空')#
            return
        ChooseId.ret = (groupName,  self.choosedId[:])
        self.close()
        
    @pyqtSignature("")
    def on_pushButton_6_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        self.close()
    
    @pyqtSignature("QModelIndex")
    def on_tableWidget_doubleClicked(self, index):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        row = index.row()
        item = self.tableWidget.item(row,  0)
        id = str(item.text().toUtf8())
        self.tableWidget_2.setSortingEnabled(False)
        if id not in self.choosedId:
            self.choosedId.append(id)
#            self.choosedId[id] = self.names[id]
            self.tableAddRow(self.tableWidget_2,  id,  myGlobal.id2name[id])
        self.tableWidget_2.setSortingEnabled(True)
    

if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    print ChooseId.getIds()
    sys.exit(app.exec_())
    
    
        #raise NotImplementedError
