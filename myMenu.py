# -*- coding: utf-8 -*-

"""
Module implementing MyAction.
"""
from PyQt4 import QtGui
import os
from PyQt4.QtGui import QMainWindow,  QMenu,  QAction
from PyQt4.QtCore import pyqtSignature,  QPoint,  SIGNAL
from myAction import MyAction
from log import log

class MyMenu(QMenu):
    """
    Class documentation goes here.
    """
    def __init__(self, title, flag, parent, group):
        """
        Constructor
        """
        QMenu.__init__(self, parent)
        self.parent = parent
        self.setTitle(title)
        self.flag = flag
        self.group = group
        self.addMyActions()
        #self.connect(self,  SIGNAL("triggered()"),  self.myTriggered)
    
    def addMyAction(self, menu, name, arg):
        action = MyAction(name, arg, self.callBack, menu)
        self.group.addAction(action)
        menu.addAction(action)
    
    def addMyActions(self):
        self.addMyAction(self, u'开盘=收盘=最高=最低', 'CLASS_0_0')
        
        subMenu = QMenu(self)
        subMenu.setTitle(u'振幅分档')
        self.addMyAction(subMenu, u'振幅 < 2%', 'CLASS_1_0')
        self.addMyAction(subMenu, u'振幅 = 0', 'CLASS_1_1')
        self.addMenu(subMenu)
        
        subMenu = QMenu(self)
        subMenu.setTitle(u'涨幅分档')
        self.addMyAction(subMenu, u'卖价 = 0, 涨幅 > 4.9%', 'CLASS_2_0')
        self.addMyAction(subMenu, u'买价 = 0, 涨幅 < -4.9%', 'CLASS_2_1')
        self.addMenu(subMenu)
        
        subMenu = QMenu(self)
        subMenu.setTitle(u'总金额分档')
        self.addMyAction(subMenu, u'总金额 < 0.9999亿', 'CLASS_3_0')
        self.addMyAction(subMenu, u'总金额 1 ~ 1.9999亿', 'CLASS_3_1')
        self.addMyAction(subMenu, u'总金额 2 ~ 4.9999亿', 'CLASS_3_2')
        self.addMyAction(subMenu, u'总金额 >= 5亿', 'CLASS_3_3')
        self.addMyAction(subMenu, u'总金额 >  9亿', 'CLASS_3_4')
        self.addMyAction(subMenu, u'总金额 >  15亿', 'CLASS_3_5')
        self.addMyAction(subMenu, u'总金额 >  20亿', 'CLASS_3_6')
        self.addMyAction(subMenu, u'总金额 >  25亿', 'CLASS_3_7')
        self.addMyAction(subMenu, u'总金额 >  30亿', 'CLASS_3_8')
        self.addMyAction(subMenu, u'总金额 >  40亿', 'CLASS_3_9')
        self.addMenu(subMenu)
        
        subMenu = QMenu(self)
        subMenu.setTitle(u'总金额分档')
        self.addMyAction(subMenu, u'换手率 < 0.9999%', 'CLASS_4_0')
        self.addMyAction(subMenu, u'换手率 1% ~ 2.9999%', 'CLASS_4_1')
        self.addMyAction(subMenu, u'换手率 3% ~ 4.9999%', 'CLASS_4_2')
        self.addMyAction(subMenu, u'换手率 5% ~ 6.9999%', 'CLASS_4_3')
        self.addMyAction(subMenu, u'换手率 7% ~ 9.9999%', 'CLASS_4_4')
        self.addMyAction(subMenu, u'换手率 >= 10%', 'CLASS_4_5')
        self.addMyAction(subMenu, u'换手率 > 15%', 'CLASS_4_6')
        self.addMyAction(subMenu, u'换手率 > 20%', 'CLASS_4_7')
        self.addMyAction(subMenu, u'换手率 > 25%', 'CLASS_4_8')
        self.addMyAction(subMenu, u'换手率 > 30%', 'CLASS_4_9')
        self.addMyAction(subMenu, u'换手率 > 35%', 'CLASS_4_10')
        self.addMyAction(subMenu, u'换手率 > 40%', 'CLASS_4_11')
        self.addMyAction(subMenu, u'换手率 > 45%', 'CLASS_4_12')
        self.addMyAction(subMenu, u'换手率 > 50%', 'CLASS_4_13')
        self.addMyAction(subMenu, u'换手率 > 60%', 'CLASS_4_14')
        self.addMenu(subMenu)
        
        
        subMenu = QMenu(self)
        subMenu.setTitle(u'时间分档')
        for year in range(2008, 2015):
            tmpCount = 0
            ssubMenu = QMenu(self)
            ssubMenu.setTitle(str(year))
            sssubMenu = QMenu(ssubMenu)
            sssubMenu.setTitle(u'季度分档')
            for i in range(1, 5):
                self.addMyAction(sssubMenu, u'第 %d 季度' %i, 'CLASS_5_%d' %tmpCount)
                tmpCount += 1
            ssubMenu.addMenu(sssubMenu)
            sssubMenu = QMenu(ssubMenu)
            sssubMenu.setTitle(u'月份分档')
            for month in range(1, 13):
                self.addMyAction(sssubMenu, u'%d 月' %month, 'CLASS_5_%d' %tmpCount)
                tmpCount += 1
            ssubMenu.addMenu(sssubMenu)
            subMenu.addMenu(ssubMenu)
        self.addMenu(subMenu)
    
    def callBack(self, arg):
#        log.log(self.name, ' is triggered')
        log('menu:',  self.flag)
        log('arg:', arg)
        self.parent.detailClassify(self.flag, arg)
        #self.setChecked(True)
        #self.callBack(self.arg)
        #print self.isChecked()
