# Classification classe générique

<div align="center">
  
  Projet semestriel - Text mining  
  **Identification de la classe générique de l’information exprimée dans un tweet**  
  [Tâche 2.1 DEFT 2015](https://deft.limsi.fr/2015/index.php)
  
</div>

### Rapport: [Classification classe générique de tweets](https://raw.githubusercontent.com/Lrakotoson/M_Python/master/S3/Text%20Mining/Mining/CC%20-%20Tweets%20generic/Rapport.pdf)




## Résultats

Performances des modèles retenus

|Model          |Preproc|F1       |AUC      |Accuracy |
|---------------|-------|---------|---------|---------|
|SGD            |classic|43.92    |64.18    |**58.93**|
|**SGD + SMOTE**|classic|**45.16**|65.74    |58.51    |
|MLP            |classic|41.23    |70.03    |57.26    |
|MPL + ROS      |classic|41.85    |**70.12**|57.08    |
|Camembert      |basic  |16.70    |55.66    |44.68    |
|Camembert + ROS|basic  |16.96    |57.61    |44.32    |
|Camembert      |nos_nol|15.55    |53.27    |44.90    |
|Camembert + ROS|nos_nol|15.47    |53.76    |44.68    |

## Informations
*"Les corpus DEFT 2015 ont été réalisés dans le cadre du projet uComp financé par l'ERA Net CHIST-ERA (ANR-12-CHRI-0003)."*

```bibtex
@inproceedings{Hamon2015AnalyseD,
  title={Analyse des {\'e}motions, sentiments et opinions exprim{\'e}s dans les tweets : pr{\'e}sentation et r{\'e}sultats de l'{\'e}dition 2015 du d{\'e}fi fouille de texte (DEFT)},
  author={Thierry Hamon and A. Fraisse and P. Paroubek and Pierre Zweigenbaum and Cyril Grouin},
  year={2015}
}


@inproceedings{inproceedings,
author = {Fraisse, Amel},
year = {2014},
month = {05},
pages = {},
title = {Twitter as a Comparable Corpus to build Multilingual Affective Lexicons}
}
```