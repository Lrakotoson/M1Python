#!/usr/bin/python3
# -*- coding:utf8 -*-
"""Script permettant d'explorer les données d'un fichier XML et d'interroger une API"""
################################################################################
# fichier  : td4.py
# Auteur : NOM Prenom
################################################################################

################################################################################
# Importation de fonctions externes :
from lxml import etree
import sys
from urllib.error import HTTPError, URLError
from urllib import request, parse
import json

# Definition locale de fonctions :

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



################################################################################
# Corps principal du programme :
# Configuration du proxy
login = input('login:')
passwd = input('password:')
proxy = urllib.request.ProxyHandler({'https': 'https://'+login+':'+passwd+'@192.168.192.17:8080'})
auth = urllib.request.HTTPBasicAuthHandler()
opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

# Quelques initialisations
base_url = "https://api.openrouteservice.org/matrix"

url_param = {} # dictionnaire des paramètres de la requête HTTP

apiKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # mettre ici votre clé d'API (entre guillemets)
