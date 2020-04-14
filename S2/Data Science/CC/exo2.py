
# coding: utf-8

# In[1]:


"""Données JSON et programmation objet"""
################################################################################
# fichier  : exo2.py
# Auteur : RAKOTOSON Loic
################################################################################


# In[2]:


################################################################################
# Importation de fonctions externes :
import json
import pandas as pd
from requests import get, HTTPError
# Definition locale de fonctions :


# In[3]:


def getJsonData(base, dico):
    with get(base, params = dico) as response:
        return response.json()


# In[4]:


################################################################################
# Definition des classes :


# In[5]:


class Residence():
    
    def __init__(self, dico):
        self.nom = dico['nom']
        self.desc = dico['description']
        self.lat = dico['latitude']
        self.lon = dico['longitude']
        self.zone = dico['zone']
    
    def __repr__(self):
        chaine = "Résidence {} ({}): {}".format(
            self.nom.upper(),
            self.zone,
            self.desc
        )
        return chaine
    
    def distanceDe(self, longitude, latitude, profil):

        base_url = "https://api.openrouteservice.org/matrix"
        source = ",".join([self.lon, self.lat])
        dest = ",".join([longitude, latitude])
        params = {
            "api_key" : APIKEY,
            "profile": profil,
            "locations": "|".join([source, dest]),
            "sources": "0",
            "destinations": "1",
            "metrics": "distance",
            "units": "m",
        }

        data = getJsonData(base_url, params)
        return data['distances'][0][0]
    
    def dureeDe(self, longitude, latitude, profil):

        base_url = "https://api.openrouteservice.org/matrix"
        source = ",".join([self.lon, self.lat])
        dest = ",".join([longitude, latitude])
        params = {
            "api_key" : APIKEY,
            "profile": profil,
            "locations": "|".join([source, dest]),
            "sources": "0",
            "destinations": "1",
            "metrics": "duration"
        }

        data = getJsonData(base_url, params)
        return data['durations'][0][0]


# In[6]:


APIKEY = '5b3ce3597851110001cf62486cfda2a850de46e4a43253fa6adffd31'


# # Exercice 2: Données JSON et programmation objet
# Question 1

# In[7]:


with open("residences.json", "r", encoding="UTF-8") as json_file:
    jsonData = json.load(json_file)


# Question 2

# In[8]:


r1 = Residence(jsonData[0])


# Question 3

# In[9]:


print(r1)


# Question 4.1

# In[10]:


UnivR2 = ("-1.702147", "48.118737")
profil = "driving-car"
r1.distanceDe(*UnivR2, profil)


# Question 4.2

# In[11]:


r1.dureeDe(*UnivR2, profil)


# Question 5

# In[12]:


list_residence = [Residence(res) for res in jsonData]
profil = "foot-walking"


# In[13]:


for residence in list_residence:
    if "Rennes" in residence.zone:
        duree = residence.dureeDe(*UnivR2, profil)/60
        if  duree <= 20:
            print(
                "A {} minutes: {}".format(
                    int(duree),
                    str(residence)
                )
            )


# Question 6

# In[14]:


profil = "driving-car"

for residence in list_residence:
    if "Rennes" not in residence.zone:
        distance = residence.distanceDe(*UnivR2, profil)/1000
        print(
            "A {} km: {}".format(
                round(distance, 2),
                str(residence)
            )
        )

