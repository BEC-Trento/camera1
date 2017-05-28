# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Apr 22 16:52:07 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(773, 582)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/basic-ui/icons/111267-basic-ui/svg/eye-close-up.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTip(_fromUtf8(""))
        MainWindow.setDocumentMode(False)
        self.mainWindowContents = QtGui.QWidget(MainWindow)
        self.mainWindowContents.setObjectName(_fromUtf8("mainWindowContents"))
        self.gridLayout = QtGui.QGridLayout(self.mainWindowContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineVertical = QtGui.QFrame(self.mainWindowContents)
        self.lineVertical.setFrameShape(QtGui.QFrame.VLine)
        self.lineVertical.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineVertical.setObjectName(_fromUtf8("lineVertical"))
        self.gridLayout.addWidget(self.lineVertical, 0, 1, 3, 1)
        self.line = QtGui.QFrame(self.mainWindowContents)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 2, 1, 1)
        self.framesWidget = FramesQWidget(self.mainWindowContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.framesWidget.sizePolicy().hasHeightForWidth())
        self.framesWidget.setSizePolicy(sizePolicy)
        self.framesWidget.setObjectName(_fromUtf8("framesWidget"))
        self.framesGridLayout = QtGui.QGridLayout(self.framesWidget)
        self.framesGridLayout.setObjectName(_fromUtf8("framesGridLayout"))
        self.plotFrameALabel = QtGui.QLabel('FrameA', self.framesWidget,)
        self.plotFrameALabel.setObjectName(_fromUtf8("plotFrameALabel"))
        self.framesGridLayout.addWidget(self.plotFrameALabel, 0, 0, 1, 1)
        self.plotFrameASpinBox = QtGui.QSpinBox(self.framesWidget)
        self.plotFrameASpinBox.setMinimum(1)
        self.plotFrameASpinBox.setObjectName(_fromUtf8("plotFrameASpinBox"))
        self.framesGridLayout.addWidget(self.plotFrameASpinBox, 0, 1, 1, 1)
        self.plotFrameBLabel = QtGui.QLabel(self.framesWidget)
        self.plotFrameBLabel.setObjectName(_fromUtf8("plotFrameBLabel"))
        self.framesGridLayout.addWidget(self.plotFrameBLabel, 1, 0, 1, 1)
        self.plotFrameBSpinBox = QtGui.QSpinBox(self.framesWidget)
        self.plotFrameBSpinBox.setMinimum(1)
        self.plotFrameBSpinBox.setProperty("value", 2)
        self.plotFrameBSpinBox.setObjectName(_fromUtf8("plotFrameBSpinBox"))
        self.framesGridLayout.addWidget(self.plotFrameBSpinBox, 1, 1, 1, 1)
        self.framesPlotLayout = QtGui.QVBoxLayout()
        self.framesPlotLayout.setObjectName(_fromUtf8("framesPlotLayout"))
        self.framesGridLayout.addLayout(self.framesPlotLayout, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.framesWidget, 0, 0, 3, 1)
        self.odWidget = OdQWidget(self.mainWindowContents)
        self.odWidget.setObjectName(_fromUtf8("odWidget"))
        self.odLayout = QtGui.QVBoxLayout(self.odWidget)
        self.odLayout.setObjectName(_fromUtf8("odLayout"))
        self.gridLayout.addWidget(self.odWidget, 2, 2, 1, 1)
        self.inputWidget = QtGui.QWidget(self.mainWindowContents)
        self.inputWidget.setObjectName(_fromUtf8("inputWidget"))
        self.formLayout = QtGui.QFormLayout(self.inputWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
#        self.formLayout.setMargin(0)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.numberOfFramesNameLabel = QtGui.QLabel(self.inputWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberOfFramesNameLabel.sizePolicy().hasHeightForWidth())
        
        self.numberOfFramesNameLabel.setSizePolicy(sizePolicy)
        self.numberOfFramesNameLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.numberOfFramesNameLabel.setObjectName(_fromUtf8("numberOfFramesLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.numberOfFramesNameLabel)
        
        self.nunberOfFramesNumLabel = QtGui.QLabel(self.inputWidget)#QtGui.QSpinBox(self.inputWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nunberOfFramesNumLabel.sizePolicy().hasHeightForWidth())
        self.nunberOfFramesNumLabel.setSizePolicy(sizePolicy)
        self.nunberOfFramesNumLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        #self.nunberOfFramesNumLabel.setSuffix(_fromUtf8(""))
        #self.nunberOfFramesNumLabel.setProperty("value", 4)
        self.nunberOfFramesNumLabel.setObjectName(_fromUtf8("nunberOfFramesNumLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.nunberOfFramesNumLabel)

        self.sourceFolderLabel = QtGui.QLabel(self.inputWidget)
        self.sourceFolderLabel.setObjectName(_fromUtf8("sourceFolderLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.sourceFolderLabel)
        self.sourceFolderLineEdit = QtGui.QLineEdit(self.inputWidget)
        self.sourceFolderLineEdit.setObjectName(_fromUtf8("sourceFolderLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.sourceFolderLineEdit)
        self.gridLayout.addWidget(self.inputWidget, 0, 2, 1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(2, 1)
        MainWindow.setCentralWidget(self.mainWindowContents)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 773, 27))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPlot = QtGui.QMenu(self.menuBar)
        self.menuPlot.setObjectName(_fromUtf8("menuPlot"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionHome = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/basic-ui/icons/111267-basic-ui/svg/home-button.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon1)
        self.actionHome.setObjectName(_fromUtf8("actionHome"))
        self.actionRefresh = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/basic-ui/icons/111267-basic-ui/svg/refresh-arrow.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon2)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.actionInfo = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/basic-ui/icons/111267-basic-ui/svg/left-justification-button.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInfo.setIcon(icon3)
        self.actionInfo.setObjectName(_fromUtf8("actionInfo"))
        self.menuFile.addAction(self.actionHome)
        self.menuPlot.addAction(self.actionRefresh)
        self.menuHelp.addAction(self.actionInfo)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuPlot.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionRefresh)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ELENA", None))
#        self.plotFrameALabel.setText(_translate("MainWindow", "Plot frame A", None))
        self.plotFrameBLabel.setText(_translate("MainWindow", "Plot frame B", None))
        self.numberOfFramesNameLabel.setText(_translate("MainWindow", "Number of frames", None))
        self.sourceFolderLabel.setText(_translate("MainWindow", "Source folder", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuPlot.setTitle(_translate("MainWindow", "Plot", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionHome.setText(_translate("MainWindow", "Home", None))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh", None))
        self.actionRefresh.setShortcut(_translate("MainWindow", "F5", None))
        self.actionInfo.setText(_translate("MainWindow", "Info", None))
        self.actionInfo.setShortcut(_translate("MainWindow", "F11", None))

from libraries.odqwidget import OdQWidget
from libraries.framesqwidget import FramesQWidget
import resources_rc
