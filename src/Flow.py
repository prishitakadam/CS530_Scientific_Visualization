from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import argparse
import sys
import h5py

from utils.flow.MagneticField import MagneticField

def get_data(filename):
    with h5py.File(filename, 'r') as f:
        bx = list(f['Bx'])
        by = list(f['By'])
        bz = list(f['Bz'])
        return [bx, by, bz]

def get_velocity_data(filename):
    with h5py.File(filename, 'r') as f:
        bx = list(f['x-velocity'])
        by = list(f['y-velocity'])
        bz = list(f['z-velocity'])
        return [bx, by, bz]

def get_window(filename, ftype):
    # Data order: ['Bx', 'By', 'Bz', 'Dark_Matter_Density', 'Density', 'Temperature']
    if ftype == 'velocity':
        [bx, by, bz] = get_velocity_data(filename)
        print(len(bx))
        # window = Temperature(data)
    elif ftype == 'magnetic':
        [bx, by, bz] = get_data(filename)
        window = MagneticField(bx, by, bz)
    else:
        print('Invalid Attribute provided for flow visualization. Select one from: [Velocity, Magnetic]')
    return window

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Flow Visualization')
    parser.add_argument('-i','--input', type=str, required=True, help='Input data')
    parser.add_argument('-ftype','--ftype', type=str, required=True, help='Select attribute for flow visualization')

    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = get_window(filename=args.input, ftype=args.ftype.lower())
    # window.ui.vtkWidget.GetRenderWindow().SetSize(1024, 1024)
    # window.show()
    # window.setWindowState(Qt.WindowState.WindowMaximized)
    # window.iren.Initialize()
    # sys.exit(app.exec())
