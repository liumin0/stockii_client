# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
#from stock import Form
#from StockUI import MainWindow
sys.path.append('UI')
from StockMain import StockMain
import atexit
import os
import resource_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/image/icon.ico"))
    
    splash = QtGui.QSplashScreen()  
    curDir = os.path.dirname( sys.path[0])
#    print curDir
#    print os.path.join(curDir, 'stockii.jpg')
#    splash.setPixmap(QtGui.QPixmap(os.path.join(curDir, 'stockii.jpg')));  
    splash.setPixmap(QtGui.QPixmap(':/image/stockii.jpg'));  

    splash.show();  
    splash.showMessage(u"连接服务器...", QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    ui = StockMain()
    ui.show()
    splash.finish(ui);  
    sys.exit(app.exec_())
