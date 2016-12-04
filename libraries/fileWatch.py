import os
import shutil
import numpy as np
import pickle

from libraries.read_lib import func_dictionary
from libraries import Sis2

from watchdog.events import PatternMatchingEventHandler

class Params():
    def __init__(self,):
        self.patterns = ["*.ppm", "*.tif"]
        self.stamp = 'Coriander-BEC3-mainTest'
        # self.source = r'C:\Users\bec2\Desktop\carmelo_camera\python\raw'
        self.source = r'\\T5600_JBTGFY1\images'
        # self.writesis_dest = r'C:\Users\bec2\Desktop\carmelo_camera\python'
        self.writesis_dest = r'C:\SIScam\SIScamProgram\Prog\img'
        self.sisname = 'test_0.sis'
        self.initNumberOfFrames = 82
        
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
#        self.waitForFile = self.source + "/test-0000000003.ppm"
        self.counter = 0
        # self.created_last = self.make_Picture_NaK_4
        self.created_last = self.make_Film6_sub_bkg

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
        self.mainWindow.framesHeaderList.append(h)
        self.mainWindow.framesImageList.append(im)
        if self.counter == self.mainWindow.framesNumber:
            self.counter = 0
            self.created_last()
            self.mainWindow.plotAcquired()
            self.removeFiles()

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

    def make_Picture_NaK_4(self,):
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
'''    
    def make_Picture_NaK_4(self,):
        print("Processing! standard Picture NaK")
        atoms, ref, b1, b2 = self.mainWindow.framesImageList
        # with open(os.path.join(self.params.writesis_dest, 'atoms.pkl'), 'wb') as f:
            # pickle.dump(atoms, f)
        # with open(os.path.join(self.params.writesis_dest, 'ref.pkl'), 'wb') as f:
            # pickle.dump(ref, f)

        OD = -np.log((atoms+0.0 - b1)/(ref+0.0 - b1))
        # OD = -np.log((atoms+0.0)/(ref+0.0))
        
        self.mainWindow.currentImage = OD
        # with open(os.path.join(self.params.writesis_dest, 'OD.pkl'), 'wb') as f:
            # pickle.dump(OD, f)
        
        stamp = self.params.stamp
        OD[OD<0] = 0
        due_righe = np.zeros((2, 1624))
        new = np.concatenate([OD, due_righe])
        b = ( (2**16/10) * new )
        b = b.astype(np.uint16)+1
        print('Written Sis with dimensions', b.shape)
        # def sis_write(self, image, filename, Bheight, Bwidth, commitProg, stamp):
        p = self.mainWindow.destinationLineEdit.text()
        Sis2.sis_write(None, b, str(p), 400, 800, '', stamp)
        
        # shutil.copy(str(self.mainWindow.framesPathList[0]), self.params.writesis_dest)
        # Sis2.sis_write_off(0,OD,'mainTest.sis',400,800,stamp)
'''    

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
