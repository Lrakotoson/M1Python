#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""Mini projet sur la programmation du festival des Rencontres Trans Musicales
 de Rennes depuis sa première édition en 1979"""
################################################################################
# fichier  : RakotosonLoïc.py
# Auteur : Rakotoson Loïc
################################################################################

################################################################################
# Importation de fonctions externes :

from datetime import datetime
import pickle


# In[2]:


################################################################################
# Definition locale de fonctions :


def readData(nomFichier):
    """
    Lecture avec pickle (Récupération des variables réponses)
    """
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


def normaliser(liste):
    """
    Normalisation des accents, majuscules, espaces et tirets.
    liste: liste des mots
    :return: dictionnaire des mots normalisé et la liste de leur index
    """
    accents = ['à','â','ã','é','è','ê','ù','û','ç','ô','î','ï','í',' ','-']
    noaccents = ['a','a','a','e','e','e','u','u','c','o','i','i','i','','']
    dic = {}

    for index, mot in enumerate(liste):
        m = mot.lower()
        for a, s in zip(accents, noaccents):
            m = m.replace(a, s)
        if m not in dic:
            dic[m] = dic.get(m, {mot: [index]})
        elif mot not in dic[m]:
            dic[m][mot] = [index]
        else:
            dic[m][mot].append(index)
    return dic


# In[4]:


def similaire(mot1, mot2):
    """
    Calcul de score de distance simplifié entre deux mots.
    mot: chaine de caractères
    :return: score entre 0 et 1
    """
    if len(mot1) == 0 or len(mot2) == 0:
        return 0
    mot1 = mot1 + " " * (len(mot2) - len(mot1))
    mot2 = mot2 + " " * (len(mot1) - len(mot2))
    return sum(1 if i == j else 0
               for i, j in zip(mot1, mot2)) / float(len(mot1))


# In[5]:


################################################################################
# Definition de classe

################################################################################
# Récupération des données

listeData = readData('data.pic')
# La variable data représente l'ensemble des données des Trans Musicales
data = listeData[0]
################################################################################
# Corps principal du programme :


# # Les données
# ##  Suppression de quelques colonnes et affichage.
# Suppressions des colonnes. **Garder** uniquement les colonnes suivantes.

# In[6]:


garder = ['ANNÉE', 'EDITION RENCONTRES TRANS MUSICALES', 'ARTISTES',
          'ORIGINES PAYS 1', 'ORIGINES VILLE 1', 'ANNEE  DE FORMATION',
          '1ère SORTIE DISCOGRAPHIQUE']

donnees = [[data[j][data[0].index(i)] for i in garder]
           for j in range(len(data))]


# Renommer les colonnes. On connait les positions des colonnes à modifier.

# In[7]:


donnees[0][1] = 'EDITION'
donnees[0][3:5] = 'PAYS', 'VILLE'


# Créer une fonction qui permet d’afficher les lignes du tableau avec le format *en ligne*

# In[8]:


def affiche(data):
    """
    On considère qu'on affiche l'entête comme le corps
    :return: None
    """
    for liste in data:
        print(*liste)


# Affichons l'entête et les 4 premières lignes du tableau.

# In[9]:


affiche(donnees[:5])


# ## Vérification et uniformisation des données
# Vérification des Années, qui doivent appartenir à l'intervalle 1979 à l'année actuelle.
# On sait que la colonne Année est la première, mais on aurait pu
# utiliser **liste.index('ANNÉE')** pour y accéder aussi.

# In[10]:


annee = datetime.today().year

erreur = 0
for liste in donnees[1:]:
    if not 1979 <= int(liste[0]) <= annee:
        erreur += 1
print(erreur, ' année.s hors intervalle')


# Création d'une fonction *corrige()* qui permet de déterminer les orthographes différentes d’un même pays.
# On utilise deux fonctions simplifiées qu'on a implémenté plus haut *normaliser()* et *similaire()*.
# La fonction retourne un dictionnaire avec l'orthographe la plus fréquente pour chaque mot et la liste des index
# où effectuer les modifications dans les données de départ.
# 

# In[11]:


def corrige(liste, score):
    """
    liste: liste des noms
    score: score seuil minimum de similarité entre deux mots
    :print: noms avec différents orthographes et occurences
    :return: dictionnaire des noms et liste des index à remplacer
    """
    correction = {}
    dico = normaliser(liste)
    listecle = sorted(list(dico.keys()))

    # Regroupement des noms normalisés similaires
    index = 1
    for cle1 in listecle[1:]:  # Le premier élément représente les données vides
        index += 1  # En comparaison à partir du 2e
        for cle2 in listecle[index:]:
            if ((cle1 in cle2 and any(x in cle2 for x in ['(','/'])) 
                or similaire(cle1, cle2) > score):
                dico[cle1].update(dico[cle2])
                del dico[cle2]

    # Sélection de l'orthographe "parfait" et affichage des occurences
    dico = {cle: dico[cle] for cle in dico.keys() if len(dico[cle]) > 1}
    for cle, diconom in dico.items():
        m = max(diconom, key=lambda x: len(diconom[x]))
        correction[m] = sum(list(diconom.values()), [])
        print("\n{}|max: {}".format(cle, m))
        for nom, listeindex in diconom.items():
            print("    {}: {} occurence.s".format(nom, len(listeindex)))
    return correction


# Modification des noms de pays. On fixe un score de similarité de 0.73.
# On notera la présence de faux positifs non détectés par *corrige()*, (Irlande, Islande) et (Irak, Iran)

# In[12]:


pays = [i[3] for i in donnees]
for nom, listeindex in corrige(pays, 0.73).items():
    for index in listeindex:
        donnees[index][3] = nom


# De même pour les villes. On fixe un score plus élevé de 0.8 pour augmenter la précision.
# Un faible taux de faux positifs (Bienne, Vienne) et (Cannes, Vannes).

# In[13]:


villes = [i[4] for i in donnees]
for nom, listeindex in corrige(villes, 0.8).items():
    for index in listeindex:
        donnees[index][4] = nom


# ## Travail sur la colonne "1re discographie"
# Affichage de ce qui ne correspond pas uniquement à une année et transformation des données.

# In[14]:


for ligne in donnees[1:]:
    if not ligne[6].isdigit() and ligne[6] != '':
        print(ligne[6])
        nombres = [int(x) for x in ligne[6].replace('(', ' ').split()
                   if x.isdigit()]
        if len(nombres) == 0:  # Absence d'année
            donnees[donnees.index(ligne)][6] = ""
        else:
            donnees[donnees.index(ligne)][6] = str(min(nombres))


# ## Travail sur la colonne " Année de formation "
# Affichage de ce qui ne correspond pas uniquement à une année et transformation des données.

# In[15]:


for ligne in donnees[1:]:
    if not ligne[5].isdigit() and ligne[5] != '':
        lpropre = ligne[5].replace('(', ' ').replace(')', ' ').replace(
            "'", ' ').lower()  # ligne nettoyée
        nombres = [
            '19' + x if len(x) < 4 else x for x in lpropre.split()
            if x.isdigit()
        ]

        if len(nombres) == 0:  # Absence d'année
            m = ""
        else:
            m = min([int(x) for x in nombres if len(x) == 4]) # Année la plus petite

            if any([str(m).replace('19', '') in lpropre.partition("début")[2],
                    str(m).replace('19','') in lpropre.partition("première")[2]]):
                m += 2  # décade + 2
            elif any([str(m).replace('19', '') in lpropre.partition("fin")[2],
                      str(m).replace('19', '') in lpropre.partition("2ème")[2]]):
                m += 8  # décade + 10 - 2
            elif any([str(m).replace('19', '') in lpropre.partition("milieu")[2],
                      str(m).replace('19', '') in lpropre and "'s" in ligne[5]]):
                m += 5  # décade + 10 -5

        print("{} | {}".format(m, ligne[5]))
        donnees[donnees.index(ligne)][5] = str(m)


# # Survol des données
# ## Exercice 5
# Nombre de groupes programmés aux Transmusicales en fonction de l’année

# In[16]:


annees = sorted([int(i[0]) for i in donnees[1:]])
for annee, groupe in {x: annees.count(x) for x in set(annees)}.items():
    print("{}: {} groupes".format(annee, groupe))


# Artistes qui ont participé au moins à 5 éditions des Transmusicales et nombre de participations.

# In[17]:


artistes = {}
for i in donnees[1:]:
    if i[2] in artistes:
        artistes[i[2]].append(i[1])
    else:
        artistes[i[2]] = [i[1]]

for artiste,part in artistes.items():
    if len(part) >= 5:
        print("{}: {} participations".format(artiste, len(part)))


# Nombre d’artistes ayant participé aux Transmusicales en fonction du pays d’origine et
# affichage des 5 pays les plus représentés.

# In[18]:


def maxN (n, by):
    """
    n: les plus représentés
    by: numéro de colonne
    :print: n by les plus représentés
    :return: None
    """
    dico = {}
    for i in donnees[1:]:
        if i[by] not in dico:
            dico[i[by]] = [i[2]]
        elif i[2] not in dico[i[by]]:
            dico[i[by]].append(i[2])
    dico = {nom:len(art) for nom,art in dico.items()}
    for i in sorted(dico, key=dico.get, reverse=True)[:n]:
        print("{}: {} artistes".format(i, dico[i]))


# In[19]:


maxN(5, by=3)


# De même avec les villes.

# In[20]:


maxN(5, by=4)


# Déterminer l’écart (en année) entre la première sortie discographique et le passage aux Transmusicales.
# Affichons les 5 premiers éléments de la liste.

# In[23]:


ecart = [int(i[0]) - int(i[6]) if i[6].isdigit() else "NA" for i in donnees[1:]]
ecart[:5]


# Déterminer le nombre d’artistes ayant leur première sortie discographique la même année
# ou alors après leur passage aux Transmusicales.

# In[43]:


sum([1 for i in ecart if isinstance(i, int) and i<=0])


# ## Exercice 6
# Déterminer le nombre moyen d’artistes programmés aux Transmusicales chaque année.
# Nous avons enregistrés l'information sur le nombre d'artistes par années dans la liste **annees**.

# In[36]:


print("{:.0f} artistes en moyenne".format(len(annees) / len(set(annees))))


# Pour les artistes ayant sortie leur premier album après leur passage aux Transmusicales,
# déterminer le nombre moyen d’année entre leur passage et leur premier disque.
# On suppose que ceux ayant un écart de 0 ont sorti leur disque avant l'évenement mais dans la même année.

# In[47]:


ecartneg = [-i for i in ecart if isinstance(i, int) and i<0]
print("{:.0f} année.s en moyenne avant le premier disque".format(
sum(ecartneg) / len(ecartneg)))

