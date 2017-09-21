import numpy as np
import unittest
from aero_util.attitude import *

def all_close(test_case, array1, array2):
    test_case.assertTrue(np.all(np.isclose(array1, array2)))

def all_true(test_case, logical_array):
    test_case.assertTrue(np.all(logical_array))

class AttitudeTestCase(unittest.TestCase):

    def setUp(self):
        # Make dimensions compatible with broadcasting
        a = np.linspace(0, 90, 7)
        p = np.linspace(-180., 180., 13)
        self.alphat, self.phi = np.meshgrid(a,p)

    def test_uvw_from_ap(self):
        u, v, w = uvw_from_ap(self.alphat, self.phi)

        # Check u is as expected
        all_close(self, u[self.alphat ==   0.0],  1.0)
        all_close(self, u[self.alphat ==  90.0],  0.0)

        # Check v is as expected
        all_close(self, v[self.phi ==   0.0], 0.0)
        all_close(self, v[self.phi == 180.0], 0.0)
        all_true(self, v[self.phi == -120.0] <= 0.0)
        all_true(self, v[self.phi ==  -60.0] <= 0.0)
        all_true(self, v[self.phi ==   60.0] >= 0.0)
        all_true(self, v[self.phi ==  120.0] >= 0.0)

        # Check w is as expected
        all_close(self, w[self.phi ==  90.0], 0.0)
        all_close(self, w[self.phi == -90.0], 0.0)
        all_true(self, w[self.phi == -120.0] <= 0.0)
        all_true(self, w[self.phi ==  -60.0] >= 0.0)
        all_true(self, w[self.phi ==   60.0] >= 0.0)
        all_true(self, w[self.phi ==  120.0] <= 0.0)

    def test_ab_from_ap(self):
        alpha, beta = ab_from_ap(self.alphat, self.phi)

        # Verify alpha == alphat, beta == alphat when rolled correctly
        all_close(self,  beta[self.phi == -90.0], -self.alphat[self.phi == -90.0] )
        all_close(self, alpha[self.phi ==   0.0],  self.alphat[self.phi ==   0.0] )
        all_close(self,  beta[self.phi ==  90.0],  self.alphat[self.phi ==  90.0] )
        all_close(self, alpha[self.phi == 180.0], -self.alphat[self.phi == 180.0] )

        # Verify that no alpha/beta when alphat = 0, 180, regardless of roll
        all_close(self, alpha[self.alphat ==   0.0], 0.0 )
        all_close(self,  beta[self.alphat ==   0.0], 0.0 )

        # Verify symmetry for +/- alpha
        all_close(self, alpha[self.phi == 30], -alpha[self.phi == 150] )
        all_close(self,  beta[self.phi == 30],   beta[self.phi == 150] )

        # Verify symmetry for +/- beta
        all_close(self, alpha[self.phi == 30], alpha[self.phi == -30] )
        all_close(self,  beta[self.phi == 30], -beta[self.phi == -30] )

    def test_inverse_pairs(self):
        # Since the alphat/phi transformation is singular for alphat=0,180, the
        # roll angle at these alphas will get messed up during the round trip.
        # Therefore, we skip alphat=0 when checking roll angles

        alphat, phi = ap_from_ab(*ab_from_ap(self.alphat, self.phi))
        all_close(self, alphat, self.alphat)
        all_close(self, phi[alphat > 0.0], self.phi[alphat > 0.0])

        alphat, phi = ap_from_uvw(*uvw_from_ap(self.alphat, self.phi))
        all_close(self, alphat, self.alphat)
        all_close(self, phi[alphat > 0.0], self.phi[alphat > 0.0])

