# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

import matplotlib
matplotlib.use('Qt4Agg')
#import matplotlib.pyplot as plt
#from matplotlib.figure import Figure



#from matplotlib.backends.backend_qt4agg import (
#    FigureCanvasQTAgg as FigureCanvas,
#    NavigationToolbar2QT as NavigationToolbar)
    
    
    
class CamDisplayQWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(CamDisplayQWidget, self).__init__(*args, **kwargs)

    
    def setupUi(self, setMainWindow):
        self.mainWindow = setMainWindow