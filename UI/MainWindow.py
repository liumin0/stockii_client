# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow,  QMessageBox,  QMenu
from PyQt4.QtCore import pyqtSignature, SIGNAL

from Ui_MainWindow import Ui_MainWindow
from chooseid import ChooseId
from customModel import CustomModel
from tableSetting import TableSetting

import myGlobal
import config
from log import log

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
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)
        self.splitter_2.setStretchFactor(0, 3)
        self.splitter_2.setStretchFactor(1, 1)
        self.initTypeCombo()
        self.ids = []
        self.tableSetting = None
        self.selectedGroup = None
        self.on_daySumRadio_clicked()
        self.initCmpMethCombo()
        self.initCmpTypeCombo()
        myGlobal.init()
        savedSetting = config.readSetting()
        if 'groups' in savedSetting:
            self.groups = savedSetting['groups']
        else:
            self.groups = {}
        self.updateFilter()
    #初始化 model#
        self.dayInfoModel = CustomModel(self)
        self.dayInfoModel.setRestApi('listStockDayInfo')
        self.calcModel = CustomModel(self)
        self.calcModel.setRestApi('listMonthSum')
        self.calcModel2 = CustomModel(self)
        self.calcModel2.setRestApi('List2DiffStockDayInfo')
        self.connect(self.tb1_headBtn,  SIGNAL("clicked()"),  self.dayInfoModel.first)
        self.connect(self.tb1_upBtn,  SIGNAL("clicked()"),  self.dayInfoModel.up)
        self.connect(self.tb1_downBtn,  SIGNAL("clicked()"),  self.dayInfoModel.down)
        self.connect(self.tb1_lastBtn,  SIGNAL("clicked()"),  self.dayInfoModel.last)
        
        self.connect(self.tb2_headBtn,  SIGNAL("clicked()"),  self.calcModel.first)
        self.connect(self.tb2_upBtn,  SIGNAL("clicked()"),  self.calcModel.up)
        self.connect(self.tb2_downBtn,  SIGNAL("clicked()"),  self.calcModel.down)
        self.connect(self.tb2_lastBtn,  SIGNAL("clicked()"),  self.calcModel.last)
        
        
        #self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
        self.action_showGroupView.setChecked(True)
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
        self.showMaximized()
    
    def updateFilter(self):
        self.listWidget.clear()
        for key in self.groups:
            self.listWidget.addItem(key)
            
    def initTypeCombo(self):
        self.customName = u'均价'
        self.customType = 'D'
        self.customNum = 3
        self.typeNames = {  
                            u'均价':'avg_price', \
                            u'涨幅':'growth', \
                            u'换手':'turn',\
                            u'振幅':'amp',\
                            u'总金额':'total',\
                            u'量比':'vol'}
        for key in self.typeNames:
            self.typeCombo.addItem(key)
    
    def initCmpMethCombo(self):
        self.cmpMethNames = {
                             u'指定两天加':'+', \
                             u'指定两天减':'-', \
                             u'指定两天比值':'/', \
                             u'指定时间内最高价减最低价':'maxmin', \
                             u'两天时间内数据分段':"seperate", 
                             }
        
        for key in self.cmpMethNames:
            self.cmpMethCombo.addItem(key)
    
    def initCmpTypeCombo(self):
        #avg_price,growth_ratio,current_price,total_stock,total_value,avg_circulation_value,cir_of_cap_stock
        self.cmpTypeCombo.clear()
        self.cmpTypeNames = {
        u'均价':'avg_price', \
        u'涨幅':'growth_ratio', \
        u'总股本':'total_stock', \
        u'总市值':'total_value', \
        u'均价流通市值':'avg_circulation_value', \
        u'流通股本':'cir_of_cap_stock', \
        u'现价':'current_price',}



