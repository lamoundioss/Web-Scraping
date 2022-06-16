from types import MemberDescriptorType
from unicodedata import name
from unittest import result
from bs4 import BeautifulSoup
from numpy import append
import requests
import csv
import modele
import base

##### initialisation de variables

modele_techno = []
memoire_ram = []
memoire_rom = []
price = []
rom = ('RO' , ' RO' , ' Ro')
ram = ('RA', ' RA', ' Ra')

###### les liens utilisés pour la recuperation des donnees et le paramettre headers

url = 'https://www.jumia.sn/telephone-tablette/?tag=CP_9#catalog-listing'
url_techno = 'https://www.jumia.sn/mlp-boutique-officielle-tecno/' 
url_iphone = 'https://www.jumia.sn/iphone/'
url_soumari = 'https://www.soumari.com/categorie-produit/smartphones-haut-de-gamme/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}


##### Fonction de recupération de données sur plusieurs balises

def get_datas_a(url,balise, class_):
    data = requests.get(url, headers = headers)
    soup = BeautifulSoup(data.content, 'html.parser')
    reponse = soup.find_all(balise, class_=class_)
    reponse = [elem.text for elem in reponse]
    return reponse

def get_datas_b(url,balise):
    data = requests.get(url, headers = headers)
    soup = BeautifulSoup(data.content, 'html.parser')
    reponse = soup.find_all(balise)
    reponse = [elem.text for elem in reponse]
    return reponse

##### Fonction de recupération de données sur une seule balise

def get_data(url, balise, class_):
    datas = requests.get(url, headers=headers)
    soup = BeautifulSoup(datas.content, 'html.parser')
    resultat = soup.find(balise, class_)
    return resultat
 
 #***************************************************************************************************************************
 ##### Fonction de nettoyage des données samsung

def data_clean():
    result = get_datas_a(url, 'h3', 'name')
    reponse = [elem.split() for elem in result]
    ram = ['2Go', '3Go', '4Go', '4GB', '6Go', ]
    rom = ['16Go', '32Go', '64Go', '128Go', '128GB']
    modele = [elem[i] for elem in reponse for i in range(len(elem)) if elem[i].startswith('A') or elem[i]=='GalaxyA22-Ecran6.6"-']
    Ram = [elem[i] for elem in reponse for i in range(len(elem)) if elem[i] in ram]
    Rom = [elem[i] for elem in reponse for i in range(len(elem)) if elem[i] in rom]
    prix = get_datas_a(url, 'div', 'prc')

    return Ram, Rom, prix, modele

Tab = data_clean()
# balise = ['div' and 'h3']

###### Fonction d'ecriture des donnees sur un fichier csv

def en_csv(fichier, en_tete, infos, prix):
    with open(fichier, 'w') as file_csv:
        writer = csv.writer(file_csv, delimiter = ',')
        writer.writerow(en_tete)
        for titre, description in zip(infos, prix):
            ligne = [titre, description ]
            writer.writerow(ligne)


#*****************************************************************************************************************************
##### Récuperation et nettoyage des données techno

resultat = get_data(url_techno, 'div', '-paxs')

infos = [line.find('h3', class_='name').text.replace('–', '-').replace('+', '-').split('-') for line in resultat]
prix = [line.find('div', class_='prc') for line in resultat]

for i in range(len(infos)):
    if infos[i][0].startswith('T') and i!=3:
        modele_techno.append(infos[i][0])
        for elem in infos[i]:
            if elem.startswith(ram) or elem.endswith('AM '):
                memoire_ram.append(elem.strip(' '))
            elif elem.startswith(rom) or elem.endswith('OM '):
                memoire_rom.append(elem.strip(' '))
        price.append(prix[i].text)

print(price)


modele_techno = [infos[i][0] for i in range(len(infos)) if infos[i][0].startswith('T') and i!=3]
memoire_rom = [elem for i in range(len(infos)) for elem in infos[i] if i!=3 and (elem.startswith(rom) or elem.endswith('OM ')) and infos[i][0].startswith('T')]
memoire_ram = [elem for i in range(len(infos)) for elem in infos[i] if i!=3 and (elem.startswith(ram) or elem.endswith('AM ')) and infos[i][0].startswith('T') ]

