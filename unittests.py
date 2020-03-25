import unittest
import numpy as np
import Cl_Curves
import elevator_func
import massandcg
from Cl_Curves import p0,T0,R

class MyTestCase(unittest.TestCase):
    def test_slope(self): #inputs are lists of 6 elements, output is a single element?
        alphatest1 = [0,0,0,0,0,0]
        alphatest2 = [-1,-0.5,0,0.5,1,1.5]
        alphatest3 = [-1000,1,2,3,4,5]
        alphatest4 = [-1,2,3,6,6000,6501]
        detest1 = [0,0,0,0,0,0]
        detest2 = [-1,-0.5,0,0.5,1,1.5]
        detest3 = [-1000,1,2,3,4,5]
        detest4 = [-1,2,3,6,6000,6501]
        #all zeros for alpha and de, also tested with nonzero for the other input:
        #self.assertIsNone(elevator_func.slope(alphatest1,detest1)) #Division by 0 gives error
        #self.assertIsNone(elevator_func.slope(alphatest1, detest2)) #Division by 0 gives error
        self.assertAlmostEqual(elevator_func.slope(alphatest2, detest1),0.00000,5)
        #Other values calculated by hand, including large negative and positive values with help of MS Excel:
        self.assertAlmostEqual(elevator_func.slope(alphatest3, detest2), 0.4001  , 5)
        self.assertAlmostEqual(elevator_func.slope(alphatest2, detest3), 402     , 5)
        self.assertAlmostEqual(elevator_func.slope(alphatest4, detest2), 0.166883, 5)
        self.assertAlmostEqual(elevator_func.slope(alphatest2, detest4), 2600.8  , 5)
        self.assertAlmostEqual(elevator_func.slope(alphatest4, detest3), 67.00043, 5)
        self.assertAlmostEqual(elevator_func.slope(alphatest3, detest4), 1299.801, 3)

    def test_elevator_eff(self):
        delta_de1 = np.radians(-0.5)
        delta_de2 = 0
        delta_de3 = 1
        Cn1 = 0.55
        Cn2 = 0
        Cn3 = 5
        c1 = 2.0569
        c2 = 0
        c3 = -3
        delta_xcg1 = -0.065
        delta_xcg2 = 0
        delta_xcg3 = 3
        #With normal inputs
        self.assertAlmostEqual(elevator_func.elevator_eff(delta_de1,Cn1,delta_xcg1,c1),-1.991661352,8)

        #With zeros as inputs
        #self.assertAlmostEqual(elevator_func.elevator_eff(delta_de2, Cn1, delta_xcg1, c1), 0.0,8) #Error division by 0
        self.assertAlmostEqual(elevator_func.elevator_eff(delta_de1, Cn2, delta_xcg1, c1), 0.0         , 8)
        self.assertAlmostEqual(elevator_func.elevator_eff(delta_de1, Cn1, delta_xcg2, c1), 0.0, 8)
        #self.assertAlmostEqual(elevator_func.elevator_eff(delta_de1, Cn1, delta_xcg1, c2), 0.0,8) #Error division by 0

        #With other inputs

            #negative chord length
        self.assertAlmostEqual(elevator_func.elevator_eff(delta_de1, Cn1, delta_xcg1, c3), 1.365549412, 8)
            #High Cn
        self.assertAlmostEqual(elevator_func.elevator_eff(delta_de1, Cn3, delta_xcg1, c1), -18.10601229, 8)
            #Center pf gravity moving backward
        self.assertAlmostEqual(elevator_func.elevator_eff(delta_de1, Cn1, delta_xcg3, c1), 91.922831654, 5)

    def test_momentfuel(self):
        fuel1 = 1000
        fuel2 = 1900
        mass2 = 1700
        mass3 = 2000
        mass4 = 2100
        moment1 = -1500
        moment2 = 0
        moment3 = 4564685
        moment4 = 8643515
        #Fuel load is outside of the low and high borders of the interpolation
        self.assertAlmostEqual(massandcg.momentfuel(fuel1,mass3,mass4,moment3,moment4), -36223615,8)
        #Negative moment
        self.assertAlmostEqual(massandcg.momentfuel(fuel2, mass2, mass3, moment1, moment2), -500, 8)
        #Fuel load is same as lower border
        self.assertAlmostEqual(massandcg.momentfuel(fuel1, fuel1, mass4, moment2, moment3), moment2, 8)

if __name__ == '__main__':
    unittest.main()
