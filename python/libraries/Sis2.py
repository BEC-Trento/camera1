# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 2016

@author: SimoneSerafini

"""

import numpy as np


def readsis(filename):
    ''' Legge i file .sis con cui mi hanno passato i dati
    Parameters
    ----------
    filename : stringa con il nome o il path relativo del file.
    Returns im1, im2, image, rawdata, width, height
    -------
    im1 : ndarray 2D
        la prima meta dell'immagine [righe 0 : height/2-1].
    im2 : ndarray 2D
        la prima meta dell'immagine [righe height/2 : height-1].
    image : ndarray 2D
        l'immagine completa.
    rawdata : ndarray 1D
        raw data letti dal file
    ### suppressed (height, width) : tuple
        dimensioni dell'array image
    Notes
    -----
    NB tutti gli output sono finestre (slices) sui raw data: ogni modifica cambierà anche gli elementi corrispondenti in rawdata
    '''
    f = open(filename, 'rb')  #apre in binario
    rawdata = np.fromfile(f,'H').astype(int)
    # 'H' = uint16
    # lo trovo in np.typeDict
    #legge in array i dati formattati uint16 e li casta ad int
    ''' NB è importantissimo castarli ad int:
        visto che sono numeri molto grandi, gli unsigned short non vanno bene (overflow) '''
    f.close

    width=rawdata[6]  # N cols
    height=rawdata[5] # N rows
    #rispetto ad octave, gli indici cambiano (python è 0-based)

    image = rawdata[-width*height : ]
    image.resize(height,width)

    #in matlab, poiché reshape legge per colonne, era necessario scambiare gli indici e poi trasporre la matrice. Ora non più

    im0 = image[:height//2, :]
    im1 = image[height//2:, :]

    return im0, im1, image, rawdata #, image.shape

def sis_write(self, image, filename):
        """
        Low-level interaction with the sis file for writing it.
        Writes the whole image, with the unused part filled with zeros.

        Args:
            image (np.array): the 2d-array that must be writed after conversion
            to 16-bit unsigned-integers (must be already normalized)
            filename (string): sis filename
        """
        #keep the double-image convention for sis files, filling the unused
        #with zeros
        if self == 0:
            image = np.concatenate((image, np.zeros_like(image)))
        elif self == 1:
            image = np.concatenate((np.zeros_like(image), image))

        with open(str(filename), 'w+b') as fid:
            # Write here SisV2 - 5 bytes
            ##fid.write('0'*10) #skip unused
            head = 'SisV2'
            fid.write(head.encode())
            #fid.write('S')
            #fid.write('i')
            #fid.write('s')
            #fid.write('V')
            #fid.write('2')
            #fid.write('0'*5)

            # This is OK
            height, width = image.shape
            size = np.array([height, width], dtype=np.uint16)
            size.tofile(fid)

            # Here we put 2*2 more bytes with the sub-block dimension
            # Also a timestamp
            # More?
            ##fid.write('0'*182)
            ##fid.write('0'*4) #skip offset

            image.astype(np.uint16).tofile(fid)
