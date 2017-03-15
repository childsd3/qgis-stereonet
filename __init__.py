# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Stereonet
                                 A QGIS plugin
 Displays a geologic stereonet of selected data
                             -------------------
        begin               : 2016-11-29
        copyright           : (C) 2016 by Daniel Childs
        email               : daniel@childsgeo.com
        git sha             : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                          *
 *   This program is free software; you can redistribute it and/or modify   *
 *   it under the terms of the GNU General Public License as published by   *
 *   the Free Software Foundation; either version 2 of the License, or      *
 *   (at your option) any later version.                                    *
 *                                                                          *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import mplstereonet
from qgis.core import *
from qgis.gui import *
import qgis.utils
import os

def classFactory(iface):
    return Stereonet(iface)

class Stereonet:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.contourAction = QAction(QIcon(str(dir_path)+"/icon.png"), u'Stereonet', self.iface.mainWindow())
        self.contourAction.triggered.connect(self.contourPlot)
        self.iface.addToolBarIcon(self.contourAction)

    def unload(self):
        self.iface.removeToolBarIcon(self.contourAction)
        del self.contourAction
    def contourPlot(self):
        fig, ax = mplstereonet.subplots()
        strikes = list()
        dips = list()
        layers = self.iface.legendInterface().layers()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                iter = layer.selectedFeatures()
                strikeExists = layer.fieldNameIndex('strike')
                ddrExists = layer.fieldNameIndex('ddr')
                dipExists = layer.fieldNameIndex('dip')
                for feature in iter:
                    if strikeExists != -1 and dipExists != -1:
                        strikes.append(feature['strike'])
                        dips.append(feature['dip'])
                    elif ddrExists != -1 and dipExists != -1:
                        strikes.append(feature['ddr']-90)
                        dips.append(feature['dip'])
            else:
                continue
        cax = ax.density_contourf(strikes, dips, measurement='poles',cmap=cm.coolwarm)
        ax.pole(strikes, dips, 'k+', markersize=7)
        ax.grid(True)
#        fig.colorbar(cax)
        plt.show()