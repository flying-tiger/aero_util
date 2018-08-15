import unittest
import aero_util as au
import numpy as np

class TestUnits(unittest.TestCase):
    ''' Verify unit testing utilities '''

    def test_basic_convert(self):
        self.assertAlmostEqual(au.deg(au.rad(15.0)), 15.0)
        self.assertAlmostEqual(au.convert(10.0,'deg','rad'), au.rad(10.0))
        self.assertAlmostEqual(au.convert(1.0,'ft','m'), au.convert_from(1.0,'ft'))
        self.assertAlmostEqual(au.convert(1.0,'m','ft'), au.convert_to(1.0,'ft'))

    def test_temp_convert(self):
        self.assertAlmostEqual(au.convert(300.0,'K','degC'), 26.85)
        self.assertAlmostEqual(au.convert(0.0,'degC','degF'), 32.0, delta=1e-6)
        self.assertAlmostEqual(au.convert_from(0.0,'degC'), 273.15)
        self.assertAlmostEqual(au.convert_to(300,'degF'), 80.33, delta=1e-6)


class TestRotation(unittest.TestCase):
    ''' Verify rotation matrices '''

    def test_rotate_seq(self):
        v0 = np.array([1., 0., 0.])
        R1 = au.rotate_seq('yx',  angles_deg=[-90,90])
        R2 = au.rotate_seq('yxz', angles_deg=[90,-90,-90])
        self.assertTrue(np.allclose(R1 @ v0, [0., -1., 0.]))
        self.assertTrue(np.allclose(R2 @ v0, [1.,  0., 0.]))

    def test_rotate_axis(self):
        Rx = au.rotate_x(angle_deg=-45.0)
        Ry = au.rotate_y(angle_deg= 30.0)
        Rz = au.rotate_z(angle_deg=-60.0)
        self.assertTrue(np.allclose(Rx, au.rotate_axis([1,0,0], angle_deg=-45.0)))
        self.assertTrue(np.allclose(Ry, au.rotate_axis([0,1,0], angle_deg= 30.0)))
        self.assertTrue(np.allclose(Rz, au.rotate_axis([0,0,1], angle_deg=-60.0)))