#*********************************************************************************************************************************************************************
###### Récuperation et nettoyage des donnees iphone

car = (" 3/", " 4/")
ter = ("Ram ", "Rom ", "Go ")

infos_iphone = [elem for elem in get_datas_a(url_iphone, 'h3', 'name')]
price_iphone = get_datas_a(url_iphone, 'div', 'prc')
donnees_pro = [el for elem in infos_iphone for el in elem if el.startswith(car)]
en_tete = ['infos', 'price']
# en_csv('fichier_iphone.csv', en_tete, infos_iphone, price_iphone)
# print(infos_iphone)

####### Recuperation et ecriture des donnes soumari sur fichier csv

infos_tel_soumari = get_datas_a(url_soumari, 'h2', 'woo-loop-product__title')
price_tel_soumari = [get_datas_b(url_soumari, 'bdi')[i] for i in range(0, len(get_datas_b(url_soumari, 'bdi')),2)]
donnees = [infos_tel_soumari[i].split('–') for i in range(0,len(infos_tel_soumari), 2)]
# print((price_tel_soumari))
mod_soum = []
ram_soum = []
rom_soum = []
price_soum = []
sam = ('Samsung', 'Galaxy')
def recup_data(marq):
    for i in range(len(donnees)):
        for elem in donnees[i]:
            if elem.startswith(marq):
                mod_soum.append(donnees[i][0])
                rom_soum.append(donnees[i][1])
                ram_soum.append(donnees[i][2])
                price_soum.append(price_tel_soumari[i+1])
    return mod_soum, rom_soum, ram_soum, price_soum

# tab_iph_soum = recup_data('Iphone')
# tab_sam_soum = recup_data(sam)
tab_tec_soum = recup_data('Tecno')

# print((tab_iph_soum))

# tab_infos = []
# tab_price = []
# for i in range(1, 11):
#     infos_tel_soumari = get_datas_a(url+str(i)+'/', 'h2', 'woo-loop-product__title')
#     price_tel_soumari = get_datas_b(url+str(i)+'/', 'bdi')
#     for i in range(len(infos_tel_soumari)):
#         tab_infos.append(infos_tel_soumari[i].text)
#         tab_price.append(price_tel_soumari[i].text)

# print(tab_infos)
# en_csv('fichier_soumari.csv', en_tete, tab_infos, tab_price)


#****************************INSETION A LA BASE DE DONNEE*************************************
name = ['JUMIA', 'SOUMARI', 'NOVA']
# for i in range(1,4):
#     vend = modele.Vendeur(i, name[i-1])
#     base.session.add(vend)
#     base.session.commit()
#     base.session.close()


def insert_tel(marque, model, prix, id_vend):
    j=0
    for i in  range(82, 82+len(model)):
        data = modele.Telephones(i,marque, model[j], prix[j], id_vend, str(i))
        # print(data)
        base.session.add(data)
        base.session.commit()
        base.session.close()
        j+=1

# insert_tel('Iphone', tab_iph_soum[0], tab_iph_soum[3], '2')
# insert_tel('Samsung', tab_sam_soum[0], tab_sam_soum[3], '2')
# insert_tel('Techno', tab_tec_soum[0], tab_tec_soum[3], '2')

def insert_car(memoire, ram):
    j=0
    for i in  range(82, 82+len(ram)):
        data = modele.Caracteristique(i, memoire[j], ram[j])
        # print(data)
        base.session.add(data)
        base.session.commit()
        base.session.close()
        j+=1

# print(tab_sam_soum)
# insert_car(tab_iph_soum[1], tab_iph_soum[2])
# insert_car(tab_sam_soum[1], tab_sam_soum[2])
# insert_car(tab_tec_soum[1], tab_tec_soum[2])

# insert_tel('Samsung', Tab[3], Tab[2], '1')
# insert_car(Tab[1], Tab[0])

# insert_tel('Techno', modele_techno, price, '1')
# insert_car(memoire_rom, memoire_ram)