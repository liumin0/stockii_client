# -*- coding: utf-8 -*-

"""
Module implementing Server.
"""

from PyQt4.QtGui import QDialog,  QMessageBox
from PyQt4.QtCore import pyqtSignature

from Ui_server import Ui_Dialog

import myGlobal

class Server(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        
        myGlobal.serverType = None
        myGlobal.serverAddr = None
        if self.radioButton.isChecked():
            myGlobal.serverType = 'local'
        else:
            myGlobal.serverType = 'web'
        
        addr = str(self.lineEdit.text().toUtf8())
        addr = addr.strip()
        
        if len(addr) > 0:
            myGlobal.serverAddr = addr
        else:
            QMessageBox.warning(self,'warning', u'地址不能为空')
            return
        
        
            