#        u'换手':'turnover_ratio', \
#        u'振幅':'amplitude_ratio', \
#        u'总金额':'total_money', \
#        u'量比':'volume_ratio'}
#        typeName = u'%s%d%s' %(self.customName, self.customNum,  {'D':u"日", 'W':u"周", 'M':u"月"}[self.customType])
#        self.cmpTypeNames[typeName]='#####tobefinished#####'
        for key in self.cmpTypeNames:
            self.cmpTypeCombo.addItem(key)
    
    @pyqtSignature("")
    def on_daySumRadio_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.customType = 'D'
        self.numCombo.clear()
        items = [str(i) for i in range(3, 31)]
        for item in items:
            self.numCombo.addItem(item)
        #raise NotImplementedError
    
    @pyqtSignature("")
    def on_weekSumRadio_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.customType = 'W'
        self.numCombo.clear()
        items = [str(i) for i in range(1, 7)]
        for item in items:
            self.numCombo.addItem(item)
        #raise NotImplementedError
    
    @pyqtSignature("")
    def on_monthSumRadio_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.customType = 'M'
        self.numCombo.clear()
        self.numCombo.addItem('1')
    
    @pyqtSignature("")
    def on_queryBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
            
        if len(self.ids) == 0:
            QMessageBox.warning(self,'warning', u'所选代码为空，请选择代码')
            return
        
        startD = self.startDateEdit.date().toPyDate()
        endD = self.endDateEdit.date().toPyDate()
        if startD == endD:
            QMessageBox.warning(self,'warning', u'起止时间相同')
            return
        #response=json&page=2&pagesize=20&stockid=000001,000002,000003,000004,000005&starttime=2008-09-24&sortname=turnover_ratio
        args = {}
        if len(self.ids) == len(myGlobal.id2name.keys()):
            args = {'starttime':startD,  'endtime':endD}
        else:
            args = {'stockId':','.join(self.ids),  'starttime':startD,  'endtime':endD}
        self.dayInfoModel.setRestArgs(args)
        customNum = self.numCombo.currentText().toInt()[0]
        calcName = self.typeNames[str(self.typeCombo.currentText().toUtf8()).decode('utf-8')]
        log(calcName)
        
        if len(self.ids) == len(myGlobal.id2name.keys()):
            args = {'starttime':startD,  'endtime':endD,  'sumType':'all',  'sumname': calcName}
        else:
            args = {'stockId':','.join(self.ids),  'starttime':startD,  'endtime':endD,  'sumType':'all',  'sumname': calcName}
        if self.customType == 'D':
            self.calcModel.setRestApi('listDaySum')
            args['days'] = customNum
        elif self.customType == 'W':
            self.calcModel.setRestApi('listWeekSum')
            args['weeks'] = customNum
        elif self.customType == 'M':
            self.calcModel.setRestApi('listMonthSum')
        self.calcModel.setRestArgs(args)
        if not self.tableView.inited:
            log(" doing init")
            self.tableView.myInit(self.dayInfoModel,  2)
            self.tableView.setSetting(self.tableSetting)
        
        if not self.tableView_2.inited:
            self.tableView_2.myInit(self.calcModel,  0)
        self.refreshTable()
        self.initCmpTypeCombo()
    
    def refreshTable(self):
        self.tb1_curPageLabel.setText('%d/%d' %(self.dayInfoModel.page,  self.dayInfoModel.totalPage))
        if self.dayInfoModel.page == 1:
            self.tb1_upBtn.setEnabled(False)
        else:
            self.tb1_upBtn.setEnabled(True)
        
        if self.dayInfoModel.page== self.dayInfoModel.totalPage:
            self.tb1_downBtn.setEnabled(False)
        else:
            self.tb1_downBtn.setEnabled(True)
            
        self.tb2_curPageLabel.setText('%d/%d' %(self.calcModel.page,  self.calcModel.totalPage))
        if self.calcModel.page == 1:
            self.tb2_upBtn.setEnabled(False)
        else:
            self.tb2_upBtn.setEnabled(True)
        
        if self.calcModel.page== self.calcModel.totalPage:
            self.tb2_downBtn.setEnabled(False)
        else:
            self.tb2_downBtn.setEnabled(True)
        #raise NotImplementedError
    @pyqtSignature("")
    def on_action_triggered(self):
        """
        Slot documentation goes here.
        设置dayinfo表中的显示列
        """
        # TODO: not implemented yet
        if not self.tableView.inited:
            QMessageBox.warning(self,'warning', u'列表中尚无内容，请先查询')
            return
        tableSetting = TableSetting.getSetting(self.tableView,  self)
        log(tableSetting)
        if tableSetting is not None:
            self.tableSetting = tableSetting
            self.tableView.setSetting(self.tableSetting)
    
    @pyqtSignature("QPoint")
    def on_listWidget_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        代码筛选框中的右键
        """
        # TODO: not implemented yet
        cur = self.cursor()
        curPos = cur.pos()
        log(curPos.x(),  curPos.y())
        menu = QMenu(self.dockWidgetContents);
        menu.addAction(self.action_addGroup);
        if self.listWidget.itemAt(pos):
            menu.addAction(self.action_editGroup); 
            menu.addAction(self.action_deleteGroup); 
        menu.exec_(curPos);
#        #raise NotImplementedError
    
    def getTextFromItem(self,  item):
        selectItem = None
        if type(item) == type([]):
            if len(item) <= 0:
                QMessageBox.warning(self,'warning', u'没有选中任何组')
                return None
            selectItem = item[0]
        else:
            selectItem = item
        selectedItemText = str(selectItem.text().toUtf8()).decode('utf-8')
        return selectedItemText
    
    @pyqtSignature("")
    def on_action_addGroup_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        ret = ChooseId.getIds(self,  self.groups)
        if ret is not None:
            self.groups[ret[0]] = ret[1]
#            self.listWidget.addItem(ret[0])
        
        log(self.groups)
        self.updateFilter()
        config.writeSetting('groups',  self.groups)
        #raise NotImplementedError
    
    @pyqtSignature("")
    def on_action_editGroup_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #print 'delete'
        selectedItemText = self.getTextFromItem(self.listWidget.selectedItems())#str(selectedItems[0].text().toUtf8()).decode('utf-8')
        if selectedItemText not in self.groups:
            QMessageBox.warning(self,'warning', u'未知分组')
            return
        ret = ChooseId.getIds(self,  self.groups,  selectedItemText )
        if ret is not None:
            if selectedItemText != ret[0]:
                self.groups.pop(selectedItemText)
            self.groups[ret[0]] = ret[1]
        
        self.updateFilter()
        config.writeSetting('groups',  self.groups)
        if self.selectedGroup == selectedItemText:
            self.ids = self.groups[self.selectedGroup]
            self.on_queryBtn_clicked()
            self.on_calculateBtn_clicked()
        #raise NotImplementedError
    
    @pyqtSignature("")
    def on_action_deleteGroup_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        selectedItemText = self.getTextFromItem(self.listWidget.selectedItems())
        if selectedItemText not in self.groups:
            QMessageBox.warning(self,'warning', u'未知分组')
            return
        self.groups.pop(selectedItemText)
        self.updateFilter()
        config.writeSetting('groups',  self.groups)
    
    @pyqtSignature("bool")
    def on_action_showGroupView_triggered(self, checked):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if checked:
            self.groupView.show()
        else:
            self.groupView.hide()
        #raise NotImplementedError
    
    @pyqtSignature("bool")
    def on_groupView_visibilityChanged(self, visible):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if visible:
            self.action_showGroupView.setChecked(True)
        else:
            self.action_showGroupView.setChecked(False)
        #raise NotImplementedError
    
    @pyqtSignature("QListWidgetItem*")
    def on_listWidget_itemDoubleClicked(self, item):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.selectedGroup = self.getTextFromItem(self.listWidget.selectedItems())
        if self.selectedGroup not in self.groups:
            QMessageBox.warning(self,'warning', u'未知分组')
            return
        self.ids = self.groups[self.selectedGroup]
        self.on_queryBtn_clicked()
        #raise NotImplementedError
    
    @pyqtSignature("")
    def on_calculateBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        if len(self.ids) == 0:
            QMessageBox.warning(self,'warning', u'所选代码为空，请选择代码')
            return
        startD = self.cmpDateEdit1.date().toPyDate()
        endD = self.cmpDateEdit2.date().toPyDate()
        if startD == endD:
            QMessageBox.warning(self,'warning', u'起止时间相同')
            return
        #response=json&page=2&pagesize=20&stockid=000001,000002,000003,000004,000005&starttime=2008-09-24&sortname=turnover_ratio
        #optname=avg_price,growth_ratio,current_price&opt=-&starttime=2008-03-25&endtime=2008-03-28&page=4&pagesize=20
        optname = self.cmpTypeNames[str(self.cmpTypeCombo.currentText().toUtf8()).decode('utf-8')] #self.cmpTypeCombo.currentText().toInt()[0]
        opt = self.cmpMethNames[str(self.cmpMethCombo.currentText().toUtf8()).decode('utf-8')]
        log(opt)
        if opt == 'seperate':
            args = {'stockId':','.join(self.ids),  'starttime':startD,  'endtime':endD}
            self.calcModel2.setRestApi('listGrowthAmpDis')
        else:
            args = {'stockId':','.join(self.ids),  'starttime':startD,  'endtime':endD,  'optname':optname,  'opt': opt}
            self.calcModel2.setRestApi('List2DiffStockDayInfo')
        if len(self.ids) == len(myGlobal.id2name.keys()):
            args.pop('stockId')
        self.calcModel2.setRestArgs(args)
        if not self.tableView_3.inited:
            self.tableView_3.myInit(self.calcModel2,  0)
    

