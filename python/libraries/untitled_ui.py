# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Wed Apr 20 16:39:35 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        MainWindow.resize(1016, 733)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icons/resources/open-iconic-master/svg/globe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.framesWidget = QtGui.QWidget(self.centralwidget)
        self.framesWidget.setObjectName(_fromUtf8("framesWidget"))
        self.framesVerticalLayout = QtGui.QVBoxLayout(self.framesWidget)
        self.framesVerticalLayout.setMargin(0)
        self.framesVerticalLayout.setObjectName(_fromUtf8("framesVerticalLayout"))
        self.horizontalLayout.addWidget(self.framesWidget)
        self.odWidget = QtGui.QWidget(self.centralwidget)
        self.odWidget.setObjectName(_fromUtf8("odWidget"))
        self.odVerticalLayout = QtGui.QVBoxLayout(self.odWidget)
        self.odVerticalLayout.setMargin(0)
        self.odVerticalLayout.setObjectName(_fromUtf8("odVerticalLayout"))
        self.horizontalLayout.addWidget(self.odWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1016, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPlot = QtGui.QMenu(self.menubar)
        self.menuPlot.setObjectName(_fromUtf8("menuPlot"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionHome = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/basic-ui/resources/111267-basic-ui/svg/home-button.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon1)
        self.actionHome.setObjectName(_fromUtf8("actionHome"))
        self.actionRefresh = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/basic-ui/resources/111267-basic-ui/svg/refresh-arrow.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon2)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.menuFile.addAction(self.actionHome)
        self.menuPlot.addAction(self.actionRefresh)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionRefresh)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MyApp", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuPlot.setTitle(_translate("MainWindow", "Plot", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionHome.setText(_translate("MainWindow", "Home", None))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh", None))
        self.actionRefresh.setShortcut(_translate("MainWindow", "F5", None))

import resources_rc
