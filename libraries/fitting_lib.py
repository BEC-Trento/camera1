# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 13:32:11 2014 by simone
Edited on Apr 2015 

@author: carmelo

Module containing the fitting routines.
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
# pylint: disable=E1101

from builtins import super
from builtins import range
from builtins import open
from builtins import dict
from builtins import zip
from builtins import str
from future import standard_library
standard_library.install_aliases()
from scipy.optimize import curve_fit, leastsq
import numpy as np
import numpy.ma as ma
from mpmath import polylog


def gaussian(XY, mx, my, sx, sy, alpha):
    """
    Returns the result of a Gaussian.

    Args:
        (X, Y) (tuple of np.array): matrices of the coordinates to be combined,
        usually results of np.meshgrid
        mx (float): horizontal center
        my (float): vertical center
        sx (float): horizontal sigma
        sy (float): vertical sigma
        alpha (float): rotation angle in degrees 
        """
    x, y = XY
    x = x - mx
    y = y - my
    alpha = (np.pi / 180.) * float(alpha)
    xr = + x * np.cos(alpha) - y * np.sin(alpha)
    yr = + x * np.sin(alpha) + y * np.cos(alpha)
    X, Y = xr, yr
    
    return ma.exp(- X**2 / (2*sx**2) - Y**2 / (2*sy**2))


def thomasfermi(XY, mx, my, rx, ry, alpha):
    """
    Returns the result of a Thomas-Fermi function (inverted parabola).

    Args:
        (X, Y) (tuple of np.array): matrices of the coordinates to be combined,
        usually results of np.meshgrid
        mx (float): horizontal center
        my (float): vertical center
        rx (float): horizontal TF radius
        ry (float): vertical TF radius
        alpha (float): rotation angle in degrees 
    """
    x, y = XY
    x = x - mx
    y = y - my
    alpha = (np.pi / 180.) * float(alpha)
    xr = + x * np.cos(alpha) - y * np.sin(alpha)
    yr = + x * np.sin(alpha) + y * np.cos(alpha)
    X, Y = xr, yr
    
    b = (1 - (X/rx)**2 - (Y/ry)**2)
    b = ma.maximum(b, 0)
    b = ma.sqrt(b)
    return b**3

def bimodal(XY, amp1, mx, my, sx, sy, amp2, rx, ry, alpha):
    return amp1*gaussian(XY, mx, my, sx, sy, alpha) +\
                      amp2*thomasfermi(XY, mx, my, rx, ry, alpha)

_bose_g = np.vectorize(polylog)
def bose_g(z, nu, order):
    if order == np.infty:
        s = _bose_g(nu, z)
        return s.astype(float)
    else:
        summed = np.zeros(z.shape)
        for k in range(order):
            k+=1
            summed += z**k / k**nu
    #    print('z: ',z)
    #    print('sum: ',summed)
        return summed


