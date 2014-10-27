# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\WorkSpace\eric4\stockii\stock\UI\xxx.ui'
#
# Created: Sun Sep 14 15:27:20 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(556, 478)
        self.widget = MyTable(Dialog)
        self.widget.setGeometry(QtCore.QRect(30, 40, 431, 211))
        self.widget.setObjectName(_fromUtf8("widget"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
import sys
sys.path.append('..')
from MyTable import MyTable

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

