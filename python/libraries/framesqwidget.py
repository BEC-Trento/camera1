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
        self.imshow_kwargs = {'cmap': 'gray'}
        
        self.figure, self.axes = plt.subplots(2,1,figsize=(1,4), 
                                              sharex=True, sharey=True)
        self.axesA, self.axesB = self.axes
        for ax in self.axes:
            ax.set(xticks=[], yticks=[])
            ax.plot(np.random.rand(5))
            
        self.figure.set_facecolor('none')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbarShort(self.canvas, self, coordinates=False)
        self.toolbar.setOrientation(Qt.Horizontal)
        
        self.mainWindow.framesPlotLayout.addWidget(self.canvas)
        self.mainWindow.framesPlotLayout.addWidget(self.toolbar)
        self.canvas.draw()
        

