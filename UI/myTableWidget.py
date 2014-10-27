# coding:utf-8
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog, QTableView
from PyQt4.QtCore import pyqtSignature,  QVariant,  QAbstractTableModel,  QModelIndex
from tableModel import MyModel
class FreezeTableWidget(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.freezeNum = 0
        
    def myInit(self,  model,  freezeNum):
        self.setModel(model)
        self.frozenTableView = QTableView(self)
        self.frozenTableView.setSortingEnabled(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.freezeNum = freezeNum
        self.init()
        
        self.connect(self.frozenTableView.horizontalHeader(), QtCore.SIGNAL("sortIndicatorChanged (int,Qt::SortOrder)"), self.fSortIndicatorChanged)
        self.connect(self.horizontalHeader(),  QtCore.SIGNAL("sortIndicatorChanged (int,Qt::SortOrder)"), self.sortIndicatorChanged)
        self.connect(self.horizontalHeader(),  QtCore.SIGNAL("sectionResized(int,int,int)"),  self.updateSectionWidth)
        self.connect(self.verticalHeader(),  QtCore.SIGNAL("sectionResized(int,int,int)"),  self.updateSectionHeight)
        self.connect(self.frozenTableView.horizontalHeader(),  QtCore.SIGNAL("sectionResized(int,int,int)"),  self.a)
        self.connect(self.frozenTableView.verticalHeader(),  QtCore.SIGNAL("sectionResized(int,int,int)"),  self.b)
        self.connect(self.frozenTableView.verticalScrollBar(),  QtCore.SIGNAL("valueChanged(int)"),  self.verticalScrollBar().setValue)
        self.connect(self.verticalScrollBar(),  QtCore.SIGNAL("valueChanged(int)"),  self.frozenTableView.verticalScrollBar().setValue)
    
    def fSortIndicatorChanged(self, index, sortOrder):
        if index < self.freezeNum:
            self.frozenTableView.horizontalHeader().setSortIndicatorShown(True)
            self.horizontalHeader().setSortIndicatorShown(False)
    
    def sortIndicatorChanged(self,  index,  sortOrder):
        if index >= self.freezeNum:
            self.frozenTableView.horizontalHeader().setSortIndicatorShown(False)
            self.horizontalHeader().setSortIndicatorShown(True)
        
    def init(self):
        
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

        self.updateFrozenTableGeometry();

        self.setHorizontalScrollMode(self.ScrollPerPixel);
        self.setVerticalScrollMode(self.ScrollPerPixel);
        self.frozenTableView.setVerticalScrollMode(self.ScrollPerPixel)
        
    def a(self, logicalIndex, a, newSize):
        self.setColumnWidth(logicalIndex,newSize);
        self.updateFrozenTableGeometry()
    def b(self, logicalIndex, a, newSize):
        self.setRowHeight(logicalIndex,  newSize)
    def updateSectionWidth(self, logicalIndex, a, newSize):
        #if logicalIndex==0 or logicalIndex == 1:
        self.frozenTableView.setColumnWidth(logicalIndex,newSize);
        self.updateFrozenTableGeometry()
    
    def updateSectionHeight(self,  logicalIndex, a, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize);

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
        self.frozenTableView.setGeometry( self.verticalHeader().width()+self.frameWidth(),  \
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

    tableView = FreezeTableWidget(model, 3);
    tableView.setWindowTitle("Frozen Column Example");
    tableView.resize(560,680)
    tableView.show()
    sys.exit(app.exec_())
