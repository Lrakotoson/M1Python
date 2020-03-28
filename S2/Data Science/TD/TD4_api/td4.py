
# coding: utf-8

# In[1]:


"""Script permettant d'explorer les données d'un fichier XML et d'interroger une API"""
################################################################################
# fichier  : td4.py
# Auteur : RAKOTOSON Loic
################################################################################


# In[2]:


################################################################################
# Importation de fonctions externes :
import pandas as pd
import json
from lxml import etree
from requests import get, HTTPError
# Definition locale de fonctions :


# In[3]:


def afficheXML(liste):
    for elem in liste:
        if isinstance(elem, etree._Element):
            print(etree.tostring(elem,encoding='unicode'))
        else:
            print(elem)


# In[4]:


def afficheTexte(liste):
    for elem in liste:
        if isinstance(elem, etree._Element):
            if elem.text:
                print(elem.text)
            afficheTexte(elem.xpath('./*'))
        else:
            print(elem)


# In[5]:


def getJsonData(base, dico):
    with get(base, params = dico) as response:
        return response.json()


# In[6]:


def getMatrix(base, dico, metric):
    """
    Retourne la matrice de la métrique
    :base: base url
    :dico: API params
    :metric: distances|durations
    :return: DataFrame
    """
    reponse = getJsonData(base, dico)
    df = pd.DataFrame(
        reponse[metric],
        columns=[
            ",".join(map(str, d['location'])) for d in reponse['destinations']
        ],
        index=[",".join(map(str, d['location'])) for d in reponse['sources']])
    return df


# In[7]:


def cleanGPS(GPSlist):
    """
    Renvoie un str formaté pour l'API
    :GPSlist: [lat, lon] du XML
    :return: str
    """
    raw = list(map(str,map(int,[coord.replace('.', '') for coord in GPSlist])))
    if '-' in raw[0]:
        lat = raw[0][:3] + '.' + raw[0][3:10]
    else:
        lat = raw[0][:2] + '.' + raw[0][2:9]
    if '-' in raw[1]:
        lon = raw[1][:2] + '.' + raw[1][2:9]
    else:
        lon = raw[1][0] + '.' + raw[1][1:8]
    return lon + ',' + lat


# In[8]:


################################################################################
# Corps principal du programme :


# In[9]:


base_url = "https://api.openrouteservice.org/matrix"
APIKEY = '5b3ce3597851110001cf62486cfda2a850de46e4a43253fa6adffd31'


# # Exercice 1: découverte de l'API Matrix de openrouteservice
# Trouver les coordonnées GPS des villes de Rennes, Paris, Nantes et Brest, et mémorisez-les (dans cet ordre)  au début du programme principal sous forme d'une liste Python de chaînes de caractères représentant chacune une paire de coordonnées séparées par une virgule:

# In[10]:


villesGPS = [
    '-1.6800198,48.1113387', '2.3514992,48.8566101',
    '-1.553621,47.218371', '-4.486076,48.390394'
]


# Écrire une fonction `getJsonData()` prenant en paramètre l'URL de base de l'API Matrix et un dictionnaire des paramètres de la requête (clé = nom du paramètre; valeur=valeur du paramètre) et retournant les données JSON renvoyées par le service, sous forme d'une structure de données Python.

# In[11]:


data = {
    "api_key" : APIKEY,
    "profile": "driving-car",
    "locations": "|".join(villesGPS),
    "sources": "0,1",
    "destinations": "2,3",
    "metrics": "distance|duration",
    "units": "km",
    
}
reponse = getJsonData(base_url, data)
print(
    "\n########## EXO 1.4 ##########\n",
    reponse
)


# Dans le programme principal, écrire le code Python permettant d'obtenir la matrice des distances avec Rennes et Paris comme villes d'origine, Brest et Nantes comme villes de destination, et d'afficher cette matrice ligne par ligne.

# In[12]:


matrix = getMatrix(base_url, data, "distances")
print(
    "\n########## EXO 1.5 ##########\n",
    matrix
)


