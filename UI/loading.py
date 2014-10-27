# -*- coding: utf-8 -*-

"""
Module implementing ChooseId.
"""

from PyQt4 import QtCore
from PyQt4.QtGui import QDialog, QTableWidgetItem,  QMessageBox,  QLabel,  QMovie
from PyQt4.QtCore import pyqtSignature,  SIGNAL
import resource_rc

class Loading(QDialog):
    """
    Class documentation goes here.
    """
    
    def __init__(self, parent = None):
        """
        
        Constructor
        """
        QDialog.__init__(self, parent)
        
        label = QLabel(self);  
        self.setFixedSize(100,100);  
        #self.setWindowOpacity(0.5)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True);
        self.setWindowFlags(QtCore.Qt.Dialog|QtCore.Qt.FramelessWindowHint  );  
  
        self.connect(self,  SIGNAL("finished()"),  self.close)
        self.setContentsMargins(0,0,0,0);  
        movie = QMovie(':/image/ajax-loader.gif');  
        label.setMovie(movie);  
        movie.start();  
   

if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    d = Loading()
    d.show()
    sys.exit(app.exec_())
    
    
        #raise NotImplementedError
