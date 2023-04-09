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
        self.ren, self.iren = self.render()
        self.scalar_bar = self.set_scalar_bar()
        self.ren.AddActor(self.scalar_bar)
        self.frame_counter = 0
        # self.set_cam_state()

    def get_vtk_image(self, data):
        vtk_image = vtk.vtkImageImport()
        vtk_image.CopyImportVoidPointer(data, len(data))
        vtk_image.SetDataScalarTypeToFloat()
        vtk_image.SetNumberOfScalarComponents(1)
        vtk_image.SetDataExtent(0, 319, 0, 319, 0, 319)
        vtk_image.SetWholeExtent(0, 319, 0, 319, 0, 319)
        return vtk_image
    
    def get_color_map(self):
        color_map_values = [[6,21, 250, 246],
                            [6.5,8, 98, 247],
                            [6.8,192, 18, 247],
                            [7,247, 18, 35],
                            [7.1,247, 136, 18],
                            [7.3, 247, 188, 18],
                            [7.4, 247, 237, 18],
                            [7.6, 247, 237, 18]]
        color_map = vtk.vtkColorTransferFunction()
        color_map.SetColorSpaceToRGB()
        for i in range(len(color_map_values)):
            [isovalue, r, g, b] = color_map_values[i]
            color_map.AddRGBPoint(isovalue, r/256, g/256, b/256)
        return color_map
    
    def get_transfer_function(self):
        opacity = [ [0.0, 0.0],
                    [6.0, 0.0],
                    [6.1, 0.05],
                    [6.3, 0.0],
                    [6.4, 0.0],
                    [6.5, 0.1], 
                    [6.7, 0.0],
                    [6.8, 0.3],
                    [7.0, 0.0],
                    [7.1, 0.7],
                    [7.2, 0.0],
                    [7.3, 0.8],
                    [7.35, 0.0],
                    [7.4, 1.0]]
        
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
    
    def set_scalar_bar(self):
        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetOrientationToHorizontal()
        scalar_bar.SetLookupTable(self.color_map)
        scalar_bar.SetMaximumWidthInPixels(120)
        scalar_bar.SetPosition(0.9, 0.2)
        scalar_bar.SetWidth(0.05)
        scalar_bar.SetHeight(0.6)
        scalar_bar.SetTitle("Temperature (log scale)")
        self.ren.AddActor(scalar_bar)

        scalar_bar_widget = vtk.vtkScalarBarWidget()
        scalar_bar_widget.SetInteractor(self.iren)
        scalar_bar_widget.SetScalarBarActor(scalar_bar)
        return scalar_bar
    
    def render(self):
        ren = vtk.vtkRenderer()
        ren.AddVolume(self.volume)
        ren.SetBackground(0, 0, 0)
        ren.ResetCamera()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(ren)
        iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        return ren, iren
    
    def set_cam_state(self):
        cam_state = [[-268.75307985095617, -255.37179336859447, -247.5624198576113],
            [0.0, 0.0, 0.0],
            [-0.45938825241278597, -0.3198487553199407, 0.8286490253813198],
            [165.23124986024567, 1424.358900214912]]
        self.camera = self.ren.GetActiveCamera()
        self.camera.SetPosition(cam_state[0][0], cam_state[0][1], cam_state[0][2])
        self.camera.SetFocalPoint(cam_state[1][0], cam_state[1][1], cam_state[1][2])
        self.camera.SetViewUp(cam_state[2])
        self.camera.SetClippingRange(cam_state[3])

        self.iren.AddObserver("KeyPressEvent", self.key_pressed_callback)
    
    def screenshot(self):
        file_name = "Temperature_VR_" + str(self.frame_counter).zfill(1) + ".png"
        window = self.ui.vtkWidget.GetRenderWindow()
        image = vtk.vtkWindowToImageFilter()
        image.SetInput(window)
        png_writer = vtk.vtkPNGWriter()
        png_writer.SetInputConnection(image.GetOutputPort())
        png_writer.SetFileName(file_name)
        window.Render()
        png_writer.Write()
        self.frame_counter += 1
    
    def get_camera_settings(self):
        camera = self.ren.GetActiveCamera()
        print("Camera settings:")
        print("  * position:        %s" % (camera.GetPosition(),))
        print("  * focal point:     %s" % (camera.GetFocalPoint(),))
        print("  * up vector:       %s" % (camera.GetViewUp(),))
        print("  * clipping range:  %s" % (camera.GetClippingRange(),))
    
    def key_pressed_callback(self, obj, event):
        key = obj.GetKeySym()
        if key == "s":
            self.screenshot()

        elif key == "c":
            self.get_camera_settings()
        
        elif key == 'q':
            sys.exit()
        
        