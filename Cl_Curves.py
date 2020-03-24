import numpy as np
import matplotlib.pyplot as plt

#Environmental Constants
gamma = 1.4
R = 287.0
g0 = 9.80665
T0 = 288.15                                                                 #Base temperature in Kelvin
p0 = 101325.0                                                               #Base pressure in Pa
rho0 = p0/(R*T0)                                                            #Base density in kg/m^3

#Aircraft dimensions
S = 30                                                                      #Wing area in m^2
b = 15.911                                                                  #Wing span in m
AR = (b**2)/S

CD0 = 0.04                                                                  #Zero lift drag coefficient
e = 0.8                                                                     #efficiency factor

hp = np.array([5030, 12010, 12000, 11990, 11990, 12000, 11990])*0.3048      #height in meters
IAS = np.array([222,254,222,188,161,131,114])*0.514444                      #IAS in m/s
alpha = np.array([2.1,1.3,2,3.4,4.9,7.8,10.2])*np.pi/180                    #Angle of attack in rad
FFl = np.array([673,698,587,449,410,382,405])*0.000125998                   #Left fuel flow in kg/s
FFr = np.array([750,750,634,489,449,415,438])*0.000125998                   #Right fuel flow in kg/s
F_used = np.array([286,462,497,543,569,590,612])*0.453592                   #Fuel used in kg
TAT = np.array([4.0,-4.2,-7.2,-9.5,-11,-12.5,-13.2])+273.15                 #TAT in Kelvin

BEW = 9165.0*0.453592                                                       #Basic empty weight[kg]
W_pay = 90+102+60+68+70+76+82+105+87                                        #Weight of passengers and pilots[kg]
W_fuel = 2628 - F_used                                                      #Weight of the fuel[kg]
W = BEW + W_pay + W_fuel                                                    #Total weight of aircraft[kg]

def isa(h):
    """Returns the temperature[K], pressure[Pa] and density[kg/m^3] for a given altitude[m] < 11000m"""
    if np.any((h<0)|(h>11000)):
        print ("The altitude must be between 0m and 11000m")
        return "Returning a string to cause errors later"
    T = T0 + -0.0065*h
    p = p0*(T/T0)**(-g0/(-0.0065*R))
    rho = p/(R*T)
    return T,p,rho

def Mach(h,Vc,p):
    """Calculate the Mach number for a given height, calbrated velocity and pressure"""
    return np.sqrt(2/(gamma-1)*((1+p0/p*((1+(gamma-1)/(2*gamma)*rho0/p0*Vc**2)**(gamma/(gamma-1))-1))**((gamma-1)/gamma)-1))

def Static_T(Temp_m,M):
    """Calculate the static air temperature for a measured temperature and Mach number"""
    return Temp_m/(1+(gamma-1)/2*M**2)

def VTrue(h,Vc,p,Temp_m):
    """Calculate the true airspeed for a given height, calibrated velocity, pressure and measured temperature"""
    M = Mach(h,Vc,p)
    return M*np.sqrt(gamma*R*Static_T(Temp_m,M))

def Thrustexe_data(h,Vc,Temp_m,FFl,FFr):
    """Returns an array of the data that can be fed into thrust.exe for the thrust value"""
    T,p,rho = isa(h)
    M = Mach(h,Vc,p)
    Delta_T = Static_T(Temp_m,M)-T
    data = np.array([h,M,Delta_T,FFl,FFr]).T

    np.savetxt("matlab.dat",data)
    return

def Thrust_from_data():
    data = np.loadtxt("thrust.dat")
    return np.sum(data,1)

def LiftCoeff(h,Vc,Temp_m,W,S):
    """Calculate the Cl for a given height, measured temperature, calibrated velocity, weight and wingspan.
        Steady flight is assumed"""
    T,p,rho = isa(h)
    return W*g0/(0.5*rho*VTrue(h,Vc,p,Temp_m)**2*S)

def DragCoeff(h,Vc,Temp_m,Thrust,S):
    """Calculate the Cd for a given height, calibrated velocity, measured temperature, thrust and wingspan.
        Steady flight is assumed"""
    T,p,rho = isa(h)
    return Thrust/(0.5*rho*VTrue(h,Vc,p,Temp_m)**2*S)

def AvgSlope(x_vals,y_vals):
    """Returns the average slope for a numpy array of x_vals and a numpy array of y_vals"""
    slopes = (y_vals[1:]-y_vals[:-1])/(x_vals[1:]-x_vals[:-1])
    return np.sum(slopes)/len(slopes)

CD = DragCoeff(hp,IAS,TAT,Thrust_from_data(),S)
CL = LiftCoeff(hp,IAS,TAT,W,S)

fig, axs = plt.subplots(3)

axs[0].plot(alpha,CL,'-o')
axs[0].set_title('CL-alpha')
axs[0].set(xlabel = "angle of attack", ylabel = "CL")

axs[1].plot(alpha,CD,'-o')
axs[1].set_title('CD-alpha')
axs[1].set(xlabel = "angle of attack", ylabel = "CD")

axs[2].plot(CD,CL,'-o')
axs[2].set_title('CL-CD')
axs[2].set(xlabel = "CD", ylabel = "CL")

plt.subplots_adjust(hspace=1.5)
#plt.show()

print ("The CL-alpha slope is:", AvgSlope(alpha,CL))

e = 1/(AvgSlope((CL**2),CD)*np.pi*AR)
print ("The Oswald's coefficient is:", 1/(AvgSlope((CL**2),CD)*np.pi*AR))
print ("The Zero Lift Drag Coefficient is:", sum(CD-(CL**2)/(np.pi*e*AR))/len(CD))
plt.plot((CL**2),CD)
#plt.show()
