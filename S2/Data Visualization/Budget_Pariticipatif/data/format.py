# coding: utf-8

__author__ = 'Lrakotoson'
__maintainer__ = 'Loïc Rakotoson'
__email__ = 'contact@loicrakotoson.com'
__status__ = 'planning'

import json
import pandas as pd
from numpy import NaN

###################### FICHIERS ########################

with open("quartiers.json", 'r', encoding = "utf-8") as file:
    quartiers = json.load(file)

budget = pd.read_csv("budget.csv", sep = ';')

###################### FONCTIONS #######################

def LongLat_to_EN(long, lat):
    try:
        easting, northing = transform(
            Proj(init='epsg:4326'),
            Proj(init='epsg:3857'),
            long, lat)
        return easting, northing
    except:
        return None, None

def bpToQuartier(chaine):
    """
    Sépare les numéros de quartiers de leurs noms
    :chaine: str
    :return: Series
    """
    try:
        list_q = chaine.split(' - ')
        num_q = int(list_q[0])
        quartier = ' - '.join(list_q[1:])
        serie = pd.Series((num_q, quartier))
    except:
        serie = pd.Series((NaN, NaN))
    return serie

def bpToYear(chaine):
    """
    Collecte l'année
    :chaine: str
    :return: str ou NaN
    """
    try:
        annee = chaine[24:28]
    except:
        annee = NaN
    return annee

#------------------------------------------------------#

###################### QUARTIERS #######################

q_id = []
q_nom = []
q_point = []
q_xshape = []
q_yshape = []

for field in quartiers:
    q = field['fields']
    q_id.append(q['nuquart'])
    q_nom.append(q['nom'])
    q_point.append(list(LongLat_to_EN(*q['geo_point_2d'][::-1])))
    
    coords = q['geo_shape']['coordinates']
    mesx = []
    mesy = []
    for level1 in coords :
        for c in level1:
            x,y = LongLat_to_EN(c[0],c[1])
            mesx.append(x)
            mesy.append(y)
    q_xshape.append(mesx)
    q_yshape.append(mesy)

df = pd.DataFrame(
    {
        'q_id': q_id,
        'q_nom': q_nom,
        'q_point': q_point,
        'q_x': q_xshape,
        'q_y':q_yshape
    }
)

df = df.sort_values('q_id').reset_index(drop = True)
df.to_json("formated_quartiers.json")

####################### BUDGET #########################

bd = pd.DataFrame()

bd[[
        'b_numero', 'b_libelle', 'b_description',
        'b_realise', 'b_lien', 'b_photo'
    ]] = budget[[
        'Numéro', 'Libellé', 'Description',
        'Réalisé', 'Lien_page_projet', 'Photo'
    ]]

bd['b_year'] = budget['Année_Budget'].apply(bpToYear)
bd[['b_q_id', 'b_quartier']] = budget['Quartier'].apply(bpToQuartier)

bd[['b_x', 'b_y']] = budget.apply(lambda x: pd.Series(
        LongLat_to_EN(x['Longitude'], x['Latitude'])), axis = 1)

bd.to_csv("formated_budget.csv", index=False)