class Fitting1d(object):
    """
    Base class for fitting routines. It has some common methods, other must be
    overridden for the specific fitting types with child classes.
    """

    def __init__(self, data, sigma=None, xvalues=None, par0=None):
        """
        Initialize the fitting routine with a given image.

        Args:
            data (np.array): image for the fit
            xvalues (np.array): data for x coordinate
            par0 (list): initial guess for the fit s(optional, not yet used)
        """
        self.data = data
        self.par0 = par0 #TODO: not used
        self.sigma = sigma
        
        if xvalues is None:
            self.X = ma.arange(self.data.size)
        else:
            self.X = xvalues
        
        #the fitted image result is initialized to None
        self.fitted = None
        self.results = None
        self.errs = None
        self.good_fit = False
        #list of the parameter string names, must be implemented
        self.par_names = tuple([])

    def init_par0(self, *args, **kwargs):
        """
        Parameters guess for the specific function (must be overridden).
        """
        pass

    def function(self, *args, **kwargs):
        """
        Specific function (must be overridden).
        """
        pass
        
    def fit(self, full_output=False):
        """
        Performs the fitting operations and returns a dictionary with the
        fitted parameters.
        """
        #TODO handle when there is a wrong fit and set fit options
        #TODO consider parameters uncertanties
        sigma = self.sigma
        if sigma is None:
            err = lambda p, x, y: ma.ravel(y - self.function(x, *p))
            args=(self.X, self.data)
        else:
            err = lambda p, x, y, sigma: ma.ravel((y - self.function(x, *p)) / sigma)
            args=(self.X, self.data, sigma)
        
        try:
            results = leastsq(err, self.par0,
                              args=args,
                              full_output=1)
            results_dict = dict(list(zip(self.par_names, results[0])))
            errors_dict = dict(list(zip(self.par_names,
                                    np.sqrt(np.diag(results[1])))))
            self.good_fit = True
            self.results = results_dict
            self.errs = errors_dict
            if full_output:
                covmat = results[1]
                opt_output = results[2:]
                return results_dict, errors_dict, covmat, opt_output
            else:
                return results_dict, errors_dict
        except:# RuntimeError:
            print("Error while fitting")
            self.good_fit = False
            if full_output:
                return None, None, None, None
            else:
                return None, None
            
    def print_res(self):
        if self.good_fit:
            for k in sorted(self.results.keys()):
                print('{}: {:03.2f} /pm {:03.2f}'.format(k, self.results[k], self.errs[k]))
        else:
            print('No print')
            
    def save(self, filename, sep=',', mode='w'):
        if not self.good_fit:
            print('No save')
            return
        with open(filename, mode) as f:
            f.write(self.__class__.__name__ + '\n')
            f.write('# Results\n')
            for k in self.results.keys():
                line = sep.join([k, str(self.results[k]), str(self.errs[k])])
                f.write(line +  ' \n')
                                        
            
            
            
class Fitting2d(object):
    """
    Base class for fitting routines. It has some common methods, other must be
    overridden for the specific fitting types with child classes.
    """

    def __init__(self, img0, par0):
        """
        Initialize the fitting routine with a given image.

        Args:
            img0 (np.array): image for the fit
            par0 (list): initial guess for the fit s(optional, not yet used)
        """
        self.img0 = img0
        if par0 is None:
            self.guess_par0(None, None, None)
        else:
            self.par0 = par0 #TODO: not used

        #calculates the matrices with the x and y coordinates
        ny, nx = self.img0.shape
        x = np.arange(nx)
        y = np.arange(ny)
#        self.X, self.Y = np.meshgrid(x, y)
        X, Y = np.meshgrid(x, y)
        self.X = ma.asarray(X)
        self.Y = ma.asarray(Y)

        #the fitted image result is initialized to None
        self.fitted = None
        self.results = None
        self.errs = None
        self.good_fit = False

        #list of the parameter string names, must be implemented
        self.par_names = tuple([])

    def guess_gauss_par0(self, slc_main=None, slc_max=None, slc_bkg=None):
        """
        Guess and returns the initial gaussian parameters from the slices

        Args:
            slc_main (tuple): tuple of 2 slices for the coordinates of the main
            area for the gaussian center guess
            slc_max (tuple): tuple of 2 slices for the coordinates of the
            maximal area for the gaussian amplitude guess
            slc_bkg (tuple): tuple of 2 slices for the coordinates of the
            background area for the gaussian offset guess

        Returns:
            Tuple with the Gaussian guessed parameters
        """
        if slc_main is None:
            height, width = self.img0.shape
            slc_main = slice(None)
            ym, xm = np.unravel_index(self.img0.argmax(), self.img0.shape)
        else:
            height, width = self.img0[slc_main].shape
            xm = ma.mean(slc_main[1].indices(self.img0.shape[1])[0:-1])
            ym = ma.mean(slc_main[0].indices(self.img0.shape[0])[0:-1])

        offs = ma.mean(self.img0[slc_bkg])
        if slc_max is None:
            slc_max = slice(None)
            
        amp1 = ma.mean(self.img0[slc_max])
        if offs is ma.masked:
#            print('bkg mascherato')
            offs = 0
