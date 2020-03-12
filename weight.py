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
g = 9.80665

#tempmassflow = 100
#freq = 20 #[Hz]
#flighttime = 90*60 #seconds
#BEM
mBEM = 9165*lbs
#print(mBEM)
xBEM = 291.65*inch
momentBEM = mBEM * xBEM
#Payload
#People

mpax = [90,102,68,70,76,82,105,87,0,60]
xpax = [131,131,214,214,251,251,288,288,170,170]
xpax = [i * inch for i in xpax]
#seat 9 is empty

#Baggage
mnose, xnose = mtemp, 74
maftcabin1, xaftcabin1 = mtemp, 321
maftcabin2, xaftcabin2 = mtemp, 338
#mpax.extend((mnose,maftcabin1,maftcabin2))
#xpax.extend((xnose,xaftcabin1,xaftcabin2))

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
momentZFM = momentBEM + momentpayload
mZFM = mBEM + mpayload
xZFM = momentZFM / mZFM
mfuelloadstart = 2628*lbs

#momentfuelload = mfuelload * xf0
wf = [286,462,497,543,569,590,612,692,710,727,746,798,814,843,873,905]
wf = [i * lbs for i in wf]


for i in range(len(wf)):
    mfuelload.append(mfuelloadstart - wf[i])
    for j in range(len(fuelmass)):
        if mfuelload[i]/lbs >= fuelmass[j] and mfuelload[i]/lbs <= fuelmass[j+1]:
            xfuelload.append(interpolate(mfuelload[i],fuelmass[j]*lbs,fuelmass[j+1]*lbs,fuelmoment[j]*lbsinch,fuelmoment[j+1]*lbsinch)/ mfuelload[i]/g)

#print(xfuelload)
#print(mfuelload)
#print(wf)


#RAMP MASS
#momentrampmass = momentZFM + momentfuelload
#mrampmass = mZFM + mfuelload
#xrampmass = momentrampmass / mrampmass

#=================Calculation of mass and cg per measurement====================#

cgloc = []
mass = []
def cg(mpax,xpax,mBEM,xBEM,xfuelload,mfuelload):
    for i in range(len(mfuelload)):
        momentsum = [mBEM*xBEM,mfuelload[i]*xfuelload[i]]
        masssum = [mBEM,mfuelload[i]]
        if i == 15:
            xpax[6] = (171+131)/2*inch
            print(xpax[6])
        for j in range(len(mpax)):
            #print(mpax,xpax)
            momentsum.append(mpax[j]*xpax[j])
            masssum.append(mpax[j])
        mass.append(sum(masssum))
        cgloc.append(sum(momentsum)/sum(masssum))
    return mass, cgloc
print(cg(mpax,xpax,mBEM,xBEM,xfuelload,mfuelload))
