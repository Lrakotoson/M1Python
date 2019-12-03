#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""lecture et analyse de tweets"""
################################################################################
# fichier  : RakotosonLoic.py
# Auteur : Rakotoson Loic
################################################################################

################################################################################
# Importation de fonctions externes :
import pickle
import numpy as np
import csv

################################################################################
# Definition locale de fonctions :

################################################################################


# In[2]:


#Lecture avec pickle (Récupération des variables réponses)
def readData(nomFichier):
    listeData = []
    try:
        with open(nomFichier, 'rb') as objet_fichier:
            objet_fichier_depickler = pickle.Unpickler(objet_fichier)
            while 1:
                try:
                    listeData.append(objet_fichier_depickler.load())
                except EOFError:
                    break
    except (IOError, OSError):
        print("Problème à l'ouverture du fichier")
    return listeData


# In[3]:


################################################################################
# Definition de classe (Définir la classe objet de l'exercice 4 ci-dessous)

################################################################################
# Aide
listeData = readData('reponses.pic')
aideEx11 = listeData[0]
aideEx12 = listeData[1]
aideEx21 = listeData[2]
aideEx22 = listeData[3]
aideEx31 = listeData[4]
aideEx32 = listeData[5]
aideEx33 = listeData[6]
# aideEx4 impossible car c'est à vous de créer et tester la classe
aideEx51 = listeData[7]
aideEx52 = listeData[8]
################################################################################
# Corps principal du programme :


# # EXO 1

# In[4]:


def lireFichier_csv(fichier, delim, encodage="utf-8"):
    with open(fichier, 'r', encoding=encodage) as file:
        data = [ligne for ligne in csv.reader(file, delimiter=delim)]
    return data


# In[5]:


data = lireFichier_csv("tweets.csv", ";")


# In[6]:


def suppressionColonnes(data):
    col = [
        data[0].index(c)
        for c in ("Tweet Id", "Date", "Hour", "User Name", "Tweet content",
                  'Followers', 'Following', 'Tweet language (ISO 639-1)',
                  'Is a RT', 'Hashtags')
    ]
    data = [[data[i][j] for j in col] for i in range(len(data))]
    return data


# In[7]:


data = suppressionColonnes(data)


# # EXO 2

# In[8]:


def typageInt(data):
    for i, ligne in enumerate(data):
        for j, col in enumerate(ligne):
            if isinstance(col, str) and col.strip().isdigit():  #strip: Enlever l'espace de fin de TweetId
                data[i][j] = int(data[i][j])
    return data


# In[9]:


data = typageInt(data)


# In[10]:


def typageBool(data):
    isrt = data[0].index("Is a RT")
    for ligne in data[1:]:
        if ligne[isrt] == "TRUE":
            ligne[isrt] = True
        else:
            ligne[isrt] = False
    return data


# In[11]:


data = typageBool(data)


# # EXO 3

# In[12]:


def extractionUserName(data):
    username = data[0].index('User Name')
    luser = list({ligne[username] for ligne in data[1:]})
    return luser


# In[13]:


def nbTweetsOriginaux(data):
    isrt = data[0].index("Is a RT")
    RT = [ligne[isrt] for ligne in data[1:]]
    nbOrig = len(RT) - sum(RT)
    return nbOrig


# In[14]:


def audienceTweets(data):
    followers = data[0].index('Followers')
    audience = sum([
        ligne[followers] for ligne in data[1:] if isinstance(
            ligne[followers], int)  # Car présence de str vides qui ont échappé au typageInt
    ])
    return audience


# # EXO 4

# In[15]:


class Tweet():
    def __init__(self, tweetId, date, hour, userName, tweetContent, followers,
                 followings, tweetLanguage, isRT, hashtags):
        self.tweetId = tweetId
        self.date = date
        self.hour = hour
        self.userName = userName
        self.tweetContent = tweetContent
        self.followers = followers
        self.followings = followings
        self.tweetLanguage = tweetLanguage
        self.isRT = isRT
        self.hashtags = hashtags

    def __str__(self):
        affichage = "Nom utilisateur: {}\nDate et heure : {} {}\nContenu du tweet:\n{}".format(
            self.userName, self.date, self.hour, self.tweetContent)
        return affichage

    def comparaisonHashtag(self, hasgtag):
        if hasgtag.lower() in self.hashtags.lower():
            return True
        else:
            return False


# # EXO 5

# In[16]:


def selectionTweets(data, sethashtag):
    htag = data[0].index('Hashtags')
    listehtag = []
    for ligne in data[1:]:
        if any(hashtag.lower() in ligne[htag].lower()
               for hashtag in sethashtag):
            listehtag.append(ligne)
    return listehtag


# In[17]:


sethtag = {"#netflix", "#nflx"}
twNetflix = selectionTweets(data, sethtag)


# In[18]:


def nbTweetsLanguage(data):
    lang = data[0].index('Tweet language (ISO 639-1)')
    listelangue = [ligne[lang] for ligne in data[1:]]
    dicolangue = {
        langue: listelangue.count(langue)
        for langue in set(listelangue)
    }
    return dicolangue


# In[19]:


print(nbTweetsLanguage(data))

