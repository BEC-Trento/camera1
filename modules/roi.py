#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Fri Feb 10 21:23:33 2017
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
import numpy as np
import pyqtgraph as pg

class ROI(pg.RectROI):
    def __init__(self, displayWidget, pos=[0,0], size=[1,1], color='w', *args, **kwargs):
        """
        color: colorspec
        """
        super(ROI, self).__init__(pos=pos, size=size,  pen=color, *args, **kwargs)
        self.addScaleHandle([1, 1], [0, 0])
        self.addRotateHandle([0, 0], [0.5, 0.5])
        
        self.link_to_display(displayWidget)
        
        self.pen = pg.mkPen(color=color)
        self.x_profile.setPen(self.pen)
        self.y_profile.setPen(self.pen)
        
        self.sigRegionChanged.connect(self.updateRoi)
        self.sigRegionChangeFinished.connect(self.call_fit)
        
        self.updateRoi()
        
    def link_to_display(self, displayWidget):
        self.displayWidget = displayWidget
        self.imageItem = displayWidget.imageItem
        self.x_profile = self.displayWidget.xPlotWidget.plot()
        self.y_profile = self.displayWidget.yPlotWidget.plot()
        
        self.x_fit = self.displayWidget.xPlotWidget.plot()
        self.y_fit = self.displayWidget.yPlotWidget.plot()
        displayWidget.view.addItem(self)
        
        
    def updateRoi(self):
        image = self.displayWidget.image
        if image is None:
            return
        if image.ndim == 2:
            axes = (0, 1)
        elif image.ndim == 3:
            axes = (1, 2)
        else:
            return
        
        arrayslice = self.getArraySlice(image.view(np.ndarray), self.imageItem, axes, returnSlice=True)
        if arrayslice is not None and image is not None:
            roi_slice = arrayslice[0]
            data = image[roi_slice]
            xsum = data.sum(0)
            ysum = data.sum(1)
            xvals = self.displayWidget.x[roi_slice[1]]
            yvals = self.displayWidget.y[roi_slice[0]]
            self.x_profile.setData(y=xsum, x=xvals)
            self.y_profile.setData(x=ysum, y=yvals)
        else:
            print('slice none')
            
    def call_fit(self,):
        raise NotImplementedError
