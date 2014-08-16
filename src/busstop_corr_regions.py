
import sys, math

def main():
    #aggregate on stop    
    stopdict = dict()
    popdict = dict()
    f = open("../R/stop-line-population.csv", "r")
    line = f.readline()
    line = f.readline()

    mis_count = 0
    while line != None and len(line) > 1:
        sp = line.split(",")
        tmpstop = int(float(sp[2]))
        if not tmpstop in stopdict:
            stopdict[tmpstop] = []
        stopdict[tmpstop].append(float(sp[7]))
        if  float(sp[15]) >=0: # and float(sp[11]) >= 0:
            popdict[tmpstop] = float(sp[15]) #*float(sp[11]) #float(sp[10])*float(sp[11]) #+float(sp[12])*float(sp[13])
        else:
            popdict[tmpstop] = 0
            mis_count += 1
        line = f.readline()
    f.close()

    maxcorr = -1.0
    mincorr = 1.0
    maxroute = 0
    minroute = 0

    for pelem in stopdict:
        
        ts1 = []
        ts2 = []

        tmpsum = 0.0
        
        for elem in stopdict:       
            tmpsum += popdict[elem]

        validavg = tmpsum/float(len(popdict)-mis_count)
        for elem in stopdict:
            if pelem == elem:
                continue
            avgload = sum(stopdict[elem])#/float(len(stopdict[elem]))
            ts1.append(avgload)
            if popdict[elem] > 0.0:
                ts2.append(popdict[elem])
            else:
                ts2.append(validavg)

        avg1 = sum(ts1)/float(len(ts1))
        avg2 = sum(ts2)/float(len(ts2))

        #print len(ts1)

        #compute Pearson's r correlation coefficient
        r1 = 0.0
        r2 = 0.0
        r3 = 0.0
        for i in range(len(ts1)):
            r1 += (ts1[i]-avg1)*(ts2[i]-avg2)
            r2 += (ts1[i]-avg1)*(ts1[i]-avg1)
            r3 += (ts2[i]-avg2)*(ts2[i]-avg2)

        corr =  r1/math.sqrt(r2)/math.sqrt(r3)

        if corr > maxcorr:
            maxcorr = corr
            maxroute = pelem

        if corr < mincorr:
            mincorr = corr
            minroute = pelem

        #print str(pelem)+":"+str(corr)

    print "min stop="+str(minroute)+" "+str(mincorr)
    print "max stop="+str(maxroute)+" "+str(maxcorr)
        

if __name__ == "__main__":
    main()
