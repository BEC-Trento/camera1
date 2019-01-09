# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui

from .ui.display_widget_ui import Ui_DisplayWidget

import pyqtgraph as pg
from .ui.mpl_cmaps import mpl_cmap_d
from pyqtgraph import debug

try:
    from bottleneck import nanmin, nanmax
except ImportError:
    from numpy import nanmin, nanmax
import numpy as np
#import pyqtgraph as pg
#print(pg)
#pg.setConfigOption('background', 'k')
#pg.setConfigOption('imageAxisOrder', 'row-major')


class DisplayQWidget(QtGui.QWidget):
    """
    Mostly a re-implementation of pyqtgraph.ImageView, adapted to our needs.
    """
    #TODO: decide if the 'time series' options are still needed:
    #      either delete or rewrite them in a better way.
    def __init__(self, parent=None, *args, **kwargs):
        super(DisplayQWidget, self).__init__(parent=parent, *args, **kwargs)
        self.levelMax = 2.5
        self.levelMin = -0.05
        self.image = None
        self.axes = {}
        self.imageDisp = None
        self.ui = Ui_DisplayWidget()
        self.ui.setupUi(self)
        self.scene = self.ui.graphicsView.scene()
                
        self.view = pg.ViewBox()
        self.ui.graphicsView.setCentralItem(self.view)
        self.view.setAspectLocked(True)
        self.view.invertY()
        
        
        self.imageItem = pg.ImageItem()
        self.imageItem.axisOrder = 'row-major'
        self.view.addItem(self.imageItem)
        
        self.ui.histogram.setImageItem(self.imageItem)
        
        ## wrap functions from view box
        for fn in ['addItem', 'removeItem']:
            setattr(self, fn, getattr(self.view, fn))

        ## wrap functions from histogram
        for fn in ['setHistogramRange', 'autoHistogramRange', 'getLookupTable', 'getLevels']:
            setattr(self, fn, getattr(self.ui.histogram, fn))
            
        # get plotWidgets as self attributes
        for attr in ['xPlotWidget', 'yPlotWidget']:
            setattr(self, attr, getattr(self.ui, attr))
#                
#        
        self.xPlotWidget.showGrid(True)
        self.yPlotWidget.showGrid(True)
        self.yPlotWidget.invertY(True)
        


        # 1D array of coordinates
        self.x = None
        self.y = None
        # 2D array
        self.X, self.Y = None, None
        
        
        self.xPlotWidget.setMouseEnabled(True, True)
        self.yPlotWidget.setMouseEnabled(True, True)
#        self.x_profile.show()
#        self.y_profile.show()
#        self.roiChanged()
        
        self.timeLine = pg.InfiniteLine(0, movable=True)
        self.timeLine.setPen((255, 255, 0, 200))
        self.timeLine.setZValue(1)
        
        self.keysPressed = {}
        self.playTimer = QtCore.QTimer()
        self.playRate = 0
        self.lastPlayTime = 0
        
        self.ui.cmapComboBox.addItems(list(mpl_cmap_d.keys()))
        self.ui.cmapComboBox.setCurrentIndex(13) # gray cmap
        self.ui.cmapComboBox.currentIndexChanged[str].connect(self.set_mpl_colormap)
        

