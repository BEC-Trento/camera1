# -*- coding: utf-8 -*-
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import Qt

import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt


from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    
    
class NavigationToolbarShort(NavigationToolbar):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]

    
class FramesQWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(FramesQWidget, self).__init__(*args, **kwargs)

    
    def setupUi(self, setMainWindow):
        self.mainWindow = setMainWindow
        
        self.figureA, self.axesA = plt.subplots(1,1,figsize=(1,4))
        self.axesA.set(xticks=[], yticks=[])
        self.figureA.set_facecolor('none')
        self.canvasA = FigureCanvas(self.figureA)
        self.toolbarA = NavigationToolbarShort(self.canvasA, self, coordinates=False)
        self.toolbarA.setOrientation(Qt.Horizontal)
        
        self.mainWindow.verticalLayoutA.addWidget(self.canvasA)
        self.mainWindow.verticalLayoutA.addWidget(self.toolbarA)
        self.axesA.plot(np.random.rand(5), 'b')
        self.canvasA.draw()
        
        self.figureB, self.axesB = plt.subplots(1,1,figsize=(1,4))
        self.axesB.set(xticks=[], yticks=[])
        self.figureB.set_facecolor('none')
        self.canvasB = FigureCanvas(self.figureB)
        self.toolbarB = NavigationToolbarShort(self.canvasB, self, coordinates=False)
        self.toolbarB.setOrientation(Qt.Horizontal)
        self.mainWindow.verticalLayoutB.addWidget(self.canvasB)
        self.mainWindow.verticalLayoutB.addWidget(self.toolbarB)
        self.axesB.plot(np.random.rand(5))
        self.canvasB.draw()
        
        self.axes = [self.axesA, self.axesB]