#        print(type(offs))
#        print(offs, amp1, xm, ym, width/4.0, height/4.0)
        return (offs, amp1, xm, ym, width/4.0, height/4.0)

    def guess_par0(self, *args, **kwargs):
        """
        Parameters guess for the specific function (must be overridden).
        """
        pass

    def function(self, *args, **kwargs):
        """
        Specific function (must be overridden).
        """
        pass

    def fit(self, full_output=False):
        """
        Performs the fitting operations and returns a dictionary with the
        fitted parameters.
        outputs: results_dict, errors_dict [, covmat (optional)]
        """
        frame = self.img0
        err = lambda p, x, y: ma.ravel(y - self.function(x, *p))
        args=((self.X, self.Y), frame.ravel())
        try:
            results = leastsq(err, self.par0,
                              args=args,
                              full_output=1)
            results_dict = dict(list(zip(self.par_names, results[0])))
            errors_dict = dict(list(zip(self.par_names,
                                    np.sqrt(np.diag(results[1])))))
            self.good_fit = True
            self.results = results_dict
            self.errs = errors_dict
            if full_output:
                covmat = results[1]
                opt_output = results[2:]
                return results_dict, errors_dict, covmat, opt_output
            else:
                return results_dict, errors_dict
        except RuntimeError:
            print("Error while fitting")
            self.good_fit = False
            if full_output:
                return None, None, None, None
            else:
                return None, None
            
    def print_res(self):
        if self.good_fit:
            for k in sorted(self.results.keys()):
                print('{}: {:03.2f} /pm {:03.2f}'.format(k, self.results[k], self.errs[k]))
        else:
            print('No print')
            
    def save(self, filename, sep=',', mode='w'):
        if not self.good_fit:
            print('No save')
            return
        with open(filename, mode) as f:
            f.write(self.__class__.__name__ + '\n')
            f.write('# Results\n')
            for k in self.results.keys():
                line = sep.join([k, str(self.results[k]), str(self.errs[k])])
                f.write(line +  ' \n')
    
   
        
class Bimodal1d(Fitting1d):
    """
    Classe di fit bimodale 1d
    """
    
    def __init__(self, data, par0=None):
        super(Bimodal1d, self).__init__(data, par0=par0)
        self.par_names = ["amp1", "mx", "sx", "amp2", "rx"]
        if par0 is None:
            self.init_par0()

    def function(self, X, amp1, mx, sx, amp2, rx):
        g = np.exp(- (X - mx)**2 / (2*sx**2))
        b = np.maximum((1 - (X-mx)**2 / rx**2), 0)
        self.fitted = amp1*g + amp2*b**2 
        return self.fitted

    def init_par0(self):
        amp1 = float(self.data.max()) / 3
        mx = float(self.X.mean())
        sx = self.X.std()
        amp2 = amp1
        rx = sx / 2
        par0 = (amp1, mx, sx, amp2, rx)
        self.par0 = par0
        return par0        

class Bimodal1d_pressure(Bimodal1d):
    """
    Classe di fit bimodale 1d -- 
    """
    
    def __init__(self, *args, **kwargs):
        super(Bimodal1d_pressure, self).__init__(*args, **kwargs)


class Bimodal1d_density(Fitting1d):
    """
    Classe di fit bimodale 1d
    """
    
    def __init__(self, data, par0=None):
        super(Bimodal1d_density, self).__init__(data, par0=par0)
        self.par_names = ["amp1", "mx", "sx", "amp2", "rx"]
        if par0 is None:
            self.init_par0()

    def function(self, X, amp1, mx, sx, amp2, rx):
        g = np.exp(- (X - mx)**2 / (2*sx**2))
        b = np.maximum((1 - (X-mx)**2 / rx**2), 0)
        self.fitted = amp2*b +amp1*g
        return self.fitted

    def init_par0(self):
        amp1 = float(self.data.max()) / 3
        mx = float(self.X.mean())
        sx = self.X.std()
        amp2 = amp1
        rx = sx / 2
        par0 = (amp1, mx, sx, amp2, rx)
        self.par0 = par0
        return par0
        
