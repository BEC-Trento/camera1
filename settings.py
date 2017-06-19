#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Wed Feb 15 17:01:03 2017
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
import numpy as np
from modules.imageio import read_pgm, read_tif
from modules.imageio.sis2_lib import read_sis0, write_sis

default_savedir = os.path.abspath('.')
default_savename = 'test_0.sis'

# all of these function must have the call save(fname, image)
save_ext_d = {
        '.sis': write_sis,
        '.npy': np.save
        }

cam_presets = {
'Stingray_CAM': 
    {'file_ext': ['*.sis'],
     'source_folder': os.path.abspath('raw'),
     'read_fun': read_sis0
     },
'Stingray_Coriander': 
    {'file_ext': ['*.ppm'],
     'source_folder': os.path.abspath('raw'),
     'read_fun': read_pgm
     },
'Hamamatsu':
    {'file_ext': ['*.tif'],
     'source_folder': os.path.abspath('raw/hamamatsu'),
     'read_fun': read_tif
     },   
}
    


def finalize_picture_OD_4_frames(frames_list,):
    frames_list = [f.astype(np.float64) for f in frames_list]
    bg = frames_list[3]
    atoms, probe = frames_list[0:2]
    atoms = atoms - bg 
    probe = probe - bg 
    #TODO: check this step here
    
#        OD = -np.log(atoms/probe)
    OD = np.log((probe+1e-5)/(atoms+1e-5))
    OD[OD<0] = 0
    return OD        

def finalize_picture_1_frame(frames_list,):
    f = frames_list[0]
    frame = f.astype(np.float64)
    return frame
    
def finalize_picture_movie_n_frames(frames_list,):
    probe = frames_list[0]
    frames = frames_list[1:]
    Nframes = len(frames)
    print('Ho trovato %d immagini'%Nframes)
    odlist = []
    for f in frames:
        OD = -np.log((f+1e-5)/(probe+1e-5))
        OD[OD<0] = 0
        odlist.append(OD)
    h, w = OD.shape
    W = 1624
    Lw = W // w
    Lh = Nframes // Lw + 1
    H = h*Lh
    image = np.zeros((H, W))
    dims = (Lh, Lw)
    print('Writing %d frames in a %d x %d matrix\ntotal picture size: %d x %d'%(Nframes, Lh, Lw, H, W))
    for j, od in enumerate(odlist):
        p, q = np.unravel_index(j, dims)
        image[p*h:(p+1)*h, q*w:(q+1)*w] = od
    return image

pictures_d = {
'Picture 4 frames': 
    {'finalize_fun': finalize_picture_OD_4_frames,
     'N_frames': 4,
     },
'Picture single frame': 
    {'finalize_fun': finalize_picture_1_frame,
     'N_frames': 1,
     },
'Movie': 
    {'finalize_fun': finalize_picture_movie_n_frames,
     'N_frames': None,
     },
}