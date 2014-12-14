# -*- coding: utf-8 -*-

"""
Module implementing MyTable.
"""

from PyQt4 import QtCore
from PyQt4.QtGui import QWidget,  QMenu,  QFileDialog,  QProgressDialog
from PyQt4.QtCore import pyqtSignature,  SIGNAL

from Ui_MyTable import Ui_Form
import platform
from log import log
import threading

class MyTable(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.model = None
        self.setting = None
        self.limit = (None,  None) #保存限制条件
        self.freezeNum = 0
        self.inited = False
        self.parent = None
        self.modelSet = False
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
        self.clearBtn.setVisible(False)
        self.undoBtn.setVisible(False)
        self.connect(self.clearBtn,  SIGNAL("clicked()"),  self.clearCombine)
        self.connect(self.undoBtn,  SIGNAL("clicked()"),  self.undo)
        
    def setButtonsVisible(self,  visible):
#        self.headBtn.setVisible(visible)
#        self.preBtn.setVisible(visible)
#        self.nextBtn.setVisible(visible)
#        self.lastBtn.setVisible(visible)
        self.curPageLabel.setVisible(visible)
        self.showAllBtn.setVisible(visible)
        self.showMoreBtn.setVisible(visible)
        
    
    def __init(self):
#        log.log('[*] __init',  self.tableView.inited)
        if not self.tableView.inited:
            self.tableView.myInit(self.model,  self.freezeNum)
            if self.setting is not None:
                self.tableView.setSetting(self.setting)
            self.inited = True
        self.tableView.setFreezeNum(self.freezeNum)
#        self.tableView.refreshHidden()
        self.refreshIndex()
    
    def init(self, model,  freezeNum = 0,  setting = None, parent = None):
        self.setModel(model)
        
        self.parent = parent
        bakFreezeNum = self.freezeNum
        self.freezeNum = freezeNum
        if setting is not None:
            self.setting = setting
        if self.model.rowCount() > 0:
            self.__init()
            if bakFreezeNum != freezeNum and model.restApi != 'liststockdayinfo' and model.restApi != 'listdaysum' and model.restApi != 'listweeksum' and model.restApi != 'listmonthsum':
                model.sort(0)
            self.tableView.horizontalHeader().setSortIndicatorShown(False)
        #print 'mytable init'
        
        self.connect(model, SIGNAL("layoutChanged()"),  self.__init)
        self.connect(self, SIGNAL("progressChanged(int,int)"),  self.setProgress)
        
    def getView(self):
        return self.tableView
    
    def setSetting(self,  setting):
        if setting is not None and self.tableView.inited:
            self.tableView.setSetting(setting)
            
    def setFreezeNum(self,  freezeNum):
        self.freezeNum = freezeNum
        if self.tableView.inited:
            self.tableView.setFreezeNum(freezeNum)
        
    def setModel(self,  model):
        self.model = model
        if self.modelSet == False:
            self.connect(self.showMoreBtn,  SIGNAL("clicked()"),  self.model.down)
            self.connect(self.showAllBtn,  SIGNAL("clicked()"),  self.model.showAll)
            
            self.modelSet = True
    
    def refreshIndex(self):
        self.curPageLabel.setText('%d/%d' %(self.model.page,  self.model.totalPage))
#        if self.model.page == 1:
#            self.preBtn.setEnabled(False)
#        else:
#            self.preBtn.setEnabled(True)
#        
#        if self.model.page== self.model.totalPage:
#            self.nextBtn.setEnabled(False)
#        else:
#            self.nextBtn.setEnabled(True)
    
    @pyqtSignature("QPoint")
    def on_tableView_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        if self.inited:
            cur = self.cursor()
            curPos = cur.pos()
            menu = QMenu(self);
            menu.addAction(self.actionDump);
            menu.addAction(self.actionDumpSelected);
            if self.model == self.parent.calcModel2 or self.model == self.parent.crossModel:
                menu.addAction(self.actionCombine);
                menu.addAction(self.actionCombineSelected);
            menu.exec_(curPos);
    
    @pyqtSignature("")
    def on_actionDump_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        self.doExport(self.model,  None)
        
    @pyqtSignature("")
    def on_actionDumpSelected_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        filter = []
        for selected in self.tableView.selectedIndexes():
            if selected.row() not in filter:
                filter.append(selected.row())
            else:
                break
        
        self.doExport(self.model,  filter)
    
    def setProgress(self, value, totalCount):
        self.progressDialog.setLabelText (u"正在导出 (%d/%d)" %(value,  totalCount))
        self.progressDialog.setValue(value)
    
    def adjustEncode(self, s, fileName, index):
        ret = s
        flag = False
        if index > 0:
            try:
                ret = float(s)
                flag = True
            except:
                pass
        if not flag and platform.system() == 'Windows':
            if fileName.endswith('.csv'):
                try:
                    ret = s.encode('gbk')
                except:
                    pass
        return str(ret)
    
    def exportThreadFunc(self, model, filter, fileName):
        headers = []
        for j in range(model.columnCount()):
            try:
                headers.append(self.adjustEncode(str(model.headerData(j, QtCore.Qt.Horizontal).toString().toUtf8()).decode('utf-8'), fileName, j))
            except:
                headers.append(self.adjustEncode(str(model.headerData(j, QtCore.Qt.Horizontal).toUtf8()).decode('utf-8'), fileName, j))
            
        f = open(fileName,  'ab')
        f.write(','.join(headers)+'\r\n')
        if filter is not None:
            totalCount = len(filter)
        else:
            totalCount = model.rowCount()
        count = 0
        datas = []
        for i in range(model.rowCount()):
            row = []
            if filter is not None and i not in filter:
                continue
            for j in range(model.columnCount()):
                try:
                    row.append(self.adjustEncode(str(model.data(model.index(i, j))), fileName, j))
                except:
                    row.append(self.adjustEncode(model.data(model.index(i, j)), fileName, j))
            if self.progressDialog.wasCanceled():
                f.close()
                return
            
            
            count += 1
            datas.append(row)
            if fileName.endswith('.xlsx') or fileName.endswith('.csv'):
                row[0] = '="%s"'%row[0]
            f.write(','.join(row)+'\r\n')
            self.emit(SIGNAL("progressChanged(int,int)"), count, totalCount)
        
        f.close()
#        print '-----start'
#        datas=tablib.Dataset(*datas,headers=headers)
#        print '-----start2'
#        if fileName.endswith('.csv'):
#            f.write(datas.csv)
#        elif fileName.endswith('.xls'):
#            f.write(datas.xls)
#        elif fileName.endswith('.xlsx'):
#            f.write(datas.xlsx)
#        
#        print datas.xlsx
#        print '-----end'
#        f.close()
#        self.emit(SIGNAL("progressChanged(int,int)"), totalCount, totalCount)
        
    def doExport(self,  model, filter):
#        print model.rowCount()
        if model.rowCount() < 1:
            QMessageBox.warning(self,'warning', "导出内容为空")
            return
        fileName = QFileDialog.getSaveFileName(self,self.tr('Save Contents'),'', u"csv文件 (*.csv)")
        if not fileName:
            return
        if platform.system() == 'Windows':
            fileName = str(fileName.toUtf8()).decode('utf-8').encode('gbk')
        else:
            fileName = str(fileName.toUtf8())
        if filter is not None:
            totalCount = len(filter)
        else:
            totalCount = model.rowCount()
        self.progressDialog = QProgressDialog(u"正在导出 (%d/%d)" %(0,  totalCount), u"取消", 0, totalCount, self)
        thread = threading.Thread(target = self.exportThreadFunc,  args=(model,  filter, fileName))
        thread.setDaemon(True)
        thread.start()
        
#        self.progressDialog.exec_()
    
    @pyqtSignature("")
    def on_actionCombine_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.parent.combineWidget.init(self.parent.combineModel, parent = self.parent)
        self.parent.combineModel.appendModel(self.model, None)
        
    def clearCombine(self):
        try:
            self.parent.combineModel.clear()
        except:
            pass
    
    def undo(self):
        try:
            self.parent.combineModel.undo()
        except:
            pass
    
    @pyqtSignature("")
    def on_actionCombineSelected_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        filter = []
        for selected in self.tableView.selectedIndexes():
            
            if selected.row() not in filter:
                filter.append(selected.row())
            else:
                break
        self.parent.combineWidget.init(self.parent.combineModel, parent = self.parent)
        if len(filter) == 0:
            filter = None
        self.parent.combineModel.appendModel(self.model, filter)
