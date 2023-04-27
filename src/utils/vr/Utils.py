import vtk

class Utils:
    def __init__(self):
        pass
    def get_vtk_image(data):
        vtk_image = vtk.vtkImageImport()
        vtk_image.CopyImportVoidPointer(data, len(data))
        vtk_image.SetDataScalarTypeToFloat()
        vtk_image.SetNumberOfScalarComponents(1)
        vtk_image.SetDataExtent(0, 319, 0, 319, 0, 319)
        vtk_image.SetWholeExtent(0, 319, 0, 319, 0, 319)
        return vtk_image
    
    def get_color_map(color_map_values):
        color_map = vtk.vtkColorTransferFunction()
        color_map.SetColorSpaceToRGB()
        for i in range(len(color_map_values)):
            [isovalue, r, g, b] = color_map_values[i]
            color_map.AddRGBPoint(isovalue, r/256, g/256, b/256)
        return color_map
    
    def get_transfer_function(opacity):
        # TODO: Opacity function values could be set in a better way
        transfer_function = vtk.vtkPiecewiseFunction()
        for i in range(len(opacity)):
            [isovalue, alpha] = opacity[i]
            transfer_function.AddPoint(isovalue, alpha)
        return transfer_function
    
    def get_volume(vtk_image, color_map, transfer_function):
        volume_mapper = vtk.vtkSmartVolumeMapper()
        volume_mapper.SetBlendModeToComposite()
        volume_mapper.SetInputConnection(vtk_image.GetOutputPort())

        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(color_map)
        volume_property.SetScalarOpacity(transfer_function)
        volume_property.SetScalarOpacityUnitDistance(10)
        volume_property.SetInterpolationTypeToLinear()
        volume_property.ShadeOn()

        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)
        return volume
    
    def set_scalar_bar(color_map, ren, iren, bar_type):
        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetOrientationToHorizontal()
        scalar_bar.SetLookupTable(color_map)
        scalar_bar.SetMaximumWidthInPixels(120)
        scalar_bar.SetPosition(0.9, 0.2)
        scalar_bar.SetWidth(0.05)
        scalar_bar.SetHeight(0.6)
        scalar_bar.SetTitle(f"{bar_type} (log scale)")
        ren.AddActor(scalar_bar)

        scalar_bar_widget = vtk.vtkScalarBarWidget()
        scalar_bar_widget.SetInteractor(iren)
        scalar_bar_widget.SetScalarBarActor(scalar_bar)
        return scalar_bar
    
    def render(volume, ui):
        ren = vtk.vtkRenderer()
        ren.AddVolume(volume)
        ren.SetBackground(0, 0, 0)
        ren.ResetCamera()
        ui.vtkWidget.GetRenderWindow().AddRenderer(ren)
        iren = ui.vtkWidget.GetRenderWindow().GetInteractor()
        return ren, iren
    
    def get_clip(reader, volume):
        # Plane X, Y, Z
        x_plane = vtk.vtkPlane()
        x_plane.SetOrigin(0, 0, 0)
        x_plane.SetNormal(1.0, 0, 0)
        x_clip = vtk.vtkClipPolyData()
        x_clip.SetInputConnection(volume.GetOutputPort())
        x_clip.SetClipFunction(x_plane)

        y_plane = vtk.vtkPlane()
        y_plane.SetOrigin(0, 0, 0)
        y_plane.SetNormal(0, 1.0, 0)
        y_clip = vtk.vtkClipPolyData()
        y_clip.SetInputConnection(x_clip.GetOutputPort())
        y_clip.SetClipFunction(y_plane)

        z_plane = vtk.vtkPlane()
        z_plane.SetOrigin(0, 0, 0)
        z_plane.SetNormal(0, 0, 1.0)
        z_clip = vtk.vtkClipPolyData()
        z_clip.SetInputConnection(y_clip.GetOutputPort())
        z_clip.SetClipFunction(z_plane)

        probe_filter = vtk.vtkProbeFilter()
        probe_filter.SetSourceConnection(reader.GetOutputPort())
        probe_filter.SetInputConnection(z_clip.GetOutputPort())

        min_clip = vtk.vtkClipPolyData()
        min_clip.SetInputConnection(probe_filter.GetOutputPort())
        min_clip.InsideOutOff()
        min_clip.SetValue(grad_min)

        max_clip = vtk.vtkClipPolyData()
        max_clip.SetInputConnection(min_clip.GetOutputPort())
        max_clip.InsideOutOn()
        max_clip.SetValue(grad_max)

        imapper = vtk.vtkDataSetMapper()
        imapper.SetInputConnection(max_clip.GetOutputPort())
        imapper.SetLookupTable(color_map)

        iactor = vtk.vtkActor()
        iactor.SetMapper(imapper)
    
        return iactor
    
    def set_cam_state():
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
    
    def screenshot():
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
    
    def get_camera_settings():
        camera = self.ren.GetActiveCamera()
        print("Camera settings:")
        print("  * position:        %s" % (camera.GetPosition(),))
        print("  * focal point:     %s" % (camera.GetFocalPoint(),))
        print("  * up vector:       %s" % (camera.GetViewUp(),))
        print("  * clipping range:  %s" % (camera.GetClippingRange(),))
    
    def key_pressed_callback(obj, event):
        key = obj.GetKeySym()
        if key == "s":
            self.screenshot()

        elif key == "c":
            self.get_camera_settings()
        
        elif key == 'q':
            sys.exit()
