import json

with open("drinking_water.geojson",encoding="utf-8") as f:
    soubor = json.load(f)

#print(type(soubor)) #zjistím o jaký se jedný typ → dic= slovník
#for k in soubor: #chci zjistit jaké jsou klíče
   #print(k)

souradnice=[]

features = soubor['features']
#print(type(soubor['features']))
for i in features:
    geo = i["geometry"]
    coord = geo["coordinates"]
    #print(coord)
    souradnice.append(coord)

print(souradnice)

dataX = sorted(souradnice, key=lambda x: x[0])
left_edge = dataX[0]
right_edge = dataX[-1]

dataY = sorted(souradnice, key=lambda y: y[1])
bottom_edge = dataY[0]
top_edge = dataY[-1]

print(left_edge)
print(right_edge)
print(bottom_edge)
print(top_edge)