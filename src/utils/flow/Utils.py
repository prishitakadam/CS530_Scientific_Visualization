from tvtk.api import tvtk, write_data
import numpy as np

class Utils:
    def __init__(self):
        pass
    
    def get_array(self, dataX, dataY, dataZ, dtype):
        arr = np.empty(dataZ.shape + (3,), dtype=dtype)
        arr[..., 0] = dataX
        arr[..., 1] = dataY
        arr[..., 2] = dataZ
        arr = arr.transpose(2, 1, 0, 3).copy()
        arr.shape = int(arr.size/3), 3
        return arr

    def get_vectors(self, bx, by, bz):
        x, y, z = np.mgrid[0:len(bx), 0:len(by), 0:len(bz)]
        points = self.get_array(x, y, z, np.int16)
        vectors = self.get_array(bx, by, bz, np.float32)
        return x, y, z, points, vectors
        
    def get_vtk_file(self, bx, by, bz):
        x, y, z, points, vectors = self.get_vectors(bx, by, bz)
        structured_grid = tvtk.StructuredGrid(dimensions=x.shape, points=points)
        structured_grid.point_data.vectors = vectors
        structured_grid.point_data.vectors.name = 'magnetic_field'
        write_data(structured_grid, 'magnetic_field.vtk')


