#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:27:57 2016

@author: carmelo
"""

from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import Qt
from libraries.mainWindow_ui import Ui_MainWindow

import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt

from watchdog.observers import Observer
from libraries.fileWatch import MyHandler

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    

class NavigationToolbarShort(NavigationToolbar):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        self.connectActions()
        self.connectButtons()
        self.setupFramesFigures()
        self.setupOdFigures()
        
    def connectActions(self):
        self.actionInfo.triggered.connect(self.infoBox)
        self.actionRefresh.triggered.connect(self.refreshOdPlot)
        self.actionToggleFramesDock = self.framesDockWidget.toggleViewAction()
        self.menuView.addAction(self.actionToggleFramesDock)
        
    def connectButtons(self):
        pass    
    
    def setupFramesFigures(self,):
        self.framesFigure, self.framesAxes = plt.subplots(4,1, figsize=(2,6), sharex=True)
        for ax in self.framesAxes:
            ax.set_xticks([])
            ax.set_yticks([])
            ax.plot(np.random.rand(5))
        self.framesFigure.set_facecolor('none')
        self.framesCanvas = FigureCanvas(self.framesFigure)
        self.framesToolbar = NavigationToolbarShort(self.framesCanvas, self.framesWidget, coordinates=True)
        self.framesToolbar.setOrientation(Qt.Horizontal)
        self.framesLayout.addWidget(self.framesCanvas)
        self.framesLayout.addWidget(self.framesToolbar)
        self.framesCanvas.draw()
                
    def setupOdFigures(self,):
        self.odFigure, self.odAxes = plt.subplots(1,1)
        self.odAxes.plot(np.random.rand(10))
        self.odFigure.set_facecolor('none')
        self.odCanvas = FigureCanvas(self.odFigure)
        self.odToolbar = NavigationToolbar(self.odCanvas, self.odWidget, coordinates=True)
        self.odToolbar.setOrientation(Qt.Horizontal)
        self.odLayout.addWidget(self.odCanvas)
        self.odLayout.addWidget(self.odToolbar)
        self.odCanvas.draw()
        
    def infoBox(self,):
        QtGui.QMessageBox.about(self, 'ELENA', 'Eliminate LabVIEW for an Enhanced New Acquisition system\n v. 0.1')
        
    def refreshOdPlot(self,):
        self.odAxes.cla()
        self.odAxes.plot(np.random.rand(10))
        self.odCanvas.draw()
        
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui    

    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    
    observer = Observer()
    observer.schedule(MyHandler(), path=checkPath)
    observer.start()
    status = app.exec_()
    observer.stop()
    observer.join()
    sys.exit(status)

