#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:27:57 2016

@author: carmelo
"""

from PyQt4.QtGui import QMainWindow
from libraries.mainWindow_ui import Ui_MainWindow

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        self.connectActions()
        self.setupFigures()
        
    def connectActions(self):
        self.actionInfo.triggered.connect(self.infoBox)
    
    def setupFigures(self,):
        framesFigure, framesAxes = plt.subplots(4,1, sharex=True)
        for ax in framesAxes:
            ax.set_xticks([])
            ax.set_yticks([])
            ax.plot(np.random.rand(5))
        framesFigure.set_facecolor('none')
        self.framesCanvas = FigureCanvas(framesFigure)
        self.framesVerticalLayout.addWidget(self.framesCanvas)
        self.framesCanvas.draw()
        self.framesToolbar = NavigationToolbar(self.framesCanvas, self.framesWidget, coordinates=True)
        self.framesVerticalLayout.addWidget(self.framesToolbar)
        
    def infoBox(self,):
        QtGui.QMessageBox.about(self, 'ELENA', 'Eliminate LabVIEW for an Enhanced New Acquisition system\n v. 0.1')
        
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui    

    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