#        self.xPlotWidget.registerPlot(self.name + '_X')
#        self.yPlotWidget.registerPlot(self.name + '_Y')
#        self.view.register(self.name)
        
        self.noRepeatKeys = [QtCore.Qt.Key_Right, QtCore.Qt.Key_Left, QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown]
        
        self.bgroi = pg.RectROI(pos=[10,10], size=[2000,200],  pen='r',)
        self.bgroi.addScaleHandle([1, 1], [0, 0])
        self.bgroi.addRotateHandle([0, 0], [0.5, 0.5])
        self.view.addItem(self.bgroi)
        
        self.setImage(np.ones((2048, 2048)))
        
    def setImage(self, img, tvals=None, autoRange=True, autoLevels=False, levels=None, axes=None, pos=None, scale=None, transform=None, autoHistogramRange=True):
        """
        Set the image to be displayed in the widget.
        
        ================== ===========================================================================
        **Arguments:**
        img                (numpy array) the image to be displayed. See :func:`ImageItem.setImage` and
                           *notes* below.
        tvals              (numpy array) 1D array of z-axis values corresponding to the third axis
                           in a 3D image. For video, this array should contain the time of each frame.
                           in a 3D image. For video, this array should contain the time of each frame.
        autoRange          (bool) whether to scale/pan the view to fit the image.
        autoLevels         (bool) whether to update the white/black levels to fit the image.
        levels             (min, max); the white and black level values to use.
        axes               Dictionary indicating the interpretation for each axis.
                           This is only needed to override the default guess. Format is::
                              
                               {'t':None, 'x':1, 'y':0, 'c':None}  for standard 2D matrices
                               {'t':0, 'x':2, 'y':1, 'c':None}     for 3D time-series or
                               {'t':None, 'x':1, 'y':0, 'c':2}     if rgba color is stored in the last axis.
                               
                               ### {'t':0, 'x':1, 'y':2, 'c':3};
        
        pos                Change the position of the displayed image
        scale              Change the scale of the displayed image
        transform          Set the transform of the displayed image. This option overrides *pos*
                           and *scale*.
        autoHistogramRange If True, the histogram y-range is automatically scaled to fit the
                           image data.
        ================== ===========================================================================

        **Notes:**        
        Image data is set to be in row-major order (row, column).
        
        """
        profiler = debug.Profiler()
        
        if hasattr(img, 'implements') and img.implements('MetaArray'):
            img = img.asarray()
        
        if not isinstance(img, np.ndarray):
            required = ['dtype', 'max', 'min', 'ndim', 'shape', 'size']
            if not all([hasattr(img, attr) for attr in required]):
                raise TypeError("Image must be NumPy array or any object "
                                "that provides compatible attributes/methods:\n"
                                "  %s" % str(required))
        
        self.image = img
        self.imageDisp = None
        
        profiler()
        
        if axes is None:
            x,y = (0, 1) if self.imageItem.axisOrder == 'col-major' else (1, 0)
            
            if img.ndim == 2:
                self.axes = {'t': None, 'x': x, 'y': y, 'c': None}
            elif img.ndim == 3:
                # Ambiguous case; make a guess
                if img.shape[2] <= 4:
                    self.axes = {'t': None, 'x': x, 'y': y, 'c': 2}
                else:
                    self.axes = {'t': 0, 'x': x+1, 'y': y+1, 'c': None}
            elif img.ndim == 4:
                # Even more ambiguous; just assume the default
                self.axes = {'t': 0, 'x': x+1, 'y': y+1, 'c': 3}
            else:
                raise Exception("Can not interpret image with dimensions %s" % (str(img.shape)))
        elif isinstance(axes, dict):
            self.axes = axes.copy()
        elif isinstance(axes, list) or isinstance(axes, tuple):
            self.axes = {}
            for i in range(len(axes)):
                self.axes[axes[i]] = i
        else:
            raise Exception("Can not interpret axis specification %s. Must be like {'t': 2, 'x': 0, 'y': 1} or ('t', 'x', 'y', 'c')" % (str(axes)))
            
        for x in ['t', 'x', 'y', 'c']:
            self.axes[x] = self.axes.get(x, None)
        axes = self.axes

        self.x = np.arange(img.shape[axes['x']])
        self.y = np.arange(img.shape[axes['y']])
        
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        if tvals is not None:
            self.tVals = tvals
        elif axes['t'] is not None:
            if hasattr(img, 'xvals'):
                try:
                    self.tVals = img.xvals(axes['t'])
                except:
                    self.tVals = np.arange(img.shape[axes['t']])
            else:
                self.tVals = np.arange(img.shape[axes['t']])
                

        profiler()
        
        
        self.currentIndex = 0
        
        self.updateImage(autoHistogramRange=autoHistogramRange)
        if autoLevels:
            self.autoLevels()
        else:
            if levels is None:
                self.defaultLevels()
            else:
                self.setLevels(*levels)
            

        

        profiler()

        if self.axes['t'] is not None:
            #self.ui.roiPlot.show()
            self.ui.roiPlot.setXRange(self.tVals.min(), self.tVals.max())
            self.timeLine.setValue(0)
            #self.ui.roiPlot.setMouseEnabled(False, False)
            if len(self.tVals) > 1:
                start = self.tVals.min()
                stop = self.tVals.max() + abs(self.tVals[-1] - self.tVals[0]) * 0.02
            elif len(self.tVals) == 1:
                start = self.tVals[0] - 0.5
                stop = self.tVals[0] + 0.5
            else:
                start = 0
                stop = 1
            for s in [self.timeLine, self.normRgn]:
                s.setBounds([start, stop])
        #else:
            #self.ui.roiPlot.hide()
            
        
        profiler()

        self.imageItem.resetTransform()
        if scale is not None:
            self.imageItem.scale(*scale)
        if pos is not None:
            self.imageItem.setPos(*pos)
        if transform is not None:
            self.imageItem.setTransform(transform)

        profiler()

        if autoRange:
            self.autoRange()

        profiler()
        
            
    def updateImage(self, autoHistogramRange=True):
        ## Redraw image on screen
        if self.image is None:
            print('Image is none')
            return
            
        image = self.image
        
        if autoHistogramRange:
            self.ui.histogram.setHistogramRange(self.levelMin, self.levelMax)
        
        # Transpose image into order expected by ImageItem
        if self.imageItem.axisOrder == 'col-major':
            axorder = ['t', 'x', 'y', 'c']
        else:
            axorder = ['t', 'y', 'x', 'c']
        axorder = [self.axes[ax] for ax in axorder if self.axes[ax] is not None]
