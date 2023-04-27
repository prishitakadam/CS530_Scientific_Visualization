import numpy as np 
import vtk
from vtk.util import numpy_support 
import argparse 
import random
import h5py
from utils.vr.Utils import Utils as utils
import json

def get_transfer_function_values(vr_type):
    tf = { "Density": "vr_density",
            "Dark matter density": "vr_dark_matter_density",
            "Temperature": "vr_temperature"}

    with open(f'./transfer_function/{tf[vr_type]}_flow.json', 'r') as f:
        json_file = f.read()
        data = json.loads(json_file)
    return data['color'], data['opacity']

def volume_rendering(reader, vr_type):
    color_map_values, opacity = get_transfer_function_values(vr_type)
    # print(color_map_values)
    color_map = utils.get_color_map(color_map_values)
    transfer_function = utils.get_transfer_function(opacity)
    volume = utils.get_volume(reader, color_map, transfer_function)
    return color_map, volume


def compute_streamlines(data, seeds, length, eps=1.0e-6, fwd=True, bwd=True):
    stream = vtk.vtkStreamTracer()
    stream.SetInputData(data)

    pts = vtk.vtkPoints()
    pts.SetData(numpy_support.numpy_to_vtk(np.array(seeds)))
    poly = vtk.vtkPolyData()
    poly.SetPoints(pts)
    stream.SetSourceData(poly)
    stream.SetIntegratorTypeToRungeKutta45()
    stream.SetMaximumPropagation(7000)
    stream.SetIntegrationDirectionToBoth()
    stream.SetComputeVorticity(True)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(stream.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compute streamlines in magnetic field')
    parser.add_argument('-i', '--input', type=str,
                        required=True, help='Input file name')
    parser.add_argument('-v', '--velocity', type=str, required=True, help='Input file name for velocity')
    parser.add_argument('-n', '--number', type=int, default=100, help='Number of seed points')
    parser.add_argument('-l', '--length', type=float, default=7000, help='Integration length')
    parser.add_argument('-vr', '--volume', type=str, required=False, help='Attrribute for volume rendering')
    parser.add_argument('-f', '--flow', type=str, required=False, default='Magnetic', help='Attrribute for flow visualisation')

    args = parser.parse_args()

    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(args.input)
    reader.Update()


    if args.flow == 'velocity':
        vreader = vtk.vtkXMLImageDataReader()
        vreader.SetFileName(args.input)
        vreader.Update()

        data = vreader.GetOutput()
        data.GetPointData().SetActiveVectors('Velocity field')

        data_2 = reader.GetOutput()
        data_2.GetPointData().SetActiveScalars(args.volume)
    
    else:
        data = reader.GetOutput()
        data.GetPointData().SetActiveVectors('Magnetic field')
        data.GetPointData().SetActiveScalars(args.volume)

    
    [xmin, xmax, ymin, ymax, zmin, zmax] = data.GetBounds()
    center = 0.5*np.array([xmin+xmax, ymin+ymax, zmin+zmax])
    radius = 0.5*np.array([xmax-xmin, ymax-ymin, zmax-zmin])
    seeds = []
    for i in range(args.number):
        x = center[0] + 0.25*(1-2*random.random())*radius[0]
        y = center[1] + 0.25*(1-2*random.random())*radius[1]
        z = center[2] + 0.25*(1-2*random.random())*radius[2]
        seeds.append(np.array([x, y, z]))

    renderer = vtk.vtkRenderer()
    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(1024, 1024)

    ctf = vtk.vtkColorTransferFunction()
    ctf.AddRGBPoint(0, 1, 1, 1)
    ctf.AddRGBPoint(10, 1, 1, 1)
    ctf.AddRGBPoint(100,1, 1, 1)
    ctf.AddRGBPoint(10000, 1, 1, 1)

    actor = compute_streamlines(data, seeds, args.length)
    actor.GetProperty().RenderLinesAsTubesOn()
    actor.GetProperty().SetLineWidth(2)
    actor.GetMapper().ScalarVisibilityOn()
    actor.GetMapper().SetLookupTable(ctf)
    actor.GetMapper().Update()


    if args.volume != None:
        color_map, volume = volume_rendering(reader, args.volume)
   
   
    renderer.AddActor(actor)
    if args.volume != None:
        renderer.AddActor(volume)
    interactor = vtk.vtkRenderWindowInteractor()
    if args.volume != None:
        scalar_bar = utils.set_scalar_bar(color_map, renderer, interactor, args.volume)
        renderer.AddActor(scalar_bar)
    interactor.SetRenderWindow(window)
    interactor.Initialize()
    window.Render()
    interactor.Start()
