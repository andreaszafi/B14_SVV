# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:32:36 2020

@author: loicm
"""
from math import *
import matplotlib.pyplot as plt
import numpy as np

def slope(alpha,de):
    slope = []
    for i in range(len(alpha)-1):
        slope.append((de[i+1]-de[i])/(alpha[i+1]-alpha[i]))
    de_da = sum(slope)/len(slope)
    return de_da

def elevator_def(de, Cmde, Cmtc, Tc, Tcs):
    #reduced elevator deflection
    de_red = []
    for i in range(len(de)):
        de_red.append(np.degrees(np.radians(de[i])-(1/Cmde)*Cmtc*(Tcs[i]-Tc[i])))
    return de_red

def elevator_eff(delta_de,Cn,delta_xcg,c):
    Cmde = -(1/delta_de)*Cn*(delta_xcg/c)
    return Cmde

def plot(de,alpha,de_red,Ve_red):
    fig, axs = plt.subplots(1, 2, constrained_layout=True)
    axs[0].scatter(alpha,de)
    axs[0].set_title('Elevator trim curve')
    axs[0].set_xlabel('Angle of attack [deg]')
    axs[0].set_ylabel('Elevator deflection angle [deg]')
    z = np.polyfit(alpha, de, 1)
    p = np.poly1d(z)
    axs[0].plot(alpha,p(alpha),"r--")
    axs[1].scatter(Ve_red,de_red)
    axs[1].set_title('Reduced elevator trim curve')
    axs[1].set_xlabel('Reduced equivalent airspeed [m/s]')
    axs[1].set_ylabel('Reduced elevator deflection angle [deg]')
    #fig.suptitle('Elevator trim curves', fontsize=16)
    plt.show()
    
def plot_f(Fe_red,Ve_red):
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.scatter(Ve_red,Fe_red)
    ax.set_xlabel('Reduced equivalent velocity [m/s]')
    ax.set_ylabel('Reduced elevator control force [N]')
    fig.suptitle('Reduced elevator control force curve')
    plt.show()