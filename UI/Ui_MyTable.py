# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\workspace\eric4\stockUI\UI\MyTable.ui'
#
# Created: Fri Sep 19 00:10:21 2014
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
        self.headBtn = QtGui.QPushButton(Form)
        self.headBtn.setMaximumSize(QtCore.QSize(30, 16777215))
        self.headBtn.setObjectName(_fromUtf8("headBtn"))
        self.horizontalLayout_16.addWidget(self.headBtn)
        self.preBtn = QtGui.QPushButton(Form)
        self.preBtn.setMaximumSize(QtCore.QSize(30, 16777215))
        self.preBtn.setObjectName(_fromUtf8("preBtn"))
        self.horizontalLayout_16.addWidget(self.preBtn)
        self.curPageLabel = QtGui.QLabel(Form)
        self.curPageLabel.setObjectName(_fromUtf8("curPageLabel"))
        self.horizontalLayout_16.addWidget(self.curPageLabel)
        self.nextBtn = QtGui.QPushButton(Form)
        self.nextBtn.setMaximumSize(QtCore.QSize(30, 16777215))
        self.nextBtn.setObjectName(_fromUtf8("nextBtn"))
        self.horizontalLayout_16.addWidget(self.nextBtn)
        self.lastBtn = QtGui.QPushButton(Form)
        self.lastBtn.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lastBtn.setObjectName(_fromUtf8("lastBtn"))
        self.horizontalLayout_16.addWidget(self.lastBtn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_16)
        self.actionDump = QtGui.QAction(Form)
        self.actionDump.setObjectName(_fromUtf8("actionDump"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.headBtn.setText(QtGui.QApplication.translate("Form", "首页", None, QtGui.QApplication.UnicodeUTF8))
        self.preBtn.setText(QtGui.QApplication.translate("Form", "上页", None, QtGui.QApplication.UnicodeUTF8))
        self.curPageLabel.setText(QtGui.QApplication.translate("Form", "0/0", None, QtGui.QApplication.UnicodeUTF8))
        self.nextBtn.setText(QtGui.QApplication.translate("Form", "下页", None, QtGui.QApplication.UnicodeUTF8))
        self.lastBtn.setText(QtGui.QApplication.translate("Form", "尾页", None, QtGui.QApplication.UnicodeUTF8))
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

