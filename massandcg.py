#constants
inch = 0.0254
lbs = 0.453592
lbsinch = 0.113
g = 9.81

#inputs(lbs,inch)
mBEM = 9165*lbs #kg
momentBEM = 2672953.5*lbsinch
mpax = [90,102,68,70,76,82,105,87,60] #kg
xpax = [131,131,214,214,251,251,288,288,170]
xpaxmoved = [131,131,214,214,251,251,150,288,170]
mfuelstart = 2628*lbs #kg
fuelmoment = []
fuelused = [286,462,497,543,569,590,612,692,710,727,746,798,814,843,873,905] #lbs
fuelused = [i * lbs for i in fuelused]
tablefuelmass = [1700,1800,1900,2000,2100,2200,2300,2400] #lbs
tablefuelmoment = [485656,514116,542564,570990,599404,627847,656282,684696]
currentfuel = [mfuelstart/lbs - i/lbs for i in fuelused]
cg = []

#Definitions

def momentfuel(currentfuel,lowfuel,highfuel,lowmoment,highmoment):
    return lowmoment + (currentfuel-lowfuel)/(highfuel-lowfuel)*(highmoment-lowmoment)

#Calculations

totalmass = [mBEM+sum(mpax) for i in fuelused]
totalmoment = [(momentBEM + sum(mpax[j]*xpax[j]*9.81*inch for j in range(len(mpax)))) for i in range(len(fuelused) -1)]
totalmoment.append(momentBEM + sum(mpax[j]*xpaxmoved[j]*9.81*inch for j in range(len(mpax))))

currentfuel = [i * lbs for i in currentfuel]

for i in range(len(currentfuel)):
    for j in range(len(tablefuelmass)):
        if currentfuel[i]/lbs >= tablefuelmass[j] and currentfuel[i]/lbs <= tablefuelmass[j+1]:
            fuelmoment.append((momentfuel(currentfuel[i]/lbs,tablefuelmass[j],tablefuelmass[j+1],tablefuelmoment[j],\
                                          tablefuelmoment[j+1]))*lbsinch)

for l in range(len(totalmoment)):
    totalmass[l] = totalmass[l] + currentfuel[l]
    totalmoment[l] = totalmoment[l] + fuelmoment[l]

for k in range(len(totalmoment)):
    cg.append(totalmoment[k]/totalmass[k]/9.81)
print("totalmoment: ",totalmoment,"totalmass: ",totalmass,"cg: ",cg)
