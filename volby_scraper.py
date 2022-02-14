import csv
import requests
import pprint
import sys
import unidecode
from bs4 import BeautifulSoup as BS


def main() -> None:
    hlavni_url = spusteni_argumentem()
    rok = uvitani_a_vyber_roku(hlavni_url)
    url = url_pro_vybrany_rok(rok)
    vyber_pozadavku = vyber_vysledku_pro_rok(rok)

    # podle volby uzivatele nacte data pro scraping
    if vyber_pozadavku == "1":
        # scraping pro kraje s nastavenymi parametry
        data_scraping = sber_dat_pozadavku(url, nastaveni_hledani= ['h3',{'class':'kraj'}])
        program_kraje(data_scraping, vyber_pozadavku, rok)
        ukonceni_programu(vyber_pozadavku, None)
    elif vyber_pozadavku == "2":
        # scraping pro okresy s nastavenymi parametry
        data_scraping = sber_dat_pozadavku(url, nastaveni_hledani=['table',None])
        program_okres(data_scraping, vyber_pozadavku, rok)
        ukonceni_programu(vyber_pozadavku, None)
    elif vyber_pozadavku == "3":
        # scraping pro obce s nastavenymi parametry
        data_scraping = sber_dat_pozadavku(url, nastaveni_hledani=['table',None])
        nazev_souboru = program_obec(data_scraping, vyber_pozadavku, rok)
        ukonceni_programu(vyber_pozadavku, nazev_souboru)

def spusteni_argumentem() -> str:
    '''
    Spuštění přes terminál pomocí jednoho argumentu proběhne
    pokud je správně zadaný argument, jinak vypne program.
    :return: str
    '''
    if sys.argv[1] == "https://volby.cz/" or "https://volby.cz" or "volby.cz" or "www.volby.cz":
        url = "https://volby.cz"
        return url
    else:
        print("ŠPATNÁ URL PROGRAMU!\nVYPÍNÁM PROGRAM")
        quit()

def uvitani_a_vyber_roku(hlavni_url) -> str:
    '''
    Vypíše ůvod programu a provede scraping pro získání zvoleného roku voleb.
    :return str
    '''
    uvitani = "Výsledky voleb do poslanecká sněmovny Parlamentu ČR"
    print(separator(symbol="~", delka=len(uvitani)))
    print(uvitani)
    print(separator(symbol= "~", delka=len(uvitani)))

    data_roku = sber_dat_pozadavku(hlavni_url,nastaveni_hledani= ['table',{'class':'home'}])
    rok = program_roky(data_roku)
    return rok

def separator(symbol,delka=45) -> str:
    '''
    Funkce vrací string pomocí zadaného symbolu a délky stringu
    :param symbol:  znak separátoru
    :param delka:   délka separátoru
    :return:        string
    '''
    separator = symbol * delka
    return separator

def sber_dat_pozadavku(url, nastaveni_hledani):
    '''
    Funkce volá funkci make_soup pro požadavek get
    a pomocí knihovny b4 vybere data podle seznamu zadaných parametrů.
    :param nastaveni_hledani: například list ['table', None] nebo ['table', {'class':'overflow'}]
    :return: bs4.BeautifulSoup
    '''
    result = make_soup(url)
    nactene_data = result.findAll(nastaveni_hledani[0],nastaveni_hledani[1])
    return nactene_data

def make_soup(URL):
    '''
    Funkce odesila pozadavek 'get' na zadanou adresu 'url'.
    Naslednou odpoved parsuje pomoci knihovny 'bs4'.

    :return: type is bs4.BeautifulSoup
    '''
    try:
        page = requests.get(URL)
        data = page.text
        soup = BS(data, "html.parser")
        return soup
    except HTTPError:
        print('Could not retrieve the page')
    except:
        print(sys.exc_info()[:1])

