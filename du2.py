import json
import click

def edges(soubor):
    """
    Funkce vytvoří ze souřadnic okraje bboxu
    :param soubor: nahraná data z geoJSON
    :return: množina krajních bodů (left,right,bottom,top)
    """

    #seznam, do kterého se vypíší souřadnice všech bodů
    souradnice = []
    for i in soubor['features']:
        coord = i["geometry"]["coordinates"]
        souradnice.append(coord)

    #určení nejzapadnejsiho(left) a nejvýchodnějšího(right) bodu
    dataX = sorted(souradnice, key=lambda x: x[0])
    left = dataX[0]
    right = dataX[-1]

    #určení nejsevernějšího(top) a nejjižnějšího(bottom) bodu
    dataY = sorted(souradnice, key=lambda y: y[1])
    bottom = dataY[0]
    top = dataY[-1]

    #výpis krajních hran pro vytvoření bbox
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

    #určení hran pro sektor vlevo nahoře
    if sector == 'A':
        S_le=le
        S_re=(le+re)/2
        S_be=(be+te)/2
        S_te=te
    # určení hran pro sektor vpravo nahoře
    elif sector == 'B':
        S_le=(le+re)/2
        S_re=re
        S_be=(be+te)/2
        S_te=te
    # určení hran pro sektor vlevo dole
    elif sector == 'C':
        S_le=le
        S_re=(le+re)/2
        S_be=be
        S_te=(be+te)/2
    # určení hran pro sektor vpravo dole
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
    :param sec: N-tice, která obsahuje umístění jednotlivých bodů v souboru
    :param le: levý okraj bboxu
    :param re: pravý okraj bboxu
    :param be: dolní okraj bboxu
    :param te: horní okraj bboxu
    :return:
    """

    #vytvoření seznamů, do kterých budou přidány pozice bodů v seznamu
    sectorA=[]
    sectorB=[]
    sectorC=[]
    sectorD=[]

    #výpočet polovin pro rozdělení do sektorů
    cx = (le+re)/2
    cy = (be+te)/2

    #rozdělení bodů do sektorů, přiřazení k atributu cluster_id a zapsání pozice do příslušhého seznamu
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

    #převedení seznamů na N-tice, které umožní využití ve for cyklu
    sectorA = tuple(sectorA)
    sectorB = tuple(sectorB)
    sectorC = tuple(sectorC)
    sectorD = tuple(sectorD)

    #další dělení pro sektory, které přesahují 50 bodů
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


#definování argumentů pro příkazovou řádku
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

    #podmínka pro situace, kdy výstup není zadán jako GeoJSON
    if '.geojson' not in output_name:
        print('Error: Output file is not set as G'
              'eoJSON')
        exit(2)
    #vyjimka pro situace, kdy není nahraný soubor GeoJSON
    try:
        soubor = json.load(input)
    except json.decoder.JSONDecodeError:
        print('Error: Input file is probably not JSON')
        exit(1)

    #vytvoření atributu cluster_id ve všech bodech
    for i in soubor['features']:
        i["properties"]["cluster_id"] = ''
    #určení počtu bodů v nahraném souboru
    sec = range(len(soubor['features']))

    #provedení samotného přiřazení atributů
    e = edges(soubor)
    sectors(soubor, sec, e[0], e[1], e[2], e[3])

    #zápis do souboru
    with open(output_name, mode='w', encoding='UTF-8') as f:
        json.dump(soubor, f)

#volání základní funkce
run()

