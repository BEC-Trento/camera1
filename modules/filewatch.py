#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Sun Dec  4 21:46:06 2016
# Copyright (C) 2016  Carmelo Mordini
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class Camera():
    def __init__(self, **kwargs):

        self.observer = None
        self._source_folder = None
        self._pic_pars = {'file_ext': None, 'read_fun': None,
                         'finalize_fun': None, 'N_frames': None, 'delete_raw': None}
        self.picture_handler = PictureBase(**self._pic_pars)
        
    @property
    def source_folder(self,):
        return self._source_folder
    @source_folder.setter
    def source_folder(self, value):
        self._source_folder = value
        self.observer_reboot(handler=self.picture_handler, path=value)
    
    @property
    def pic_pars(self,):
        return self._pic_pars
    @pic_pars.setter
    def pic_pars(self, dic):
        for k in dic:
            if k in self._pic_pars:
                self._pic_pars[k] = dic[k]
        self.picture_handler.set_pic_pars(**self._pic_pars)
        print(self)
        if 'source_folder' in dic:
            self._source_folder = dic['source_folder']
        if self.source_folder is not None:
            self.observer_reboot(handler=self.picture_handler, path=self.source_folder)
            
        
    def observer_reboot(self, handler, path):
        if self.observer is not None:
#            self.observer.join()
            self.observer.stop()
            print('observer stopped')
        self.observer = Observer()
        self.observer.schedule(handler, path=path)
        print('observer scheduled on ', path)
        self.observer.start()
        
    def __str__(self,):
        s = "\nFilewatch attributes:\n"+\
        "source folder: {:s}\n".format(str(self.source_folder)) +\
        "\n".join(["{:s}: {:s}".format(k, str(self.pic_pars[k])) for k in self.pic_pars])
        return s
        

class PictureBase(PatternMatchingEventHandler):
    ''' Parent class with commom methods for the pictures
    event.event_type
        'modified' | 'created' | 'moved' | 'deleted'
    event.is_directory
        True | False
    event.src_path
        path/to/observed/file
    '''
#    signalFinalizedPicture = QtCore.Signal(np.ndarray)
    def __init__(self, file_ext, read_fun, finalize_fun, N_frames, delete_raw, **kwargs):
        super(PictureBase, self).__init__(patterns=file_ext, **kwargs)
#        QtCore.QObject.__init__(self,)
        self._final_picture = None
        self._raw_to_save = None
        self._slots_on_final = []
        self._slots_on_final_raw = []
        self.counter = 0
        self.list_frames = []
        self.set_pic_pars(file_ext, read_fun, finalize_fun, N_frames, delete_raw, **kwargs)
        
    def set_pic_pars(self, file_ext, read_fun, finalize_fun, N_frames, delete_raw, **kwargs):        
        self._patterns = file_ext
        self.finalize_fun = finalize_fun
        self.N_frames = N_frames
        self.read_fun = read_fun
        self.flag_delete_raw = delete_raw
        
    @property
    def final_picture(self):
        return self._final_picture
    @final_picture.setter
    def final_picture(self, value):
        self._final_picture = value
        for f in self._slots_on_final:
            print('about to apply slot: final pic %s'%f.__name__)
            f(value)
            
    @property
    def raw_to_save(self):
        return self._raw_to_save
    @raw_to_save.setter
    def raw_to_save(self, value):
        self._raw_to_save = value
        for f in self._slots_on_final_raw:
            print('about to apply slot: raw pic %s'%f.__name__)
            f(value)
        
        
            
    def on_deleted(self, event):
        print(str(event.src_path) + ' ' + str(event.event_type))
        print("The raw file has been deleted: ")
        print("Ready!")

    def on_created(self, event):
        print(str(event.src_path) + ' ' + str(event.event_type))
        frame = self.read_fun(event.src_path, full_output=False)
        if self.flag_delete_raw:
            try:
                os.remove(event.src_path)
            except OSError:
                pass
        self.counter += 1
        self.list_frames.append(frame)
        print('Read frame #%d'%self.counter)
        print('Nframes = %d'%self.N_frames)
        if self.counter == self.N_frames:
            print('Finalize picture')
            self.final_picture, self.raw_to_save = self.finalize(self.list_frames)
            self.reset()
            print('Ready for new picture')
            
    def finalize(self, *args):
        final, raw = self.finalize_fun(*args)
#        self.signalFinalizedPicture.emit(final)
        print('FINALIZED')
        return final, raw
  
 
    def reset(self,):
        self.counter = 0
        self.list_frames = []

#class QPictureBase(QtCore.QObject, PictureBase):
#    signalFinalizedPicture = QtCore.Signal(np.ndarray)
#    def __init__(self, *args, **kwargs):
#        super(QPictureBase, self).__init__()
#        
#    def finalize(self, *args):
#        final = self.finalize_fun(*args)
#        self.signalFinalizedPicture.emit(final)
#        return final
 


if __name__ == '__main__':
    from pictures import Picture_OD_4_frames
    from presets import cam_presets
    sett = cam_presets['Stingray_CAM']
    cam = Camera(sett, Picture_OD_4_frames, source_folder='/home/carmelo/bec-projects/CAMERA/future')
