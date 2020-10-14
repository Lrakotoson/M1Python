# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 19:18:23 2017

@author: Mathieu BEN

This module provides utilities for itemsets reresentation/manipulation
and association rules mining using the Apriori algorithm
"""

### Classical imports
""
from collections import Iterable


### Class definition
""
class ItemSet(set):
    """The ItemSet class represents a model for itemset objects
    
        This class inherits from the built-in Python set class
    """
    
    def __init__(self, items=None):
        """ItemSet object constructor
            :param items : singleton string item or iterable collection of items
            to be put in the ItemSet
        """
        if(isinstance(items, str)):
            super(ItemSet, self).__init__([items])
        elif(isinstance(items, Iterable)):
            super(ItemSet, self).__init__([str(x) for x in items])
        else:
            super(ItemSet, self).__init__([str(items)])
    
    def __repr__(self):
        return "{}".format(set(self))
    
    def union(self, itemset2):
        return ItemSet(super(ItemSet, self).union(itemset2))
             
    def support(self, dataset):
        """Computes the ItemSet support relative to a dataset
            :param dataset : list of itemsets representing the working dataset
            :return : the value of the ItemSet support
        """
        
        count = 0
        for iset in dataset :
            if self.issubset(iset) :
                count +=1   
        return count
    
    def subsets(self):
        """Extracts all subsets of size k-1 of the current ItemSet of size k
            :return : list subsets (ItemSet object) of size k-1        
        """
        ret = []
        for item in self:
            subset = {it for it in self if it != item}
            if len(subset) > 0:
                ret.append(subset)
        return ret


# ## Function definition
# ################### ## 

def readItemSets(filename):
    """Reads a dataset (list of itemsets) from a text file
        :param filename: name of the text file containing the dataset
        :return : list of ItemSet objects
    """
        
    isList = []
    try:
        with open(filename, 'r') as f:
            for line in f.readlines():
                isList.append(ItemSet(line.strip().split(',')))
                
    except IOError as e:
        print("ERROR: can't read file {} ({})".format(filename, e))
    
    return isList


# +
from itertools import chain

def allSingletons(dataset, minSupport = 0):
    """Extracts all singleton itemsets from a dataset
        
        If minSupport is given, extracts all singleton ItemSet from the dataset
        that have support at least equal to minSupport
        
        :param dataset : dataset (list of ItemSet objects) from wich the
        singleton itemsets are extracted
        :param minSupport (optional) : if given, defines the minimum support for  
        a singleton itemset to be extracted
        :return : list of singleton ItemSet objects
    """
    singletons = list(map(ItemSet, set(chain(*dataset))))
    return [
        item for item, support in zip(
            singletons, map(lambda its: its.support(dataset), singletons))
        if support >= minSupport
    ]


# -

def candidateGeneration(isList_k):
    """Generates a list of canditate itemsets of size k+1 from the list of
    minSupport-frequent itemsets of size k
        :param isList_k : list of ItemSet objects of size k given by the previous
        iteration of Apriori
        :return : list of candidates ItemSet objects of size k+1 for the
        Apriori run
    """
    k = len(isList_k[0])
    candidats = [l1.union(l2) for l1 in isList_k for l2 in isList_k if len(
        l1.union(l2)) == k+1]
    listcandidats = {tuple(itset) for itset in candidats if all(
        x in isList_k for x in itset.subsets())}
    
    return list(map(ItemSet, listcandidats))


def aPriori(dataset, minSupport = 0) :
    """Returns the list of minSupport-frequent ItemSets in a dataset
        :param dataset : dataset from which ItemSets should be extracted
        :param minSupport : threshold for support
        :return : list of minSupport-frequent ItemSets in the dataset
    """
    union = list()
    lk = allSingletons(dataset, minSupport)
    while len(lk) > 0:
        cand = candidateGeneration(lk)
        union += lk
        lk = [itemset for itemset, support in zip(
            cand, map(lambda its: its.support(dataset), cand))
            if support >= minSupport]
    return union
