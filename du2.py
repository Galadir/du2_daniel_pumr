import json

with open("drinking_water.geojson",encoding="utf-8") as f:
    soubor = json.load(f)

# print(type(soubor)) #zjistím o jaký se jedný typ → dic= slovník
# for k in soubor: #chci zjistit jaké jsou klíče
#    print(k)

souradnice=[]
features = soubor['features']
print(features)
for i in features:
    geo = i["geometry"]
    coord = geo["coordinates"]
    souradnice.append(coord)

print(souradnice)

def edges(souradnice):
    """
    Funkce vytvoří ze souřadnic okraje bboxu
    :param souradnice: list souřadnic
    :return: množina krajních bodů (left,right, bottom, top, centerX,centerY)
    """
    dataX = sorted(souradnice, key=lambda x: x[0])
    left = dataX[0]
    right = dataX[-1]

    dataY = sorted(souradnice, key=lambda y: y[1])
    bottom = dataY[0]
    top = dataY[-1]

    left_edge = left[0]
    right_edge = right[0]
    bottom_edge = bottom[1]
    top_edge = top[1]
    center_X = (left_edge+right_edge)/2
    center_Y = (bottom_edge+top_edge)/2

    return(left_edge,right_edge,bottom_edge,top_edge,center_X,center_Y)

# ans=edges(souradnice)
# print(ans)

for i in soubor['features']:
    i["properties"]["cluster_id"] = 1

features = soubor['features']
print(features)


with open('drinking_water_pokus.geojson', mode = 'w',encoding='UTF-8') as f:
    json.dump(soubor,f)