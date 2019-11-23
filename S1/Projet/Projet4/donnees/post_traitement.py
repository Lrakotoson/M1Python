#!/usr/bin/python3
# -*- coding:utf8 -*-
"""Mini projet sur les données de valeurs foncières en France"""
################################################################################
# fichier  : post_traitement.py
# Auteur : Nom Prenom
################################################################################

################################################################################
# Importation de fonctions externes :
import folium

################################################################################
# Definition locale de fonctions :

def creationCarteGeographique(data, points_milieu_cadastre, indices, origine):
    c = folium.Map(location=origine, zoom_start=18)
    html_popup = '<h1>Caractéristiques du bien</h1>' \
                 '<p>Adresse : {}</br>' \
                 'Surface reelle bati : {}m2</br>' \
                 'Surface du terrain : {}m2</br>' \
                 'Valeur foncière : {}€</br>' \
                 'Date mutation : {}'
    for indice in indices:
        folium.Marker(points_milieu_cadastre[indice],
                      popup=html_popup.format(data[indice]['No voie']+' '+data[indice]['Type de voie']+' '+data[indice]['Voie']+' '+data[indice]['Code postal']+' '+data[indice]['Commune'],
                                              data[indice]['Surface reelle bati'],
                                              data[indice]['Surface terrain'],
                                              data[indice]['Valeur fonciere'],
                                              data[indice]['Date mutation']))\
            .add_to(c)
        folium.Polygon([[coord[1], coord[0]] for coord in eval(data[indice]['Coordonnees GPS parcelle'])[0]]).add_to(c)
    c.save('carteGeographiqueValeursFoncieres.html')

################################################################################
# Corps principal du programme :
# Lecture des coordonnées GPS pour la recherche
