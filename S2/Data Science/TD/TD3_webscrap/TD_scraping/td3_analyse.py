# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 18:13:57 2017

@author: dsiadmin
"""

from pandas import DataFrame, Series
import pickle
import re
from math import *

# fonctions
def getTokens(doc):
    regex = r"""\w+"""
    tokens = [word.strip().lower() for word in re.findall(regex, doc)]
    return tokens

#classes


# prog principal