def program_roky(data) -> str:
    '''
    Funkce z dat v knihovně bs4 provede vnitřní funkce a vrátí zadaný rok výsledků.
    :param data: bs4.BeautifulSoup
    :return: str
    '''

    seznam_roku = hledani_odkazu_a_roku(data, nastaveni_hledani=["tr", {"class":"sudy"}], nastaveni_indexu=1)
    del seznam_roku[0:3]

    rok = vyber_vysledku_zvoleneho_roku(seznam_roku)
    return rok

def hledani_odkazu_a_roku(data, nastaveni_hledani, nastaveni_indexu) -> list:
    '''
    Funkce z dat bs4 rozdeli text v elementu podle nastaveneho hledani a indexu a vrátí seznam roků.
    :param data: bs4.BeautifulSoup
    :param nastaveni_hledani: například list ["tr", {"class":"sudy"}]
    :param nastaveni_indexu: int
    :return: list
    '''
    seznam_roku = []
    filtrovane_roky = []
    for table in data:
        for link in table.find_all(nastaveni_hledani):
            filtrovane_roky.append(link)
    filtrovane_roky = filtrovane_roky[nastaveni_indexu]
    bunka = filtrovane_roky.find_all("a")
    for i in bunka:
        seznam_roku.append(i.contents[0])
    return seznam_roku

def vyber_vysledku_zvoleneho_roku(seznam_roku) -> str:
    '''
    Funkce vypíše dostupné roky výsledků a zeptá se na požadovaný rok výsledků.
    :param seznam_roku: list
    :return: str
    '''
    print("Výsledky voleb za roky:")
    print("\t".join(seznam_roku))
    print(separator(symbol= "-", delka=51))
    vyber_roku = input("Zadej rok výsledků: ")
    print(separator(symbol="=", delka=51))
    return vyber_roku

def url_pro_vybrany_rok(vyber_roku) -> str:
    '''
    Funkce vybere url adresu pro vybraný rok.
    Pokud vybraný rok neexistuje, tak vypne program
    :param vyber_roku: str
    :return: str
    '''
    if vyber_roku == "2006":
        url = "https://volby.cz/pls/ps2006/ps3?xjazyk=CZ"
    elif vyber_roku == "2010":
        url = "https://volby.cz/pls/ps2010/ps3?xjazyk=CZ"
    elif vyber_roku == "2013":
        url = "https://volby.cz/pls/ps2013/ps3?xjazyk=CZ"
    elif vyber_roku == "2017":
        url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    elif vyber_roku == "2021":
        url = "https://volby.cz/pls/ps2021/ps3?xjazyk=CZ"
    else:
        print("Zadaná rok není v možnostech\nVYPÍNÁM PROGRAM")
        quit()
    return url

def vyber_vysledku_pro_rok(rok) -> str:
    '''
    Funkce vypíše možnosti druhů výsledků voleb a zeptá se, kterou volbu uživatel požaduje.
    Pokud zvolená volba není v možnostech, tak vypíná program.
    :param rok: str
    :return: str
    '''

    print(f"""VÝSLEDKY VOLEB {rok}""")
    print(separator(symbol="-", delka=51))
    print(f"""Vyber číslem výsledky z následujících možností:
1. výsledky krajů
2. výsledky okresů
3. výsledky obcí podle okresu""")
    print(separator(symbol="-", delka=51))
    vstup = input("Zadej číslo výsledků: ")
    print(separator(symbol="-", delka=51))
    print("NAČÍTÁM DATA")
    print(separator(symbol="-", delka=51))
    # Pokud uživatel zadá číslo z možností pokračuj nebo vypni program
    if vstup.isdigit() and int(vstup) in range(1,4):
        return vstup
    else:
        print("Zadaná hodnota není v možnostech\nVYPÍNÁM PROGRAM")
        quit()
    return vstup

