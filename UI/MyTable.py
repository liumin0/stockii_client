# -*- coding: utf-8 -*-

"""
Module implementing MyTable.
"""

from PyQt4 import QtCore
from PyQt4.QtGui import QWidget,  QMenu,  QFileDialog,  QProgressDialog
from PyQt4.QtCore import pyqtSignature,  SIGNAL

from Ui_MyTable import Ui_Form
import platform
import log

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
        self.modelSet = False
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
    
    def setButtonsVisible(self,  visible):
        self.headBtn.setVisible(visible)
        self.preBtn.setVisible(visible)
        self.nextBtn.setVisible(visible)
        self.lastBtn.setVisible(visible)
        self.curPageLabel.setVisible(visible)
    
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
    
    def init(self, model,  freezeNum = 0,  setting = None):
        self.setModel(model)
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
            self.connect(self.headBtn,  SIGNAL("clicked()"),  self.model.first)
            self.connect(self.preBtn,  SIGNAL("clicked()"),  self.model.up)
            self.connect(self.nextBtn,  SIGNAL("clicked()"),  self.model.down)
            self.connect(self.lastBtn,  SIGNAL("clicked()"),  self.model.last)
            self.modelSet = True
    
    def refreshIndex(self):
        self.curPageLabel.setText('%d/%d' %(self.model.page,  self.model.totalPage))
        if self.model.page == 1:
            self.preBtn.setEnabled(False)
        else:
            self.preBtn.setEnabled(True)
        
        if self.model.page== self.model.totalPage:
            self.nextBtn.setEnabled(False)
        else:
            self.nextBtn.setEnabled(True)
    
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
            menu.exec_(curPos);
    
    @pyqtSignature("")
    def on_actionDump_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        self.doExport(self.model)
    
    def doExport(self,  model):
#        print model.rowCount()
        if model.rowCount() < 1:
            QMessageBox.warning(self,'warning', "导出内容为空")
            return
        fileName = QFileDialog.getSaveFileName(self,self.tr('Save csv'),'',self.tr("*.csv"))
        if not fileName:
            return
        if platform.system() == 'Windows':
            fileName = str(fileName.toUtf8()).decode('utf-8').encode('gbk')
        else:
            fileName = str(fileName.toUtf8())
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
                    content += str(model.data(model.index(i, j))).encode('utf-8') + ','
                except:
                    content += model.data(model.index(i, j)).encode('utf-8') + ','
#                try:
#                    content += str(model.data(model.index(i, j)).toString().toUtf8())+ ','
#                except:
#                    content += str(model.data(model.index(i, j)).toUtf8())+ ','
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
