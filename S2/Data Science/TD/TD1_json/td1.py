#!/usr/bin/env python
# coding: utf-8
# %%

# %%


"""Script permettant d'explorer les données de travaux sur Rennes, au format JSON"""
################################################################################
# fichier  : td1.py
# Auteur : RAKOTOSON Loic
################################################################################


# %%


################################################################################
# Importation de fonctions externes :
import json
from datetime import datetime, timedelta
# Definition locale de fonctions :


# %%


def initListeChantiers(data):
    listeChantier = [Chantier(dico["properties"]) for dico in data["features"]]
    return listeChantier


# %%


def listeChantiersEnCours(listeChantiers,
                          date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    liste = [chantier for chantier in listeChantiers if chantier.enCours(date)]
    return liste


# %%


def affichePlanningChantiers(
        listeChantiers, ID, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):

    dateformat = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    listequartier = [
        chantier for chantier in listeChantiers if chantier.quartierID == ID
    ]

    chaine = "Planning des chantiers pour le quartier {}".format(
        Chantier.quartiers[ID])
    for chantier in listequartier:
        chaine += "\n {} ({}): ".format(chantier.localisation, chantier.type)
        if chantier.enCours(date):
            fin = chantier.fin - dateformat
            chaine += "chantier en cours (fin dans {} jours et {} heures)".format(
                fin.days, fin.seconds // 3600)
        elif chantier.aVenir(date):
            debut = dateformat - chantier.debut
            chaine += "chantier à venir (début dans {} jours et {} heures)".format(
                debut.days, fin.seconds // 3600)
        elif chantier.termine(date):
            fin = dateformat - chantier.fin
            chaine += "chantier terminé depuis {} jours et {} heures)".format(
                fin.days, fin.seconds // 3600)
        else:
            chaine += "Manque d'informations"
    print(chaine)


# %%


def dumpListeChantiersJSON(output, listeChantier):
    data = {
        "chantiers":
        [chantier.jsonDictionnary() for chantier in listeChantier]
    }
    with open(output + ".json", "w", encoding="UTF-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)


# %%


################################################################################
# Definition des classes :


# %%


class Chantier():
    quartiers = dict()

    def __init__(self, properties):
        quartier = properties["quartier"]

        self.id = properties["id"]
        self.quartierID = int(quartier.split(" - ")[0])
        self.localisation = properties["localisation"]
        self.type = properties["type"]
        self.libelle = properties["libelle"]
        self.perturbation = properties["niv_perturbation"]

        if self.quartierID not in self.__class__.quartiers:
            self.__class__.quartiers[self.quartierID] = "/".join(
                quartier.split(" - ")[1:])

        self.debut = datetime.strptime(properties["date_deb"],
                                       "%Y-%m-%d %H:%M:%S")
        self.fin = datetime.strptime(properties["date_fin"],
                                     "%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        chaine = "{}, {} du {} au {}: {} ({}, {})".format(
            self.quartierID, self.localisation,
            self.debut.strftime("%Y/%m/%d %H:%M:%S"),
            self.fin.strftime("%Y/%m/%d %H:%M:%S"), self.libelle, self.type,
            self.perturbation)
        return chaine

    def enCours(self, date):
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return self.debut < date < self.fin

    def termine(self, date):
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return date > self.fin

    def aVenir(self, date):
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return date < self.debut

    def jsonDictionnary(self):
        dico = dict()
        dico["id"] = self.id
        dico["quartier"] = self.__class__.quartiers[self.quartierID]
        dico["localisation"] = self.localisation
        dico["libelle"] = self.libelle
        dico["type"] = self.type
        dico["perturbation"] = self.perturbation
        dico["debut"] = self.debut.strftime("%Y/%m/%d %H:%M:%S")
        dico["fin"] = self.fin.strftime("%Y/%m/%d %H:%M:%S")
        return dico


# %%


################################################################################
# Corps principal du programme :


# # EXO 1
# Lecture et récupération des données

# %%


with open("travaux.json", "r", encoding="UTF-8") as json_file:
    travaux = json.load(json_file)


# # EXO 2
# Classe Chantier
print("\n############## EXO 2 ##############\n")
# %%

listeChantier = initListeChantiers(travaux)
print(listeChantier[0])


# # EXO 3
# Gestion des dates
print("\n############## EXO 3 ##############\n")
# %%

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Le chantier précédent en cours ajd ?\n", listeChantier[0].enCours(date))


# # EXO 4
# Utilisation Json
print("\n############## EXO 4 ##############\n")
# %%


affichePlanningChantiers(listeChantier, 1)


# %%


dumpListeChantiersJSON("export", listeChantier)