class TFermi1d_density(Fitting1d):
    """
    Classe di fit bimodale 1d
    """
    
    def __init__(self, data, par0=None):
        super(TFermi1d_density, self).__init__(data, par0=par0)
        self.par_names = ["amp2", "mx", "rx",]
        if par0 is None:
            self.init_par0()

    def function(self, X, amp2, mx, rx,):
        b = np.maximum((1 - (X-mx)**2 / rx**2), 0)
        self.fitted = amp2*b
        return self.fitted

    def init_par0(self):
        amp2 = float(self.data.max()) / 3
        mx = float(self.X.mean())
        rx = self.X.std()
        par0 = (amp2, mx, rx,)
        self.par0 = par0
        return par0       
        
class TFermi1d_pressure(Fitting1d):
    """
    Classe di fit bimodale 1d
    """
    
    def __init__(self, data, par0=None):
        super(TFermi1d_pressure, self).__init__(data, par0=par0)
        self.par_names = ["amp2", "mx", "rx",]
        if par0 is None:
            self.init_par0()

    def function(self, X, amp2, mx, rx,):
        b = np.maximum((1 - (X-mx)**2 / rx**2), 0)
        self.fitted = amp2*b**2
        return self.fitted

    def init_par0(self):
        amp2 = float(self.data.max()) / 3
        mx = float(self.X.mean())
        rx = self.X.std()
        par0 = (amp2, mx, rx,)
        self.par0 = par0
        return par0       
''' ora i fit 2d per gaussiana, thomasfermi e bimodale '''


class Bose2d_meno_parametri(Fitting2d):
    """
    Bose-enhanced integrated 2D fit.
    """
    
    def __init__(self, img0, mx, my, par0=None, nu=5/2, order=6):
        super(Bose2d_meno_parametri, self).__init__(img0, par0)
        self.par_names = ["amp1", "mu", "sx", "sy", "alpha"]
        self.nu = nu
        self.order = order
        self.mx = mx
        self.my = my
            
    def function(self, XY, amp1, mu, sx, sy,):
        """
        Implements the bose fitting function.
        (see gaussian() and bose_g())
        """
        zeta = np.exp(mu) * gaussian(XY, self.mx, self.my, sx, sy, 0)    
        self.fitted = amp1* bose_g(zeta, self.nu, self.order)
        return self.fitted.ravel()

    def guess_par0(self, slc_main=None, slc_max=None, slc_bkg=None):
        """
        Implements the gaussian parameter guess from slices.
        (see Fitting.guess_gauss_par0())
        """
        offs, amp1, mx, my, sx, sy = self.guess_gauss_par0(slc_main,
                                                           slc_max,
                                                           slc_bkg)
        alpha0 = -1.
        mu0 = 1
#        par0 = (offs, amp1, mx, my, sx, sy, alpha0)
#        par0 = (offs, amp1, mu0, mx, my, sx, sy, alpha0)
        par0 = (amp1, mu0, sx, sy, )


        self.par0 = par0
        return par0

class Bose2d(Fitting2d):
    """
    Bose-enhanced integrated 2D fit.
    """
    
    def __init__(self, img0, par0=None, nu=2, order=6):
        super(Bose2d, self).__init__(img0, par0)
        self.par_names = ["offs", "amp1", "mu", "mx", "my", "sx", "sy", "alpha"]
        self.nu = nu
        self.order = order
            
    def function(self, XY, offs, amp1, mu, mx, my, sx, sy, alpha):
        """
        Implements the bose fitting function.
        (see gaussian() and bose_g())
        """
        zeta = np.exp(mu) * gaussian(XY, mx, my, sx, sy, alpha)    
        self.fitted = amp1* bose_g(zeta, self.nu, self.order) + offs
        return self.fitted.ravel()

    def guess_par0(self, slc_main=None, slc_max=None, slc_bkg=None):
        """
        Implements the gaussian parameter guess from slices.
        (see Fitting.guess_gauss_par0())
        """
        offs, amp1, mx, my, sx, sy = self.guess_gauss_par0(slc_main,
                                                           slc_max,
                                                           slc_bkg)
        alpha0 = -1.
        mu0 = 1
#        par0 = (offs, amp1, mx, my, sx, sy, alpha0)
        par0 = (offs, amp1, mu0, mx, my, sx, sy, alpha0)

        self.par0 = par0
        return par0

