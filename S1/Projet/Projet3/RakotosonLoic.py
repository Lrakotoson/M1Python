#!/usr/bin/python3
# -*- coding:utf8 -*-
"""Mini projet sur les menus des cantines de Rennes métropole"""
################################################################################
# fichier  : NomPrenom.py
# Auteur : Nom Prenom
################################################################################

################################################################################
# Importation de fonctions externes :
import pickle

################################################################################
# Definition locale de fonctions :

# Récupération des variables
def readData(nomFichier):
    listeData=[]
    try :
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
################################################################################
# Definition de classe

################################################################################
#Récupération des données

listeData=readData('data.pic')
#Les variables ci-dessous correspondent aux réponses (exemple aide_ex_11 => exercice 1 question 1)
aide_ex_11 = listeData[0]
aide_ex_12 = listeData[1]
aide_ex_21 = listeData[2]
aide_ex_22 = listeData[3]
aide_ex_31 = listeData[4]
aide_ex_32 = listeData[5]
aide_ex_33 = listeData[6]
aide_ex_42 = listeData[7]

################################################################################
# Corps principal du programme :
# Constantes
entrees_crudites = ('Pamplemousse', 'Carottes râpées', 'Radis', 'Champignons et filet de citron', 'Tomates à la menthe', 'Concombre', 'Concombre à la grècque', 'Melon', 'Tomates à la ciboulette', 'Tomates au basilic', 'Carottes à la martiniquaise', 'Champignons', 'Salade de carottes et pommes', 'Champignons citronnés', 'Pastèque', 'Betteraves crues râpées', "Mousse d'avocats", "Salade d'avocats et tomates", 'Carottes, pommes, gruyère', 'Salade de tomates', 'Carottes râpées et gruyère')

desserts_fruits_crus = ('Banane', 'Clémentine', 'Orange', 'Corbeille de fruits', 'Kiwi', 'Banane mixée', 'Poire', 'Pomme', 'Fraises', 'Banane et framboise mixée', 'Nectarine', 'Pêche', 'Abricot', 'Prune', 'Ananas', 'Banane et fraise mixée', 'FLS', 'Melon', 'Raisin', 'Poire mixée', 'Fruits mixés')

plats_acides_gras = ('Poisson sauce tomate fraîche', 'Gratin de pâtes au thon', 'Thon', 'Sardine', 'Poisson', 'Poisson sauce tomate', 'Poisson au citron', 'Poisson beurre citron')