def program_kraje(data, pozadavek, rok):
    '''
    Funkce provádí vnitrní funkce pro výsledky krajů z dat
    v knihovně bs4 pro vybraný rok a druh výsledků.
    :param data: bs4.BeautifulSoup
    :param pozadavek: str
    :param rok: str
    '''
    seznam_nazvu_kraju = vyhledavani_nazvu_nadpisem(data)
    seznam_url_kraju = vyhledavani_url_nadpisem(data)
    seznam_cele_url_kraju = tvorba_cele_url(seznam_url_kraju, rok)
    # vybere nazvy headers pouze z jedne url, protoze jsou vsude stejne
    headers_to_convert = sber_headers(seznam_cele_url_kraju[0], rok)
    data_to_convert = sber_dat_pro_vsechny_stranky(seznam_cele_url_kraju,seznam_nazvu_kraju, rok)
    ulozeni_do_csv(headers_to_convert, data_to_convert, pozadavek, None)

def vyhledavani_nazvu_nadpisem(data) -> list:
    '''
    Funkce z dat bs4 rozdělí text v elementu na názvy krajů.
    :param data: bs4.BeautifulSoup
    :return: list
    '''
    nazvy_nadpisu = []
    for nadpis in data:
        nazev = nadpis.string
        nazvy_nadpisu.append(nazev)
    return nazvy_nadpisu

def vyhledavani_url_nadpisem(data) -> list:
    '''
    Funkce z dat bs4 rozdělí text v elementu na url krajů.
    :param data: bs4.BeautifulSoup
    :return: list
    '''
    url_nadpisu = []
    for link in data:
        nadpis = link.find("a")
        url_nadpisu.append(nadpis.get("href"))
    return url_nadpisu

def tvorba_cele_url(seznam_short_url, vyber_roku) -> list[str]:
    '''
    Funkce z přednastavených url pro daný rok vytvoří
    list celých hledaných url pro všechny kraje.
    :param seznam_short_url: list
    :param vyber_roku: str
    :return: list[str]
    '''
    if vyber_roku == "2006":
        url = "https://volby.cz/pls/ps2006/"
    elif vyber_roku == "2010":
        url = "https://volby.cz/pls/ps2010/"
    elif vyber_roku == "2013":
        url = "https://volby.cz/pls/ps2013/"
    elif vyber_roku == "2017":
        url = "https://volby.cz/pls/ps2017nss/"
    elif vyber_roku == "2021":
        url = "https://volby.cz/pls/ps2021/"
    else:
        print("Zadaná rok není v možnostech\nVYPÍNÁM PROGRAM")
        quit()
    url_cela = []
    # vytvori celou url pro vsechny kraje
    for i in seznam_short_url:
        url_cela.append((url + i))
    return url_cela

def sber_headers(odkaz, rok) -> list[str]:
    '''
    Funkce z url pomocí vnitřních funkcí scrapuje nadpisy názvů pro export do csv.
    :param odkaz: str
    :param rok: str
    :return: list[str]
    '''
    headers_nazvy = data_for_csv(odkaz, nastaveni_kroku=[1, 6, None], hledani_sloupcu=['th', None], krok_tabulky=[0])
    headers_nazvy = ["Název", headers_nazvy[0], headers_nazvy[1], headers_nazvy[4]]

    headers_strany = headers_vsechny_strany(rok)
    headers = headers_nazvy + list(headers_strany.values())
    return headers

def data_for_csv(url, nastaveni_kroku, hledani_sloupcu, krok_tabulky) -> list:
    '''
    Funkce pomocí vnitřních funkcí získá data pro obsah tabulky k exportu.
    Parametry se zadávají pomocí listu, který umožní množství kombinací hledání.
    Pokud u indexu v listu nevyžadujeme žádnou hodnotu vyplníme jako None.
    :param url: str
    :param nastaveni_kroku: například list [1, 6, None] -> pro vybrání konkrétních sloupců
    :param hledani_sloupcu: například list ['th', None] -> pro hledání v html
    :param krok_tabulky: například list [0] -> pro vybrání tabulky nebo tabulek
    :return: list
    '''
    precti_data = sber_dat_pozadavku(url, nastaveni_hledani=['table', None])
    bunka = vyhledavani_nazvu_tabulkou(precti_data, nastaveni_kroku, hledani_sloupcu, krok_tabulky)
    return bunka

