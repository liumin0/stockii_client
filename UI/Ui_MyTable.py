# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\WorkSpace\eric4\stockii\stockii_client\UI\MyTable.ui'
#
# Created: Sun Dec 07 17:51:03 2014
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

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
        self.clearBtn = QtGui.QPushButton(Form)
        self.clearBtn.setObjectName(_fromUtf8("clearBtn"))
        self.horizontalLayout_16.addWidget(self.clearBtn)
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
        self.actionDumpSelected = QtGui.QAction(Form)
        self.actionDumpSelected.setObjectName(_fromUtf8("actionDumpSelected"))
        self.actionCombineSelected = QtGui.QAction(Form)
        self.actionCombineSelected.setObjectName(_fromUtf8("actionCombineSelected"))
        self.actionCombine = QtGui.QAction(Form)
        self.actionCombine.setObjectName(_fromUtf8("actionCombine"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.clearBtn.setText(_translate("Form", "清除", None))
        self.showMoreBtn.setText(_translate("Form", "显示更多", None))
        self.curPageLabel.setText(_translate("Form", "0/0", None))
        self.showAllBtn.setText(_translate("Form", "显示全部", None))
        self.actionDump.setText(_translate("Form", "导出本页", None))
        self.actionDumpSelected.setText(_translate("Form", "导出选中内容", None))
        self.actionCombineSelected.setText(_translate("Form", "拼接所选", None))
        self.actionCombine.setText(_translate("Form", "拼接本页", None))

from freezetablewidget import FreezeTableWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

