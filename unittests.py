import unittest
import numpy as np
import Cl_Curves
import elevator_func
import massandcg
from massandcg import mpax,xpax,totalmass,totalmoment,fuelmoment,currentfuel
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
        fuel3 = 2025
        fuel4 = 2099
        mass2 = 1700
        mass3 = 2000
        mass4 = 2100
        moment1 = -1500
        moment2 = 0
        moment3 = 4564685
        moment4 = 8643515
        #Different fuelloads within the interpolation range
        self.assertAlmostEqual(massandcg.momentfuel(fuel3, mass3, mass4, moment3, moment4), 5584392.5, 8)
        self.assertAlmostEqual(massandcg.momentfuel(fuel4, mass3, mass4, moment3, moment4), 8602726.7, 8)
        #Negative moment
        self.assertAlmostEqual(massandcg.momentfuel(fuel2, mass2, mass3, moment1, moment2), -500, 8)
        #Fuel load is same as lower border
        self.assertAlmostEqual(massandcg.momentfuel(fuel1, fuel1, mass4, moment2, moment3), moment2, 8)

    def test_cgloc(self):
        mpax = [90,102,68,70,76,82,105,87,60]
        xpax = [131,131,214,214,251,251,288,288,170]
        mpax1,mpax2,mpax3 = mpax,mpax,mpax
        mpax1[0] = 40
        mpax2[8] = 80
        mpax3[4] = 90
        totalmass1,totalmass2,totalmass3 = totalmass,totalmass,totalmass
        totalmass1[0] - sum(mpax) + sum(mpax1)
        totalmass2[8] - sum(mpax) + sum(mpax2)
        totalmass3[4] - sum(mpax) + sum(mpax3)
        totalmoment1,totalmoment2,totalmoment3 = totalmoment,totalmoment,totalmoment
        totalmoment[0] = totalmoment[0] + xpax[0] * (mpax1[0] - mpax[0])
        totalmoment[8] = totalmoment[8] + xpax[8] * (mpax1[8] - mpax[8])
        totalmoment[4] = totalmoment[4] + xpax[4] * (mpax1[4] - mpax[4])
        cgmain = massandcg.cgloc(totalmass, currentfuel, totalmoment, fuelmoment)
        cg1 = massandcg.cgloc(totalmass1, currentfuel, totalmoment1, fuelmoment)
        cg2 = massandcg.cgloc(totalmass1, currentfuel, totalmoment1, fuelmoment)
        cg3 = massandcg.cgloc(totalmass1, currentfuel, totalmoment1, fuelmoment)
        self.assertGreater(cg1, cgmain)
        self.assertGreater(cg2, cgmain)
        self.assertGreater(cg3, cgmain)
        #self.assertGreater(massandcg.cgloc(totalmass - mpax + mpax1, totalmoment + xpax[8] * (mpax2[8] - mpax[8])))
        #self.assertGreater(massandcg.cgloc(totalmass - mpax + mpax1, totalmoment + xpax[4] * (mpax1[4] - mpax[4])))
        #self.assertGreater()

if __name__ == '__main__':
    unittest.main()
