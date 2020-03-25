# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 16:17:18 2020

@author: loicm
"""

from math import *
import numpy as np
import matplotlib.pyplot as plt
from elevator_func import *

# CONSTANTS

W = 9.81*5678.710       #[N] weight airplane
Ws = 60500              #[N] standard aircraft mass
delta_de = np.radians(-0.2 - 0.3) #[deg] change in elevator deflection
delta_xcg =  -0.065     #[m] change in c.g. location
S = 30                  #[m^2] wing surface
c = 2.0569              #[m] mean chord
Rho_0 = 1.225           #[kg/m^3] standard density

# LEFT TO CALCULATE: !!!!!!!!!!!

Cn = 0.55               #[-] = Cl, lift coefficient, from measurements
Cna = 5.14              #[-] = Cla, from measurements
Cm0 = 0.0297            #FROM C.2
Cmtc = -0.0064          #FROM C.2
Tcs = 0                 # CALCULATE THIS!!!!

# INTERPOLATION DEFLECTION/ALPHA

alpha = [4.6,           #[deg] Angle of attack
5.5,
6.3,
7.5,
4,
3.5,
]

de = [0.2,              #[deg] elevator deflection
-0.2,
-0.5,
-1,
0.5,
0.8,
]

Tc = [3.787427758,
4.3482783,
5.070447062,
6.083485245,
3.332688155,
2.864115706,
]

Tcs = [3.161408252,
3.701599267,
4.415373375,
5.416353357,
2.760714783,
2.300036348,
]

Ve_red =[75.71644761,
71.16158352,
66.49449559,
61.3739985,
80.19741727,
85.872358,
]

Fe_red = [0,
-17.12362433,
-23.14166639,
-30.89255652,
13.77523493,
32.74936331
]

# REFERENECE DATA

delta_de_ref = np.radians(-0.5 - 0)     #[rad]
delta_xcg_ref = -0.048                  #[m]
Cn_ref = 0.55796595                     #[-]

alpha_ref = [5.3,
6.3,
7.3,
8.5,
4.5,
4.1,
3.4
]

de_ref = [0,
-0.4,
-0.9,
-1.5,
0.4,
0.6,
1
]

# FUNCTIONS

#Calculate d(elevator deflection)/d(alpha) slope of elevator curve
de_da = slope(alpha,de)
Cmde = elevator_eff(delta_de,Cn,delta_xcg,c)
Cma = -de_da*Cmde
print(de_da)
# REFERENCE DATA
de_da_ref = slope(alpha_ref,de_ref)
Cmde_ref = elevator_eff(delta_de_ref,Cn_ref,delta_xcg_ref,c)
Cma_ref = -de_da_ref*Cmde_ref

de_red = elevator_def(de, Cmde, Cmtc, Tc, Tcs)

plot_f(Fe_red,Ve_red)

#plot(de,alpha,de_red,Ve_red)