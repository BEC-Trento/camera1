# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camdisplaydockwidget.ui'
#
# Created: Sun May 28 15:00:01 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from PySide import QtCore, QtGui

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(793, 493)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.inputWidget = QtGui.QWidget(self.dockWidgetContents)
        self.inputWidget.setObjectName("inputWidget")
        self.formLayout = QtGui.QFormLayout(self.inputWidget)
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.numberOfFramesLabel = QtGui.QLabel(self.inputWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberOfFramesLabel.sizePolicy().hasHeightForWidth())
        self.numberOfFramesLabel.setSizePolicy(sizePolicy)
        self.numberOfFramesLabel.setMinimumSize(QtCore.QSize(500, 0))
        self.numberOfFramesLabel.setObjectName("numberOfFramesLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.numberOfFramesLabel)
        self.numberOfFramesSpinBox = QtGui.QSpinBox(self.inputWidget)
        self.numberOfFramesSpinBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.numberOfFramesSpinBox.setSuffix("")
        self.numberOfFramesSpinBox.setProperty("value", 4)
        self.numberOfFramesSpinBox.setObjectName("numberOfFramesSpinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.numberOfFramesSpinBox)
        self.setBackgroundFrameLabel = QtGui.QLabel(self.inputWidget)
        self.setBackgroundFrameLabel.setObjectName("setBackgroundFrameLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.setBackgroundFrameLabel)
        self.setBackgroundFrameSpinBox = QtGui.QSpinBox(self.inputWidget)
        self.setBackgroundFrameSpinBox.setProperty("value", 2)
        self.setBackgroundFrameSpinBox.setObjectName("setBackgroundFrameSpinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.setBackgroundFrameSpinBox)
        self.gridLayout.addWidget(self.inputWidget, 0, 3, 1, 1)
        self.horizontalLine = QtGui.QFrame(self.dockWidgetContents)
        self.horizontalLine.setFrameShape(QtGui.QFrame.HLine)
        self.horizontalLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.horizontalLine.setObjectName("horizontalLine")
        self.gridLayout.addWidget(self.horizontalLine, 1, 2, 1, 2)
        self.odWidget = OdQWidget(self.dockWidgetContents)
        self.odWidget.setObjectName("odWidget")
        self.odLayout = QtGui.QVBoxLayout(self.odWidget)
        self.odLayout.setObjectName("odLayout")
        self.gridLayout.addWidget(self.odWidget, 2, 3, 1, 1)
        self.framesWidget = FramesQWidget(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.framesWidget.sizePolicy().hasHeightForWidth())
        self.framesWidget.setSizePolicy(sizePolicy)
        self.framesWidget.setObjectName("framesWidget")
        self.framesGridLayout = QtGui.QGridLayout(self.framesWidget)
        self.framesGridLayout.setObjectName("framesGridLayout")
        self.plotFrameBLabel = QtGui.QLabel(self.framesWidget)
        self.plotFrameBLabel.setObjectName("plotFrameBLabel")
        self.framesGridLayout.addWidget(self.plotFrameBLabel, 2, 0, 1, 1)
        self.plotFrameALabel = QtGui.QLabel(self.framesWidget)
        self.plotFrameALabel.setObjectName("plotFrameALabel")
        self.framesGridLayout.addWidget(self.plotFrameALabel, 0, 0, 1, 1)
        self.plotFrameBSpinBox = QtGui.QSpinBox(self.framesWidget)
        self.plotFrameBSpinBox.setObjectName("plotFrameBSpinBox")
        self.framesGridLayout.addWidget(self.plotFrameBSpinBox, 2, 1, 1, 1)
        self.verticalLayoutB = QtGui.QVBoxLayout()
        self.verticalLayoutB.setObjectName("verticalLayoutB")
        self.framesGridLayout.addLayout(self.verticalLayoutB, 3, 0, 1, 2)
        self.plotFrameASpinBox = QtGui.QSpinBox(self.framesWidget)
        self.plotFrameASpinBox.setObjectName("plotFrameASpinBox")
        self.framesGridLayout.addWidget(self.plotFrameASpinBox, 0, 1, 1, 1)
        self.verticalLayoutA = QtGui.QVBoxLayout()
        self.verticalLayoutA.setObjectName("verticalLayoutA")
        self.framesGridLayout.addLayout(self.verticalLayoutA, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.framesWidget, 0, 0, 3, 1)
        self.verticalLine = QtGui.QFrame(self.dockWidgetContents)
        self.verticalLine.setFrameShape(QtGui.QFrame.VLine)
        self.verticalLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.verticalLine.setObjectName("verticalLine")
        self.gridLayout.addWidget(self.verticalLine, 0, 1, 3, 2)
        self.gridLayout.setRowStretch(2, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QtGui.QApplication.translate("DockWidget", "DockWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.numberOfFramesLabel.setText(QtGui.QApplication.translate("DockWidget", "Number of frames", None, QtGui.QApplication.UnicodeUTF8))
        self.setBackgroundFrameLabel.setText(QtGui.QApplication.translate("DockWidget", "Set background frame", None, QtGui.QApplication.UnicodeUTF8))
        self.plotFrameBLabel.setText(QtGui.QApplication.translate("DockWidget", "Plot frame B", None, QtGui.QApplication.UnicodeUTF8))
        self.plotFrameALabel.setText(QtGui.QApplication.translate("DockWidget", "Plot frame A", None, QtGui.QApplication.UnicodeUTF8))

from libraries.framesqwidget import FramesQWidget
from libraries.odqwidget import OdQWidget
