#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""Script permettant d'effectuer du web scraping"""
################################################################################
# fichier  : td3.py
# Auteur : RAKOTOSON Loic
################################################################################


# In[2]:


################################################################################
# Importation de fonctions externes :
import pandas as pd
import pickle
import re
from math import *
from bs4 import BeautifulSoup, Tag, NavigableString, Comment
from requests import get, HTTPError
# Definition locale de fonctions :


# In[3]:


def getTokens(doc):
    regex = r"""\w+"""
    tokens = [word.strip().lower() for word in re.findall(regex, doc)]
    return tokens


# In[4]:


################################################################################
# Definition des classes :


# In[5]:


class DTM:

    with open('mots_vides.txt', 'r', encoding="UTF-8") as texte:
        stopwords = [
            line.split('|')[0].strip() for line in texte.readlines()
            if line.split('|')[0].strip() != ''
        ]

    def __init__(self, dico):
        self.url = dico['url']
        self.title = dico['titre']
        self.data = self.__cleaner(dico['data'])
        self.tfidf = self.__tfidfTransform()

    def __repr__(self):
        return self.data.__repr__()

    def __cleaner(self, data):
        """
        Supprime les colonnes stopwords
        :data: DataFrame
        :return: DataFrame
        """
        stopwords = [
            word for word in __class__.stopwords if word in list(data.columns)
        ]
        return data.drop(stopwords, axis=1)

    def __tfidfTransform(self):
        """
        Calcule la matrice tfidf
        :return: DataFrame
        """
        N = self.data.shape[0]
        tf = self.data / self.data.values.max()
        idf = (N / pd.concat([
            self.data.applymap(lambda x: 1 if x != 0 else 0).sum(
                axis=0).to_frame().T
        ] * N,
                             ignore_index=True)).applymap(lambda x: log(x))

        return tf * idf

    def nBest(self, N):
        return self.data.sum(axis=0).sort_values(ascending=False)[:N]

    def nBestDoc(self, N, index):
        return self.data.iloc[index].sort_values(ascending=False)[:N]

    def query(self, string):
        columns = string.split()
        data = self.data[columns]
        return list(data.loc[(data != 0).all(1)].index)

    def queryScore(self):
        return pd.concat(
            [pd.DataFrame({'url': self.url}),
             self.tfidf.sum(axis=1)], axis=1).rename(columns={
                 0: 'score'
             }).sort_values(by=['score'], ascending=False)


# In[6]:


################################################################################
# Corps principal du programme :


# # Exercice 1: récolte d'information sur le web
# Pour simplifier la tâche, nous n’explorerons que les pages de la catégorie elle-même, en laissant de côté les sous-catégories.  
# 1. A l’aide du module BeautifulSoup, écrire le code Python permettant de récupérer une liste de toutes les URLs des pages de la catégorie «Énergie renouvelable»

# In[7]:


url = "https://fr.wikipedia.org/wiki/Catégorie:Énergie_renouvelable"
with get(url) as response:
    page = BeautifulSoup(response.text, 'html.parser')
    listlink = [
        link['href'] for sub in [
            element.find_all('a')
            for element in page.select("#mw-pages .mw-category-group")
        ] for link in sub
    ]


# 2. A partir de cette liste d’URL, écrire le code Python permettant de récupérer le titre de chaque page, et l’ensemble du texte de la division d’attribut `id="mw-content-text"`, à l’exception du texte contenus dans les éléments de classe `'toc'` (zone pour le sommaire), `'mw-editsection'` (zones pour les liens [modifier | modifier le code]), `'mwe-math-element'` (zones éventuelles de formules mathématiques), `'bandeau-portail'` (bandeau de navigation vers les autres portails Wikipédia, en bas de la page).

# In[8]:


url, titre, texte = [], [], []
for links in listlink:
    link = "https://fr.wikipedia.org" + links

    with get(link) as response:
        p1 = BeautifulSoup(response.text, 'html.parser')
    title = p1.title.text

    tclass = ['toc', 'mw-editsection', 'mwe-math-element', 'beandeau-portail']
    tags = ['style', 'sup']
    body = p1.find(id="mw-content-text")
    ignore = body.find_all('div',
                           class_=lambda x: x in tclass) + body.find_all(tags)
    for div in ignore:
        div.decompose()
    text = body.text.strip()

    url.append(link)
    titre.append(title)
    texte.append(text)


