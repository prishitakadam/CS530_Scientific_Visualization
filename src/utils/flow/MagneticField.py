from PyQt6.QtWidgets import QMainWindow
from utils.Setup_UI import Ui_MainWindow
from utils.flow.Utils import Utils
import numpy as np
import pandas as pd
import json
import pdb

class MagneticField(QMainWindow):
    def __init__(self, bx, by, bz, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.bx = np.array(bx)
        self.by = np.array(by)
        self.bz = np.array(bz)

        utils = Utils()
        utils.get_vtk_file(self.bx, self.by, self.bz)


        


        