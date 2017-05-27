import os
import shutil
import numpy as np
import pickle

from .read_lib import func_dictionary
from . import Sis2

from watchdog.events import PatternMatchingEventHandler

class Params():
    def __init__(self,):
        self.patterns = ["*.ppm", "*.tif"]
        self.stamp = 'Coriander-BEC3-mainTest'
        self.source = os.path.join(os.getcwd(), 'raw_horiz')
        self.writesis_dest = '/home/gabriele/Desktop/CAMERA/CAM/img'
        self.sisname = 'test_0.sis'
        self.initNumberOfFrames = 40
        
class MyHandler(PatternMatchingEventHandler):
    """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
    """
    def __init__(self, params, setMainWindow):
        self.mainWindow = setMainWindow
        self.params = params

        super(MyHandler, self).__init__(patterns=self.params.patterns)
        self.source = self.params.source
        self.counter = 0

        self.created_last = None
        self.max_frames = None

    def on_deleted(self, event):
        print(str(event.src_path) + ' ' + str(event.event_type))
        print("The raw file has been deleted: ")
        print("Ready!")


    def on_created(self, event):
        print(str(event.src_path) + ' ' + str(event.event_type))
        if self.counter == 0:
            self.mainWindow.resetLists()
        self.counter += 1
        print("New data: reading file #", self.counter)
        file = event.src_path
        ext = os.path.splitext(file)[1]
        self.mainWindow.framesPathList.append(file)
        print("Using %s: "%ext+str(func_dictionary[ext]))
        h, im = func_dictionary[ext](file)
        print(im)
        self.mainWindow.framesHeaderList.append(h)
        self.mainWindow.framesImageList.append(im)
        if self.counter == self.max_frames:
            self.counter = 0
            self.created_last()
            self.mainWindow.plotAcquired()
            self.removeFiles()

    def make_Picture_NaK_4_CAM(self,):
        """ qui aspetto di ricevere 4 frames
            [0]: foto con gli atomi
            [1]: foto con solo il probe
            [2]: background (foto al buio)
            [3]: e' uguale alla seconda, infatti non viene usata.
        """
        print("Processing! standard Picture NaK")
        bk = self.mainWindow.framesImageList[2]
        probe = self.mainWindow.framesImageList[1]
        frames = [self.mainWindow.framesImageList[0],]
        odlist = []
        for f in frames:
            OD = -np.log((f+0.0 - bk)/(probe+0.0 - bk))
            OD[OD<0] = 0
            # to be commented eventually:
            # OD.T
            odlist.append(OD)
        image = np.zeros((1234, 1624))
        h, w = OD.shape
        # to be inverted eventually, if OD is not transposed:
        dims = (1,1)
        for j, od in enumerate(odlist):
            p, q = np.unravel_index(j, dims)
            image[p*h:(p+1)*h, q*w:(q+1)*w] = od
        self.mainWindow.currentImage = image
        stamp = self.params.stamp
        b = ( (2**16/10) * image )
        b = b.astype(np.uint16)+1
        print('Written Sis with dimensions', b.shape)
        # def sis_write(self, image, filename, Bheight, Bwidth, commitProg, stamp):
        p = self.mainWindow.destinationLineEdit.text()
        Sis2.sis_write(None, b, str(p), h, w, '', stamp)

    def make_Picture_NaK_2_manual(self,):
        print("Processing! manual Picture NaK")
        probe = self.mainWindow.framesImageList[1]
        frames = [self.mainWindow.framesImageList[0],]
        odlist = []
        for f in frames:
            OD = -np.log((f+0.0)/(probe+0.0))
            OD[OD<0] = 0
            # to be commented eventually:
            # OD.T
            odlist.append(OD)
        image = np.zeros((1234, 1624))
        h, w = OD.shape
        # to be inverted eventually, if OD is not transposed:
        dims = (1,1)
        for j, od in enumerate(odlist):
            p, q = np.unravel_index(j, dims)
            image[p*h:(p+1)*h, q*w:(q+1)*w] = od
        self.mainWindow.currentImage = image
        stamp = self.params.stamp
        b = ( (2**16/10) * image )
        b = b.astype(np.uint16)+1
        print('Written Sis with dimensions', b.shape)
        # def sis_write(self, image, filename, Bheight, Bwidth, commitProg, stamp):
        p = self.mainWindow.destinationLineEdit.text()
        Sis2.sis_write(None, b, str(p), h, w, '', stamp)

    def make_Picture_single_frame(self,):
        """ qui aspetto di ricevere 4 frames
            [0]: foto con gli atomi
        """
        print("Processing! standard Picture NaK")
        image = self.mainWindow.framesImageList[0]
        h, w = image.shape
        # to be inverted eventually, if OD is not transposed:
        self.mainWindow.currentImage = image
        stamp = self.params.stamp
        b = image.astype(np.uint16)
        print('Written Sis with dimensions', b.shape)
        # def sis_write(self, image, filename, Bheight, Bwidth, commitProg, stamp):
        p = self.mainWindow.destinationLineEdit.text()
        Sis2.sis_write(None, b, str(p), h, w, '', stamp)
        
