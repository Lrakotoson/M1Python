# coding: utf-8

__author__ = 'Lrakotoson'
__maintainer__ = 'Loïc Rakotoson'
__email__ = 'contact@loicrakotoson.com'
__status__ = 'planning'
__all__ = ['Data']

import pandas as pd

class Data():
    """
    Classe qui traite et filtre les données
    """
    
    def __init__(self, budget, quartier):
        """
        budget, quartier: Dataframe pandas
        brut_bd, brut_qt: réserves intactes
        bd, qt: bases actives
        proj, etat: bases calculées
        """
        self.brut_bd = budget
        self.brut_qt = quartier
        self.bd = budget
        self.qt = quartier
        self.proj = self.projQuartier()
        self.etat = self.etatProjet()
    
    def reset(self):
        """
        Réinitialise les bases actives
        """
        self.bd = self.brut_bd
        self.qt = self.brut_qt
    

    def projQuartier(self):
        """
        Nombre de projet par quartier et par état de projet
        :return: DataFrame
        """
        colormap = {
            'Réalisé': '#2ecc71',
            'Non réalisable': '#c0392b',
            "A l'étude": '#f0932b',
            'En cours': '#f1c40f'
        }
        
        def minQuartier(quartiers):
            """
            Le nom de quartier le plus court
            quartiers: valeur de DataFrame
            :return: str ou quartiers
            """
            if isinstance(quartiers, str):
                quartiers = quartiers.split(' - ')
                q_min = min(quartiers, key = len).strip()
                return q_min
        
        if self.bd.shape[0] == 0:
            return pd.DataFrame()
        
        bd_frame = self.bd.copy(deep=True)
        bd_frame.b_quartier = bd_frame.b_quartier.apply(minQuartier)

        dico = bd_frame.groupby(['b_quartier', 'b_realise'
                                ]).size().unstack().fillna(0).stack().to_dict()

        bf_proj = pd.DataFrame({
            'x': list(dico.keys()),
            'counts': list(dico.values()),
            'legends': [legend[1] for legend in list(dico.keys())],
            'quartiers': [quartier[0] for quartier in list(dico.keys())],
            'color': [
                colormap[legend]
                for legend in [legend[1] for legend in list(dico.keys())]
            ]
        })

        bf_proj.legends = pd.Categorical(
            bf_proj['legends'], ['Réalisé', "A l'étude", 'En cours', 'Non réalisable'])
        bf_proj = bf_proj.sort_values('legends')
        
        return bf_proj.copy(deep = True)
        

    def etatProjet(self):
        """
        Etat des projets par année
        :return: DataFrame
        """
        if self.bd.shape[0] == 0:
            return pd.DataFrame()
        
        bd_frame = self.bd.copy(deep = True)
        bd_frame = bd_frame[bd_frame.b_year.notna()]
        bd_frame.b_year = bd_frame.b_year.astype('Int64').astype(str)
        
        bf_etat = bd_frame.groupby(['b_year', 'b_realise'
                                    ]).size().unstack().fillna(0).reset_index()
        bf_etat = bf_etat.rename(
            columns = {
                "Réalisé": "Realise",
                "A l'étude": "Etude",
                'En cours': 'En_cours',
                'Non réalisable': 'Non_realisable'
            })
        return bf_etat.copy(deep = True)

    
    def chooseYear(self, rangeYear):
        """
        Filtre les années dans le budget
        rangeYear: liste d'index
        """
        year = [2016, 2017, 2018, 2019]
        if len(rangeYear) == 0:
            self.bd = self.brut_bd
        else:
            selectYear = [year[i] for i in rangeYear]
            self.bd = self.brut_bd[self.brut_bd.b_year.isin(selectYear)]
    
    def chooseRealise(self, rangeRealise):
        """
        Filtre les états des projets dans le budget
        rangeRealise: liste d'index
        """
        realise = ['Réalisé', 'Non réalisable', "A l'étude", 'En cours']
        if len(rangeRealise) > 0:
            selectRealise = [realise[i] for i in rangeRealise]
            self.bd = self.bd[self.bd.b_realise.isin(selectRealise)]
    
    def chooseQuartier(self, rangeQuartier):
        """
        Filtre les quartiers dans le budget et les quartiers
        rangeQuartier: liste d'index
        """
        quartier = list(range(1,13))
        if len(rangeQuartier) > 0:
            selectQuartier = [quartier[i] for i in rangeQuartier]
            self.bd = self.bd[self.bd.b_q_id.isin(selectQuartier)]
            self.qt = self.brut_qt[self.brut_qt.q_id.isin(selectQuartier)]
        else:
            self.qt = self.brut_qt
    
    def query(self, rangeYear, rangeRealise, rangeQuartier):
        """
        Filtre les bases actives
        range*: listes d'index Year, Realise, Quartier
        """
        self.chooseYear(rangeYear)
        self.chooseRealise(rangeRealise)
        self.chooseQuartier(rangeQuartier)
        self.proj = self.projQuartier()
        self.etat = self.etatProjet()