class Gauss2d(Fitting2d):
    """
    Gaussian 2D fit.
    2015-05-15 ho rimosso l'offset
    2015-05-18 ho messo di nuovo l'offset
    """
    def __init__(self, img0, par0=None):
        super(Gauss2d, self).__init__(img0, par0)
        self.par_names = ["offs", "amp1", "mx", "my", "sx", "sy", "alpha"]

    def function(self, XY, offs, amp1, mx, my, sx, sy, alpha):
        """
        Implements the gaussian fitting function.
        (see gaussian() and thomasfermi())
        """
        self.fitted = amp1*gaussian(XY, mx, my, sx, sy, alpha) + offs
        return self.fitted.ravel()

    def guess_par0(self, slc_main=None, slc_max=None, slc_bkg=None):
        """
        Implements the gaussian parameter guess from slices.
        (see Fitting.guess_gauss_par0())
        """
        offs, amp1, mx, my, sx, sy = self.guess_gauss_par0(slc_main,
                                                           slc_max,
                                                           slc_bkg)
        alpha0 = -1.
#        par0 = (offs, amp1, mx, my, sx, sy, alpha0)
        par0 = (offs, amp1, mx, my, sx, sy, alpha0)

        self.par0 = par0
        return par0
        
class Gauss2d_no_offs(Fitting2d):
    """
    Gaussian 2D fit.
    2015-05-18 no offset
    """
    def __init__(self, img0, par0=None):
        super(Gauss2d_no_offs, self).__init__(img0, par0)
        self.par_names = ["amp1", "mx", "my", "sx", "sy", "alpha"]

    def function(self, XY, amp1, mx, my, sx, sy, alpha):
        """
        Implements the gaussian fitting function.
        (see gaussian() and thomasfermi())
        """
        self.fitted = amp1*gaussian(XY, mx, my, sx, sy, alpha)
        return self.fitted.ravel()

    def guess_par0(self, slc_main=None, slc_max=None, slc_bkg=None):
        """
        Implements the gaussian parameter guess from slices.
        (see Fitting.guess_gauss_par0())
        """
        offs, amp1, mx, my, sx, sy = self.guess_gauss_par0(slc_main,
                                                           slc_max,
                                                           slc_bkg)
        alpha0 = -1.
#        par0 = (offs, amp1, mx, my, sx, sy, alpha0)
        par0 = (amp1, mx, my, sx, sy, alpha0)

        self.par0 = par0
        return par0


class ThomasFermi2d(Fitting2d):
    """
    Thomas-Fermi 2D fit (inverted parabola).
    """
    def __init__(self, img0, par0=None):
        super(ThomasFermi2d, self).__init__(img0, par0)
        self.par_names = ["offs", "amp1", "mx", "my", "rx", "ry", "alpha"]

    def function(self, XY, offs, amp2, mx, my, rx, ry, alpha):
        """
        Implements the Thomas-Fermi fitting function.
        (see gaussian() and thomasfermi())
        """
        self.fitted = amp2*thomasfermi(XY, mx, my, rx, ry, alpha) + offs
        return self.fitted.ravel()

    def guess_par0(self, slc_main, slc_max, slc_bkg):
        """
        Implements the Thomas-Fermi parameter guess.
        (see Fitting.guess_gauss_par0())
        """
        offs, amp1, mx, my, sx, sy = self.guess_gauss_par0(slc_main,
                                                           slc_max,
                                                           slc_bkg)
        alpha0 = 10.
        par0 = (offs, amp1, mx, my, sx*2.0, sy*2.0, alpha0)

        self.par0 = par0
        return par0


class Bimodal2d(Gauss2d, ThomasFermi2d):
    """
    Gaussian+Thomas Fermi bimodal 2D fit.
    2015-05-15 ho rimosso l'offset
    """
    def __init__(self, img0, par0=None):
        super(Bimodal2d, self).__init__(img0, par0)
        self.par_names = ["offs", "amp1", "mx", "my", "sx", "sy",
                          "amp2", "rx", "ry", "alpha"]

    def function(self, XY, offs, amp1, mx, my, sx, sy, amp2, rx, ry, alpha):
        """
        Implements the bimodal fitting function.
        (see gaussian() and thomasfermi())
        """
        self.fitted = amp1*gaussian(XY, mx, my, sx, sy, alpha) +\
                      amp2*thomasfermi(XY, mx, my, rx, ry, alpha) + offs
        return self.fitted.ravel()

    def guess_par0(self, slc_main, slc_max, slc_bkg):
        """
        Implements the bimodal parameter guess.
        (see Fitting.guess_gauss_par0())
        """
        offs, amp1, mx, my, sx, sy = self.guess_gauss_par0(slc_main,
                                                           slc_max,
                                                           slc_bkg)
        alpha0 = 1.
