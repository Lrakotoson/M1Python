#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""Script permettant de créer et d'interroger une base de données SQL"""
################################################################################
# fichier  : td5_creation.py
# Auteur : RAKOTOSON Loic
################################################################################


# In[2]:


################################################################################
# Importation de fonctions externes :
import sqlite3 as db
import csv

# Definition locale de fonctions :


# In[34]:


def sqlQuery(query):
    """
    Execute une requête SQL
    query: str, requête
    Un objet de classe Connection doit exister
    """
    global cnx
    cursor = cnx.cursor()
    
    try:
        cursor.execute(query)
        cnx.commit()
    except:
        cnx.rollback()
    


# In[3]:


################################################################################
# Corps principal du programme :


# # Exercice 1: Création de la base
# Lire le fichier agenda_culturel.csv à l'aide du module csv de Python et placer les données dans une liste Python `dataCSV`.

# In[6]:


with open("agenda_culturel.csv", "r", encoding="UTF8") as f:
    dataCSV = list(csv.reader(f, delimiter=";"))


# ## Question 1
# #### 1.1 Placer en premier les instructions permettant de supprimer les tables si elles existent (utile pour repartir à zéro lorsqu'on fait plusieurs essais). On veillera à supprimer en premier la table qui possède des clés étrangères.

# In[37]:


tables = ["typeEvenement", "organisme", "commune", "evenement"]
cnx = db.connect("base.sqlite")
cursor = cnx.cursor()
for tb in tables:
    query = "DROP TABLE IF EXISTS " + tb
    cursor.execute(query)
    cnx.commit()


# #### 1.2 Créer ensuite les tables ne possédant pas de clé étrangère.

# In[36]:


typeEvenement = """CREATE TABLE IF NOT EXISTS typeEvenement(
                   TE_id TINYINT(2) PRIMARY KEY,
                   TE_nom VARCHAR(25) NOT NULL,
                   TE_theme TEXT CHECK(TE_theme IN ('Loisir', 'Pratique')) NOT NULL
                   )
                """
organisme = """CREATE TABLE IF NOT EXISTS organisme(
               O_id INTEGER PRIMARY KEY,
               O_nom VARCHAR(25) NOT NULL,
               O_type VARCHAR(25) NOT NULL
               )
            """

commune = """CREATE TABLE IF NOT EXISTS commune(
             C_INSEE INTEGER PRIMARY KEY,
             C_nom VARCHAR(25) NOT NULL,
             C_dep TINYINT(2) NOT NULL,
             C_cp SMALLINT NOT NULL
             )
          """
for query in [typeEvenement, organisme, commune]:
    sqlQuery(query)


# #### 1.3 Créer en dernier la table qui possède des clés étrangères.

# In[ ]:




