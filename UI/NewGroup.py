# -*- coding: utf-8 -*-

"""
Module implementing NewGroup.
"""

from PyQt4.QtGui import QDialog, QMessageBox
from PyQt4.QtCore import pyqtSignature

from Ui_NewGroup import Ui_Dialog

class NewGroup(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, ids, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.ids = ids
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        groupName = str(self.lineEdit.text().toUtf8()).decode('utf-8')
        if groupName is None or groupName == '':
            QMessageBox.warning(self.parent,'warning', u'组名不能为空')
            return
        
        #print groupName
        if groupName in self.parent.groups:
            QMessageBox.warning(self.parent,'warning', u'%s 已经存在' %groupName)#
            return
        
        if len(self.ids) == 0:
            QMessageBox.warning(self.parent,'warning', u'已选列表为空')#
            return
        
        self.parent.groups[groupName] = self.ids
        self.parent.updateFilter()
        self.close()
        #raise NotImplementedError
    
    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        self.close()
