#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:27:57 2016

@author: carmelo
"""
from PyQt4 import QtGui

from libraries.mainwindow_ui import Ui_MainWindow

import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')


from watchdog.observers import Observer
from libraries.fileWatch import MyHandler, Params

PROG_NAME = 'ELENA'
PROG_COMMENT = 'Eliminate LabVIEW for an Enhanced New Acquisition system'
PROG_VERSION = '0.9 (beta)'


class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.params = Params()
        self.observer = None
        
        self.setupUi(self)
        self.setWindowTitle(PROG_NAME+' '+PROG_VERSION)
        self.odWidget.setupUi(self)
        self.framesWidget.setupUi(self)
        
        self.connectActions()
        self.connectInputWidget()
        
        self.framesPathList = []
        self.framesHeaderList = []
        self.framesImageList = []
        self.currentImage = None
        self.sourceFolderLineEdit.setText(self.params.source)
        self.setMaxima()
        
        
        
    def connectActions(self):
        self.actionInfo.triggered.connect(self.infoBox)
        self.actionRefresh.triggered.connect(self.refreshPlots)
        
    def connectInputWidget(self):
        self.numberOfFramesSpinBox.valueChanged.connect(self.setMaxima)
        self.sourceFolderLineEdit.editingFinished.connect(
            lambda: self.observerReboot(self.sourceFolderLineEdit.text())) 
    
    def observerReboot(self, path=None):
        if self.observer is not None:
#            self.observer.join()
            self.observer.stop()
            print('observer stopped')
        self.params.source = path
        self.observer = Observer()
        self.observer.schedule(MyHandler(self.params, setMainWindow=self), path=path)
        print('observer scheduled on ', path)
        self.observer.start()


    def setMaxima(self,):
        self.framesNumber = self.numberOfFramesSpinBox.value()
        self.plotFrameASpinBox.setMaximum(self.framesNumber)
        self.plotFrameBSpinBox.setMaximum(self.framesNumber)
        self.setBackgroundFrameSpinBox.setMaximum(self.framesNumber)
        self.observerReboot(self.sourceFolderLineEdit.text())
        
    def resetLists(self,):
        self.framesPathList = []
        self.framesHeaderList = []
        self.framesImageList = []
        
    def infoBox(self,):
        QtGui.QMessageBox.about(self, PROG_NAME, PROG_COMMENT+'\n v. '+PROG_VERSION)
        
    def refreshPlots(self,):
        for ax in self.framesWidget.axes:
            ax.cla()
            ax.set(xticks=[], yticks=[])
            ax.plot(np.random.rand(5))
        self.odWidget.axes.cla()
        self.odWidget.axes.plot(np.random.rand(10))
        self.framesWidget.canvas.draw()
        self.odWidget.canvas.draw()
        
    def plotAcquired(self,):
        for ax in self.framesWidget.axes:
            ax.cla()
            ax.set(xticks=[], yticks=[])
        self.framesWidget.axesA.imshow(self.framesImageList[self.plotFrameASpinBox.value()-1], **self.params.imshow_kwargs)
        self.framesWidget.axesB.imshow(self.framesImageList[self.plotFrameBSpinBox.value()-1], **self.params.imshow_kwargs)
        self.odWidget.axes.cla()
        self.odWidget.axes.imshow(self.currentImage, **self.params.imshow_kwargs)
        self.framesWidget.canvas.draw()
        self.odWidget.canvas.draw()

if __name__ == '__main__':
    import sys  

    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
#    main.observerReboot(path=main.params.source)
    status = app.exec_()
    main.observer.stop()
    main.observer.join()
    sys.exit(status)

