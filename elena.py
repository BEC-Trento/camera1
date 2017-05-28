#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:27:57 2016

@author: carmelo
"""
import os
from PySide import QtGui

from libraries.mainwindow_ui import Ui_MainWindow

import matplotlib
from matplotlib.pyplot import colorbar
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
        self.handler = MyHandler(self.params, setMainWindow=self)
        self.functions = {'Picture 4 frames': ('make_Picture_NaK_4_CAM', 4),
                          'Picture 2 frames': ('make_Picture_NaK_2_manual', 2),
                          'Picture single frame': ('make_Picture_single_frame', 1)}
        
#        self.cloner = Observer()
#        self.cloner_source = os.path.join(os.getcwd(), 'raw')
#        self.cloner.schedule(HandlerCloner(), path=str(self.cloner_source))
#        print('cloner scheduled on ', self.cloner_source)
#        self.cloner.start()
        
        self.setupUi(self)
        self.destinationLineEdit = QtGui.QLineEdit(self.inputWidget)
        self.destinationLineEdit.setObjectName("destinationLineEdit")
        self.formLayout.insertRow(0, "Sis file", self.destinationLineEdit)
        self.destinationLineEdit.setText(os.path.join(self.params.writesis_dest, self.params.sisname))
        self.nunberOfFramesNumLabel.setProperty("value", self.params.initNumberOfFrames)
        
        self.selectFunctions = QtGui.QComboBox(self.inputWidget)
        self.selectFunctions.addItems(list(self.functions.keys()))
        self.selectFunctions.setObjectName("selectFunctions")
        self.formLayout.insertRow(2, "Function", self.selectFunctions)        
        
        self.deleteButton = QtGui.QPushButton(self.inputWidget)
        self.deleteButton.setObjectName('deleteButton')
        self.formLayout.insertRow(5, "Delete Raw", self.deleteButton)
        self.deleteButton.setCheckable(True)
        self.deleteButton.setChecked(True)
        self.deleteButton.setText('Yes')
        
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
        
    def on_toggleDeleteButton(self,):
        if self.deleteButton.isChecked():
            self.deleteButton.setText('Yes')
        else:
            self.deleteButton.setText('No')
        pass
        
        
    def connectActions(self):
        self.actionInfo.triggered.connect(self.infoBox)
        self.actionRefresh.triggered.connect(self.plotAcquired)
        self.deleteButton.toggled.connect(self.on_toggleDeleteButton)
        
    def connectInputWidget(self):
        self.selectFunctions.currentIndexChanged.connect(self.setMaxima)
        self.plotFrameASpinBox.valueChanged.connect(self.refreshFrames)
        self.plotFrameBSpinBox.valueChanged.connect(self.refreshFrames)
        self.sourceFolderLineEdit.editingFinished.connect(
            lambda: self.observerReboot(path=self.sourceFolderLineEdit.text())) 
    
    def observerReboot(self, path=None, func='Picture 4 frames'):
        funct, maxf = self.functions[func]
        self.nunberOfFramesNumLabel.setText(str(maxf))
        if self.observer is not None:
#            self.observer.join()
            self.observer.stop()
            print('observer stopped')
        self.params.source = path
        self.observer = Observer()
        self.handler = MyHandler(self.params, setMainWindow=self)
        self.handler.created_last = getattr(self.handler, funct)
        self.handler.max_frames = maxf
        self.observer.schedule(self.handler, path=str(path))
        print('observer scheduled on ', path)
        self.observer.start()


    def setMaxima(self,):
        self.framesNumber = self.functions[self.selectFunctions.currentText()][1]
        self.plotFrameASpinBox.setMaximum(self.framesNumber)
        self.plotFrameBSpinBox.setMaximum(self.framesNumber)
        self.observerReboot(func=self.selectFunctions.currentText(), path=self.sourceFolderLineEdit.text())
        
    def resetLists(self,):
        self.framesPathList = []
        self.framesHeaderList = []
        self.framesImageList = []
        
    def infoBox(self,):
        QtGui.QMessageBox.about(self, PROG_NAME, PROG_COMMENT+'\n v. '+PROG_VERSION)
        
    def refreshOd(self,):
        self.odWidget.axes.cla()
        i = self.odWidget.axes.imshow(self.currentImage, **self.odWidget.imshow_kwargs)
        colorbar(i, cax=self.odWidget.cax, **self.odWidget.kk)
        self.odWidget.canvas.draw()
        
    def refreshFrames(self,):
        if len(self.framesImageList) == 0:
            print('No list')
        else:
            print(len(self.framesImageList))
            print('refreshing')
            for ax in self.framesWidget.axes:
                ax.cla()
                ax.set(xticks=[], yticks=[])
            self.framesWidget.axesA.imshow(self.framesImageList[self.plotFrameASpinBox.value()-1], **self.framesWidget.imshow_kwargs)
            self.framesWidget.axesB.imshow(self.framesImageList[self.plotFrameBSpinBox.value()-1], **self.framesWidget.imshow_kwargs)
            self.framesWidget.canvas.draw()
            
    def plotAcquired(self,):
        self.refreshFrames()
        self.refreshOd()


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

