# Budget Participatif

<div align="center">

<a href="https://github.com/Lrakotoson/M1Python/tree/master/S2/Data%20Visualization">
<img src="https://raw.githubusercontent.com/Lrakotoson/M1Python/master/S2/Data%20Visualization/Budget_Participatif/statics/banner.jpg"  width="50%" style="min-height:'250px'"/>
</a>

![GitHub](https://img.shields.io/github/license/Lrakotoson/M1Python?style=for-the-badge)
[![Work](https://img.shields.io/badge/kernel-bokeh-f9ca24?style=for-the-badge&logo=Python&logoColor=f9ca24&labelColor=1B1464)](https://github.com/Lrakotoson/M1Python/tree/master/S2/Data%20Visualization)

Tableau de bord des campagnes de Budget Participatif dans la ville de Rennes.

</div>

# Execution

Cette application tourne sous Python avec Bokeh.  
Pour lancer l'application, exécuter la commande suivante depuis cette racine:

```shell
bokeh serve --show Budget_Participatif/
```

Si vous vous trouvez dans le dossier `Budget_Participatif/`, cela revient à exécuter la commande:

```shell
bokeh serve --show main.py
```

Si vous voulez effectuer une mise à jour avant lancement, exécutez:

```shell
python Budget_Participatif/data/format.py
bokeh serve --show Budget_Participatif/
```
Notez que les données sont mises à jour annuellement donc de multiples mises à jour ne sont pas nécessaires.

# Interface

L'interface est divisée en 2 grandes parties.  
D'un côté, la principale qui contient les différentes représentations de nos données, et d'un autre, la barre latérale gauche qui permet de sélectionner les données à partir de plusieurs filtres.

<div align="center">
<img src="https://raw.githubusercontent.com/Lrakotoson/M1Python/master/S2/Data%20Visualization/Budget_Participatif/statics/screenshot.png" width="90%" style="min-height:'250px'"/>
</div>

## Filtres
Les filtres permettent de sélectionner les données à analyser et à présenter.

- **Année de campagne:** Sélectionne la ou les années de campagne de budget participatif.
- **Quartiers:** Sélectionne les projets proposés dans le ou les quartiers filtrés parmi les 12 quartiers de Rennes.
- **Statut:** Sélectionne les projets selon leurs statuts, en l'occurrence "Réalisé", "Non réalisable", "A l'étude" ou "En cours".

## Graphes
Les graphes permettent différentes représentations qui se complètent.

- **Carte:** Répartition géographique des différents projets. On peut constater les projets proposés par un quartier qui s'étend aussi dans d'autres. En cliquant sur un projet, on peut obtenir les détails, la photo et le lien s'ils existent.
- **Projets par quartiers:** Nombre de projets et leurs statuts par quartier. On peut y voir les projets "Non réalisables" qui ne peuvent donc pas être représenté sur la carte.
- **Etats des projets par année:** Nombre de projets proposés par année et la distribution de leurs status. On peut y voir la baisse de projets et aussi l'année où les projets ont été refusés.

# Données
## Source
Les données proviennent de l'[Open Data de Renne Metropole](https://data.rennesmetropole.fr/pages/home/).

- [Quartiers](https://data.rennesmetropole.fr/explore/dataset/perimetres-des-12-quartiers-de-la-ville-de-rennes/information/): Cette couche indique les périmètres des 12 quartiers de la Ville de Rennes. **Chargé en local**
- [Budget](https://data.rennesmetropole.fr/explore/dataset/localisation-et-etat-des-projets-du-budget-participatif/information/?disjunctive.quartier&sort=libelle): Ce jeu de données recense la localisation et l'état d'avancement de tout les projets lauréats du Budget Participatif (toutes années comprises). **Récolté via l'API**.

Les données Budget sont récoltés via l'API. Les Quartiers sont chargés en local puisque ces données ne changent que peu (*dernière modification en 2014*).  
La récolte des données se fait en manuel **juste en exécutant le script `data/format.py`**, mais elle aurait pû être automatique avec chaque connexion au serveur bokeh.

Mais avec la contrainte du temps d'exécution quant au prétraitement (quelques secondes au démarrage) ainsi que la fréquence de mise à jour des données (annuelle), il est préférable de mettre à jour les données **Budget** une fois par an et modifier les fichiers suivants:

- `main.py`: ajout de l'année à la ligne 55
- `scripts/filterdata.py`: ajout de l'année à la ligne 117

## Prétraitement
Pour gagner du temps de calcul, il est nécessaire de prétraiter les données brutes. Le script `data/format.py` permet d'effectuer les prétraitements suivants:

### Quartier
- Conversion de l'ensemble des coordonées longitude/latitude des contours de chaque quartier en coordonnées Cartésiens X/Y
- Nettoyage des noms de quartier
- Récupération de l'ID de quartier

### Budget
- Conversion de chaque coordonées longitude/latitude des projets en coordonnées Cartésiens X/Y
- Nettoyage des noms de colonnes
- Nettoyage des noms de quartier

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

<span style = "color:#d63031"><i style = "font-size: x-large" class="fa fa-exclamation-circle" aria-hidden="true"></i> <strong>Effectuer une copie sauvegarde des anciennes données</strong></span> avant d'exécuter le script de prétraitement sur de nouvelles données.

Pour effectuer une mise à jour pour une nouvelle année, éxecuter:

```shell
python Budget_Participatif/data/format.py
```
Ceci écrasera les fichiers `formated_budget.csv` et `formated_quartiers.json` en créera de nouveaux.

# Modules
Les différents modules sont répertoriés dans le dossier `scripts/`

## `filterdata.py`
Ce module contient la classe `Data`.

La classe `Data` est le **chef d'orchestre** de l'application.  
Elle contrôle les données, effectue les calculs en fonction des requêtes et fournit les bonnes données à chaque fonction des autres modules qui, elles, font toujours les mêmes graphes avec les données qu'on leur donne.

## `plotmap.py`
Ce module contient la fonction `mapPlot( )`.  
Cette fonction renvoie une carte de la situation géographique de l'ensemble des projets dans les données que `Data` lui a fournies. Elle colore les projets en fonction de leurs statuts.

Un survol des points permet d'afficher les détails du projet avec la photo si elle existe.

## `plotbar.py`
Ce module contient les fonctions `barPlot( )` et `stackPlot( )`.

`barPlot( )` renvoie, pour chaque quartier et pour la période totale des données que `Data` lui fournit, le nombre de projets de chaque statut de projet.

`stackPlot( )` renvoie les projets et la part de chaque statut pour chaque année des données fournies par `Data`.

## `markups.py`
Ce module rassemble toutes les fonctions qui renvoient des éléments HTML de classe `Div`. Il s'agit d'éléments statiques. 

- `header()` et `footer()` renvoient respectivement l'en-tête et le pied de page du rendu.
- `style()` renvoie les styles CSS qui s'appliquent à l'ensemble du rendu. Ils ont pour but d'écraser les styles par défaut du document.
- `textInit()` renvoie la division qui contient l'explication des filtres au début du sidebar.
- `textTitle()` renvoie le titre qu'on lui a fourni avec les styles qui s'accordent avec le document
- `blank()` renvoie une colonne vide pour répondre à un bug non résolu de bokeh quant à la mise en forme des pages. Elle servira entre autre à décaler les plots vers la gauche.

# Projet
Ce projet à été réalisé dans le cadre du cours de Data Vizualisation en 1<sup>re</sup> année de Master dans la filière Mathématiques appliquées, Statistique.