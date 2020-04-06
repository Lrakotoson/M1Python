# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 12:25:36 2017

@author: ben_m
"""



################################################################################
# fichier  : td5_requetes.py
# Auteur : NOM Prenom
# ###############################################################################

################################################################################
# Importation de fonctions externes :
import sqlite3 as db
from urllib import request, parse
import json

# fonctions

def afficheXML(liste):
    for elem in liste:
        if isinstance(elem, etree._Element):
            print(etree.tostring(elem,encoding='unicode'))
        else:
            print(elem)

def afficheTexte(liste):
    for elem in liste:
        if isinstance(elem, etree._Element):
            if elem.text:
                print(elem.text)
            afficheTexte(elem.xpath('./*'))
        else:
            print(elem)

def getJsonData(base_url, url_param):
    url_values = parse.urlencode(url_param)
    full_url = base_url + "?" + url_values
    # print(full_url)
    jsonData = {}
    try:
        response = request.urlopen(full_url)  # requête
    except (HTTPError, URLError) as e:
        sys.exit(e) # sortie du programme avec affichage de l’erreur
            
    jsonData = json.loads(response.read()) # récupération des données JSON

    return jsonData

################################################################################
# Corps principal du programme :