# 3. Mémoriser l’ensemble des informations récoltées (url, titre et texte) dans un dictionnaire «docs» possédant trois clés associées aux trois listes d’informations:  
# doc = {"url": [] , "titre": [], "texte":[]}  
# et enregistrer ce dictionnaire dans un fichier à l’aide du module pickle.

# In[9]:


doc = {
    "url" : url,
    "titre" : titre,
    "texte" : texte
}

with open('td3scrap.pickle', 'wb') as export:
    pickle.dump(doc, export)


# # Exercice 2: recherche d’information dans un corpus de texte
# On se propose de simuler de façon simplifié le fonctionnement d’un moteur de recherche.
# 
# 1. Écrire une classe DTM dont le constructeur prend en paramètre le dictionnaire enregistré à la fin de l’exercice 1 et possédant les attributs suivants:
# 
#  - url: listes des URLs des documents
#  - title: liste des titres des documents
#  - data: une DataFrame de pandas représentant la matrice document-terme du corpus. Les indices de ligne de cette DataFrame seront les indices des documents et les intitulés de colonne seront les termes du corpus. Remplacer, dans cette DataFrame, les valeurs manquante NaN par la valeur 0 (cas où aucune occurrence du terme représenté par l’intitulé de colonne n’a été trouvée dans le document de la ligne correspondante).

# In[10]:


doc['data'] = pd.DataFrame(
    [{x: token.count(x)
      for x in set(token)}
     for token in [getTokens(text) for text in doc['texte']]]).fillna(0)
del doc['texte']


# In[11]:


work = DTM(doc)


# 2. Ajouter à cette classe la méthode `__repr( )__` pour que l’affichage d’un objet DTM renvoie la DataFrame contenu dans l’attribut data.

# In[12]:
print('\n\n####################\n>>> print(work)\n')

print(work)


# 3. Ajouter à la classe DTM une méthode `nBest( )` prenant en argument un nombre entier N et renvoyant la liste des N termes les plus fréquents dans le corpus entier, avec leur fréquence, par ordres décroissant des fréquences. Indication: utiliser la méthode `sum()` des DataFrame pandas. 

# In[13]:
print('\n\n####################\n>>> print(work.nBest(10))\n')

print(work.nBest(10))


# 4. Rajouter une deuxième méthode `nBestDoc( )` prenant en deuxième argument l’indice (entier) d’un document et renvoyant la liste des N termes les plus fréquents dans ce document, avec leur fréquence, par ordres décroissant des fréquences.

# In[14]:
print('\n\n####################\n>>> print(work.nBestDoc(10, 1))\n')

print(work.nBestDoc(10, 1))


# 5. Testez les deux méthodes précédentes en observant les 10 termes les plus fréquents pour le corpus entier et pour différents documents. Concluez.
# 
# Les termes les plus fréquents sont des stopwords qui ne donnent pas plus d'informations sur les corpus puisqu'ils sont communs. Ils ne sont pas pertinents à analyser.

# 6. Ajoutez la liste de mots-vide comme nouvel attribut de la classe DTM: attribut stopWords. Testez à nouveau les deux méthode `nBest()` et `nBestDoc()` après avoir exclu ces mots-vides.

# 7. Ajouter à la classe DTM une méthode `query( )` prenant en paramètre une requête (chaîne de caractères) représentant une liste de mots séparés par des espaces, et renvoyant la liste des documents contenant l’ensemble des mots de la requête.

# In[15]:
print('\n\n####################\n>>> print(work.query("réseau vent"))\n')

print(work.query("réseau vent"))


# 8. Remplir la matrice document-terme avec le tf.idf et utiliser ces scores pour classer les documents résultats de la requête, en sortie d'une nouvelle méthode `queryScore()`. Le score global de la requête sera la somme des scores tf.idf de chaque terme. La méthode renverra une Dataframe avec en première colonne l'url des documents, et en seconde colonne le score associé, par ordre décroissant de ces scores.

# In[16]:
print('\n\n####################\n>>> print(work.queryScore())\n')

print(work.queryScore())

