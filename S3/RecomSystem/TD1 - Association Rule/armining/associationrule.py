# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 22:49:12 2017

@author: Mathieu BEN

This module provides utilities for association rules representation/manipulation
"""
from armining import itemset as its  # import for armining package

# ## Class definition
# ###################

class AssociationRule():
    """The AssociationRule class represents a model for association rule objects
    
        This class inherits from the built-in Python set class
    """
    def __init__(self, antecedent, consequent):
        """AssociationRule object constructor"""
        
        self.antecedent = its.ItemSet(antecedent)
        self.consequent = its.ItemSet(consequent)
        
    def __repr__(self):
        """Returns string to be displayed for an AssociationRule object"""
        return "{} -> {}".format(self.antecedent, self.consequent)

# ## Function definition
# ################### ## 

def associationRules(it_set) :
    """Extract all association rules derived from the provided ItemSet
        :return : list of AssociationRule objects
    """
    ar = [(its.ItemSet(ante), its.ItemSet(cons)) for ante,cons in zip(it_set.subsets(), it_set)]
    return ar


def confidence(it_set, dataset):
    """Compute the confidence of the AssociationRule in a dataset
        :param it_set: ItemSet
        :param dataset : dataset (list of ItemSet objects) on which confidence
        should be computed
        :return : confidence of the AssociationRule in the dataset
    """
    confid = [
        ante.union(cons).support(dataset) / ante.support(dataset)
        if ante.support(dataset) != 0 else 0
        for ante, cons in associationRules(it_set)
    ]
    return confid


def mineAssociationRules(dataset, minSupport = 0, minConfidence = 0):
    """Extract a list of frequent and confident association rules from a dataset
        :param dataset : dataset from which association rules should be extracted
        :param minSupport : threshold for support of association rules
        :param minConfidence : threshold for confidence of association rules
        :return : list of AssociationRule objects with at least minSupport and minConfidence
    """
    discover = list(filter(lambda x: len(x) >= 2, its.aPriori(dataset, minSupport)))
    minAR = map(
        lambda x: AssociationRule(*x[0]),
        filter(
            lambda x: x[1] >= minConfidence,
            zip(sum(map(associationRules, discover), []),
                sum(map(confidence, discover, [dataset] * len(discover)), []))))
    return list(minAR)
