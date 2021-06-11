# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 23:39:37 2019

@author: Ramin
"""
from MeekLUT import Meek
from GraphTools import nEdges
from ConnectedComponents import ConnectedComponents
from Clique import AllCliques
from Clique import MaximalCliques

def FullIdentificationHauserLUT(neigh,Config):

    Dict = {"IntSet":list([])}
    E = nEdges(neigh["graph"])
    
    while E > 0:
        
        MeekObj = Meek(neigh["graph"])
        _,v = COLD_MinMax(neigh["graph"],E,MeekObj,Config)   

        to_remove = MeekObj.MeekResults(v,neigh["dag"][v]&neigh["graph"][v],neigh["graph"][v])
        for i,j in to_remove:
            if j in neigh["graph"]:
                neigh["graph"][j] -=set([i]) 
                if neigh["graph"][j] == set():
                    del neigh["graph"][j]
            if i in neigh["graph"]:
                neigh["graph"][i] -=set([j]) 
                if neigh["graph"][i] == set():
                    del neigh["graph"][i]

        E = nEdges(neigh["graph"])
        Dict["IntSet"]   += list([v])
    
    return Dict


def COLD_MinMax(neigh,nAllEdges,MeekObj,Config):

    dicVal ={}

    ChainComp = ConnectedComponents(neigh)
    
    for CC in ChainComp:
        if Config != 'MAXIMAL':
            Clique = list(AllCliques(CC))
        else:   
            Clique =list(MaximalCliques(CC))
            for v in list(CC.keys()):
                Clique += list([list([v])])
                
        for v in list(CC.keys()):
            dicVal[v] = 0

            for c in list(Clique):
                if v in c:
                    Inv = set(CC[v]) & set(c)
                    to_remove = MeekObj.MeekResults(v,Inv,CC[v])
                    Cnt = len(to_remove)
                    
                    if(dicVal[v] <= nAllEdges - Cnt):
                        dicVal[v]  = nAllEdges - Cnt
 
    #--- Min Calculaion -----------------------
    zVal = float("inf")
    zIdx = -1
    V = list(dicVal.keys())
    V.sort()
    for v in V:
        if(zVal>=dicVal[v]):
            zIdx = v
            zVal = dicVal[v]
    return dicVal,zIdx