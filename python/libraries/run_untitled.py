#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:27:57 2016

@author: carmelo
"""

from PyQt4.uic import loadUiType
 
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


Ui_MainWindow, QMainWindow = loadUiType('untitled.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
 
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
 
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
