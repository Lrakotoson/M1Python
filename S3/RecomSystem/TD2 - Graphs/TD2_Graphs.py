
# coding: utf-8

__author__: "Loic Rakotoson"

# # Fouille de graphes

# In[1]:


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
from itertools import combinations


# In[2]:


# get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


def sorted_dict(d):
    return sorted(d.items(), key=lambda t: t[1], reverse=True)

def top_k_triplets(triplets, k):
    return sorted(triplets, key=lambda t: t[2], reverse=True)[:k]

def generic_adamic_adar(g, ebunch=None):
    if ebunch is None:
        ebunch = nx.non_edges(g) # connexion non existante dans le graphe

    def predict(u, v):
        return sum([1. / math.log(g.degree(w)) for w in generic_common_neighbors(g, u, v)])

    return [(u, v, predict(u, v)) for u, v in ebunch]


# ## Graphes non orientés
# Stockez dans une variable le graphe non orienté contenu dans le fichier `data/graph1.txt` (le format de ce fichier est appelé Edge List dans la nomenclature NetworkX).  
# Affichez la liste de ses noeuds et la liste de ses liens.

# In[4]:


with open('data/graph1.txt') as f:
    data_1 = list(map(lambda x: x.split(), f.readlines()))


# In[5]:
print('\n[+] Exercice 1')

print(f'nodes :{set(sum(data_1, []))}\nedges: {data_1}')


# In[6]:


graph_1 = nx.Graph()
graph_1.add_edges_from(data_1)
nx.draw(graph_1)


# Affichez, pour chacun des noeuds de ce graphe, son degré et la liste de ses voisins dans le graphe

# In[7]:
print('\n[+] Exercice 2')

nodes = dict()
for node1, node2 in data_1:
    nodes[node1] = nodes.get(node1,[]) + [node2]
    nodes[node2] = nodes.get(node2,[]) + [node1]
print({node: (len(k),k) for node,k in nodes.items()})


# Affichez, pour chaque paire de noeuds du graphe, un chemin menant d'un noeud à l'autre dans le graphe, s'il en existe.

# In[8]:
print('\n[+] Exercice 3')

for x in combinations(graph_1.nodes(), 2):
    print(f"{x}: {nx.shortest_path(graph_1, *x)}")


# ## Graphes orientés
# Effectuez les mêmes manipulations pour `data/graphM2.txt`

# In[9]:


graph_2 = nx.readwrite.edgelist.read_edgelist("data/graphM2.txt", create_using=nx.DiGraph())
nx.draw(graph_2)


# In[10]:
print('\n[+] Exercice 4')

print(f'nodes: {graph_2.nodes}\nedges: {graph_2.edges}')


# In[11]:


print({x[0]: (x[1], list(graph_2.neighbors(x[0]))) for x in graph_2.degree})


# Comment obtenir les degrés entrant et sortant d'un noeud ?

# In[12]:


for node in graph_2.nodes:
    print(f"{node:<21} |in: {graph_2.in_degree(node)}, out: {graph_2.out_degree(node)}")


# Implémentez une fonction `pagerank` qui calcule, pour un graphe et une valeur de $\alpha$ donnés, l'indice en question.  
# Quels sont les noeuds les plus influents du graphe créé à la manipulation précédente ?

# In[13]:


def pagerank(graph, alpha, iterations):
    """
    :graph: networkx graph
    :alpha: float
    :iterations: int
    :return: list of tuples (node, pagerank index)
    """
    n = len(graph.nodes)
    r_t = dict(zip(graph.nodes, [1/n]*n))
    for i in range(iterations):
        r_iter = dict(zip(graph.nodes, [(1-alpha)/n]*n))
        for j in graph.nodes:
            for i in graph.predecessors(j):
                r_iter[j] += r_t[i]*alpha / graph.out_degree(i)
        r_t = r_iter.copy()
    return sorted_dict(r_t)


# In[14]:
print('\n[+] Exercice 5')

print(pagerank(graph_2, .5, 10)[:5])


# In[15]:


print(sorted_dict(nx.pagerank(graph_2, .5))[:5])


# Repérez les autres fonctions d'analyse des liens proposées par `NetworkX` (algortihme HITS) et affichez les noeuds du graphe par ordre décroissant d'importance selon chacun de ces critère.

# In[16]:
print('\n[+] Exercice 6')

print(list(map(sorted_dict, nx.hits(graph_2))))


# ## Visualisation des graphes
# Tracez, tour à tour, les deux graphes manipulés ci-dessus. Pour le graphe orienté, vous ferez en sorte que la taille des noeuds du graphe soit proportionnelle à leur importance dans le graphe telle qu'évaluée par la fonction `pagerank`.

# In[17]:


nx.draw_networkx(graph_1)


# In[18]:


plt.rcParams["figure.figsize"] = (20, 15)
nx.draw_networkx(graph_2, node_size = np.array(list(nx.pagerank(graph_2, .5).values()))*10**5)


# ## Prédiction de liens
# Évaluez la similarité, au sens de l'indice Adamic/Adar, entre toutes les paires de noeuds non adjacents du graphe non orienté `graph_1`

# In[19]:
print('\n[+] Exercice 8')

print(top_k_triplets(nx.adamic_adar_index(graph_1), 5))


# Implémentez la fonction `generic_common_neighbors` utilisée par `generic_adamic_adar`.

# In[20]:


def generic_common_neighbors(g, u, v):
    """
    Intersection of u's neighbors and v's neighbors
    :g: networkx graph
    :u, v: str, nodes
    :return: list, of common neighbors
    """
    common = set(g.neighbors(u)).intersection(g.neighbors(v))
    return list(common)


# Pour chacun des deux graphes, quels sont les trois liens manquants les plus "prévisibles" ?

# In[21]:
print('\n[+] Exercice 9')

print(top_k_triplets(generic_adamic_adar(graph_1), 3))


# In[22]:


print(top_k_triplets(generic_adamic_adar(graph_2), 3))

