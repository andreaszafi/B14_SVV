import numpy as np
import scipy.integrate as integrate

def interpolate(mass,masslow,masshigh,armlow,armhigh):
    return armlow + (mass-masslow)/(masshigh-masslow)*(armhigh-armlow)


#inputs(in pounds, inches)
mtemp = 100
xtemp = 200
inch = 0.0254
lbs = 0.453592
lbsinch = 0.113
g = 9.81

#tempmassflow = 100
#freq = 20 #[Hz]
#flighttime = 90*60 #seconds
#BEM
mBEM = 9165*lbs
xBEM = 291.65*inch
momentBEM = mBEM * xBEM
print(mBEM,momentBEM)
#Payload
#People

mpax = [90,102,68,70,76,82,105,87,0,60]
mpax = [x / lbs for x in mpax]
print(mpax)
xpax = [131,131,214,214,251,251,288,288,170,170]
momentpax = []
for k in range(len(mpax)):
    momentpax.append(mpax[k] * xpax[k])
print(momentpax)
print("sum of mass: ", sum(mpax))
print("sum of moments: ", sum(momentpax))
xpax = [i * inch for i in xpax]
#seat 9 is empty

#totalpayload

temppayloadmoment = []
for i in range(len(mpax)):
    temppayloadmoment.append(mpax[i]*xpax[i])
mpayload = sum(mpax)
xpayload = sum(temppayloadmoment)/mpayload
momentpayload = sum(temppayloadmoment)
#print(mpayload,xpayload)
#FUEL
mfuelload = []
fuelarm = []
xfuelload = []
fuelmass = [1700,1800,1900,2000,2100,2200,2300,2400]
fuelmoment = [485656,514116,542564,570990,599404,627847,656282,684696]
mfuelloadstart = 2628*lbs

#momentfuelload = mfuelload * xf0
wf = [286,462,497,543,569,590,612,692,710,727,746,798,814,843,873,905]
wf = [i * lbs for i in wf]
momentfuelload = []

for i in range(len(wf)):
    mfuelload.append(mfuelloadstart - wf[i])
    for j in range(len(fuelmass)):
        if mfuelload[i]/lbs >= fuelmass[j] and mfuelload[i]/lbs <= fuelmass[j+1]:
            xfuelload.append(interpolate(mfuelload[i],fuelmass[j]*lbs,fuelmass[j+1]*lbs,fuelmoment[j]*lbsinch,fuelmoment[j+1]*lbsinch)/ mfuelload[i]/g)
            momentfuelload.append(mfuelload[i] * 9.81 * xfuelload[i])

print("fuel mass in kg:", mfuelload)
print("fuel moment in Nm:", momentfuelload)

#=================Calculation of mass and cg per measurement====================#

cgloc = []
mass = []
totalmoment = []
masssum = []
def cg(mpax,xpax,mBEM,xBEM,xfuelload,mfuelload):
    for i in range(len(mfuelload)):
        masssum.append(mBEM+sum(mpax))
        totalmoment.append(mBEM*xBEM*9.81)
    print("masssum is:, ",masssum)
    print("totalmoment is:, ", totalmoment)
    for j in range(len(mfuelload)):
        if j == 15:
            xpax[6] = (170+131)/2*inch
        for k in range(len(mpax)):
            totalmoment[j] += mpax[k]*xpax[k]*9.81
        masssum[j] += mfuelload[j]
        totalmoment[j] += mfuelload[j]*xfuelload[j]*9.81
        print("totalmomentj: ", totalmoment)
        cgloc.append(totalmoment[j]/9.81/masssum[j])
    return masssum,"momentsum",totalmoment,"cg",cgloc


print(cg(mpax,xpax,mBEM,xBEM,xfuelload,mfuelload))
