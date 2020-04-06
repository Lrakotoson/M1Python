
# coding: utf-8

# In[1]:


"""Script permettant d'interroger une base de données SQL"""
################################################################################
# fichier  : td5_interrogation.py
# Auteur : RAKOTOSON Loic
################################################################################


# In[2]:


################################################################################
# Importation de fonctions externes :
import json
import pandas as pd
import sqlite3 as db
from requests import get

# Definition locale de fonctions :


# In[3]:


def getQuery(query, database = "base.sqlite"):
    """
    Intérroge et renvoie la réponse en DataFrame
    :query: str, requête SQL
    :database: str, base de données
    :return: DataFrame
    """
    cnx = db.connect(database)
    table = pd.read_sql_query(query, cnx)
    cnx.close()
    return table


# In[4]:


def getMatrix(base, dico, metric):
    """
    Retourne la matrice de la métrique
    :base: base url
    :dico: API params
    :metric: distances|durations
    :return: DataFrame
    """
    
    def getJsonData(base, dico):
        with get(base, params = dico) as response:
            return response.json()
    
    reponse = getJsonData(base, dico)
    df = pd.DataFrame(
        reponse[metric],
        columns=[
            ",".join(map(str, d['location'])) for d in reponse['destinations']
        ],
        index=[",".join(map(str, d['location'])) for d in reponse['sources']]).T
    return df


# In[5]:


################################################################################
# Corps principal du programme :


# # Exercice 2: utilisation des données de la base
# La fonction `getQuery( )` a été créée pour obtenir les réponses des requêtes SQL en tant que DataFrame.
# 
# En utilisant les données de la base et éventuellement d'autres ressources, trouver:
# 
# #### Question 1
# Les titres, dates de début et de fin des événements de type «Exposition, musée» qui se sont déroulés (totalement ou partiellement) en février 2019.

# In[6]:
print("\n########## Q1 ##########\n")

query = """SELECT e_titre, e_datedebut, e_datefin
           FROM evenement
           WHERE "02" IN (strftime('%m', e_datedebut), strftime('%m', e_datefin))
           AND e_typeid = (SELECT te_id FROM typeEvenement WHERE te_nom = "Exposition, musée")
        """

print(getQuery(query))


# #### Question 2 :
# Les titres, dates de début et de fin, et la commune des événements affichés complets

# In[7]:
print("\n########## Q2 ##########\n")

query = """SELECT e_titre, e_datedebut, e_datefin, c_nom
           FROM evenement JOIN commune ON e_communeid = c_insee
           WHERE e_complet = 'True'
        """

print(getQuery(query))


# #### Question 3 :
# Les titres, dates de début et de fin, et la description des événements proposés par des organismes de type «Etablissement scolaire, universitaire» en Ille-et-Vilaine, avec le nom de l'organisme

# In[8]:
print("\n########## Q3 ##########\n")

query = """SELECT e_titre, e_datedebut, e_datefin, o_nom, e_description
           FROM evenement JOIN commune ON e_communeid = c_insee
                          JOIN organisme on e_organismeid = o_id
           WHERE o_type = 'Etablissement scolaire, universitaire'
           AND c_dep = 35
        """

print(getQuery(query))


# #### Question 4 :
# Les titres, date de début, date de fin et département des événements non accessibles aux moins de 12 ans qui se déroulent en dehors de la Bretagne (c'est à dire hors des départements bretons: 22, 29, 35, 56)

# In[9]:
print("\n########## Q4 ##########\n")

query = """SELECT e_titre, e_datedebut, e_datefin, c_dep
           FROM evenement JOIN commune ON e_communeid = c_insee
           WHERE e_agemin >= 12
           AND c_dep NOT IN (22, 29, 35, 56)
        """

print(getQuery(query))


# #### Question 5 :
# Les titres, date de début, date de fin et type (nom du type) des événements accessibles aux personnes ayant un handicap «Moteur», proposés en Ille-et-Vilaine par des associations, avec le nom de l’association.

# In[10]:
print("\n########## Q5 ##########\n")

query = """SELECT e_titre, e_datedebut, e_datefin, te_nom, o_nom
           FROM evenement JOIN commune ON e_communeid = c_insee
                          JOIN typeEvenement ON e_typeid = te_id
                          JOIN organisme ON e_organismeid = o_id
           WHERE e_accessibilite LIKE '%Moteur%'
           AND c_dep = 35
           AND o_type = 'Association'
        """

print(getQuery(query))


# #### Question 6 :
# Les titres, dates de début et de fin, et les coordonnées GPS de tous les événements gratuits à Rennes dans le thème «Loisir» qui ont lieu après le 1er mars 2019 et qui se déroulent à moins de 45 minutes à pied du campus de Villejean, «Place du Recteur Henri Le Moal, 35000 Rennes».

# In[11]:
print("\n########## Q6 ##########\n")

query = """SELECT e_titre, e_datedebut, e_datefin, e_gps
           FROM evenement JOIN commune ON e_communeid = c_insee
                          JOIN typeEvenement ON e_typeid = te_id
           WHERE e_gratuit = 'oui'
           AND c_cp = 35000
           AND te_theme = 'Loisir'
           AND e_datedebut > DATE('2019-03-01')
        """

df = getQuery(query)


# In[12]:


r2 = ['-1.701901,48.11981']
e_gps = [','.join(gps.split(', ')[::-1]) for gps in list(df.E_gps)]

base_url = "https://api.openrouteservice.org/matrix"
APIKEY = '5b3ce3597851110001cf62486cfda2a850de46e4a43253fa6adffd31'

params = {
    "api_key": APIKEY,
    "profile": "foot-walking",
    "locations": "|".join(r2 + e_gps),
    "sources": "0",
    "destinations": ",".join(map(str, range(1, len(r2 + e_gps)))),
    "metrics": "duration",
}


# In[13]:


duration = getMatrix(base_url, params, "durations").reset_index(drop = True) / 60
duration.columns = ['duration']
df = pd.concat([df, duration], join = "inner", axis = 1)

print(df[df['duration'] < 45])


# #### Question 7 :
# Les titres, dates de début et de fin et la commune des événements de type «Concert»  gratuits ou dont le tarif réduit est inférieur ou égal à 10 euros et situés à moins de 1h de voiture de votre domicile à Rennes (ou du campus de Villejean).

# In[14]:
print("\n########## Q7 ##########\n")

query = """SELECT e_titre, e_datedebut, e_datefin, c_nom, e_gps
           FROM evenement JOIN commune ON e_communeid = c_insee
                          JOIN typeEvenement ON e_typeid = te_id
           WHERE (e_gratuit = 'oui' OR e_tarifreduit <= 10)
           AND te_nom = 'Concert'
        """

df = getQuery(query)


# In[15]:


e_gps = [','.join(gps.split(', ')[::-1]) for gps in list(df.E_gps)]
df = df.drop(['E_gps'], axis=1)

params = {
    "api_key": APIKEY,
    "profile": "driving-car",
    "locations": "|".join(r2 + e_gps),
    "sources": "0",
    "destinations": ",".join(map(str, range(1, len(r2 + e_gps)))),
    "metrics": "duration",
}


# In[16]:


duration = getMatrix(base_url, params, "durations").reset_index(drop = True) / 3600
duration.columns = ['duration']
df = pd.concat([df, duration], join = "inner", axis = 1)

print(df[df['duration'] < 1])

