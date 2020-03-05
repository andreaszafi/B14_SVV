import numpy as np
import scipy.integrate as integrate


#inputs(in pounds, inches)
mtemp = 100
xtemp = 200
tempmassflow = 100
freq = 20 #[Hz]
flighttime = 90*60 #seconds
#BEM
mBEM = mtemp
xBEM = xtemp
momentBEM = mtemp * xtemp

#Payload
#People
mloc = [mtemp, mtemp,mtemp,mtemp,mtemp,mtemp,mtemp,mtemp,0,mtemp]
xloc = [131,131,214,214,251,251,288,288,0,170]
#seat 9 is empty

#Baggage
mnose, xnose = mtemp, 74
maftcabin1, xaftcabin1 = mtemp, 321
maftcabin2, xaftcabin2 = mtemp, 338
mloc.extend((mnose,maftcabin1,maftcabin2))
xloc.extend((xnose,xaftcabin1,xaftcabin2))

#totalpayload

temppayloadmoment = []
for i in range(len(mloc)):
    temppayloadmoment.append(mloc[i]*xloc[i])
mpayload = sum(mloc)
xpayload = sum(temppayloadmoment)/mpayload
momentpayload = sum(temppayloadmoment)
print(mpayload,xpayload)
#FUEL
momentZFM = momentBEM + momentpayload
mZFM = mBEM + mpayload
xZFM = momentZFM / mZFM
mfuelload = mtemp
xfuelload = xtemp
momentfuelload = mfuelload * xfuelload

#RAMP MASS
momentrampmass = momentZFM + momentfuelload
mrampmass = mZFM + mfuelload
xrampmass = momentrampmass / mrampmass

massflow = tempmassflow
usedfuel = 0
tmeasure = [10, 180, 549, 782, 3650, 3777]
mlocfuel = []
xlocfuel = []
momentlocfuel = []
for i in range(flighttime):
    usedfuel -= (tempmassflow / freq)
    if i in tmeasure:
        mlocfuel.append(mfuelload-usedfuel)
        xlocfuel.append()
        momentlocfuel.append()
print(usedfuel)