# # Exercice 2: utilisation des données XML des points de vente de carburant et des données en ligne de l'API
# Choisir une voiture et déterminer son type de carburant et sa consommation moyenne en allure «route». Mémoriser ces informations dans 2 variables «carburant» et «conso» de votre programme.

# In[13]:


carburant = "Gazole"
conso = "4.1"


# La première étape du voyage est de faire le plein d'essence sur Rennes au tarif le plus avantageux pour votre carburant.A l'aide des données du fichier *PrixCarburants_quotidien_AAAAMMJJ.xml*, déterminez quel est ce point de vente le plus avantageux pour vous à Rennes. Affichez ce prix et l'adresse complète du point de vente correspondant.  
# Remarque: dans le fichier XML, le nom de ville peut apparaître sous la forme «Rennes» ou «RENNES».

# In[14]:


root = etree.parse("PrixCarburants_quotidien_20200316.xml").getroot()
gazoleRennes = list(
    map(
        int,
        root.xpath(
            "pdv[contains('Rennes RENNES', ville)]/prix[@nom = '{}']//@valeur".
            format(carburant))))


# In[15]:


# Le meilleur à Rennes
bestRennes = root.xpath(
    "pdv[contains('Rennes RENNES', ville)][prix/@nom = '{}' and prix/@valeur = '{}']"
    .format(carburant, min(gazoleRennes)))[0]


# In[16]:


# Le pire à Rennes
maxRennes = root.xpath(
    "pdv[contains('Rennes RENNES', ville)][prix/@nom = '{}' and prix/@valeur = '{}']"
    .format(carburant, max(gazoleRennes)))[0]


# In[17]:


chaine = "Le meilleur point de vente se trouve à {} au prix de {}€".format(
    *bestRennes.xpath("adresse//text()|prix[@nom = '{}']/@valeur".format(
        carburant)))
print(
    "\n########## EXO 2.2 ##########\n",
    chaine
)


# La deuxième (grande) étape de votre voyage est de vous ravitailler en carburant avant de passer la frontière. Le voyage jusqu'à ce point de vente se fera donc avec le carburant au meilleur tarif que vous avez trouvé sur Rennes. On supposera que la suite du voyage jusqu'à Rome se fera au tarif du carburant chargé au point de ravitaillement.  
# Pour ce point de ravitaillement, vous avez quelques contraintes:
# 
# - Il devra se trouver dans le département de Savoie (**73**) ou de Haute Savoie (**74**)
# - Vous aurez besoin de faire un petit tour aux toilettes avant de repartir (service «Toilettes publiques» obligatoire)
# - Vous aurez besoin d'acheter quelque chose à grignoter (service "Boutique alimentaire" ou "Restauration à emporter" obligatoire)
# - Vous aurez besoin de retirer de l'argent liquide (service «DAB (Distributeur automatique de billets)» obligatoire)
# 
# Déterminez une expression Xpath unique permettant d'obtenir les nœuds «point de vente» répondant à l'ensemble des contraintes ci-dessus. Afficher le nombre de pointde vente correspondants obtenus

# In[18]:


request = "pdv[starts-with(@cp, '73') or starts-with(@cp, '74')]""[contains('Toilettes publiques', service)]""[services[service = 'Boutique alimentaire' or service = 'Restauration à emporter']]""[contains('DAB', service)]"

nodes = root.xpath(request)
print(
    "\n########## EXO 2.3.1 ##########\n",
    len(nodes)
)


# Parmi les points de ventes retournés, déterminez lequel permet d'optimiser le prix global en carburant du voyage, en tenant compte des deux distances parcourues, Rennes → ravitaillement et ravitaillement → Rome (utilisez l'API Matrix pour calculer ces distances), et du tarif du carburant pour ces deux portions.
# 
# On regroupe en premier lieu toutes les locations, les sources comprises.  
# On enregistre ensuite les paramètres qui seront nécessaires pour effectuer la requête dans un dictionnaire *params*.  
# Enfin, on calcule la matrice avec l'API Matrix, en passant par la fonction `getMatrix()`.

# In[19]:


Rome = "12.4963655,41.9027835"
Rennes = cleanGPS(bestRennes.xpath("@latitude | @longitude"))
stations = [
    cleanGPS(node.xpath("@latitude | @longitude")) for node in nodes
    if node.xpath("@latitude")[0] != ''
]

