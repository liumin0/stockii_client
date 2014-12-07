# coding:utf-8
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog, QTableView
from PyQt4.QtCore import pyqtSignature,  QVariant,  QAbstractTableModel,  QModelIndex
#from tableModel import MyModel
from log import log
class FreezeTableWidget(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.freezeNum = 0
        self.inited = False
        self.frozenTableView = QTableView(self)
    
    def columnCountChanged (self, old, new):
        log('columnCountChanged',  old,  new)

    def setSetting(self,  setting):
        if self.inited and setting is not None:
            if 'freezeNum' in setting:
                self.setFreezeNum(setting['freezeNum'])
            if 'hideColumns' in setting:
                for col in range(self.model().columnCount()):
                    if col in setting['hideColumns']:
                        self.hideColumn(col)
                    else:
                        self.showColumn(col)
            if 'hideRows' in setting:
                for row in range(self.model().rowCount()):
                    if row in setting['hideRows']:
                        self.hideRow(row)
                    else:
                        self.showRow(row)
            
    def setFreezeNum(self,  num):
        self.resizeColumnsToContents()
        for col in range(num):
            self.frozenTableView.setColumnHidden(col, False)
            if not self.isColumnHidden(col):
                width = self.columnWidth(col)
#                    log('width:', col,  width)
                if width != 0:
                    self.frozenTableView.setColumnWidth(col, width)
#            self.setColumnHidden(col, False)

        for col in range(num,  self.model().columnCount()):
            if not self.frozenTableView.isColumnHidden(col):
#                self.resizeColumnToContents(col)
                width = self.frozenTableView.columnWidth(col)
                self.frozenTableView.setColumnHidden(col, True)
                if width != 0:
                    self.setColumnWidth(col, width)
            else:
                self.frozenTableView.setColumnHidden(col, True)

        #self.viewport().update()
        self.freezeNum = num
        #self.frozenTableView.viewport().stackUnder(self)
        #self.raise_()
        #self.viewport().stackUnder(self.frozenTableView);
        self.updateFrozenTableGeometry()

        
#        self.resizeColumnsToContents()
    
    def myInit(self,  model,  freezeNum):
        self.inited = True
        
        
        self.frozenTableView.setSortingEnabled(True)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers);
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.setModel(model)
        self.setAlternatingRowColors(True)
        self.freezeNum = freezeNum
        self.frozenTableView.setModel(self.model());
        self.frozenTableView.setFocusPolicy(QtCore.Qt.NoFocus);
        self.frozenTableView.verticalHeader().hide();
        #self.frozenTableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed);

        self.viewport().stackUnder(self.frozenTableView);
        
        self.frozenTableView.setStyleSheet("QTableView { border: none;"
                                     "background-color: #8EDE21;"
                                     "selection-background-color: #999}"); 
        self.frozenTableView.setSelectionModel(self.selectionModel())
        self.frozenTableView.setSelectionMode(self.selectionMode())
        self.frozenTableView.setSelectionBehavior(self.selectionBehavior())
        for col in range(self.freezeNum, self.model().columnCount()):
            self.frozenTableView.setColumnHidden(col, True)
        
        for i in range(self.freezeNum):
            self.frozenTableView.setColumnWidth(self.freezeNum, self.columnWidth(self.freezeNum) )
        self.frozenTableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff);
        self.frozenTableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff);
        self.frozenTableView.show();

        

        self.setHorizontalScrollMode(self.ScrollPerItem);
        self.setVerticalScrollMode(self.ScrollPerItem);
        self.frozenTableView.setVerticalScrollMode(self.ScrollPerItem)
        
        self.connect(self.frozenTableView.horizontalHeader(), QtCore.SIGNAL("sortIndicatorChanged (int,Qt::SortOrder)"), self.fSortIndicatorChanged)
        self.connect(self.horizontalHeader(),  QtCore.SIGNAL("sortIndicatorChanged (int,Qt::SortOrder)"), self.sortIndicatorChanged)
        self.connect(self.horizontalHeader(),  QtCore.SIGNAL("sectionResized(int,int,int)"),  self.updateSectionWidth)
        self.connect(self.verticalHeader(),  QtCore.SIGNAL("sectionResized(int,int,int)"),  self.updateSectionHeight)
        self.connect(self.frozenTableView.horizontalHeader(),  QtCore.SIGNAL("sectionResized(int,int,int)"),  self.updateColumn)
        self.connect(self.frozenTableView.verticalHeader(),  QtCore.SIGNAL("sectionResized(int,int,int)"),  self.updateRow)
        self.connect(self.frozenTableView.verticalScrollBar(),  QtCore.SIGNAL("valueChanged(int)"),  self.verticalScrollBar().setValue)
        self.connect(self.verticalScrollBar(),  QtCore.SIGNAL("valueChanged(int)"),  self.frozenTableView.verticalScrollBar().setValue)
        
        
        self.resizeColumnsToContents()
        self.updateFrozenTableGeometry();
            
    def fSortIndicatorChanged(self, index, sortOrder):
        if index < self.freezeNum:
            self.frozenTableView.horizontalHeader().setSortIndicatorShown(True)
            self.horizontalHeader().setSortIndicatorShown(False)
    
    def sortIndicatorChanged(self,  index,  sortOrder):
        if index >= self.freezeNum:
            self.frozenTableView.horizontalHeader().setSortIndicatorShown(False)
            self.horizontalHeader().setSortIndicatorShown(True)

    def updateColumn(self, logicalIndex, a, newSize):
        self.setColumnWidth(logicalIndex,newSize);
        self.updateFrozenTableGeometry()
        
    def updateRow(self, logicalIndex, a, newSize):
        self.setRowHeight(logicalIndex,  newSize)
        
        
    def updateSectionWidth(self, logicalIndex, a, newSize):
        #if logicalIndex==0 or logicalIndex == 1:
        self.frozenTableView.setColumnWidth(logicalIndex,newSize);
        self.updateFrozenTableGeometry()
    
    def updateSectionHeight(self,  logicalIndex, a, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize);
        self.updateFrozenTableGeometry()
        
    def resizeEvent(self,  event):
        pass
        QTableView.resizeEvent(self, event);
        self.updateFrozenTableGeometry()
        
    def moveCursor(self,  cursorAction,  modifiers):
        pass
        current = QTableView.moveCursor(self,  cursorAction, modifiers);

        if cursorAction == self.MoveLeft and current.column()>0 \
         and self.visualRect(current).topLeft().x() < self.frozenTableView.columnWidth(0):

            newValue = self.horizontalScrollBar().value() + self.visualRect(current).topLeft().x() - self.frozenTableView.columnWidth(0)
            self.horizontalScrollBar().setValue(newValue)
        return current
        
#    def scrollTo(self,  index,  hint):
#        pass
#        #if(index.column()>0):
#        print 'here'
        #QTableView.scrollTo(self,  index, hint)
            
    def updateFrozenTableGeometry(self):

        
        width = 0
        for i in range(self.freezeNum):
            width += self.columnWidth(i)
        self.frozenTableView.setGeometry(self.verticalHeader().sizeHint().width()+self.frameWidth(),  \
                                    self.frameWidth(), width,
                                    self.viewport().height()+self.horizontalHeader().height())

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    model = MyModel()#QtGui.QStandardItemModel()
    #model.setHorizontalHeaderLabels([u"aa", u"bb", u"test", u"sxxxx", u"12345"])
#    for i in range(50):
#        for j in range(50):
#            newItem = QtGui.QStandardItem(QtCore.QString(i+j))
#            model.setItem(i ,j, newItem)

    tableView = FreezeTableWidget();
    tableView.myInit(model,  2)
    tableView.setWindowTitle("Frozen Column Example");
    tableView.resize(560,680)
    tableView.show()
    sys.exit(app.exec_())
