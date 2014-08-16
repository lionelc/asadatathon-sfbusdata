
import sys, os, json

def main():
    lldict = dict()
    #read file and extract all the lat lngs
    f = open("/cygdrive/e/WebDownloads/passenger-count.csv" , "r")
    line = f.readline()
    line = f.readline()
    while line != None and len(line) > 1:
        sp = line.split(",")
        try:
            tmplat = float(int(float(sp[10])*100.0))/100.0
            tmplng = float(int(float(sp[11])*100.0))/100.0
            llkey = str(tmplat)+"%2c-"+str(tmplng)
            lldict[llkey] = 0
        except ValueError:
            pass  
        line = f.readline()
    f.close()

    #call the web service to get demographics info
    print len(lldict)
    ind = 1
    for elem in lldict:
        os.system("curl 'http://www.datasciencetoolkit.org/coordinates2statistics/"+elem+"' > tmpstats.json")
        f = open("tmpstats.json", "r")
        fdata = f.read()
        data = json.loads(fdata)
        res = []
        try:
            res.append(str(data[0]["statistics"]["us_housing_units_no_vehicle"]["value"]))
            res.append(str(data[0]["statistics"]["us_housing_units_no_vehicle"]["proportion_of"]))
        except KeyError:
            res.append("-1")
            res.append("-1")

        try:
            res.append(str(data[0]["statistics"]["us_population_low_income"]["value"]))
            res.append(str(data[0]["statistics"]["us_population_low_income"]["proportion_of"]))
        except KeyError:
            res.append("-1")
            res.append("-1")

        try:
            res.append(str(data[0]["statistics"]["population_density"]["value"]))
        except KeyError:
            res.append("-1")

        try:
            res.append(str(data[0]["statistics"]["us_population"]["value"]))
        except KeyError:
            res.append("-1")

        try:
            res.append(str(data[0]["statistics"]["us_population_eighteen_to_twenty_four_years_old"]["value"]))
            res.append(str(data[0]["statistics"]["us_population_eighteen_to_twenty_four_years_old"]["proportion_of"]))
        except KeyError:
            res.append("-1")
            res.append("-1")
            
        try:
            res.append(str(data[0]["statistics"]["us_population_twenty_five_to_sixty_four_years_old"]["value"]))
            res.append(str(data[0]["statistics"]["us_population_twenty_five_to_sixty_four_years_old"]["proportion_of"]))
        except KeyError:
            res.append("-1")
            res.append("-1")
            
        lldict[elem] = res
        f.close()
        print ind
        ind += 1

    #append the new 10 rows to the original file
    colnum = 10
    f1 = open("/cygdrive/e/WebDownloads/passenger-count.csv" , "r")
    f2 = open("passenger-count-new.csv", "w")
    line = f1.readline()
    line = line[:-1]+",us_housing_units_no_vehicle_po,us_housing_units_no_vehicle,us_population_low_income_po,us_population_low_income,population_density,us_population,us_population_eighteen_to_twenty_four_years_old,us_population_eighteen_to_twenty_four_years_old_po,us_population_twenty_five_to_sixty_four_years_old_po,us_population_twenty_five_to_sixty_four_years_old"
    f2.write(line+"\n")
    ind = 1
    line = f1.readline()
    while line != None and len(line) > 1:
        sp = line.split(",")
        try:
            tmplat = float(int(float(sp[10])*100.0))/100.0
            tmplng = float(int(float(sp[11])*100.0))/100.0
            llkey = str(tmplat)+"%2c-"+str(tmplng)
            tmpres = lldict[llkey]
        except ValueError:
            tmpres = ["-1"]*colnum
        line = line[:-1]+","
        for j in range(colnum):
            line += tmpres[j]
            if j < colnum-1:
                line += ","
        line += "\n"
        f2.write(line)
        line = f1.readline()
        if ind % 2000 == 0:
            print ind
        ind += 1
    f2.close()
    f1.close()
    

if __name__ == "__main__":
    main()
