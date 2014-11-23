# -*- coding: utf-8 -*-

"""
Module implementing MyAction.
"""
from PyQt4 import QtGui
import os
from PyQt4.QtGui import QMainWindow,  QMenu,  QAction
from PyQt4.QtCore import pyqtSignature,  QPoint,  SIGNAL
import log

class MyAction(QAction):
    """
    Class documentation goes here.
    """
    def __init__(self, name,  arg,  callBack,  parent = None):
        """
        Constructor
        """
        QAction.__init__(self, parent)
        self.setCheckable(True)
        self.name = name
        self.parent = parent
        self.arg = arg
        self.callBack = callBack
        self.setText(name)
        self.connect(self,  SIGNAL("triggered()"),  self.myTriggered)
    
    
    def myTriggered(self):
#        log.log(self.name, ' is triggered')
        self.setChecked(True)
        self.callBack(self.arg)
        #print self.isChecked()
