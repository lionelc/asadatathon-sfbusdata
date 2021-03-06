
import sys, math

def main():
    #aggregate on routes    
    routedict = dict()
    popdict = dict()
    f = open("../R/stop-line-population.csv", "r")
    line = f.readline()
    line = f.readline()

    mis_count = 0
    while line != None and len(line) > 1:
        sp = line.split(",")
        tmproute = int(float(sp[1]))
        if not tmproute in routedict:
            routedict[tmproute] = []
        routedict[tmproute].append(float(sp[7]))

        if not tmproute in popdict:
            popdict[tmproute] = []
            
        if float(sp[14]) >= 0: # and float(sp[11]) >= 0:
            popdict[tmproute].append(float(sp[14]))
        else:
            mis_count += 1
        line = f.readline()
    f.close()

    ts1 = []
    ts2 = []

    for elem in routedict:
        avgload = sum(routedict[elem]) #/float(len(routedict[elem]))
        ts1.append(avgload)
        ts2.append(sum(popdict[elem])) #/len(popdict[elem]))

    avg1 = sum(ts1)/float(len(ts1))
    avg2 = sum(ts2)/float(len(ts2))

    print len(ts1)

    #compute Pearson's r correlation coefficient
    r1 = 0.0
    r2 = 0.0
    r3 = 0.0
    for i in range(len(ts1)):
        r1 += (ts1[i]-avg1)*(ts2[i]-avg2)
        r2 += (ts1[i]-avg1)*(ts1[i]-avg1)
        r3 += (ts2[i]-avg2)*(ts2[i]-avg2)

    print r1/math.sqrt(r2)/math.sqrt(r3)
        

if __name__ == "__main__":
    main()