#        image = image.transpose(axorder)
            
        # Select time index
        if self.axes['t'] is not None:
            self.ui.roiPlot.show()
            image = image[self.currentIndex]
            
        self.imageItem.updateImage(image, autoLevels=False)
        
        
    def setColorMap(self, colormap):
        """Set the color map. 

        ============= =========================================================
        **Arguments**
        colormap      (A ColorMap() instance) The ColorMap to use for coloring 
                      images.
        ============= =========================================================
        """
        self.ui.histogram.gradient.setColorMap(colormap)
        
    def set_mpl_colormap(self, name='gist_stern'):  
        try:
            pos, vals = mpl_cmap_d[name]
        except KeyError:
            print("KeyError: '{:s}'. Falling back to grayscale".format(name))
#            warnings.warn(e)
            pos, vals = mpl_cmap_d['gray']
        cmap = pg.colormap.ColorMap(pos, vals)
        self.setColorMap(cmap)        

    
    def autoLevels(self):
        """Set the min/max intensity levels automatically to match the image data."""
        lmin, lmax = self.quickMinMax(self.image)
        self.setLevels(lmin, lmax)
    
    def defaultLevels(self):
        """Set the min/max intensity levels automatically to the built-in values."""
        self.setLevels(self.levelMin, self.levelMax)

    def setLevels(self, levelmin, levelmax):
        """Set the min/max (bright and dark) levels."""
        self.ui.histogram.setLevels(levelmin, levelmax)
        self.ui.histogram.setHistogramRange(levelmin, levelmax)

    def autoRange(self):
        """Auto scale and pan the view around the image such that the image fills the view."""
        self.view.autoRange()
        
    def close(self):
        """Closes the widget nicely, making sure to clear the graphics scene and release memory."""
        self.ui.roiPlot.close()
        self.ui.graphicsView.close()
        self.scene.clear()
        del self.image
        del self.imageDisp
        super(DisplayQWidget, self).close()
        self.setParent(None)
        

            
    def clear(self):
        self.image = None
        self.imageItem.clear()
        

        
    def setCurrentIndex(self, ind):
        """Set the currently displayed frame index."""
        self.currentIndex = np.clip(ind, 0, self.image.shape[self.axes['t']]-1)
        self.updateImage()
        self.ignoreTimeLine = True
        self.timeLine.setValue(self.tVals[self.currentIndex])
        self.ignoreTimeLine = False

  
    def hasTimeAxis(self):
        return 't' in self.axes and self.axes['t'] is not None

    def quickMinMax(self, data):
        """
        Estimate the min/max values of *data* by subsampling.
        """
        while data.size > 1e6:
            ax = np.argmax(data.shape)
            sl = [slice(None)] * data.ndim
            sl[ax] = slice(None, None, 2)
            data = data[sl]
        return nanmin(data), nanmax(data)
        


    def getView(self):
        """Return the ViewBox (or other compatible object) which displays the ImageItem"""
        return self.view
        
    def getImageItem(self):
        """Return the ImageItem for this ImageView."""
        return self.imageItem
        
    def getRoiPlot(self):
        """Return the ROI PlotWidget for this ImageView"""
        return self.ui.roiPlot
       
    def getHistogramWidget(self):
        """Return the HistogramLUTWidget for this ImageView"""
        return self.ui.histogram

    def export(self, fileName):
        """
        Export data from the ImageView to a file, or to a stack of files if
        the data is 3D. Saving an image stack will result in index numbers
        being added to the file name. Images are saved as they would appear
        onscreen, with levels and lookup table applied.
        """
        img = self.image
        if self.hasTimeAxis():
            base, ext = os.path.splitext(fileName)
            fmt = "%%s%%0%dd%%s" % int(np.log10(img.shape[0])+1)
            for i in range(img.shape[0]):
                self.imageItem.setImage(img[i], autoLevels=False)
                self.imageItem.save(fmt % (base, i, ext))
            self.updateImage()
        else:
            self.imageItem.save(fileName)
            
    def exportClicked(self):
        fileName = QtGui.QFileDialog.getSaveFileName()
        if fileName == '':
            return
        self.export(fileName)



        
if __name__ == '__main__':
    import sys
#    from imageio import read_sis as readsis
    from roi import ROI
    app = QtGui.QApplication(*sys.argv)

    win = DisplayQWidget()
#    win.set_mpl_colormap('viridis')
    
    im = np.load('../testing/mypicture_spinor.npy')
    win.setImage(im)
#    im = readsis('../testing/mypicture.sis', verbose=True)[0]/(2**16/10)
#    im_npy = np.load('testing/mypicture.npy')
#    im_sis = readsis('testing/mypicture.sis', verbose=True)[0]/(2**16/10)
#    
#    win.setImage(im_npy - im_sis,)# autoLevels=True)


    
    roi1 = ROI(win, pos=(0, 500), size=(1000, 500))
    
    roi2 = ROI(win, pos=(100, 300), size=(800, 300), color='r')
#    win = pg.ImageView()

    win.show()
    sys.exit(app.exec_())
