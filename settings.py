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

from scipy.ndimage import gaussian_filter

default_source = r'C:\SIScam\SIScamProgram\Prog\img\temp_hamamatsu'
default_savedir = r'C:\SIScam\SIScamProgram\Prog\img'
default_savename = 'test_1.sis'

C_cam = 1.0463994082840237e+18
pix_size = 6.5e-6/8.5
Isat0 = 62.6
alpha = 1.82
blur_raw = 1

# all of these function must have the call save(fname, image)
save_ext_d = {
        '.sis': write_sis,
        '.npy': np.save
        }

cam_presets = {
'Hamamatsu':
    {'file_ext': ['*.tif', '*.tiff'],
     'source_folder': default_source,
     'read_fun': read_tif
     },
'Stingray_ppm':
    {'file_ext': ['*.ppm'],
     'source_folder': os.path.abspath('raw'),
     'read_fun': read_pgm
     },
}

def fit_beta(A, B, fit_area, ):
    a = A[fit_area].ravel()
    b = B[fit_area].ravel()
    return (b*a).sum()/(b**2).sum()
    
def load_frames_ODs(frames_list, tprobe, roislice, *args):
    frames_list0 = [f.astype(np.float64) for f in frames_list]
    frames_list = [gaussian_filter(f, blur_raw) for f in frames_list0]
    #dead_pixels = (np.array([ 539,  763, 1234, 1760], dtype=np.int64), np.array([1259,  283,  372,  392], dtype=np.int64))
    # for f in frames_list:
        # f[dead_pixels] = 0
    F1, F2 = frames_list[0:2]
    B = frames_list[2]
    Bm = B.mean()
    print('******* ',F1.shape)
    beta = fit_beta(F1-Bm, F2-Bm, roislice)
    print(beta)
    atoms = F1 - Bm
    probe = beta*(F2 - Bm)
    ODlog = np.log(probe/atoms)
    Isatcount = C_cam*tprobe*Isat0*pix_size**2
    ODlin = (probe - atoms)/Isatcount
    cam_count = probe[roislice].mean()
    noise_count = frames_list[2].std()
    s0 = cam_count/Isatcount
    Nphot = tprobe*30.67e6*s0/(s0+alpha)
    s = '''    probe_time : {:.2f} us
    s0 : {:.3f}
    Nphot: {:.3f}
    cam count: {:.2f} + {:.2f} ({:.1f}) bkg
    max OD: {:.1f} + {:.1f}
    '''.format(tprobe*1e6, s0, Nphot, cam_count, Bm, noise_count,
               alpha*np.log(cam_count/noise_count), cam_count/Isatcount)
    print(s)
    raw_to_save = np.concatenate(frames_list0[:-1])
    return ODlin, ODlog, raw_to_save
    
    
def finalize_picture_5_extra_frame(frames_list, tprobe, roislice, *args):
    frames_list.pop(0)
    ODlin, ODlog, raw_to_save = load_frames_ODs(frames_list, tprobe, roislice, *args)
    OD = alpha*ODlog
    return OD, raw_to_save
	
def finalize_picture_5_extra_frame_Isat(frames_list, tprobe, roislice, *args):
    frames_list.pop(0)
    ODlin, ODlog, raw_to_save = load_frames_ODs(frames_list, tprobe, roislice, *args)
    OD = ODlin + alpha*ODlog
    return OD, raw_to_save

    
def finalize_picture_OD_4_frames(frames_list, tprobe, roislice, *args):
    ODlin, ODlog, raw_to_save = load_frames_ODs(frames_list, tprobe, roislice, *args)
    OD = alpha*ODlog
    return OD, raw_to_save

def finalize_picture_1_frame(frames_list, *args):
    f = frames_list[0]
    frame = f.astype(np.float64)
    return frame, frame
    
def finalize_picture_movie_n_frames(frames_list, *args):
    probe = frames_list[0]
    frames = frames_list[1:]
    Nframes = len(frames)
    print('Ho trovato %d immagini'%Nframes)
    odlist = []
    for f in frames:
        OD = -np.log((f+1e-5)/(probe+1e-5))
        # OD[OD<0] = 0
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
    return image, np.zeros_like(image)

pictures_d = {
'Picture 4 frames': 
    {'finalize_fun': finalize_picture_OD_4_frames,
     'N_frames': 4,
     },
'Picture 5 extra frame':
    {'finalize_fun': finalize_picture_5_extra_frame,
     'N_frames': 5,
     },
'Picture 5 extra frame Isat':
    {'finalize_fun': finalize_picture_5_extra_frame_Isat,
     'N_frames': 5,
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

default_fun = 'Picture 5 extra frame Isat'