#        par0 = (offs, amp1/2.0, mx, my, sx, sy, amp1/2.0, sx*2.0, sy*2.0, alpha0)
        par0 = (offs, amp1/2.0, mx, my, sx, sy, amp1/2.0, sx*2.0, sy*2.0, alpha0)

        self.par0 = par0
        return par0
        
class Bimodal2d_no_offs(Gauss2d, ThomasFermi2d):
    """
    Gaussian+Thomas Fermi bimodal 2D fit.
    2015-05-15 ho rimosso l'offset
    """
    def __init__(self, img0, par0=None):
        super(Bimodal2d_no_offs, self).__init__(img0, par0)
        self.par_names = ["amp1", "mx", "my", "sx", "sy",
                          "amp2", "rx", "ry", "alpha"]

    def function(self, XY, amp1, mx, my, sx, sy, amp2, rx, ry, alpha):
        """
        Implements the bimodal fitting function.
        (see gaussian() and thomasfermi())
        """
        self.fitted = amp1*gaussian(XY, mx, my, sx, sy, alpha) +\
                      amp2*thomasfermi(XY, mx, my, rx, ry, alpha)
        return self.fitted.ravel()

    def guess_par0(self, slc_main, slc_max, slc_bkg):
        """
        Implements the bimodal parameter guess.
        (see Fitting.guess_gauss_par0())
        """
        offs, amp1, mx, my, sx, sy = self.guess_gauss_par0(slc_main,
                                                           slc_max,
                                                           slc_bkg)
        alpha0 = 1.
#        par0 = (offs, amp1/2.0, mx, my, sx, sy, amp1/2.0, sx*2.0, sy*2.0, alpha0)
        par0 = (amp1/2.0, mx, my, sx, sy, amp1/2.0, sx*2.0, sy*2.0, alpha0)

        self.par0 = par0
        return par0


def reloadFittedBimodal(database, fid):
    D = eval(database.ix[fid].unpack_dict)
    H, L = D['frame_size']
    x = np.arange(L)
    y = np.arange(H)
    XY = np.meshgrid(x, y)
    d = database.ix[fid][["amp1", "mx", "my", "sx", "sy", "amp2", "rx", "ry", "alpha"]]
    return bimodal(XY, **d)

def bimodAxialDensity(X, amp1, mx, my, sx, sy, amp2, rx, ry, part=None):
    """ Computes the axial density from the bimodal fit parameters"""
    g = np.exp(- (X - mx*pixel_length)**2 / (2*sx**2* pixel_length**2))
    b = np.maximum((1 - (X-mx* pixel_length)**2 / (rx**2* pixel_length**2)), 0)
    nt0 = amp1 / (np.sqrt(2*np.pi) * sy)
    nc0 = amp2 / (4*ry/3)
    if part == 'gauss':
        return nt0*g /(sigma_transv*pixel_length)
    elif part == 'tf':
        return nc0*b /(sigma_transv*pixel_length)
    else:
        return (nt0*g + nc0*b) /(sigma_transv*pixel_length)

def reloadAxialDensity(database, fid, x=None, part=None):
    """ Returns the 1D vector with the axial density, as calculated FROM THE BIMODAL FIT of the raccordo"""
    D = eval(database.ix[fid].unpack_dict)
    H, L = D['frame_size']
    if x is None:
        x = np.arange(L) * pixel_length
    d = database.ix[fid][["amp1", "mx", "my", "sx", "sy", 
    "amp2", "rx", "ry",]]
    return bimodAxialDensity(x, part=part, **d)
    

