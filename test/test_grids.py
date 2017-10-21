import numpy as np
import unittest
from . import common
from aero_util import grids

class StructuredGridTestCase(unittest.TestCase):

    def test_load_grid(self):

        # Load single block 2D grid
        r0, = grids.load(common.data_dir/'rectangle.p3d')
        self.assertAlmostEqual(r0.x[0,0], -1.0)
        self.assertAlmostEqual(r0.y[0,0], -0.5)
        self.assertAlmostEqual(r0.x[1,1],  0.0)
        self.assertAlmostEqual(r0.y[1,1],  0.5)

        # Load multi block 2D grid
        # Note: r2 is r1 rotated by 90deg
        r1, r2 = grids.load(common.data_dir/'rectangles.p3d')
        self.assertAlmostEqual(np.linalg.norm(r1.x - r0.x), 0.0)
        self.assertAlmostEqual(np.linalg.norm(r1.y - r0.y), 0.0)
        self.assertAlmostEqual(np.linalg.norm(r2.x - r0.y), 0.0)
        self.assertAlmostEqual(np.linalg.norm(r2.y - r0.x), 0.0)

        # Load single block 3D grid in multi-block format
        cube, = grids.load(common.data_dir/'cube.p3d')
        self.assertAlmostEqual(cube.x[0,0,0], -1.0)
        self.assertAlmostEqual(cube.y[0,0,0], -1.0)
        self.assertAlmostEqual(cube.z[0,0,0], -1.0)
        self.assertAlmostEqual(cube.x[3,1,1],  0.5)
        self.assertAlmostEqual(cube.y[3,1,1],  0.0)
        self.assertAlmostEqual(cube.z[3,1,1],  1.0)
