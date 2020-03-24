import unittest
import Cl_Curves
from Cl_Curves import p0,T0,R

class MyTestCase(unittest.TestCase):
    def test_isa(self):
        #h = 0
        h=0
        rho = p0/(T0*R)
        self.assertAlmostEqual(Cl_Curves.isa(h), (T0, p0, rho), 8)
        #h = 11000


if __name__ == '__main__':
    unittest.main()
