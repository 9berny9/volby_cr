# **VOLBY ČR**
Výsledky voleb do Poslanecké sněmovny Parlamentu České republiky.

## **Popis projektu**
Tento projekt slouží k extrahování výsledků z parlamentních voleb pro dostupná data od roku 2006 do 2021. Výsledky voleb lze extrahovat podle výsledků krajů, okresů nebo obcí v okresech.

Odkaz k prohlédnutí stránky [zde](https://www.volby.cz).

## **Instalace knihoven**
Knihovny, které jsou použity v kódu jsou uloženy v souboru `requirements.txt`. 
Pro instalaci doporučuji použít nové virtuální prostředí:
```
$ pip3 --version git status            # overim verzi manazeru
$ pip3 install -r requirements.txt      # nainstaluji knihovny
```
## **Spuštění projektu**
Spuštění souboru `volby-scraper.py` v příkazovém řádku pomocí povinného argumentu.
Povinný argument musí odkazovat na hlavní stránku volby.cz

`python volby_scraper <odkaz--volby-cr>`

Následně budete dotazování na výsledky, které chcete stáhnout a během pár vteřin se výsledky uloží jako soubor s příponou `.csv` 

## **Ukázka projektu**
**Spuštění programu:**
```
python volby_scraper.py 'https://www.volby.cz'
```
**Průběh dotazování:**

1. Výsledky pro dostupné roky z odkazu, ale pouze od roku 2006.
```
Výsledky voleb za roky:
2006    2010    2013    2017    2021
--------------------------------------
Zadej rok výsledků: 2010                    # pro výsledky za rok 2010
```
2. Typ výsledků, které požadujete exportovat.
```
Vyber číslem výsledky z následujících možností:
1. výsledky krajů
2. výsledky okresů
3. výsledky obcí podle okresu
-------------------------------------
Zadej číslo výsledků: 3                     # pro stažení výsledků obcí v konkrétním okrese
```
3. Pokud si zvolíte výsledky obcí podle okresu, tak zvolíte okres. V jiných případech už dojde ke stažení výsledků.
```
{1: 'Praha',
 2: 'Benešov',
 3: 'Beroun',
 4: 'Kladno',
 5: 'Kolín',
 ...
 ...
 ...
 
 Zadej číslo výsledků obcí v okrese: 2     # pro stažení výsledků obcí v okrese Benešov
```
**Ukončení programu:**
```
---------------------------------------------------
NAČÍTÁM DATA
---------------------------------------------------
Výsledky obcí v okrese byly převedeny do csv
a uloženy pod názvem vysledky_benesov.csv
===================================================
VYPÍNÁM PROGRAM
===================================================
```
Výstup programu v csv:
```
Název;Voliči v seznamu;Vydané obálky;Platné hlasy....
Benešov;13246;8589;8584....
Bernartice;202;144;144....
Bílkovice;161;110;110....
Blažejovice;90;68;68....
....
```
