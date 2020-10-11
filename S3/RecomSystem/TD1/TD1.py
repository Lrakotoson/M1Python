# coding: utf-8

__author__: "Loïc Rakotoson"

# # Fouille d’itemsets et de règles d’association

# In[1]:


from armining import itemset as its, associationrule as ar


# ## Prise en main du squelette Python
# ### Manipulation 1.
# Construire un `ItemSet` ne contenant qu’un élément. Ajouter à cet `ItemSet` des éléments, un à un, à l’aide de la méthode `add` (héritée de la classe set) , puis afficher le contenu de l’ `ItemSet` ainsi que sa cardinalité.

# In[2]:
print('\nManipulation 1')

its_0 = its.ItemSet("Madara")
for uchiha in ["Sasuke", "Itachi", "Shisui"]:
    its_0.add(uchiha)
    
print(f'Itemset: {its_0}\nCardinalité: {len(its_0)}')


# ### Manupulation 2.
# Importez, à l’aide de la fonction `readItemSets` du module `itemset`, les données contenues dans le fichier `"data/beer_diapers.txt"`.

# In[3]:
print('\nManipulation 2')

dataset = its.readItemSets("data/beer_diapers.txt")
print(dataset)


# ### Manipulation 3.
# Calculez, à l’aide de la méthode adaptée, le support de l’`ItemSet` créé à la Manipulation 1 dans le jeu de données de la Manipulation 2. Répétez l’expérience avec un `ItemSet` plus adapté aux données du fichier `"data/beer_diapers.txt"`.

# In[4]:
print('\nManipulation 3')

print(its_0.support(dataset))
its_1 = its.ItemSet(('Bread', 'Beer'))
print(its_1.support(dataset))


# ### Manipulation 4.
# Observez, pour quelques `ItemSet` de votre création, que la règle vue en cours selon laquelle si un `ItemSet` $I_1$ est inclus dans un autre `ItemSet` $I_2$ , alors on a support($I_1$) ≥ support($I_2$).

# In[5]:
print('\nManipulation 4')

its_2 = its_1
its_2.add('Coke')

print(its_1.support(dataset) >= its_2.support(dataset))


# ### Manipulation 5.
# 
# Implémentez la méthode `associationRules` de la classe `AssociationRule` qui renvoie une liste de toutes les règles d’associations dérivées de l’`Itemset` fourni (on ne considèrera que les règles d’association dont le conséquent est de cardinalité 1 et l’antécédent de cardinalité $k−1$ où $k$ est la cardinalité de l’`ItemSet`).

# In[6]:
print('\nManipulation 5')

print(ar.associationRules(its_2))


# ### Manipulation 6.
# Pour un `ItemSet` de votre choix (de cardinalité au moins égale à 2), générez l’ensemble des règles d’association dérivées (à l’aide de la méthode `associationRules` implémentée à la question précédente) et calculez la confiance de chacune d’entre elles pour le jeu de données de la Manipulation 2

# In[7]:
print('\nManipulation 6')

its_3 = its.ItemSet(['Beer', 'Diapers', 'Milk'])
print(ar.confidence(its_3, dataset))


# ## Implémentations des fonctions de fouille des règles d’association
# ### Manipulation 7.
# Implémenter la fonction `allSingletons` prenant en premier argument un dataset et en second argument optionnel un seuil de support minimum, et qui renvoie une liste de tous les items contenus dans le dataset (sous forme d’une liste d’`ItemSet` singletons) ayant un support au moins égal au seuil fourni en second argument. Si ce second argument n’est pas fourni, tous les singletons sont renvoyés quel que soit leur support.

# In[8]:
print('\nManipulation 7')

print(its.allSingletons(dataset, 2))


# ### Manipulation 8.
# Implémentez la fonction `candidateGeneration` qui prend en entrée la liste $L_k$ des `ItemSet` de taille $k$ et retourne la liste des `ItemSet` candidats de taille $k + 1$ tels que tous leurs sous-ItemSet de taille $k$ sont dans $L_k$. Notez pour cela qu’un `ItemSet` de l’ensemble de sortie ne peut être composé que comme l’union de deux ItemSet de $L_k$.  
# Vérifiez sur la liste suivante que la valeur de retour de la fonction précédente est correcte : `[{'Beer', 'Diapers'}, {'Beer', 'Coke'}, {'Coke', 'Diapers'}, {'Beer', 'Milk'}]`

# In[9]:
print('\nManipulation 8')

list_k = list(map(its.ItemSet, [{'Beer', 'Diapers'}, {
              'Beer', 'Coke'}, {'Coke', 'Diapers'}, {'Beer', 'Milk'}]))
print(its.candidateGeneration(list_k))


# ### Manipulation 9.
# Implémentez l’algorithme A priori de découverte d’`ItemSet` fréquents dans la fonction `aPriori` du module `itemset`. Cette fonction fera appel à celles développées lors des manipulations 7 et 8.

# In[10]:
print('\nManipulation 9')

print(its.aPriori(list_k, 1))


# ### Manipulation 10.
# Implémentez la fonction `mineAssociationRules` du module `assoiationrule` qui appelle `aPriori`, puis génère, pour chaque `ItemSet` fréquent de taille au moins égale à 2, l’ensemble des règles d’association dérivées. Pour chaque règle dérivée, on vérifiera qu’elle remplit la condition de confiance et, si c’est le cas, on la retiendra comme règle valable.
# 
# Vérifier le bon fonctionnement de cette fonction en prenant un support minimum de 3 et une confiance minimum de 0.9.

# In[11]:


list_k = list(
    map(its.ItemSet, [{'Bread', 'Milk'}, {'Bread', 'Diapers', 'Beer', 'Eggs'},
                      {'Milk', 'Diapers', 'Beer', 'Coke'},
                      {'Bread', 'Milk', 'Diapers', 'Beer'},
                      {'Bread', 'Milk', 'Diapers', 'Coke'}]))


# In[12]:
print('\nManipulation 10')

print(ar.mineAssociationRules(list_k, 3, .9))

