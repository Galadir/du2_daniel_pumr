# Dělení adresních bodů
Tento progra byl vytvořen v rámci domácího úkolu pro předmět Úvod do programování na Přírodovědecké fakultě Univerzity
Karlovy. Do zadání úkolu je možné nahlédnout zde:
https://github.com/xtompok/uvod-do-prg/tree/master/du2 

## Stručný popis programu
Program dokáže nahrát bodová prostorová data ze souboru formátu GeoJSON. Tato data program rozdělí do částí podle algoritmu quadtree. 

(Algoritmus quadtree vytváří kolem dat v prostoru obdelník a poté daný prostror rozdělí na čtvrtiny. Každou čtvrtinu dále
stejným způsobem dělí na menší a menší části, pokud není počet bodů v dané části menší než 50.) 

Program přiřadí nahraným datům nový atribut "cluster_id" podle toho, v jaké části se nachází. 
Nakonec jsou upravená data vyexportována jako nový soubor ve formátu GeoJSON.

## Ovládání programu
Program lze spustit v příkazové řádce pro Windows zadáním:
```
python du1.py <vstupní soubor> <název výstupního souboru>
```
Vstupní soubor musí existovat, musí být správně zadána cesta k souboru a je třeba, aby byl soubor v korektním formátu GeoJSON.
Pokud tomu tak nebude, skončí program s chybou. 
Druhý argument definující název výstupního souboru nemusí být uživatelem zadán – v takovém případě bude výstup nazván "output.geojson". 
Pokud je název zadán, ale neobsahuje koncovku .geojson, bude program ukončen s chybou.

Aby program fugoval, je třeba mít nainstalovaný modul click.

## Fungování programu
V programu je nejprve definována funkce, která určí krajní body v prostoru. 
Dále funkce, která po zadání celkových krajních bodů a definování o jaký se jedná sektor, vypočítá krajní body daného sektoru.
Hlavní funkce `sectors` nakonec přiřazuje atribut `cluster_id` podle polohy bodu vzhledem k sektorům. Funkce je rekurzivní a sama sebe volá, 
dokud není ve všech sektorech méně než padesát bodů
Všechny funkce jsou nakonec volány v rámci hlavní funkce `run`. Pro funkci run jsou také pomocí modulu click nastaveny argumenty zadávané uživatelem v příkazové řádce.