#    def saveSis(self, image, name, h, w, stamp):
#        p = self.mainWindow.destinationLineEdit.text()
#        Sis2.sis_write(None, b, str(p), h, w, '', stamp)
#        # hack: salvo anche test_1
#        p2 = os.path.join(os.path.split(p)[0], 'test_1.sis')
#        Sis2.sis_write(None, b, str(p2), h, w, '', stamp)
        

    def removeFiles(self,):
        print(self.mainWindow.framesPathList)
        for file in self.mainWindow.framesPathList:
                try:
#                    os.rename(file, os.path.join('./raw/trash',os.path.split(file)[1]))
                    # os.rename(file, os.path.join('./hamamatsu',os.path.split(file)[1]))
                    if self.mainWindow.deleteButton.isChecked():
                        os.remove(file)
                    pass
                except OSError:
                    pass
#### Functions for making films with the Hamamatsu
    def make_Film6_sub_bkg(self,):
        print("Processing! Film6")
        bk = self.mainWindow.framesImageList[0]
        probe = self.mainWindow.framesImageList[1]
        frames = self.mainWindow.framesImageList[2:]
        print('Ho trovato %d immagini'%len(frames))
        odlist = []
        for f in frames:
            OD = -np.log((f+0.0 - bk)/(probe+0.0 - bk))
            OD[OD<0] = 0
            # to be commented eventually:
            # OD = np.transpose(OD)
            odlist.append(OD)
        H, W = 3000, 1600
        image = np.zeros((H, W))
        h, w = OD.shape
        # to be inverted eventually, if OD is not transposed:
        Lh, Lw = H//h, W//w
        dims = (Lh, Lw)
        Nframes = Lh*Lw
        print('Writing %d frames out of %d on %d x %d'%(Nframes, len(frames), Lh, Lw))
        for j, od in enumerate(odlist[:Nframes]):
            p, q = np.unravel_index(j, dims)
            image[p*h:(p+1)*h, q*w:(q+1)*w] = od
        
        self.mainWindow.currentImage = image
        stamp = self.params.stamp

        b = ( (2**16/10) * image )
        b = b.astype(np.uint16)+1
        print('Written Sis with dimensions', b.shape)
        # def sis_write(self, image, filename, Bheight, Bwidth, commitProg, stamp):
        p = self.mainWindow.destinationLineEdit.text()
        Sis2.sis_write(None, b, str(p), h, w, '', stamp)

        b = ( (2**16/10) * image )
        b = b.astype(np.uint16)+1
        print('Written Sis with dimensions', b.shape)
        # def sis_write(self, image, filename, Bheight, Bwidth, commitProg, stamp):
        p = self.mainWindow.destinationLineEdit.text()
        Sis2.sis_write(None, b, str(p), h, w, '', stamp)
        
    def make_Film6_no_bkg(self,):
        print("Processing! Film6 no bkg")
        probe = self.mainWindow.framesImageList[0]
        frames = self.mainWindow.framesImageList[1:]
        print('Ho trovato %d immagini'%len(frames))
        odlist = []
        for f in frames:
            OD = -np.log((f+0.0)/(probe+0.0))
            OD[OD<0] = 0
            # to be commented eventually:
            # OD = np.transpose(OD)
            odlist.append(OD)
        H, W = 3000, 1600
        image = np.zeros((H, W))
        h, w = OD.shape
        # to be inverted eventually, if OD is not transposed:
        Lh, Lw = H//h, W//w
        dims = (Lh, Lw)
        Nframes = Lh*Lw
        print('Writing %d frames out of %d on %d x %d'%(Nframes, len(frames), Lh, Lw))
        for j, od in enumerate(odlist[:Nframes]):
            p, q = np.unravel_index(j, dims)
            image[p*h:(p+1)*h, q*w:(q+1)*w] = od
        
        self.mainWindow.currentImage = image
        stamp = self.params.stamp

        b = ( (2**16/10) * image )
        b = b.astype(np.uint16)+1
        print('Written Sis with dimensions', b.shape)
        # def sis_write(self, image, filename, Bheight, Bwidth, commitProg, stamp):
        p = self.mainWindow.destinationLineEdit.text()
        Sis2.sis_write(None, b, str(p), h, w, '', stamp)

class HandlerCloner(PatternMatchingEventHandler):

    def __init__(self,):
        self.mypatterns = ["*.ppm", "*.tif"]
        super(HandlerCloner, self).__init__(patterns=self.mypatterns)
        
    def on_deleted(self, event):
        pass
        # print(str(event.src_path) + ' ' + str(event.event_type))
        # print("The raw file has been deleted: ")
        # print("Ready!")

    def on_created(self, event):
        print(str(event.src_path) + ' ' + str(event.event_type))
        dest = r'C:\Users\bec2\Desktop\carmelo_camera\python\hamamatsu'
        file = event.src_path
        # os.rename(file, os.path.join(dest,os.path.split(file)[1]))
        shutil.copy(file, dest)
        
#def FWatch(checkPath):
#    observer = Observer()
#    observer.schedule(MyHandler(), path=checkPath)
#    observer.start()
#
#    print("Osservo!")
#
#    try:
#        while True:
#            time.sleep(1)
#    except KeyboardInterrupt:
#        observer.stop()
#
#    observer.join()
