#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importation de fonctions externes:
import pickle
import csv
from datetime import datetime


# In[2]:


# Récupération des données
def readData(nom_fichier):
    listeData = []
    try:
        with open(nom_fichier, 'rb') as objet_fichier:
            objet_fichier_depickler = pickle.Unpickler(objet_fichier)
            while 1:
                try:
                    listeData.append(objet_fichier_depickler.load())
                except EOFError:
                    break
    except (IOError, OSError):
        print("Problème à l'ouverture du fichier")
    return listeData

listeData = readData('data.pic')
# La variable listeData représente l'ensemble des réponses
aide_ex_11 = listeData[0]
aide_ex_12 = listeData[1]
aide_ex_13 = listeData[2]
aide_ex_14 = listeData[3]
aide_ex_31 = listeData[4]
aide_ex_32 = listeData[5]
aide_ex_33 = listeData[6]
aide_ex_34 = listeData[7]
aide_ex_35 = listeData[8]
aide_ex_41 = listeData[9]
aide_ex_42 = listeData[10]
aide_ex_43 = listeData[11]
aide_ex_51 = listeData[12]


# # Exo 1: Lecture des fichiers csv
# Une fonction pour lire les fichiers

# In[3]:


def lire_csv(fichier, delim):
    with open(fichier, 'r', encoding="utf-8") as file:
        data = [ligne for ligne in csv.reader(file, delimiter=delim)]
    return data


# In[4]:


data = lire_csv("eco-counter-data.csv",";")


# In[5]:


date = data[0].index('date')
counts = data[0].index('counts')
geo = data[0].index('geo')

data = [[ligne[date], ligne[counts], ligne[geo]] for ligne in data]


# In[6]:


sites = lire_csv("eco-counter-sites.csv",";")


# In[7]:


name = sites[0].index('name')
interval = sites[0].index('interval')
geo = sites[0].index('geo')

sites = [[ligne[name], ligne[interval], ligne[geo]] for ligne in sites]


# In[11]:


def afficher_comptage(data, ligne):
    date_format_have = "%Y-%m-%dT%H:%M:%S"
    date_format_want = "%b %d %Y %H:%M:%S"
    date = datetime.strftime(
        datetime.strptime(data[ligne][0], date_format_have), date_format_want)
    nombre = data[ligne][1]
    coordonnees = data[ligne][2]

    print("Le {}, il y a eu {} vélos et piétons sur le point de comptage ({})".
          format(date, nombre, coordonnees))


# In[12]:


afficher_comptage(data, 100)


# In[19]:


def ConversionEntier(data, col):
    for ligne in data[1:]:
        if isinstance(ligne[col],str) and ligne[col].isdigit():
            ligne[col] = int(ligne[col])
    return data


# In[20]:


data = ConversionEntier(data, 1)
sites = ConversionEntier(sites, 1)


# In[26]:


def ConversionCoord(data):
    donnees = [[ligne[0], ligne[1], tuple(ligne[2].split(","))] for ligne in data[1:]]
    donnees.insert(0, data[0]) #entête
    return donnees


# In[27]:


data = ConversionCoord(data)
sites = ConversionCoord(sites)


# In[28]:


def ConversionDate(data):
    date_format_have = "%Y-%m-%dT%H:%M:%S"
    for ligne in data[1:]:
        try:
            date = datetime.strptime(ligne[0], date_format_have)
        except:
            date = None
        finally:
            ligne[0] = date
    return data


# In[ ]:





# # Exo 4

# In[31]:


dsites = {}
for ligne in sites[1:]:
    dsites[ligne[2]] ={'interval':ligne[1], 'name':ligne[0]}


# In[36]:


ddata = {}
for ligne in data[1:]:
    ddata[ligne[2]] = ligne[:-2]


# In[43]:


ddata = {cle: val for cle, val in sorted(ddata.items(), key=lambda x: x[1][0])}

