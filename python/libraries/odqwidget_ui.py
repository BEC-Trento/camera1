# -*- coding: utf-8 -*-
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import Qt

import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
#from matplotlib.figure import Figure



from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    
    
    
class OdQWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(OdQWidget, self).__init__(*args, **kwargs)

    
    def setupUi(self,):
        self.figure, self.axes = plt.subplots(1,1, figsize=(9,6))
#        self.figure = Figure()
#        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlim(0,1)
        self.axes.set_ylim(0,1)
        self.axes.plot(np.random.rand(10))
        self.figure.set_facecolor('none')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.parentWidget().odLayout.addWidget(self.canvas)
        self.parentWidget().odLayout.addWidget(self.toolbar)
        self.canvas.draw()