params = {
    "api_key":
    APIKEY,
    "profile":
    "driving-car",
    "locations":
    "|".join([Rennes, Rome] + stations),
    "sources":
    "0,1",
    "destinations":
    ",".join(map(str, range(2,
                            len([Rennes, Rome] + stations) - 1))),
    "metrics":
    "distance|duration",
    "units":
    "km",
}

RennesRome = getMatrix(base_url, params, "distances")

print(
    "\n########## EXO 2.3.2 ##########\n",
    "Les distances avec les stations qui remplissent les conditions\n",
    RennesRome
)


# On a supposé que la voiture a une autonomie d'environ 900km, et que, partant avec le pleinde carburant de Rennes, nous devrons refaire un ravitaillement juste avant de passer la frontière.  
# Symétriquement, la distance entre le point de ravitaillement et Rome ne doit pas éxcéder l'autonomie.  
# On supprime donc les colonnes vérifiant cette condition.

# In[20]:


RennesRome = RennesRome.loc[:, ~(RennesRome > 900).any()]
print(
    "Les distances avec les stations candidates\n",
    RennesRome
)


# Enfin, on supprime toutes les colonnes dont la somme des distances est supérieure à la somme des distance minimale.  
# Il ne devra en rester qu'une. Il s'agit de la station la plus otpimisée.

# In[21]:


cols = RennesRome.columns[RennesRome.sum(axis=0) > RennesRome.sum(
    axis=0).min()]
best = RennesRome.drop(cols, axis=1)
print(
    "Les distances avec la meilleure station\n",
    best
)


# Donnez le prix en carburant de ce voyage optimisé, et la différence avec le prix le plus élevé (y compris en faisant le plein le plus cher à Rennes), avec les mêmes contraintes sur le point de ravitaillement.

# In[22]:


RennesMax = cleanGPS(maxRennes.xpath("@latitude | @longitude"))
params['locations'] = "|".join([RennesMax, Rome] + stations)
maxcarb = getMatrix(base_url, params, "distances")
maxcarb = maxcarb.loc[:, ~(maxcarb > 900).any()]
maxcarb = maxcarb.drop(
    maxcarb.columns[maxcarb.sum(axis=0) > maxcarb.sum(axis=0).min()], axis=1)


# In[23]:


worst = RennesRome[RennesRome.columns[RennesRome.sum(axis=0) == RennesRome.sum(
    axis=0).max()]]


# In[24]:


prixbest = float(
    bestRennes.xpath("prix[@nom = '{}']/@valeur".format(carburant))[0][0] +
    '.' +
    bestRennes.xpath("prix[@nom = '{}']/@valeur".format(carburant))[0][1:])


# In[25]:


print(
    "\n########## EXO 2.3.3 ##########\n",
    "Les prix pour le meilleur, le pire et en partant de la station la plus chère à Rennes\n",
    pd.DataFrame({
        'best': best.sum(axis=0).reset_index(drop=True),
        'worst': worst.sum(axis=0).reset_index(drop=True),
        'maxcarb': maxcarb.sum(axis=0).reset_index(drop=True)
    }) * prixbest
)


# Se ravitailler dans la station la moins avantageuse augmente le coût de 46 euros. En passant par la station la plus chère de Rennes, le coût n'augmente que de 1.30 euro.
# 
# Calculer également la durée estimée du voyage optimisé et celle du voyage le plus court en temps (même point de vente à Rennes et mêmes contraintes pour le point deravitaillement)

# In[26]:


params['locations'] = "|".join([Rennes, Rome] + stations)
duration = getMatrix(base_url, params, "durations")
duration = duration[duration.columns[duration.sum(axis=0) == duration.sum(
    axis=0).min()].append(best.columns)]
duration.loc['Total'] = duration.sum(axis = 0)

print(
    "\n########## EXO 2.3.4 ##########\n",
    "Durée pour le voyage le plus court et le moins cher\n",
    duration
)


# Il y a environ 8h de différence entre les deux trajets.
