from collections import Iterable


### Class definition
####################

class ItemSet(set):
    """The ItemSet class represents a model for itemset objects

        This class inherits from the built-in Python set class
    """

    def __init__(self, items=None):
        """ItemSet object constructor
            :param items : singleton string item or iterable collection of items
            to be put in the ItemSet
        """
        if (items is None):
            super(ItemSet, self).__init__()
        elif (isinstance(items, str)):
            super(ItemSet, self).__init__([items])
        elif (isinstance(items, Iterable)):
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
        for iset in dataset:
            if self.issubset(iset):
                count += 1
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

    def associationRules(self):
        """Extract all association rules derived from the current ItemSet
            :return : list of AssociationRule objects
        """
        ret = []
        for item in self:
            antecedent = ItemSet([it for it in self if it != item])
            consequent = ItemSet(item)
            myAr = AssociationRule(antecedent, consequent)
            if len(antecedent) > 0:
                ret.append(myAr)
        return ret


### Function definition
#################### ##

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


def allSingletons(dataset, minSupport=1):
    """Extracts all singleton itemsets from a dataset

        If minSupport is given, extracts all singleton ItemSet from the dataset
        that have support at least equal to minSupport

        :param dataset : dataset (list of ItemSet objects) from wich the
        singleton itemsets are extracted
        :param minSupport (optional) : if given, defines the minimum support for
        a singleton itemset to be extracted
        :return : list of singleton ItemSet objects
    """
    ret = []
    for itSet in dataset:
        for item in itSet:
            candidate = ItemSet(item)
            if candidate not in ret and candidate.support(dataset) >= minSupport:
                ret.append(candidate)

    return ret


def candidateGeneration(isList_k):
    """Generates a list of canditate itemsets of size k+1 from the list of
    minSupport-frequent itemsets of size k
        :param isList_k : list of ItemSet objects of size k given by the previous
        iteration of Apriori
        :return : list of candidates ItemSet objects of size k+1 for the
        Apriori run
    """
    k = len(isList_k[0])
    isList_k_plus_1 = []
    for is1 in isList_k:
        for is2 in isList_k:
            new_is = is1.union(is2)
            if len(new_is) == k + 1 and new_is not in isList_k_plus_1:
                all_in_Lk = True
                for iset in new_is.subsets():
                    if not iset in isList_k:
                        all_in_Lk = False
                        break
                if all_in_Lk:
                    isList_k_plus_1.append(new_is)
    return isList_k_plus_1


def aPriori(dataset, minSupport):
    """Returns the list of minSupport-frequent ItemSets in a dataset
        :param dataset : dataset from which ItemSets should be extracted
        :param minSupport : threshold for support
        :return : list of minSupport-frequent ItemSets in the dataset
    """
    unionLk = []
    Lk = allSingletons(dataset, minSupport)
    while len(Lk) > 0:
        Ckplus1 = candidateGeneration(Lk)
        unionLk.extend(Lk)
        Lk = [iset for iset in Ckplus1 if iset.support(dataset) >= minSupport]
    return unionLk


### Class definition
####################

class AssociationRule():
    """The AssociationRule class represents a model for association rule objects

        This class inherits from the built-in Python set class
    """

    def __init__(self, antecedent, consequent):
        """AssociationRule object constructor"""

        self.antecedent = ItemSet(antecedent)
        self.consequent = ItemSet(consequent)

    def __repr__(self):
        """Returns string to be displayed for an AssociationRule object"""
        return "{} -> {}".format(self.antecedent, self.consequent)

    def confidence(self, dataset):
        """Compute the confidence of the AssociationRule in a dataset
            :param dataset : dataset (list of ItemSet objects) on which confidence
            should be computed
            :return : confidence of the AssociationRule in the dataset
        """
        if self.antecedent.support(dataset) == 0 or self.consequent.support(dataset) == 0:
            return 0
        return self.antecedent.union(self.consequent).support(dataset) / self.antecedent.support(dataset)


### Function definition
#################### ##

def mineAssociationRules(dataset, minSupport, minConfidence):
    """Extract a list of frequent and confident association rules from a dataset
        :param dataset : dataset from which association rules should be extracted
        :param minSupport : threshold for support of association rules
        :param minConfidence : threshold for confidence of association rules
        :return : list of AssociationRule objects with at least minSupport and minConfidence
    """
    arList = []
    isetList = aPriori(dataset, minSupport)
    for iset in isetList:
        for ar in iset.associationRules():
            if ar.confidence(dataset) >= minConfidence:
                arList.append(ar)
    return arList