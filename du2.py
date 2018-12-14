import json

with open("drinking_water.geojson",encoding="utf-8") as f:
    soubor = json.load(f)

#print(type(soubor)) #zjistím o jaký se jedný typ → dic= slovník
#for k in soubor: #chci zjistit jaké jsou klíče
   #print(k)


features = soubor['features']
#print(type(soubor['features']))
for i in features:
    geo = i["geometry"]
    coord = geo["coordinates"]
    print(coord)

