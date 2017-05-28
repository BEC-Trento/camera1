# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camdisplaywidget.ui'
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

class Ui_camDisplayQWidget(object):
    def setupUi(self, camDisplayQWidget):
        camDisplayQWidget.setObjectName("camDisplayQWidget")
        camDisplayQWidget.resize(848, 597)
        self.gridLayout_2 = QtGui.QGridLayout(camDisplayQWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineHorizontal = QtGui.QFrame(camDisplayQWidget)
        self.lineHorizontal.setFrameShape(QtGui.QFrame.HLine)
        self.lineHorizontal.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineHorizontal.setObjectName("lineHorizontal")
        self.gridLayout_2.addWidget(self.lineHorizontal, 2, 2, 1, 1)
        self.inputWidget = QtGui.QWidget(camDisplayQWidget)
        self.inputWidget.setObjectName("inputWidget")
        self.formLayout = QtGui.QFormLayout(self.inputWidget)
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.numberOfFramesLabel = QtGui.QLabel(self.inputWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberOfFramesLabel.sizePolicy().hasHeightForWidth())
        self.numberOfFramesLabel.setSizePolicy(sizePolicy)
        self.numberOfFramesLabel.setMinimumSize(QtCore.QSize(0, 0))
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
        self.gridLayout_2.addWidget(self.inputWidget, 0, 2, 1, 1)
        self.framesWidget = QtGui.QWidget(camDisplayQWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.framesWidget.sizePolicy().hasHeightForWidth())
        self.framesWidget.setSizePolicy(sizePolicy)
        self.framesWidget.setObjectName("framesWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.framesWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2.addWidget(self.framesWidget, 0, 0, 4, 1)
        self.odWidget = QtGui.QWidget(camDisplayQWidget)
        self.odWidget.setObjectName("odWidget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.odWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton = QtGui.QPushButton(self.odWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_4.addWidget(self.pushButton)
        self.gridLayout_2.addWidget(self.odWidget, 3, 2, 1, 1)
        self.lineVertical = QtGui.QFrame(camDisplayQWidget)
        self.lineVertical.setFrameShape(QtGui.QFrame.VLine)
        self.lineVertical.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineVertical.setObjectName("lineVertical")
        self.gridLayout_2.addWidget(self.lineVertical, 0, 1, 4, 1)
        self.gridLayout_2.setColumnStretch(0, 100)
        self.gridLayout_2.setRowStretch(3, 10)

        self.retranslateUi(camDisplayQWidget)
        QtCore.QMetaObject.connectSlotsByName(camDisplayQWidget)

    def retranslateUi(self, camDisplayQWidget):
        camDisplayQWidget.setWindowTitle(QtGui.QApplication.translate("camDisplayQWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.numberOfFramesLabel.setText(QtGui.QApplication.translate("camDisplayQWidget", "Number of frames", None, QtGui.QApplication.UnicodeUTF8))
        self.setBackgroundFrameLabel.setText(QtGui.QApplication.translate("camDisplayQWidget", "Set background frame", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("camDisplayQWidget", "PushButton", None, QtGui.QApplication.UnicodeUTF8))

