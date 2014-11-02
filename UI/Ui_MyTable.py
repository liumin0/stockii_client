# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\WorkSpace\eric4\stockii\stockii_client\UI\MyTable.ui'
#
# Created: Sun Nov 02 11:13:46 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(593, 337)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView = FreezeTableWidget(Form)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem)
        self.showMoreBtn = QtGui.QPushButton(Form)
        self.showMoreBtn.setObjectName(_fromUtf8("showMoreBtn"))
        self.horizontalLayout_16.addWidget(self.showMoreBtn)
        self.curPageLabel = QtGui.QLabel(Form)
        self.curPageLabel.setObjectName(_fromUtf8("curPageLabel"))
        self.horizontalLayout_16.addWidget(self.curPageLabel)
        self.showAllBtn = QtGui.QPushButton(Form)
        self.showAllBtn.setObjectName(_fromUtf8("showAllBtn"))
        self.horizontalLayout_16.addWidget(self.showAllBtn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_16)
        self.actionDump = QtGui.QAction(Form)
        self.actionDump.setObjectName(_fromUtf8("actionDump"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.showMoreBtn.setText(QtGui.QApplication.translate("Form", "显示更多", None, QtGui.QApplication.UnicodeUTF8))
        self.curPageLabel.setText(QtGui.QApplication.translate("Form", "0/0", None, QtGui.QApplication.UnicodeUTF8))
        self.showAllBtn.setText(QtGui.QApplication.translate("Form", "显示全部", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDump.setText(QtGui.QApplication.translate("Form", "导出本页", None, QtGui.QApplication.UnicodeUTF8))

from freezetablewidget import FreezeTableWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

