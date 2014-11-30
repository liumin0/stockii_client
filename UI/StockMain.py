# -*- coding: utf-8 -*-

"""
Module implementing StockMain.
"""
from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow,  QMessageBox,  QMenu,  QActionGroup,  QRegExpValidator
from PyQt4.QtCore import pyqtSignature, SIGNAL,  QPoint,  QDate,  QRegExp

from Ui_StockMain import Ui_MainWindow
from chooseid import ChooseId
from customModel import CustomModel
from tableSetting import TableSetting
from myAction import MyAction
from myMenu import MyMenu
import myGlobal
import config
import log
import datetime


class StockMain(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.initTypeCombo()
        self.ids = []
        self.tableSetting = None
        self.selectedGroup = None
        self.classifyMenuGroup = None
        regx = QRegExp("[0-9]*[\.]{0,1}[0-9]*$");
        validator = QRegExpValidator(regx, self)
        self.smallValueEdit.setValidator( validator )
        self.bigValueEdit.setValidator( validator )
        self.on_daySumRadio_clicked()
        self.initCmpMethCombo()
        self.initCmpTypeCombo()
        self.filter = ''
#        myGlobal.init()
#        myGlobal.initDealDays()
        self.dayInfoModel = CustomModel(self)
        self.dayInfoModel.setRestApi('liststockdayinfo')
        self.dayInfoModel.setPageSize(10000)
        self.calcModel = CustomModel(self)
        self.calcModel.setRestApi('listmonthsum')
        self.calcModel.setPageSize(20000)
        self.calcModel2 = CustomModel(self)
        self.calcModel2.setRestApi('liststockdaysdiff')
        self.calcModel2.setPageSize(10000)
        self.classifyMenu = None
        self.startDate = QDate.currentDate()
        self.endDate = self.startDate.addDays(-1)
        self.calcTableWidget.setButtonsVisible(False)
        #self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
        savedSetting = config.readSetting()
        if 'groups' in savedSetting:
            self.groups = savedSetting['groups']
        else:
            self.groups = {}
        self.updateFilter()
        self.listWidget.setVisible(False)
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
        self.modifyDateEdit()
        self.showGroupBtn.setChecked(True)
        self.on_showGroupBtn_clicked()
        self.showMaximized()
        
    def modifyDateEdit(self):
        curIndex = self.tabWidget.currentIndex()
        if curIndex == 0:
            self.startDateEdit = self.startDateEdit_1
            self.endDateEdit = self.endDateEdit_1
        elif curIndex == 1:
            self.startDateEdit = self.startDateEdit_2
            self.endDateEdit = self.endDateEdit_2
        elif curIndex == 2:
            self.startDateEdit = self.startDateEdit_3
            self.endDateEdit = self.endDateEdit_3
        
        self.startDateEdit.setDate(self.startDate)
        self.endDateEdit.setDate(self.endDate)
        
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
        
        self.sumTypeNames = {
                            u'正和':'positive', \
                            u'负和':'negative', \
                            u'所有和':'all'
                    }
        for key in self.sumTypeNames:
            self.sumTypeCombo.addItem(key)
    
    def initCmpMethCombo(self):
        self.cmpMethNames = {
                             u'指定两天加':'plus', \
                             u'指定两天减':'minus', \
                             u'指定两天比值':'divide', \
                             u'指定时间段内最大值减最小值':'maxmin', \
                             u'指定时间段内最大值比最小值':'maxmindivide', \
                             u'指定时间段内的和':'sum', \
                             u'两个时间内涨幅,振幅数据分段':"seperate", 
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
        u'现价':'current_price',\
        u'换手':'turnover_ratio',\
        u'总金额':'total_money',\
        u'振幅':'amplitude_ratio',\
        u'量比':'volume_ratio'}
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
        items = [str(i) for i in range(1, 13)]
        for item in items:
            self.numCombo.addItem(item)
    
    def chooseNearDate(self, d, ):
        lastDate = ''
        for tmpDate in myGlobal.dealDays:
            
            if tmpDate > d:
                if lastDate != '':
                    return lastDate.strftime("%Y-%m-%d")+ ', ' +tmpDate.strftime("%Y-%m-%d")
                else:
                    return u'无, ' +tmpDate.strftime("%Y-%m-%d")
            lastDate = tmpDate
        
        return lastDate.strftime("%Y-%m-%d") + u', 无'
    
    def testDate(self, startD, endD):
        if startD >= endD:
            QMessageBox.warning(self,'warning', u'开始时间大于或等于结束时间')
            return False
        if startD not in myGlobal.dealDays:
            QMessageBox.warning(self,'warning', u'开始时间非交易日或无数据，请重新选择，前后的交易日期分别为： '+ self.chooseNearDate(startD))
            return False
        if endD not in myGlobal.dealDays:
            QMessageBox.warning(self,'warning', u'结束时间非交易日或无数据，请重新选择，前后的交易日期分别为： '+ self.chooseNearDate(endD))
            return False
        return True
        
    @pyqtSignature("")
    def on_queryBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
#        from loading import Loading
#        import http
#        http.callRestAsync(self, "xxx",  {"sss":'s'},  self.callBack)
#        if True:
#            return
        if len(self.ids) == 0:
            QMessageBox.warning(self,'warning', u'所选代码为空，请选择代码')
            return
        
        startD = self.startDateEdit.date().toPyDate()
        endD = self.endDateEdit.date().toPyDate()
        self.startDate = self.startDateEdit.date()
        self.endDate = self.endDateEdit.date()
        if not self.testDate(startD, endD):
            return
        
        #response=json&page=2&pagesize=20&stockid=000001,000002,000003,000004,000005&starttime=2008-09-24&sortname=turnover_ratio
        config.collect('info', u'原始数据查询, 起始时间:%s, 结束时间:%s, 代码: %s' %(startD, endD, self.ids))
        args = {}
        if len(self.ids) == len(myGlobal.id2name.keys()):
            args = {'starttime':startD,  'endtime':endD}
        else:
            args = {'stockid':','.join(self.ids),  'starttime':startD,  'endtime':endD}
        self.dayInfoModel.setRestArgs(args)
        
        self.srcTableWidget.init(self.dayInfoModel, 2,  self.tableSetting)
    
    @pyqtSignature("")
    def on_queryBtn_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
            
        if len(self.ids) == 0:
            QMessageBox.warning(self,'warning', u'所选代码为空，请选择代码')
            return
        
        startD = self.startDateEdit_2.date().toPyDate()
        endD = self.endDateEdit_2.date().toPyDate()
        self.startDate = self.startDateEdit.date()
        self.endDate = self.endDateEdit.date()
        #response=json&page=2&pagesize=20&stockid=000001,000002,000003,000004,000005&starttime=2008-09-24&sortname=turnover_ratio
        if not self.testDate(startD, endD):
            return
            
        customNum = self.numCombo.currentText().toInt()[0]
        calcName = self.typeNames[str(self.typeCombo.currentText().toUtf8()).decode('utf-8')]
        sumType = self.sumTypeNames[str(self.sumTypeCombo.currentText().toUtf8()).decode('utf-8')]
        log.log(calcName)
        config.collect('info', u'X日和查询, 起始时间:%s, 结束时间:%s, 查询指标:%s, 查询类型:%s 代码: %s,' %(startD, endD, str(self.typeCombo.currentText().toUtf8()).decode('utf-8'), str(customNum)+self.customType.replace('D', u'日').replace('W', u'周').replace('M', u'月'), self.ids))
        if len(self.ids) == len(myGlobal.id2name.keys()):
            args = {'starttime':startD,  'endtime':endD,  'sumType':sumType,  'sumname': calcName}
        else:
            args = {'stockid':','.join(self.ids),  'starttime':startD,  'endtime':endD,  'sumType':sumType,  'sumname': calcName}
        if self.customType == 'D':
            self.calcModel.setRestApi('listdaysum')
            args['days'] = customNum
        elif self.customType == 'W':
            self.calcModel.setRestApi('listweeksum')
            args['weeks'] = customNum
        elif self.customType == 'M':
            self.calcModel.setRestApi('listmonthsum')
            args['months'] = customNum
        self.calcModel.setRestArgs(args)
        self.sumTableWidget.init(self.calcModel)

        #raise NotImplementedError
    @pyqtSignature("")
    def on_action_triggered(self):
        """
        Slot documentation goes here.
        设置dayinfo表中的显示列
        """
        # TODO: not implemented yet
        if not self.srcTableWidget.inited:
            QMessageBox.warning(self,'warning', u'列表中尚无内容，请先查询')
            return
        tableSetting = TableSetting.getSetting(self.srcTableWidget.getView(),  self)
        log.log(tableSetting)
        if tableSetting is not None:
            self.tableSetting = tableSetting
            self.srcTableWidget.setSetting(self.tableSetting)
    
    @pyqtSignature("QPoint")
    def on_listWidget_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        代码筛选框中的右键
        """
        # TODO: not implemented yet
        cur = self.cursor()
        curPos = cur.pos()
        log.log(curPos.x(),  curPos.y())
        menu = QMenu(self);
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
        if ret is None:
            return
        self.groups[ret[0]] = ret[1]
#            self.listWidget.addItem(ret[0])
        config.collect('info', u'添加分组, 分组名称: %s, 分组详情: %s' %(ret[0], ','.join(ret[1])))
        log.log(self.groups)
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
        else:
            return
        config.collect('info', u'编辑分组, 分组名称: %s, 新分组详情: %s' %(ret[0], ','.join(ret[1])))
        self.updateFilter()
        config.writeSetting('groups',  self.groups)
        if self.selectedGroup == selectedItemText:
            self.ids = self.groups[self.selectedGroup]
            self.clearClassify()
            self.changeIds(self.groups[self.selectedGroup])
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
        config.collect('info', u'删除分组, 分组名称: %s, 分组详情: %s' %(selectedItemText, ','.join(self.groups[selectedItemText])))
        self.groups.pop(selectedItemText)
        self.updateFilter()
        config.writeSetting('groups',  self.groups)
    
#    @pyqtSignature("bool")
#    def on_action_showGroupView_triggered(self, checked):
#        """
#        Slot documentation goes here.
#        """
#        # TODO: not implemented yet
#        if checked:
#            self.groupView.show()
#        else:
#            self.groupView.hide()
#        #raise NotImplementedError
    
#    @pyqtSignature("bool")
#    def on_groupView_visibilityChanged(self, visible):
#        """
#        Slot documentation goes here.
#        """
#        # TODO: not implemented yet
#        if visible:
#            self.action_showGroupView.setChecked(True)
#        else:
#            self.action_showGroupView.setChecked(False)
#        #raise NotImplementedError
    
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
#        log.log('self.ids:',  self.ids)
        self.clearClassify()
        self.changeIds(self.groups[self.selectedGroup])
        
#        log('self.ids:',  self.ids)
#        curIndex = self.tabWidget.currentIndex()
#        if curIndex == 0:
#            self.on_queryBtn_clicked()
#        elif curIndex == 1:
#            self.on_queryBtn_2_clicked()
#        elif curIndex == 2:
#            self.on_calculateBtn_clicked()
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
        startD = self.startDateEdit_3.date().toPyDate()
        endD = self.endDateEdit_3.date().toPyDate()
        self.startDate = self.startDateEdit.date()
        self.endDate = self.endDateEdit.date()
        if not self.testDate(startD, endD):
            return
        #response=json&page=2&pagesize=20&stockid=000001,000002,000003,000004,000005&starttime=2008-09-24&sortname=turnover_ratio
        #optname=avg_price,growth_ratio,current_price&opt=-&starttime=2008-03-25&endtime=2008-03-28&page=4&pagesize=20
        optname = self.cmpTypeNames[str(self.cmpTypeCombo.currentText().toUtf8()).decode('utf-8')] #self.cmpTypeCombo.currentText().toInt()[0]
        opt = self.cmpMethNames[str(self.cmpMethCombo.currentText().toUtf8()).decode('utf-8')]
        log.log(opt)
        config.collect('info', u'计算查询, 起始时间:%s, 结束时间:%s, 计算指标:%s, 计算类型:%s, 代码: %s' %(startD, endD, str(self.cmpTypeCombo.currentText().toUtf8()).decode('utf-8'), str(self.cmpMethCombo.currentText().toUtf8()).decode('utf-8'), self.ids))

        if opt == 'seperate':
            args = {'stockid':','.join(self.ids),  'starttime':startD,  'endtime':endD}
            self.calcModel2.setRestApi('listgrowthampdis')
        elif opt == 'sum':
            args = {'stockid':','.join(self.ids),  'starttime':startD,  'endtime':endD,  'sumname':optname}
            self.calcModel2.setRestApi('listndayssum')
        else:
            args = {'stockid':','.join(self.ids),  'starttime':startD,  'endtime':endD,  'optname':optname,  'opt': opt}
            self.calcModel2.setRestApi('liststockdaysdiff')
        
        log.log("ids",  len(self.ids),   len(myGlobal.id2name.keys()))
        if len(self.ids) == len(myGlobal.id2name.keys()):
            args.pop('stockid')
        
        
        self.calcModel2.setRestArgs(args)
        
        if self.calcModel2.restApi == 'listgrowthampdis':
            self.calcTableWidget.init(self.calcModel2, 6)
        else:
            self.calcTableWidget.init(self.calcModel2, 2)
            
#        smallLimit = self.smallValueEdit.text().toFloat()
#        bigLimit = self.bigValueEdit.text().toFloat()
#        smallValue = None
#        bigValue = None
#        if smallLimit[1]:
#            smallValue = smallLimit[0]
#        if bigLimit[1]:
#            bigValue = bigLimit[0]
#        hideRows = self.calcModel2.calcRowsInLimit(4,  smallValue,  bigValue)
#        log(hideRows)
#        log(self.smallValueEdit.text().toFloat()).


#        log(self.bigValueEdit.text().toFloat())
#        self.calcTableWidget.init(self.calcModel2,  0,  {'hideRows': hideRows})
    @pyqtSignature("int")
    def on_tabWidget_currentChanged(self, index):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
#        raise NotImplementedError
        self.modifyDateEdit()
        self.clearClassify()
        if index == 0:
            self.dayInfoModel.removeFilter()
        elif index == 1:
            self.calcModel.removeFilter()
        elif index == 2:
            self.calcModel2.removeFilter()
    
    def changeIds(self,  ids):
        log.log('ChangeIds')
        log.log('self.ids:',  self.ids)
        self.ids = ids
        curIndex = self.tabWidget.currentIndex()
        if curIndex == 0:
            self.dayInfoModel.removeFilter()
            self.on_queryBtn_clicked()
        elif curIndex == 1:
            self.calcModel.removeFilter()
            self.on_queryBtn_2_clicked()
        elif curIndex == 2:
            self.calcModel2.removeFilter()
            self.on_calculateBtn_clicked()
    
    @pyqtSignature("")
    def on_showGroupBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        if self.classifyBtn.isChecked():
            self.classifyBtn.setChecked(False)
        if self.showGroupBtn.isChecked():
            self.listWidget.setVisible(True)
        else:
            self.listWidget.setVisible(False)
    
    @pyqtSignature("")
    def on_classifyBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        if self.showGroupBtn.isChecked():
            self.showGroupBtn.setChecked(False)
            self.on_showGroupBtn_clicked()
        if self.classifyMenu is None:
            self.classifyMenu = QMenu(self)
            subMenu = QMenu(self)
            subMenu.setTitle(u'地区板块')
            self.classifyMenuGroup = QActionGroup(self)
            for key in myGlobal.area2ids:
                if len(key) != 0:
                    action = MyAction(key,  myGlobal.area2ids[key],  self.changeIds,  self)
                    subMenu.addAction(action)
                    self.classifyMenuGroup.addAction(action)
            self.classifyMenu.addMenu(subMenu)
            subMenu = QMenu(self)
            subMenu.setTitle(u'行业板块')
            for key in myGlobal.industry2ids:
                if len(key) != 0:
                    action = MyAction(key,  myGlobal.industry2ids[key],  self.changeIds,  self)
                    subMenu.addAction(action)
                    self.classifyMenuGroup.addAction(action)
            self.classifyMenu.addMenu(subMenu)
            subMenu = MyMenu(u'向上版块', 'FLAG_UP', self, self.classifyMenuGroup)
            self.classifyMenu.addMenu(subMenu)
            subMenu = MyMenu(u'向下版块', 'FLAG_DOWN', self, self.classifyMenuGroup)
            self.classifyMenu.addMenu(subMenu)
            
        self.classifyBtn.setChecked(True)
        pos = QPoint()
        pos.setX(0);
        pos.setY(-self.classifyMenu.sizeHint().height());
        self.classifyMenu.exec_(self.classifyBtn.mapToGlobal(pos));

    def clearClassify(self):
        if self.classifyMenuGroup is not None:
            checkedAction = self.classifyMenuGroup.checkedAction()
            if checkedAction is not None:
                checkedAction.setChecked(False)
    
    @pyqtSignature("QString")
    def on_cmpMethCombo_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        if str(p0.toUtf8()).decode('utf-8') == u'两个时间内涨幅,振幅数据分段':
            self.cmpTypeCombo.setEnabled(False)
        else:
            self.cmpTypeCombo.setEnabled(True)
    
    @pyqtSignature("QListWidgetItem*")
    def on_listWidget_itemClicked(self, item):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.selectedGroup = self.getTextFromItem(self.listWidget.selectedItems())
        if self.selectedGroup not in self.groups:
            QMessageBox.warning(self,'warning', u'未知分组')
            return
        self.ids = self.groups[self.selectedGroup]
#        log.log('self.ids:',  self.ids)
        self.clearClassify()
        #raise NotImplementedError
    def detailClassifyDate(self, arg):
        clz, switchType, subType = arg.split('_')
        if switchType != '5':
            return
        subTypeL = subType.split('.')
        subType = subTypeL[0]
        year = int(subTypeL[1])
        self.startDate, self.endDate = {
         '0': (QDate(year, 1, 1), QDate(year, 3, 31)),                                          #u'第 1 季度'
         '1': (QDate(year, 4, 1), QDate(year, 6, 30)),                                          #u'第 2 季度'
         '2': (QDate(year, 7, 1), QDate(year, 9, 30)),                                          #u'第 3 季度'
         '3': (QDate(year, 10, 1), QDate(year, 12, 31)),                                        #u'第 4 季度'
         '4': (QDate(year, 1, 1), QDate(year, 2, 1).addDays(-1)),                               #u'1 月'
         '5': (QDate(year, 2, 1), QDate(year, 3, 1).addDays(-1)),                               #u'2 月'
         '6': (QDate(year, 3, 1), QDate(year, 4, 1).addDays(-1)),                               #u'3 月'
         '7': (QDate(year, 4, 1), QDate(year, 5, 1).addDays(-1)),                               #u'4 月'
         '8': (QDate(year, 5, 1), QDate(year, 6, 1).addDays(-1)),                               #u'5 月'
         '9': (QDate(year, 6, 1), QDate(year, 7, 1).addDays(-1)),                               #u'6 月'
         '10': (QDate(year, 7, 1), QDate(year, 8, 1).addDays(-1)),                              #u'7 月'
         '11': (QDate(year, 8, 1), QDate(year, 9, 1).addDays(-1)),                              #u'8 月'
         '12': (QDate(year, 9, 1), QDate(year, 10, 1).addDays(-1)),                             #u'9 月'
         '13': (QDate(year, 10, 1), QDate(year, 11, 1).addDays(-1)),                            #u'10 月'
         '14': (QDate(year, 11, 1), QDate(year, 12, 1).addDays(-1)),                            #u'11 月'
         '14': (QDate(year, 12, 1), QDate(year, 12, 31)),                                       #u'12 月'
        }[subType]
        self.modifyDateEdit()
        
    def detailClassify(self, type, arg):
        curIndex = self.tabWidget.currentIndex()
        self.detailClassifyDate(arg)
        
        if curIndex == 0:
            self.dayInfoModel.setFilter(type + '#' + arg)
            self.on_queryBtn_clicked()
        elif curIndex == 1:
            self.calcModel.setFilter(type + '#' + arg)
            self.on_queryBtn_2_clicked()
        elif curIndex == 2:
            self.calcModel2.setFilter(type + '#' + arg)
            self.on_calculateBtn_clicked()
    
