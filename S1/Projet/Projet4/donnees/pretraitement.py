#!/usr/bin/python3
# -*- coding:utf8 -*-
"""Mini projet sur les données de valeurs foncières en France"""
################################################################################
# fichier  : pretraitement.py
# Auteur : Nom Prenom
################################################################################

################################################################################
# Importation de fonctions externes :
import pickle

################################################################################
# Definition locale de fonctions :

################################################################################
# Lecture avec pickle
# Récupération des variables
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

# La variable data représente l'ensemble des données################################################################################
# Definition de classe

################################################################################
#Récupération des données

#reponses=readData('reponses.pic')
#La variable reponses représente l'ensemble des réponses aux questions du projet
#Aide_ex14 = reponses[0]
#Aide_ex21 = reponses[1]
#Aide_ex22 = reponses[2]
#Aide_ex32 = reponses[3]
################################################################################
# Corps principal du programme :
