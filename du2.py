import json

with open("drinking_water.geojson",encoding="utf-8") as f:
    soubor = json.load(f)


def edges(soubor):
    """
    Funkce vytvoří ze souřadnic okraje bboxu
    :param soubor: nahraná data z geoJSON
    :return: množina krajních bodů (left,right, bottom, top, centerX,centerY)
    """

    souradnice = []
    for i in soubor['features']:
        coord = i["geometry"]["coordinates"]
        souradnice.append(coord)

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


    return left_edge,right_edge,bottom_edge,top_edge

def sector_edges(sector,le,re,be,te):
    if sector == 'A':
        S_le=le
        S_re=(le+re)/2
        S_be=(be+te)/2
        S_te=te
    elif sector == 'B':
        S_le=(le+re)/2
        S_re=re
        S_be=(be+te)/2
        S_te=te
    elif sector == 'C':
        S_le=le
        S_re=(le+re)/2
        S_be=be
        S_te=(be+te)/2
    elif sector == 'D':
        S_le=(le+re)/2
        S_re=re
        S_be=be
        S_te=(be+te)/2
    return S_le,S_re,S_be,S_te


def sectors(soubor,le,re,be,te):
    """
    Funkce přiřadí bodům do properties atribut cluster_id podle too v jakém sektoru se nachází
    :param soubor:nahraná data z geoJSON
    :return:
    """
    sectorA=[]
    sectorB=[]
    sectorC=[]
    sectorD=[]

    cx = (le+re)/2
    cy = (be+te)/2


    for i in soubor['features']:
        if i["geometry"]["coordinates"][0] < cx and i["geometry"]["coordinates"][1] > cy:
            i["properties"]["cluster_id"] += 'A'
            sectorA.append(i)
        elif i["geometry"]["coordinates"][0] > cx and i["geometry"]["coordinates"][1] > cy:
            i["properties"]["cluster_id"] += 'B'
            sectorB.append(i)
        elif i["geometry"]["coordinates"][0] < cx and i["geometry"]["coordinates"][1] < cy:
            i["properties"]["cluster_id"] += 'C'
            sectorC.append(i)
        elif i["geometry"]["coordinates"][0] > cx and i["geometry"]["coordinates"][1] < cy:
            i["properties"]["cluster_id"] += 'D'
            sectorD.append(i)

    print(sectorA)
    print(sectorB)
    print(sectorC)
    print(sectorD)

    if len(sectorA)>10:
        S_e=sector_edges('A',le,re,be,te)
        (soubor,sectorA, S_e[0], S_e[1], S_e[2], S_e[3])
    if len(sectorB)>10:
        S_e=sector_edges('B',le,re,be,te)
        (soubor,sectorB, S_e[0], S_e[1], S_e[2], S_e[3])
    if len(sectorC)>10:
        S_e=sector_edges('C',le,re,be,te)
        (soubor,sectorC, S_e[0], S_e[1], S_e[2], S_e[3])
    if len(sectorD)>10:
        S_e=sector_edges('D',le,re,be,te)
        (soubor,sectorD,S_e[0], S_e[1], S_e[2], S_e[3])


for i in soubor['features']:
    i["properties"]["cluster_id"] = ''

# sector_calc=[]
# for i in soubor['features']:
#     sector_calc.append(i)
#     print(sector_calc)

sec= range(len(soubor['features']))
print(sec)

e=edges(soubor)
sectors(soubor,e[0],e[1],e[2],e[3])


features = soubor['features'][1]
print(features)



with open('drinking_water_pokus6.geojson', mode = 'w',encoding='UTF-8') as f:
    json.dump(soubor,f)