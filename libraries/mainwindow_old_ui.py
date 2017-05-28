# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_old.ui'
#
# Created: Sun May 28 15:00:01 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1016, 733)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/basic-ui/icons/111267-basic-ui/svg/eye-close-up.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTip("")
        MainWindow.setDocumentMode(False)
        self.mainWindowContents = QtGui.QWidget(MainWindow)
        self.mainWindowContents.setObjectName("mainWindowContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.mainWindowContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.odWidget = OdQWidget(self.mainWindowContents)
        self.odWidget.setObjectName("odWidget")
        self.odLayout = QtGui.QVBoxLayout(self.odWidget)
        self.odLayout.setObjectName("odLayout")
        self.verticalLayout.addWidget(self.odWidget)
        MainWindow.setCentralWidget(self.mainWindowContents)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1016, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuPlot = QtGui.QMenu(self.menubar)
        self.menuPlot.setObjectName("menuPlot")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.framesDockWidget = FramesQDockWidget(MainWindow)
        self.framesDockWidget.setObjectName("framesDockWidget")
        self.framesDockWidgetContents = QtGui.QWidget()
        self.framesDockWidgetContents.setObjectName("framesDockWidgetContents")
        self.framesLayout = QtGui.QVBoxLayout(self.framesDockWidgetContents)
        self.framesLayout.setObjectName("framesLayout")
        self.framesDockWidget.setWidget(self.framesDockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.framesDockWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionHome = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/basic-ui/icons/111267-basic-ui/svg/home-button.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon1)
        self.actionHome.setObjectName("actionHome")
        self.actionRefresh = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/basic-ui/icons/111267-basic-ui/svg/refresh-arrow.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon2)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionInfo = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/basic-ui/icons/111267-basic-ui/svg/left-justification-button.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInfo.setIcon(icon3)
        self.actionInfo.setObjectName("actionInfo")
        self.menuFile.addAction(self.actionHome)
        self.menuPlot.addAction(self.actionRefresh)
        self.menuHelp.addAction(self.actionInfo)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionRefresh)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "ELENA", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlot.setTitle(QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.framesDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Raw frames", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHome.setText(QtGui.QApplication.translate("MainWindow", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInfo.setText(QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInfo.setShortcut(QtGui.QApplication.translate("MainWindow", "F11", None, QtGui.QApplication.UnicodeUTF8))

from libraries.odqwidget_ui import OdQWidget
from libraries.framesqdockwidget_ui import FramesQDockWidget
from . import resources_rc
