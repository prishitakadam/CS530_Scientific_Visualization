from PyQt6.QtWidgets import QMainWindow
from utils.Setup_UI import Ui_MainWindow
from utils.vr.Utils import Utils as utils
# import vtk
import numpy as np
import pandas as pd
import json
import pdb

class Temperature(QMainWindow):
    def __init__(self, data, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.data = np.log10(np.array(data))*1
        # pdb.set_trace()
        self.make()
        self.frame_counter = 0
        # self.set_cam_state()
    
    def get_transfer_function_values(self):
        with open('./transfer_function/vr_temperature.json', 'r') as f:
            json_file = f.read()
            data = json.loads(json_file)
        return data['color'], data['opacity']

    def make(self):
        self.vtk_image = utils.get_vtk_image(self.data.tostring())
        self.color_map_values, self.opacity = self.get_transfer_function_values()
        self.color_map = utils.get_color_map(self.color_map_values)
        self.transfer_function = utils.get_transfer_function(self.opacity)
        self.volume = utils.get_volume(self.vtk_image, self.color_map, self.transfer_function)
        self.ren, self.iren = utils.render(self.volume, self.ui)
        self.scalar_bar = utils.set_scalar_bar(self.color_map, self.ren, self.iren, 'Temperature')
        self.ren.AddActor(self.scalar_bar)

    def getActors(self):
        return self.volume, self.scalar_bar
    