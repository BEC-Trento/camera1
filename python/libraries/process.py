import os, glob
import numpy as np
import matplotlib

from libraries.read_lib import read_pgm
from libraries import params
from libraries import Sis2

source = params.source
waitForFile = source + "/test-4.ppm"

def created(filename):
    if filename == waitForFile:
        print("Processing!")
        filelist = glob.glob(source + '/test*.ppm')
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
        matplotlib.image.imsave("atoms.png",atoms)
        matplotlib.image.imsave("ref.png",ref)

        stamp = params.stamp
        Sis2.sis_write(0,OD,'mainTest.sis',400,800,stamp)
    else:
        print("Wait for " + waitForFile)

def deleted(filename):
    print("Ready!")
