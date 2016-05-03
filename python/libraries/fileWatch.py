import os
import numpy as np

from libraries.read_lib import read_pgm
from libraries import Sis2

from watchdog.events import PatternMatchingEventHandler

class Params():
    def __init__(self,):
        self.patterns = ["*.ppm"]
        self.stamp = 'Coriander-BEC3-mainTest'
        #source = os.path.realpath('../data/samples/')
        self.source = os.path.realpath('./raw')


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
        self.mainWindow.framesPathList.append(file)
        h, im = read_pgm(file)
        self.mainWindow.framesHeaderList.append(h)
        self.mainWindow.framesImageList.append(im)
        if self.counter == self.mainWindow.framesNumber:
            self.counter = 0
            self.created_last()
            self.mainWindow.plotAcquired()
            self.removeFiles()


    def created_last(self,):
        print("Processing!")
        atoms, ref, b1, b2 = self.mainWindow.framesImageList
        od_crop = (slice(None), slice(None))

        #OD = -np.log((atoms[od_crop]-b1[od_crop])/(ref[od_crop]-b2[od_crop]+1))
        OD = -np.log((atoms[od_crop]+1)/(ref[od_crop]+1))
        self.mainWindow.currentImage = OD

        stamp = self.params.stamp
        OD[OD<0] = 0
        b = ( (2**16/10) * OD )
        print('Written Sis with dimensions', b.shape)
        Sis2.sis_write(0,b.astype(np.uint16)+1,'mainTest.sis',400,800,stamp)
        #Sis2.sis_write_off(0,OD,'mainTest.sis',400,800,stamp)

    def removeFiles(self,):
        print(self.mainWindow.framesPathList)
        for file in self.mainWindow.framesPathList:
                try:
#                    os.rename(file, os.path.join('./raw/trash',os.path.split(file)[1]))
                    os.rename(file, os.path.join('./stingray',os.path.split(file)[1]))
#                    os.remove(file)
                except OSError:
                    pass



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
