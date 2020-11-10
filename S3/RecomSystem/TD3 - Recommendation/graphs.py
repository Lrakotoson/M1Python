import networkx as nx
import math

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'


def sorted_dict(d):
    return sorted(d.items(), key=lambda t: t[1], reverse=True)


def top_k_triplets(triplets, k):
    return sorted(triplets, key=lambda t: t[2], reverse=True)[:k]


def pagerank(g, alpha=0.9, max_iter=100):
    n_nodes = len(g)
    pagerank_dict = {node: 1. / n_nodes for node in g.nodes()}
    for iter in range(max_iter):
        pagerank_dict_new = {node: (1. - alpha) / n_nodes for node in g.nodes()}
        for node_j in g.nodes():
            for node_i in g.predecessors(node_j):
                pagerank_dict_new[node_j] += alpha * (pagerank_dict[node_i] / g.out_degree(node_i))
        pagerank_dict = pagerank_dict_new.copy()
    return pagerank_dict


def cosine_sim(v1, v2):
    dot = lambda u,v: sum(x*y for x,y in zip(u,v))
    return dot(v1,v2) / ((dot(v1,v1) **.5) * (dot(v2,v2) ** .5))


def common_grades(other_user, target_user, scores):
    target, other = [], []
    for (u,i) in scores:
        if (u,i) in scores:
            if (target_user,i) in scores and u==other_user:
                target.append(scores[(target_user,i)])
                other.append(scores[(other_user,i)])
    return other, target


def cosine_sim_all(scores, pairs):
    cos_sim_all = []
    for (other_user, target_user) in pairs:
        (v_other, v_target) = common_grades(other_user, target_user, scores)
        cos_sim_all.append((other_user, target_user, cosine_sim(v_other, v_target)))
    return cos_sim_all


def collaborative_filtering(scores, target, n_neighbors=5, similarity_fun=None, graph=None):
    target_user, target_item = target
    if similarity_fun is None:
        if graph is not None:
            similarity_fun = nx.adamic_adar_index
        else:
            similarity_fun = cosine_sim_all
    if graph is not None:
        list_neighbors = [n for n in graph.nodes() if (n, target_item) in scores.keys()]
    else:
        list_neighbors = [user for (user, item) in scores.keys() if item == target_item and user != target_user]

    triplets = []
    target_score = 0.
    if len(list_neighbors):
        triplets = similarity_fun(graph if graph is not None else scores, [(n, target_user) for n in list_neighbors])

    sum_sim = 0
    for v,_,sim in top_k_triplets(triplets, n_neighbors):
        rv = [scores[(u,i)] for (u,i) in scores if u==v]
        target_score += sim * (scores[(v, target_item)] - sum(rv)/len(rv))
        sum_sim += sim
        target_score /= sum_sim if sum_sim != 0 else 1

    target_user_scores = [v for k, v in scores.items() if k[0] == target_user]
    if len(target_user_scores) == 0:
        target_score += sum(scores.values()) / len(scores)
    else:
        target_score += sum(target_user_scores) / len(target_user_scores)
    return target_score


def user_based_collaborative_filtering(scores, target, n_neighbors=5, similarity_fun=None, graph=None):
    return collaborative_filtering(scores, target, n_neighbors, similarity_fun, graph)


def item_based_collaborative_filtering(scores, target, n_neighbors=5, similarity_fun=None, graph=None):
    scores = {k[::-1]:note for k,note in scores.items()}
    target = target[::-1]
    return collaborative_filtering(scores, target, n_neighbors, similarity_fun, graph)


def generic_common_neighbors(g, u, v):
    list_common_neighbors = []
    for w in g.nodes():
        if (g.has_edge(u, w) and g.has_edge(w, v)) or (g.has_edge(v, w) and g.has_edge(w, u)):
            list_common_neighbors.append(w)
    return list_common_neighbors


def generic_adamic_adar(g, ebunch=None):
    if ebunch is None:
        ebunch = nx.non_edges(g)

    def predict(u, v):
        return sum([1. / math.log(g.degree(w)) for w in generic_common_neighbors(g, u, v)])

    return [(u, v, predict(u, v)) for u, v in ebunch]
