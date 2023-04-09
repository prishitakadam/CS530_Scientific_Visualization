from PyQt6.QtWidgets import QApplication
# import PyQt6.QtCore as QtCore
from PyQt6.QtCore import Qt
# from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
# from vtk.util.misc import vtkGetDataRoot
# import vtk
import argparse
import sys
import h5py
# import sys
# import json
# import numpy as np
# import pandas as pd

# Load Class
from Temperature import Temperature
from Density import Density
from Dark_Matter_Density import Dark_Matter_Density

def get_data(filename, vrtype):
    with h5py.File(filename, 'r') as f:
        data = list(f[vrtype])
        return data

def get_window(filename, vrtype):
    # Data order: ['Bx', 'By', 'Bz', 'Dark_Matter_Density', 'Density', 'Temperature']
    if vrtype == 'temperature':
        data = get_data(filename, 'Temperature')
        window = Temperature(data)
    elif vrtype == 'density':
        data = get_data(filename, 'Density')
        window = Density(data)
    elif vrtype == 'dark_matter_density':
        data = get_data(filename, 'Dark_Matter_Density')
        window = Dark_Matter_Density(data)
    else:
        print('Invalid Attribute provided for volume rendering. Select one from: [Temperature, Density, Dark_Matter_Density]')
    return window



if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Cluster Temperature')
    parser.add_argument('-i','--input', type=str, required=True, help='Input data')
    parser.add_argument('-vrtype','--vrtype', type=str, required=False, default='temperature', help='Select attribute for volume rendering')

    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = get_window(filename=args.input, vrtype=args.vrtype.lower())
    window.ui.vtkWidget.GetRenderWindow().SetSize(1024, 1024)
    window.show()
    window.setWindowState(Qt.WindowState.WindowMaximized)
    window.iren.Initialize()
    sys.exit(app.exec())
