# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Stereonet
                                 A QGIS plugin
 Displays a geologic stereonet of selected data
                             -------------------
        begin                : 2016-11-29
        copyright            : (C) 2016 by Daniel Childs
        email                : daniel@childsgeo.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
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

        
        print(dir_path)

    def unload(self):
        self.iface.removeToolBarIcon(self.contourAction)
        del self.contourAction
    #stereonetWithoutContour is unused as of now
    def stereonetWithoutContour(self):
        plt.rcParams['toolbar'] = 'None'
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='stereonet')
        strikes = list()
        dips = list()
        try:
            layer = qgis.utils.iface.activeLayer()
            iter = layer.selectedFeatures()
            for feature in iter:
                strikes.append(feature['ddr']-90)
                dips.append(feature['dip'])
            ax.pole(strikes, dips, 'k+', markersize=7)
            ax.grid()
            plt.show()
        except:
            return
    def contourPlot(self):
        fig, ax = mplstereonet.subplots()
        strikes = list()
        dips = list()
        try:
            layers = self.iface.legendInterface().layers()
            for layer in layers:
                iter = layer.selectedFeatures()
                for feature in iter:
                    strikes.append(feature['ddr']-90)
                    dips.append(feature['dip'])
            cax = ax.density_contourf(strikes, dips, measurement='poles',cmap=cm.coolwarm)
            ax.pole(strikes, dips, 'k+', markersize=7)
            ax.grid(True)
            fig.colorbar(cax)
            plt.show()
        except:
            return