# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 12:17:02 2017

@author: dsiadmin
"""

import sys      
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import pickle

# fonctions

    

# prog principal
login = input('login:')
passwd = input('password:')
try:   # gestion des exceptions avec un bloc try/except
	# configuration du proxy
    proxy = urllib.request.ProxyHandler({'https': 'https://'+login+':'+passwd+'@192.168.192.17:8080'})
    auth = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)

except (HTTPError, URLError) as e:
    sys.exit(e)   # sortie du programme avec affichage de l’erreur
