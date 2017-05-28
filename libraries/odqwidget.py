# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
from PySide.QtGui import QWidget
from PySide.QtCore import Qt

import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
from matplotlib.colorbar import make_axes
#from matplotlib.figure import Figure



from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    
    
    
class OdQWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(OdQWidget, self).__init__(*args, **kwargs)

    
    def setupUi(self, setMainWindow):
        self.mainWindow = setMainWindow
        self.imshow_kwargs = {'cmap': 'gist_stern', }#'vmin': -0.05, 'vmax': 1.5}
        
        self.figure, self.axes = plt.subplots(1,1, figsize=(9,6))
#        self.figure = Figure()
#        self.axes = self.figure.add_subplot(111)
#        self.axes.set_xlim(0,1)
#        self.axes.set_ylim(0,1)
        self.axes.plot(np.random.rand(10))
        self.figure.set_facecolor('none')
        self.cax, self.kk = make_axes(self.axes, location='right')
        self.cax.set(xticks=[], yticks=[])
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.mainWindow.odLayout.addWidget(self.canvas)
        self.mainWindow.odLayout.addWidget(self.toolbar)
        self.canvas.draw()