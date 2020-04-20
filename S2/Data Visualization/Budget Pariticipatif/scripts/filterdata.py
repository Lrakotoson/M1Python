class Data():
    """
    Classe qui traite et filtre les données
    """
    
    def __init__(self, budget, quartier):
        """
        budget, quartier: Dataframe pandas
        brut_bd, brut_qt: réserves intactes
        bd, qt: bases actives
        """
        self.brut_bd = budget
        self.brut_qt = quartier
        self.bd = budget
        self.qt = quartier
    
    def reset(self):
        self.bd = self.brut_bd
        self.qt = self.brut_qt
    
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