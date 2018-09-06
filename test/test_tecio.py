import io
import unittest
from aero_util.tecio import *
from . import common

class TestTecIO(unittest.TestCase):

    def test_simple_example(self):
        ''' Test that we can read a simple Tecplot *.dat file '''
        data = read_dat(common.data_dir/'example1.dat')
        self.assertEqual(len(data), 1)
        self.assertEqual(set(data[0].keys()), {"X", "Y"})
        self.assertTrue(all(np.equal(data[0]['X'], [1., 2., 2., 1.])))
        self.assertTrue(all(np.equal(data[0]['Y'], [1., 1., 2., 2.])))

    def test_blayer_example(self):
        ''' Test that we can read a BLAYER output file '''
        data = read_dat(common.data_dir/'blayer2d.dat')
        self.assertEqual(len(data), 1)
        self.assertTrue(all(np.equal(data[0]['xw (m)'][0:6],[
            1.000000000E-30,
            9.521124155E-06,
            4.759823346E-05,
            1.237390843E-04,
            2.379385096E-04,
            3.902034650E-04,
        ])))
        self.assertTrue(all(np.equal(data[0]['pw (Pa)'][0:6],[
            3.044047349E+02,
            3.044047349E+02,
            3.044855657E+02,
            3.041873005E+02,
            3.037223769E+02,
            3.031704390E+02,
        ])))
        self.assertEqual(set(data[0].keys()), {
            "xw (m)", "yw (m)", "running length (m)", "rhow (kg/m^3)",
            "pw (Pa)", "Tw (K)", "Tvw (K)", "Hw (J/kg)", "muw (Pa.s)", "n2w",
            "o2w", "now", "no+w", "n2+w", "o2+w", "nw", "ow", "n+w", "o+w",
            "ew", "qw (W/m^2)", "qvw (W/m^2)", "tauwx (Pa)", "tauwy (Pa)",
            "kappaw (W/m.K)", "rhoe (kg/m^3)", "pe (Pa)", "Te (K)", "Tve (K)",
            "He (J/kg)", "ue (m/s)", "ve (m/s)", "Me", "mue (Pa.s)", "n2e",
            "o2e", "noe", "no+e", "n2+e", "o2+e", "ne", "oe", "n+e", "o+e",
            "ee", "delta (m)", "deltastar (m)", "theta (m)", "Re-ue",
            "CH (kg/m^2.s)", "kappae (W/m.K)", "roughness (m)", "rhok (kg/m^3)",
            "velk (m/s)", "muk (Pa.s)", "Re-kk",
        })

    def test_cube_grid(self):
        ''' Verify reading blocked, multi-zone, 2D data file '''
        data = read_dat(common.data_dir/'cube.dat')
        self.assertEqual(len(data),6)
        self.assertAlmostEqual(data[3]['x'][8,3], -0.30)
        self.assertAlmostEqual(data[3]['y'][8,3],  0.50)
        self.assertAlmostEqual(data[3]['z'][8,3],  0.20)
