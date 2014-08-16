
#gdal is required for getting zipcode from shapefile
#from osgeo import ogr
import os, json

#read shapefile to get zipcode
def readZipCode():
    shapeData = ogr.Open("E:/Projects/contests/data_challenges/asadatathon/newdata/bayarea_zipcodes", 1)
    layer = shapeData.GetLayer()
    zipar = []
    for i in xrange(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        tmpar = []
        for j in range(3):
            tmpar.append(feature.GetFieldAsString(j))
        zipar.append(tmpar)
        #layer = shapeData.GetLayer()
    return zipar

#input one zipcode, query google map api to get its bounding box as lat lng min max
def getZipcodeCoords(zcode):
    os.system("curl http://maps.googleapis.com/maps/api/geocode/json?address="+str(zcode)+" > tmp.json")
    f = open("tmp.json", "r")
    fdata = f.read()
    data = json.loads(fdata)
    res = []
    try:
        tmplat = []
        tmplat.append(data["results"][0]["geometry"]["bounds"]["northeast"]["lat"])
        tmplat.append(data["results"][0]["geometry"]["bounds"]["southwest"]["lat"])
        tmplng = []
        tmplng.append(data["results"][0]["geometry"]["bounds"]["northeast"]["lng"])
        tmplng.append(data["results"][0]["geometry"]["bounds"]["southwest"]["lng"])
    except:
        return []
    res.append(tmplat)
    res.append(tmplng)
    f.close()
    return res
    
def main():
    #zipcodes = readZipCode()
    #fw = open("zipcodes.csv", "w")
    #for elem in zipcodes:
    #    for j in range(len(elem)):
    #        fw.write(str(elem[j]))
    #        if j < len(elem)-1:
    #            fw.write(",")
    #    fw.write("\n")
    #fw.close()
    f = open("zipcodes.csv", "r")
    lines = f.readlines()
    f.close()
    fw = open("zipcoords2.csv", "w")
    ind = 1
    for line in lines:
        curcode = line.split(",")[0]
        curcoord = getZipcodeCoords(curcode)
        if len(curcoord) > 0:
            fw.write(curcode+","+str(curcoord[0][0])+","+str(curcoord[0][1])+","+str(curcoord[1][0])+","+str(curcoord[1][1])+"\n")
        print str(ind)
        ind +=1 
    fw.close()
    
if __name__ == "__main__":
    main()
