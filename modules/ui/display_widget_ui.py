# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/fitter_widget_dock.ui'
#
# Created: Sun Mar  5 12:20:27 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DisplayWidget(object):
    def setupUi(self, DisplayWidget):
        DisplayWidget.setObjectName("DisplayWidget")
#        DisplayWidget.resize(805, 642)
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DisplayWidget.sizePolicy().hasHeightForWidth())
        DisplayWidget.setSizePolicy(sizePolicy)
        
        DisplayWidget.setObjectName("DockWidgetContents")
        self.gridLayout = QtGui.QGridLayout(DisplayWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.histogram = HistogramLUTWidget(DisplayWidget)
        self.histogram.setObjectName("histogram")
        self.gridLayout.addWidget(self.histogram, 0, 2, 1, 1)
        self.graphicsView = GraphicsView(DisplayWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 1, 1, 1)
        self.yPlotWidget = PlotWidget(DisplayWidget)
        self.yPlotWidget.setObjectName("yPlotWidget")
        self.gridLayout.addWidget(self.yPlotWidget, 0, 0, 1, 1)
        self.xPlotWidget = PlotWidget(DisplayWidget)
        self.xPlotWidget.setObjectName("xPlotWidget")
        self.gridLayout.addWidget(self.xPlotWidget, 1, 1, 1, 1)
        self.glayout = QtGui.QGridLayout(DisplayWidget)
        self.gridLayout.addLayout(self.glayout, 1, 2, 1, 1)
        
        self.viewProjCheckBox = QtGui.QCheckBox(DisplayWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DisplayWidget.sizePolicy().hasHeightForWidth())
        self.viewProjCheckBox.setSizePolicy(sizePolicy)
        self.viewProjCheckBox.setText("View xy proj.")
        self.viewProjCheckBox.setIconSize(QtCore.QSize(24, 24))
        self.viewProjCheckBox.setChecked(False)
        self.viewProjCheckBox.setObjectName("viewProjCheckBox")
        self.on_toggle_proj()
        self.viewProjCheckBox.stateChanged.connect(self.on_toggle_proj)
        self.glayout.addWidget(self.viewProjCheckBox, 0, 0, 1, 2)
        
        self.cmapLabel = QtGui.QLabel('Colormap', DisplayWidget)
        self.glayout.addWidget(self.cmapLabel, 1, 0, 1, 1)
        self.cmapComboBox = QtGui.QComboBox(DisplayWidget)
        self.glayout.addWidget(self.cmapComboBox, 1, 1, 1, 1)
        
        
        
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(0, 3)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(DisplayWidget)
        QtCore.QMetaObject.connectSlotsByName(DisplayWidget)
        
    def on_toggle_proj(self,):
        self.xPlotWidget.setVisible(self.viewProjCheckBox.isChecked())
        self.yPlotWidget.setVisible(self.viewProjCheckBox.isChecked())

    def retranslateUi(self, DisplayWidget):
        DisplayWidget.setWindowTitle(QtGui.QApplication.translate("DisplayWidget", "Display image", None, QtGui.QApplication.UnicodeUTF8))

from pyqtgraph import HistogramLUTWidget, GraphicsView, PlotWidget
