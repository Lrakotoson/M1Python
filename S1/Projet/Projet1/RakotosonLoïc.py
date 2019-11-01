#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""Mini projet sur les grandes marées à Saint-Malo"""
################################################################################
# fichier  : RakotosonLoïc.py
# Auteur : Rakotoson Loïc
################################################################################

################################################################################
#Importation de fonctions externes :

from datetime import datetime
import pickle


# In[2]:


################################################################################
#Definition locale de fonctions :

################################################################################
#Lecture avec pickle (Récupération des variables réponses)

def readData(nomFichier):
    listeData=[]
    try:
        with open(nomFichier,'rb') as objet_fichier:
            objet_fichier_depickler = pickle.Unpickler(objet_fichier)
            while 1 :
                try :
                    listeData.append(objet_fichier_depickler.load())
                except EOFError:
                    break
    except (IOError, OSError) :
        print("Problème à l'ouverture du fichier")
    return listeData


# In[3]:


################################################################################
#Definition de classe

################################################################################
#Récupération des données

listeData=readData('data.pic')
#La variable jour représente le jour de la semaine de la grande marée
jour = listeData[0]
#La variable date représente la date de la grande marée
date = listeData[1]

################################################################################
#Corps principal du programme :


# # Les données
# ## Exercice 1
# Conversion des dates en datetime et triage par ordre décroissant

# In[4]:


dateformat = sorted([datetime.strptime(i, '%Y-%m-%d') for i in date], reverse=True)


# ## Exercice 2
# Affichage de la prochaine grande marrée. On affichera celui le plus récent.

# In[5]:


print(dateformat[0].strftime('%d %B %Y'))


# # Exploitation des données
# ## Exercice 3
# Le nombre de grande marée pour chaque année.

# In[6]:


annee = [i.year for i in dateformat]

for year in sorted(set(annee)):
    print("{} : {}".format(year, annee.count(year)))


# ## Exercice 4
# Fréquence moyenne des grandes marées par mois toutes années confondues

# In[7]:


mois = [(i.strftime('%B'), i.month) for i in dateformat]

for month in sorted(set(mois), key=lambda x: x[1]):
    print("{} : {}".format(month[0], round(mois.count(month)/len(set(annee)), 2)))

