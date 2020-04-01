
# coding: utf-8

# In[1]:


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


# In[3]:


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
    


# In[4]:


def typage(data):
    """
    Adapte et crée les données pour être sql-friendly
    :data: liste de liste
    :return: liste de liste
    """
    for i, ligne in enumerate(data):
        data[i].append(" ".join(
            [data[i][k] for k in [14, 15, 16, 55, 56, 57] if data[i][k]]))
        for j, col in enumerate(ligne):
            if col == "":
                data[i][j] = "NULL"
            elif col.strip().isdigit():
                data[i][j] = int(data[i][j])
            else:
                data[i][j] = "'{}'".format(data[i][j].replace("'", " "))
    return data


# In[5]:


def insertInto(table, listValues):
    """
    Insère une liste de valeurs dans une table existante
    :table: str, nom de la table
    :listValues: liste de liste de valeurs
    :return: None
    """
    for values in listValues:
        query = """INSERT INTO """ + table + """ VALUES(
                """ + ("{}," * len(values))[:-1] + """
                )"""
        
        sqlQuery(query.format(*values))


# In[6]:


################################################################################
# Corps principal du programme :


# # Exercice 1: Création de la base
# Lire le fichier agenda_culturel.csv à l'aide du module csv de Python et placer les données dans une liste Python `dataCSV`.
# 
# La fonction `typage( )` a été créée pour formater les données afin qu'elles soient sql-friendly et adaptées à notre structure.

# In[7]:


with open("agenda_culturel.csv", "r", encoding="UTF8") as f:
    dataCSV = list(csv.reader(f, delimiter=";"))


# In[8]:


dataCSV = typage(dataCSV)


# ## Question 1
# #### 1.1 Placer en premier les instructions permettant de supprimer les tables si elles existent (utile pour repartir à zéro lorsqu'on fait plusieurs essais). On veillera à supprimer en premier la table qui possède des clés étrangères.

# In[10]:


tables = ["typeEvenement", "organisme", "commune", "evenement"]
cnx = db.connect("base.sqlite")
cursor = cnx.cursor()
for tb in tables:
    query = "DROP TABLE IF EXISTS " + tb
    cursor.execute(query)
    cnx.commit()


# #### 1.2 Créer ensuite les tables ne possédant pas de clé étrangère.
# La fonction `sqlQuery( )` a été créée pour exécuter et commit les requêtes en gérant les exceptions.

# In[11]:


typeEvenement = """CREATE TABLE IF NOT EXISTS typeEvenement(
                   TE_id TINYINT(2) PRIMARY KEY,
                   TE_nom VARCHAR(30) NOT NULL,
                   TE_theme TEXT CHECK(TE_theme IN ('Loisir', 'Pratique')) NOT NULL
                   )
                """
organisme = """CREATE TABLE IF NOT EXISTS organisme(
               O_id INTEGER PRIMARY KEY,
               O_nom VARCHAR(30) NOT NULL,
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

# In[12]:


evenement = """CREATE TABLE IF NOT EXISTS evenement(
               E_id INTEGER PRIMARY KEY,
               E_titre VARCHAR(50) NOT NULL,
               E_typeID TINYINT(2),
               E_dateDebut DATE,
               E_dateFin DATE,
               E_organismeID INTEGER,
               E_communeID INTEGER,
               E_gps VARCHAR(25) NOT NULL,
               E_tarifGene FLOAT,
               E_tarifReduit FLOAT,
               E_gratuit BOOL NOT NULL,
               E_complet BOOL,
               E_ageMin TINYINT(2),
               E_ageMax TINYINT(3),
               E_accessibilite CHAR,
               E_description LONGTEXT,
               FOREIGN KEY (E_typeID) REFERENCES typeEvenement(TE_id),
               FOREIGN KEY (E_organismeID) REFERENCES organisme(O_id),
               FOREIGN KEY (E_communeID) REFERENCES commune(C_INSEE)
               )
            """

sqlQuery(evenement)


# ## Question 2
# Remplir les tables créées grâce aux données contenues dans le fichier CSV.
# #### 1. Remplir d'abord les tables ne possédant pas de clé étrangères
# La fonction `insertInto( )` a été créée pour effectuer l'insertion des données en fonction de la structure de la table.

# In[13]:


typeEvent = list({tuple(data[i] for i in [2, 1, 8]) for data in dataCSV[1:]})
insertInto("typeEvenement", typeEvent)


# In[14]:


orga = list({tuple(data[i] for i in [6, 4, 5]) for data in dataCSV[1:]})
insertInto("organisme", orga)


# In[15]:


comm = list({tuple(data[i] for i in [19, 17, 18, 20]) for data in dataCSV[1:]})
insertInto("commune", comm)


# #### 2. Remplir ensuite la table possédant des clés étrangères

# In[16]:


event = list({
    tuple(
        data[i]
        for i in [0, 13, 2, 28, 29, 6, 19, 21, 32, 33, 30, 47, 44, 45, 48, 70])
    for data in dataCSV[1:]
})


# In[17]:


insertInto("evenement", event)


# <hr>
# Fermeture de la connexion.

# In[18]:


cnx.close()