def vyhledavani_nazvu_tabulkou(data,nastaveni_kroku, hledani_sloupcu, krok_tabulky) -> list:
    '''
    Funkce získává hodnoty knihovny bs4, které využíváme pro pozdější export headers.
    Parametry se zadávají pomocí listu, který umožní množství kombinací hledání.
    Pokud u indexu v listu nevyžadujeme žádnou hodnotu vyplníme jako None.
    :param data: bs4.Beautifulsoup
    :param nastaveni_kroku: například list [1, 6, None] -> pro vybrání konkrétních sloupců
    :param hledani_sloupcu: například list ['th', None] -> pro hledání v html
    :param krok_tabulky: například list [0] -> pro vybrání tabulky nebo tabulek
    :return: list
    '''
    seznam_sloupcu = []
    bunky = []
    for table in data[krok_tabulky[0] : None : None]:
        for link in table.find_all(hledani_sloupcu[0],hledani_sloupcu[1]):
            bunka = link.get_text(" ")
            bunky.append(bunka)
    for i in bunky[nastaveni_kroku[0] : nastaveni_kroku[1] : nastaveni_kroku[2]]:
        seznam_sloupcu.append(i)
    # odstrani prazdne radky v tabulkach
    seznam_sloupcu = [i for i in seznam_sloupcu if i != "-"]
    return seznam_sloupcu

def headers_vsechny_strany(rok) -> dict:
    '''
    Funkce pro vybraný rok načte z url nadpisy stran pomocí vnitřní funkce do listu
     a následně vytvoří slovník očíslovaných stran.
    :param rok: str
    :return: dict
    '''
    if rok == "2006":
        url = "https://volby.cz/pls/ps2006/ps11?xjazyk=CZ&xv=1&xt=1"
    elif rok == "2010":
        url = "https://volby.cz/pls/ps2010/ps11?xjazyk=CZ&xv=1&xt=1"
    elif rok == "2013":
        url = "https://volby.cz/pls/ps2013/ps11?xjazyk=CZ&xv=1&xt=1"
    elif rok == "2017":
        url = "https://volby.cz/pls/ps2017nss/ps11?xjazyk=CZ&xv=1&xt=1"
    elif rok == "2021":
        url = "https://volby.cz/pls/ps2021/ps11?xjazyk=CZ&xv=1&xt=1"

    headers_strany = data_for_csv(url, nastaveni_kroku=[1, None, None],
                                  hledani_sloupcu=['th', {"class":"leg_sloupec"}], krok_tabulky=[0])
    rozdeleny = []
    slovnik_headers_stran = dict()
    # pro kazdy nazev v listu rozdeli list podle mezery na dva stringy
    for nazev in headers_strany:
        rozdeleny.append(nazev.split())
    # z rozdeleneho listu prida do prazdneho slovniku prvni index jako key a druhy jako value
    for i in rozdeleny:
        slovnik_headers_stran.update([(i[0], i[1])])
    return slovnik_headers_stran

def sber_dat_pro_vsechny_stranky(seznam_url, seznam_nazvu, rok) -> list:
    '''
    Funkce pomocí vnitřní funkce vytvoří pro každou url seznam, který vloží do hlavního seznamu.
    :param seznam_url: list
    :param seznam_nazvu: list
    :param rok: str
    :return: list[list]
    '''
    seznam_dat_vsech_stranek = []
    nazvy = []
    data_vsechny_radky = []
    for i in seznam_nazvu:
        nazvy.append(i)
    for link in seznam_url:
        data_radku = sber_dat_jedne_stranky(link, rok)
        data_vsechny_radky.append(data_radku)
    for i in range(len(nazvy)):
        seznam_dat_vsech_stranek.append([nazvy[i]])
        seznam_dat_vsech_stranek[i].extend(data_vsechny_radky[i])

    return seznam_dat_vsech_stranek

