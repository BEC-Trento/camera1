#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:27:57 2016

@author: carmelo
"""
from PyQt4.QtGui import QMainWindow

from libraries.mainwindow_ui import Ui_MainWindow

import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')


from watchdog.observers import Observer
from libraries.fileWatch import MyHandler, Params

PROG_NAME = 'ELENA'
PROG_COMMENT = 'Eliminate LabVIEW for an Enhanced New Acquisition system'
PROG_VERSION = '0.1'


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(PROG_NAME+' '+PROG_VERSION)
#        self.camDisplayWidget.setupUi(self)
        self.odWidget.setupUi(self)
        self.framesWidget.setupUi(self)
        
        self.connectActions()
        self.connectButtons()
        
        self.framesList = []
        self.setMaxima()
        
        
    def connectActions(self):
        self.actionInfo.triggered.connect(self.infoBox)
        self.actionRefresh.triggered.connect(self.refreshPlots)
        
    def connectButtons(self):
        self.numberOfFramesSpinBox.valueChanged.connect(self.setMaxima)
        pass    

    def setMaxima(self,):
        self.framesNumber = self.numberOfFramesSpinBox.value()
        self.plotFrameASpinBox.setMaximum(self.framesNumber)
        self.plotFrameBSpinBox.setMaximum(self.framesNumber)
        self.setBackgroundFrameSpinBox.setMaximum(self.framesNumber)
        
    def infoBox(self,):
        QtGui.QMessageBox.about(self, PROG_NAME, PROG_COMMENT+'\n v. '+PROG_VERSION)
        
    def refreshPlots(self,):
        for ax in self.framesWidget.axes:
            ax.cla()
            ax.plot(np.random.rand(5))
        self.odWidget.axes.cla()
        self.odWidget.axes.plot(np.random.rand(10))
        self.framesWidget.canvasA.draw()
        self.framesWidget.canvasB.draw()   
        self.odWidget.canvas.draw()

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui    

    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    
    params = Params()
    observer = Observer()
    observer.schedule(MyHandler(params), path=params.source)
    observer.start()
    status = app.exec_()
    observer.stop()
    observer.join()
    sys.exit(status)

