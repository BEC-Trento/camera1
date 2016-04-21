import os, glob
import numpy as np

from libraries.read_lib import read_pgm
from libraries import Sis2

from watchdog.events import PatternMatchingEventHandler

class Params():
    def __init__(self,):
        self.patterns = ["*.ppm"]
        self.stamp = 'Coriander-BEC3-mainTest'
        #source = os.path.realpath('../data/samples/')
        self.source = os.path.realpath('.')
        

class MyHandler(PatternMatchingEventHandler):
    """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
    """
    def __init__(self, params):        
        self.params = params
        super(MyHandler, self).__init__(patterns=self.params.patterns)
        self.source = self.params.source
        self.waitForFile = self.source + "/test-0000000003.ppm"
        

    def on_deleted(self, event):
        print(str(event.src_path) + ' ' + str(event.event_type))
        print("The raw file has been deleted: ")
        print("Ready!")

    def on_created(self, event):
        print(str(event.src_path) + ' ' + str(event.event_type))
        print("New data: ")
        filename = str(event.src_path)
        if filename == self.waitForFile:
            print("Processing!")
            filelist = glob.glob(os.path.join(self.source, 'test*.ppm'))
            filelist.sort()
            headlist = []
            imlist = []
            for file in filelist[-4:]:
                print(file)
                h, im = read_pgm(file)
                headlist.append(h)
                imlist.append(im)
    
            atoms, ref, b1, b2 = imlist
            od_crop = (slice(800,1200), slice(200,1000))
    
            #OD = -np.log((atoms[od_crop]-b1[od_crop])/(ref[od_crop]-b2[od_crop]+1))
            OD = -np.log((atoms[od_crop]+1)/(ref[od_crop]+1))
    
            stamp = self.params.stamp
            OD[OD<0] = 0
            b = ( (2**16/10) * OD )
            Sis2.sis_write(0,b.astype(np.uint16)+1,'mainTest.sis',400,800,stamp)
            #Sis2.sis_write_off(0,OD,'mainTest.sis',400,800,stamp)
        else:
            print("Wait for " + self.waitForFile)


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