def sber_dat_jedne_stranky(odkaz, rok) -> list:
    '''
    Funkce pomocí vnitřních funkcí sbírá data z jedné url a vkládá do seznamu pro následný export.
    :param odkaz: str
    :param rok: str
    :return: list
    '''
    data_z_tabulek = data_for_csv(odkaz, nastaveni_kroku=[0, None, None], hledani_sloupcu=['td', {"class": "cislo"}],
                                  krok_tabulky=[0])
    # vybere sloupce podle indexu
    data_z_tabulek = [data_z_tabulek[3], data_z_tabulek[4], data_z_tabulek[6]]

    upravena_data_tabulek = odstraneni_specialnich_znaku(data_z_tabulek)

    cislo_dat_strany = data_for_csv(odkaz, nastaveni_kroku=[0, None, 3], hledani_sloupcu=['td', {"class": "cislo"}],
                              krok_tabulky=[1])

    data_stran = data_for_csv(odkaz, nastaveni_kroku=[1, None, 3], hledani_sloupcu=['td', {"class": "cislo"}],
                              krok_tabulky=[1])

    upravena_data_stran = odstraneni_specialnich_znaku(data_stran)

    # vytvori ocislovany slovnik pro vysledky stran
    slovnik_stran = {cislo_dat_strany[i]: upravena_data_stran[i] for i in range(len(cislo_dat_strany))}

    slovnik_headers_stran = headers_vsechny_strany(rok)
    # porovnava jestli pro nazev strany existuji data, pokud neexistuji, vlozi do seznamu string
    data_stran_result = kontrola_dat_stran_a_seznamu_stran(slovnik_headers_stran,slovnik_stran)
    # secte dva slovniky do jednoho
    data_hodnot = upravena_data_tabulek + data_stran_result

    return data_hodnot

def odstraneni_specialnich_znaku(seznam) -> list:
    '''
    Funkce hledá v seznamu speciální znak \xa0 a nahrazuje ho prázdným stringem.
    :param seznam: list
    :return: list
    '''
    int_seznam = []
    for i in seznam:
        int_seznam.append(i.replace("\xa0", ""))
    return int_seznam

def kontrola_dat_stran_a_seznamu_stran(slovnik_headers, slovnik_stran) -> list:
    '''
    Funkce porovnává podle číselného klíče názvu strany jestli existuje číselný klíč v datech strany.
    Pokud neexistuje, tak vkládá string Nekandiduje. Následně seřazené data podle čísla vloží do seznamu.
    :param slovnik_headers: dict
    :param slovnik_stran: dict
    :return: list
    '''
    strany_data_result = []
    porovnani_headers = slovnik_headers.keys()
    porovnani_data = slovnik_stran.keys()
    for i in porovnani_headers:
        if i not in porovnani_data:
            slovnik_stran[i] = "Nekandiduje"
    # prevede string na int u vsech keys
    slovnik_stran = {int(k): v for k, v in slovnik_stran.items()}
    # seradi hodnoty a vrati vysledny seznam
    for key, value in sorted(slovnik_stran.items()):  # Note the () after items!
        strany_data_result.append(value)

    return strany_data_result

