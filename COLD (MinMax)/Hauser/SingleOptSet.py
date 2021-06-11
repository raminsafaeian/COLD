# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 23:39:37 2019

@author: Ramin
"""
import networkx as nx
from Hauser.GraphUtil import Neighbors
from Hauser.GraphUtil import MeekRule



def SingleOptSet(essential,G,MAXnIntervention):
    
    
    Dict = {}
    Dict["IntSet"]   = list([])
    e = essential.CountUndirected(essential.MEC)
    if len(essential.MEC) >0:
        while(essential.nUndirected > 0) and  MAXnIntervention > len(Dict["IntSet"]):

            v = SingleOpt(essential.MEC,essential.nUndirected)   
            essential.MEC, essential.nUndirected = essential.Intervene(G,v)
            Dict["IntSet"]   += list([v])
            

    return Dict


def SingleOpt(MEC,nAllEdges):

    dicVal ={}

    for k in range(len(MEC)):
        Clique = list(nx.algorithms.clique.enumerate_all_cliques(MEC[k].to_undirected()))

        for v in MEC[k].nodes():
            dicVal[v] = 0

            N =  Neighbors(MEC[k],v)
            for c in Clique:
                MEC_cpy = MEC[k].copy()
                if v in c:
                    for v1 in N:
                        if v1 in c:
                            MEC_cpy.remove_edge(v,v1)
                        else:
                            MEC_cpy.remove_edge(v1,v)
                    MeekRule(MEC_cpy)
                    to_remove = [(v,u) for v,u in MEC_cpy.edges() if not MEC_cpy.has_edge(u,v)]

                    if(dicVal[v] <= nAllEdges - len(to_remove)):
                        dicVal[v]  = nAllEdges - len(to_remove)

    #--- MAX Calculaion -----------------------
    zVal = float("inf")
    zIdx = -1
    V = list(dicVal.keys())
    V.sort()
    for v in V:
        if(zVal>=dicVal[v]):
            zIdx = v
            zVal = dicVal[v]

    return zIdx