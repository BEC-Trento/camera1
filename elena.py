#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:27:57 2016

@author: carmelo
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import str
from future import standard_library
standard_library.install_aliases()

import os
import numpy as np
from PySide import QtGui
from PySide.QtCore import Slot

from modules.ui.mainwindow_ui import Ui_MainWindow

from modules.filewatch import Camera
from modules.functions import cam_presets, pictures_d

PROG_NAME = 'ELENA'
PROG_COMMENT = 'Eliminate LabVIEW for an Enhanced New Acquisition system'
PROG_VERSION = '0.9 (beta)'

output_folder = os.path.join(os.getcwd(), 'img')

class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        
        self.camera = Camera()
        
#        d0 = cam_presets['Stingray_Coriander'].copy()
#        source = d0.pop('source_folder')
#        d0.update(pictures_d['Picture 4 frames'])
#        d0['delete_raw'] = self.deleteRawCheckBox.isChecked()
#        print(d0)
        
        self.connectInputWidget()
        self.sourcePresetsComboBox.addItems(list(cam_presets.keys()))
        self.pictureSelectComboBox.addItems(list(pictures_d.keys()))
#        
#        self.camera.pic_pars = d0
#        self.camera.source_folder = source
        

        self.camera.picture_handler.signalFinalizedPicture.connect(self.plot_finalized)
        
    def connectActions(self):
        self.actionInfo.triggered.connect(self.infoBox)
#        self.actionRefresh.triggered.connect(self.plotAcquired)
        
    def connectInputWidget(self):
        self.sourcePresetsComboBox.currentIndexChanged[str].connect(self.load_source_presets)
        self.pictureSelectComboBox.currentIndexChanged[str].connect(self.load_picture)
        
        self.sourceFolderLineEdit.textChanged.connect(self.on_source_folder_changed)
        self.nFramesSpinBox.valueChanged.connect(self.on_n_frames_changed)
        self.deleteRawCheckBox.stateChanged.connect(self.on_delete_raw_state_changed)
        
    def load_source_presets(self, preset_name):
        sets = cam_presets[preset_name]
        self.fileExtLineEdit.setText(', '.join(sets['file_ext']))
        self.sourceFolderLineEdit.setText(str(sets['source_folder']))
        self.reload_pic_pars()
        
    def load_picture(self, pic_name):
        d = pictures_d[pic_name]
        n_frames = d['N_frames']
        if n_frames is not None:
            self.lock_n_frames(lock=True, value=n_frames)
        else:
            self.lock_n_frames(lock=False, value=-1)
        self.reload_pic_pars()
        
    def reload_pic_pars(self,):
        pars = {}
        pars.update(cam_presets[self.sourcePresetsComboBox.currentText()])
        pars.update(pictures_d[self.pictureSelectComboBox.currentText()])
        pars['source_folder'] = self.sourceFolderLineEdit.text()
        pars['N_frames'] = self.nFramesSpinBox.value()
        pars['delete_raw'] = self.deleteRawCheckBox.isChecked()
        self.camera.pic_pars = pars
        
    def on_source_folder_changed(self, path):
        print('folder changed')
        self.camera.source_folder = path
        
    def on_n_frames_changed(self, n_frames):
        print('N frames set to %d'%n_frames)
        self.camera.picture_handler.N_frames = n_frames
        print(self.camera)
        
    def on_delete_raw_state_changed(self,):
        self.camera.picture_handler.flag_delete_raw = self.deleteRawCheckBox.isChecked()            
        print(self.camera)
        
    def lock_n_frames(self, lock=True, value=1):
        self.nFramesSpinBox.setValue(value)
        if lock:
            self.nFramesSpinBox.setStyleSheet("QSpinBox {\n"
            "border: 1px solid rgb(0,0,0);\n"
            "border-radius: 4px;\n"
            "background-color: rgb(229, 229, 229)\n"
            "}")
            self.nFramesSpinBox.setReadOnly(True)
            self.nFramesSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        else:
            self.nFramesSpinBox.setStyleSheet("")
            self.nFramesSpinBox.setReadOnly(False)
            self.nFramesSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
    
    @Slot(np.ndarray)
    def plot_finalized(self, image):
        print('finalized and plotting')
        self.displayWidget.setImage(image)

        
    def infoBox(self,):
        QtGui.QMessageBox.about(self, PROG_NAME, PROG_COMMENT+'\n v. '+PROG_VERSION)
        
    
    


if __name__ == '__main__':
    import sys  

    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
#    main.observerReboot(path=main.params.source)
    status = app.exec_()
    main.observer.stop()
    main.observer.join()
    sys.exit(status)

