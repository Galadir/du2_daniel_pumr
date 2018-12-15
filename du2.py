import json
import click

def edges(soubor):
    """
    Funkce vytvoří ze souřadnic okraje bboxu
    :param soubor: nahraná data z geoJSON
    :return: množina krajních bodů (left,right,bottom,top)
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
    """
    Funkce počítá krajní body pro jednotlivé sektory.
    :param sector: Sektor, pro který se má funkce počítat
    :param le: Levý okraj vnějšího bboxu
    :param re: Pravý okraj vnějšího bboxu
    :param be: Dolní okraj vnějšího bboxu
    :param te: Horní okraj vnějšího bboxu
    :return: množina krajních bodů sektoru (left,right,bottom,top)
    """
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


def sectors(soubor,sec,le,re,be,te):
    """
    Funkce přiřadí bodům do properties atribut cluster_id podle toho v jakém sektoru se nachází.
    funkce je rekurzivní a provádí přiřazování, dokud je v nějakém sektoru více než padesát bodů
    :param soubor: nahraná data z GeJSON, která jsou editována
    :param sec: N-tice, která obsahuje umístění features v souboru
    :param le: levý okraj bboxu
    :param re: pravý okraj bboxu
    :param be: dolní okraj bboxu
    :param te: horní okraj bboxu
    :return:
    """
    sectorA=[]
    sectorB=[]
    sectorC=[]
    sectorD=[]

    cx = (le+re)/2
    cy = (be+te)/2


    for i in sec:
        if soubor['features'][i]["geometry"]["coordinates"][0] < cx and soubor['features'][i]["geometry"]["coordinates"][1] > cy:
            soubor['features'][i]["properties"]["cluster_id"] += 'A'
            sectorA.append(i)
        elif soubor['features'][i]["geometry"]["coordinates"][0] > cx and soubor['features'][i]["geometry"]["coordinates"][1] > cy:
            soubor['features'][i]["properties"]["cluster_id"] += 'B'
            sectorB.append(i)
        elif soubor['features'][i]["geometry"]["coordinates"][0] < cx and soubor['features'][i]["geometry"]["coordinates"][1] < cy:
            soubor['features'][i]["properties"]["cluster_id"] += 'C'
            sectorC.append(i)
        elif soubor['features'][i]["geometry"]["coordinates"][0] > cx and soubor['features'][i]["geometry"]["coordinates"][1] < cy:
            soubor['features'][i]["properties"]["cluster_id"] += 'D'
            sectorD.append(i)

    sectorA = tuple(sectorA)
    sectorB = tuple(sectorB)
    sectorC = tuple(sectorC)
    sectorD = tuple(sectorD)

    if len(sectorA)>50:
        S_e=sector_edges('A',le,re,be,te)
        sectors(soubor,sectorA, S_e[0], S_e[1], S_e[2], S_e[3])
    if len(sectorB)>50:
        S_e=sector_edges('B',le,re,be,te)
        sectors(soubor,sectorB, S_e[0], S_e[1], S_e[2], S_e[3])
    if len(sectorC)>50:
        S_e=sector_edges('C',le,re,be,te)
        sectors(soubor,sectorC, S_e[0], S_e[1], S_e[2], S_e[3])
    if len(sectorD)>50:
        S_e=sector_edges('D',le,re,be,te)
        sectors(soubor,sectorD,S_e[0], S_e[1], S_e[2], S_e[3])




@click.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output_name', default='output.geojson')

def run(input,output_name):
    """
    Funkce přebírající argumenty získané pomocí modulu Click,
    volající další funkce a provádějící zbylé operace v programu.
    :param input: vstupní spoubor GeoJSON
    :param output_name: název výstpního souboru
    :return:
    """
    if '.geojson' not in output_name:
        print('Error: Output file was not set as geoJSON')
        exit(2)
    try:
        soubor = json.load(input)
    except json.decoder.JSONDecodeError:
        print('Error: Input file is probably not JSON')
        exit(1)

    for i in soubor['features']:
        i["properties"]["cluster_id"] = ''
    sec = range(len(soubor['features']))

    e = edges(soubor)
    sectors(soubor, sec, e[0], e[1], e[2], e[3])

    with open(output_name, mode='w', encoding='UTF-8') as f:
        json.dump(soubor, f)

#if __name__ == '__main__':
run()

