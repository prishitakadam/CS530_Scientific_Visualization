from PyQt6.QtWidgets import QMainWindow
from Setup_UI import Ui_MainWindow
import vtk
import numpy as np
import pandas as pd
import pdb

class Temperature(QMainWindow):
    def __init__(self, data, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        data = np.log10(np.array(data))*1
        self.vtk_image = self.get_vtk_image(data.tostring())
        self.color_map = self.get_color_map()
        self.transfer_function = self.get_transfer_function()
        self.volume = self.get_volume()
        self.iren = self.render()

    def get_vtk_image(self, data):
        vtk_image = vtk.vtkImageImport()
        vtk_image.CopyImportVoidPointer(data, len(data))
        vtk_image.SetDataScalarTypeToFloat()
        vtk_image.SetNumberOfScalarComponents(1)
        vtk_image.SetDataExtent(0, 319, 0, 319, 0, 319)
        vtk_image.SetWholeExtent(0, 319, 0, 319, 0, 319)
        return vtk_image
    
    def get_color_map(self):
        color_map_values = [[5, 128, 255, 0],
                            [6, 255, 255, 51],
                            [6.5, 255, 153, 51],
                            [7, 255, 0, 0]]
        color_map = vtk.vtkColorTransferFunction()
        color_map.SetColorSpaceToRGB()
        for i in range(len(color_map_values)):
            [isovalue, r, g, b] = color_map_values[i]
            color_map.AddRGBPoint(isovalue, r/256, g/256, b/256)
        return color_map
    
    def get_transfer_function(self):
        opacity = [[0, 0.0],
                    [6.5, 0.05],
                    [5.8, 0.0],
                    [6.6, 0.06],
                    [6.51, 0.0],
                    [7.2, 0.1],
                    [7.0, 0.0]]
        
        transfer_function = vtk.vtkPiecewiseFunction()
        for i in range(len(opacity)):
            [isovalue, alpha] = opacity[i]
            transfer_function.AddPoint(isovalue, alpha)
        return transfer_function
    
    def get_volume(self):
        volume_mapper = vtk.vtkSmartVolumeMapper()
        volume_mapper.SetBlendModeToComposite()
        volume_mapper.SetInputConnection(self.vtk_image.GetOutputPort())

        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(self.color_map)
        volume_property.SetScalarOpacity(self.transfer_function)
        volume_property.SetScalarOpacityUnitDistance(10)
        volume_property.SetInterpolationTypeToLinear()
        volume_property.ShadeOn()

        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)
        return volume
    
    def render(self):
        ren = vtk.vtkRenderer()
        ren.AddVolume(self.volume)
        ren.SetBackground(0, 0, 0)
        ren.ResetCamera()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(ren)
        iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        return iren
        
        