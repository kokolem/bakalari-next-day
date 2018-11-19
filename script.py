import requests
import xml.etree.ElementTree as et
import hashlib
import base64
import time
import datetime

class Bakalari: # Trida pro pristup k API bakalaru
    
    
    def __init__(self, login, password, adresa): # Argumenty jsou string s prihlasovacim jmenem, string s heslem a string s url adresou bakalaru skoly. Ze zadanych udaju se vypocita token a ulozi jako self.token
        
        # Adresa je potreba i v ostatnich metodach, heslo a prihlasovaci jmeno ne (staci token). 
        self.adresa = adresa
        
        # Ziskani zakladnich komponent pro token
        loginInitR = requests.get(adresa, params = {"gethx": login})
        loginInitX = et.fromstring(loginInitR.text)
        typ = loginInitX.find("typ").text
        ikod = loginInitX.find("ikod").text
        salt = loginInitX.find("salt").text
        
        # Vypocet hesla
        passwordHashOriginal = salt+ikod+typ+password
        passwordHashOriginal = passwordHashOriginal.encode("UTF-8")
        
        # Zahashovani hesla
        passwordHash = hashlib.sha512()
        passwordHash.update(passwordHashOriginal)
        passwordHash = base64.encodebytes(passwordHash.digest()).decode("UTF-8").replace("\n","")
        
        # Vypocet tokenu
        tokenOriginal = "*login*" + login + "*pwd*" + passwordHash + "*sgn*ANDR" + time.strftime('%Y%m%d')
        
        # Zahashovani tokenu
        token = hashlib.sha512()
        token.update(tokenOriginal.encode("UTF-8"))
        self.token = base64.encodebytes(token.digest()).decode("UTF-8").replace("\n","").replace("/","_").replace("\\","_").replace("+","-")
    
    
    def rozvrh(self): # Vraci xml.etree.ElementTree.Element s rozvrhem a vytvori promenou scheduleXml se stejnym obsahem

        # Ziskani rozvrhu
        scheduleStr = requests.get(self.adresa, params = {"hx": self.token, "pm": "rozvrh"})
        self.scheduleXml = et.fromstring(scheduleStr.text)
        return (self.scheduleXml)

class SkolniTyden(): # Trida pro zpracovavani XML z bakalaru


    def __init__(self, scheduleXML): # Argument je XML s rozvrhem z Bakalaru
        
        self.rozvrh = [] 
        cisloDnu = 0      
        
        # Pro kazdy den v rozvrhu se do self.rozvrh prida prazdne pole
        dny = scheduleXML.find("rozvrh").find("dny").findall("den")
        for den in dny:
            hodiny = den.find("hodiny").findall("hod")
            self.rozvrh.append([])
            
            # Pro kazde pole (reprezentuje den ve skolnim rozvrhu) v self.rozvrh se do nej pridaji nazvy hodin, ktere v ten den jsou
            for hodina in hodiny:
                if hodina.find("pr") != None:
                    self.rozvrh[cisloDnu].append(hodina.find("pr").text)
                
            cisloDnu += 1
    
    
    def vzitNa(self, den): # Int den 0 pro pondeli, 1 pro utery, ..., 4 pro patek. Vraci list se dvema listy, prvni obsahuje predmety co do tazky pridat, druhy co z ni vyndat
        
        # Pokud je pondeli, predchozi den je patek
        if den == 0:
            vcera = self.rozvrh[4]
        else:
            vcera = self.rozvrh[den-1]
        
        dnes = self.rozvrh[den]
        pridat = []
        odebrat = []
        
        # Pokud je hodina dnes a nebyla vcera, prida se do promene pridat, pokud byla vcera a neni dnes, prida se do promene odebrat
        for hodina in dnes:
            if hodina not in vcera:
                pridat.append(hodina)
                
        for hodina in vcera:
            if hodina not in dnes:
                odebrat.append(hodina)
        
        # Filtrovani opakujicich se predmetu
        pridat = set(pridat)
        pridat = list(pridat)
        
        odebrat = set(odebrat)
        odebrat = list(odebrat)
        
        return([pridat, odebrat])
    
# Ziskani udaju
jmeno = input("Prihlasovaci jmeno: ")
heslo = input("Heslo: ")
adresa = input("URL adresa bakalaru skoly: ")
    
# Inicializace trid    
uzivatel = Bakalari(jmeno, heslo, adresa)
tyden = SkolniTyden(uzivatel.rozvrh())

# Pokud neni zitra vikend, zobrazi se co si na zitrek vzit a co vyndat
zitra = datetime.datetime.today().weekday()+1
if zitra != 6 and zitra != 7:
    naZitra = tyden.vzitNa(zitra)

    # Odpoved
    print("")
    print ("Do tasky si pridej: \n")
    for predmet in naZitra[0]:
        print(predmet)
        # Za poslednim udelat prazdnou radku
        if naZitra[0][len(naZitra[0])-1] == predmet:
            print("")

    print ("A vyndej: \n")
    for predmet in naZitra[1]:
        print (predmet)
else:
    print ("Zitra je vikend :)")