def ulozeni_do_csv(headers,data, pozadavek, okres) -> None:
    '''
    Funkce pomocí vnitřní funkce nastaví název souboru k exportu,
    a poté provede uložení do csv.
    :param headers: list
    :param data: list
    :param pozadavek: str
    :param okres: None nebo pokud se jedná o obce, tak str s názvem okresu
    '''
    nazev_souboru = volba_ulozeni(pozadavek, okres)
    with open(nazev_souboru, "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(headers)
        writer.writerows(data)

def volba_ulozeni(pozadavek, okres) -> str:
    '''
    Funkce podle úvodního požadavku výsledků nastaví název souboru.
    :param pozadavek: str
    :param okres: str
    :return: str
    '''
    if pozadavek == "1":
        name = "vysledky_kraju.csv"
    elif pozadavek == "2":
        name = "vysledky_okresu.csv"
    elif pozadavek == "3":
        name = f"""vysledky_{okres}.csv"""
    return name

def program_okres(data, pozadavek, rok) -> None:
    '''
    Funkce provádí vnitřní funkce pro výsledky okresů z dat
    v knihovně bs4 pro vybraný rok a druh výsledků.
    :param data: bs4.BeautifulSoup
    :param pozadavek: str
    :param rok: str
    '''
    seznam_nazvu_okresu = vyhledavani_nazvu_tabulkou(data,
                                                     nastaveni_kroku= [1, None, 4],
                                                     hledani_sloupcu= ['td', None],
                                                     krok_tabulky=[0])

    seznam_url_okresu = vyhledavani_url_tabulkou(data,
                                                 nastaveni_kroku=[0, None, 4],
                                                 hledani_sloupcu=['td', None])
    seznam_cele_url_okresu = tvorba_cele_url(seznam_url_okresu, rok)
    # vybere nazvy headers pouze z jedne url, protoze jsou vsude stejne
    headers_to_convert = sber_headers(seznam_cele_url_okresu[0], rok)
    data_to_convert = sber_dat_pro_vsechny_stranky(seznam_cele_url_okresu,seznam_nazvu_okresu, rok)
    ulozeni_do_csv(headers_to_convert, data_to_convert, pozadavek, None)

def vyhledavani_url_tabulkou(data,nastaveni_kroku, hledani_sloupcu) -> list:
    '''
    Funkce z dat bs4 rozdělí text v elementu na url krajů.
    :param data: bs4.Beautifulsoup
    :param nastaveni_kroku: například list [0, None, 4] -> pro vybrání konkrétních sloupců
    :param hledani_sloupcu: například list ['td', None] -> pro hledání v html
    :return: list
    '''
    seznam_sloupcu = []
    bunky = []
    for table in data:
        for link in table.find_all(hledani_sloupcu[0],hledani_sloupcu[1]):
            bunka = link.find("a")
            bunky.append(bunka)
    for i in bunky[nastaveni_kroku[0] : nastaveni_kroku[1] : nastaveni_kroku[2]]:
        seznam_sloupcu.append(i.get("href"))
    return seznam_sloupcu

def program_obec(data, pozadavek, rok) -> str:
    '''
    Funkce převádí pomocí vnitřních funkcí pro výsledky obcí z dat
    v knihovně bs4  na výsledky pro vybraný rok a druh výsledků.
    Následně vrací název zvoleného okresu.
    :param data: bs4.BeautifulSoup
    :param pozadavek: str
    :param rok: str
    :return: str
    '''
    # nejdrive hledam okresy a znich potom pokracuji do obci
    seznam_nazvu_okresu = vyhledavani_nazvu_tabulkou(data,
                                                     nastaveni_kroku= [1, None, 4],
                                                     hledani_sloupcu= ['td', None],
                                                     krok_tabulky=[0])

    seznam_url_okresu = vyhledavani_url_tabulkou(data,
                                                 nastaveni_kroku=[3, None, 4],
                                                 hledani_sloupcu=['td', None])
    seznam_cele_url_okresu = tvorba_cele_url(seznam_url_okresu, rok)
    # vytvorim slovniky pro nasledny vyber
    slovnik_nazvu_okresu = tvorba_slovniku_moznosti(seznam_nazvu_okresu)
    slovnik_url_okresu = tvorba_slovniku_moznosti(seznam_cele_url_okresu)
    # vypisu slovnik nazvu okresu
    pprint.pprint(slovnik_nazvu_okresu)

    volba = volba_odkazu_convertovani(slovnik_url_okresu, seznam_nazvu_okresu)
    # rozdeleni seznamu na jednotlivé seznamy
    vybrana_url = volba[0]
    nazev_okresu = volba[1]
    # z požadovaného okresu vyberu všechny obce pro následný export
    precti_data_obce = sber_dat_pozadavku(vybrana_url, nastaveni_hledani=['table', None])
    seznam_nazvu_obce = vyhledavani_nazvu_tabulkou(precti_data_obce,
                                                   nastaveni_kroku=[1, None, 3],
                                                   hledani_sloupcu=["td", None],
                                                   krok_tabulky=[0])

    seznam_url_obce = vyhledavani_url_tabulkou(precti_data_obce,
                                               nastaveni_kroku=[0, None, 1],
                                               hledani_sloupcu=["td", {"class":"cislo"}])

    seznam_cele_url_obce = tvorba_cele_url(seznam_url_obce, rok)
    # vybere nazvy headers pouze z jedne url, protoze jsou vsude stejne
    headers_to_convert = sber_headers(seznam_cele_url_obce[0], rok)
    data_to_convert = sber_dat_pro_vsechny_stranky(seznam_cele_url_obce,seznam_nazvu_obce, rok)
    ulozeni_do_csv(headers_to_convert, data_to_convert, pozadavek, nazev_okresu)
    return nazev_okresu

def tvorba_slovniku_moznosti(seznam) -> dict:
    '''
    Funkce převede seznam na slovník s klíčy od 1 do konce seznamu.
    :param seznam: list
    :return: dict
    '''
    slovnik = dict(zip(range(1, len(seznam) + 1), seznam))
    return slovnik

def volba_odkazu_convertovani(slovnik, seznam_nazvu) -> list:
    '''
    Funkce žádá vstup uživatele pro vybrání okresu ze seznamu okresů
    a ohraničuje výběr na délku seznamu + 1.
    Volba uživatele vrací seznam s url, která se rovná číslu klíče slovníku a
    upraveny nazev okresu bez diakritiky a mezer.
    :param slovnik: dict
    :param seznam_nazvu: list
    :return: list[str]
    '''

    pocet = len(seznam_nazvu)
    print(separator(symbol="-", delka=51))
    volba = input(f"""Zadej číslo výsledků obcí v okrese: """)
    print(separator(symbol="-", delka=51))
    print("NAČÍTÁM DATA")
    print(separator(symbol="-", delka=51))
    if volba.isdigit() and int(volba) in range(1, pocet + 1):
        odkaz = slovnik[int(volba)]
        nazev = seznam_nazvu[int(volba) - 1]
        # funkce odstrani diakritiku a odstrani mezery v nazvu
        nazev_upraveny = unidecode.unidecode(nazev.lower().replace(" ", ""))
        seznam = [odkaz, nazev_upraveny]
        return seznam
    else:
        print(f"""Zvolené číslo okresu neexistuje.\nVYPÍNÁM PROGRAM""")
        quit()

def ukonceni_programu(vyber_pozadavku, nazev_obce) -> None:
    '''
    Funkce pomocí vnitřní funkce vypíše závěrečný komentář programu.
    :param vyber_pozadavku: str
    :param nazev_obce: list
    '''
    nazev = nastaveni_nazvu_ukonceni(vyber_pozadavku, nazev_obce)
    nazev_vysledku = nazev[0]
    nazev_souboru = nazev[1]
    print(f"""Výsledky {nazev_vysledku} byly převedeny do csv
a uloženy pod názvem vysledky_{nazev_souboru}.csv""")
    print(separator(symbol="=", delka=51))
    print("VYPÍNÁM PROGRAM")
    print(separator(symbol="=", delka=51))

def nastaveni_nazvu_ukonceni(vyber_pozadavku, nazev_okresu) -> list:
    '''
    Funkce pro vybrany pozadavek nastavi do seznamu na nultý index název pro print
    a na první index název souboru pro ulozeni.
    Pokud se jedná o výsledky obcí v okrese, tak využije parametr nazev_okresu.
    :param vyber_pozadavku: str
    :param nazev_okresu: str
    :return: list
    '''
    if vyber_pozadavku == "1":
        nazev = ["krajů", "kraje"]
        return nazev
    elif vyber_pozadavku == "2":
        nazev = ["okresů", "okresu"]
        return nazev
    elif vyber_pozadavku == "3":
        nazev = ["obcí v okrese", nazev_okresu]
        return nazev

### SPUSTENI KODU ###
if __name__ == "__main__":
    main()
