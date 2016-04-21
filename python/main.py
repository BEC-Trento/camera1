#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:27:57 2016

@author: carmelo
"""
from PyQt4.QtGui import QMainWindow

from libraries.mainWindow_ui import Ui_MainWindow

import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')


from watchdog.observers import Observer
from libraries.fileWatch import MyHandler, Params


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        self.framesDockWidget.setupUi()
        self.odWidget.setupUi()
            
        self.connectActions()
        self.connectButtons()
        
    def connectActions(self):
        self.actionInfo.triggered.connect(self.infoBox)
        self.actionRefresh.triggered.connect(self.refreshOdPlot)
        self.actionToggleFramesDock = self.framesDockWidget.toggleViewAction()
        self.menuView.addAction(self.actionToggleFramesDock)
        
    def connectButtons(self):
        pass    

        
    def infoBox(self,):
        QtGui.QMessageBox.about(self, 'ELENA', 'Eliminate LabVIEW for an Enhanced New Acquisition system\n v. 0.1')
        
    def refreshOdPlot(self,):
        for ax in self.framesDockWidget.axes:
            ax.cla()
        self.odWidget.axes.cla()
        self.odWidget.axes.plot(np.random.rand(10))
        self.framesDockWidget.canvas.draw()        
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

