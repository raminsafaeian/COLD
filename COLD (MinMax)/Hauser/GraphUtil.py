# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 21:29:26 2019

@author: Ramin
"""
import networkx as nx

def Neighbors(G,v):
    return list(dict.fromkeys(list(nx.all_neighbors(G,v))))
    
def ChainComponent(G):
    O=list([])
    O1=list(G.to_undirected().subgraph(c) for c in nx.connected_components(G.to_undirected()))
    for i in range(len(O1)):
        if (len(list(O1[i])) > 1):
            O.append(nx.to_directed(O1[i]))  
    return O
                
    
class Essential:
    def __init__(self,DAG):
        self.MEC = list([])
        MEC = DAG.copy()
        self.V = []
        self.nUndirected = MEC.number_of_edges()
        V_Edges = Extract_V_Structures(DAG)
#        print(V_Edges)
        if(len(V_Edges) != 0 ):
            print("V Structure Detected")

        for i,j in list(DAG.edges):
            if((i,j) not in V_Edges):
                MEC.add_edge(j,i)
        
        MeekRule(MEC)
        for i,j in list((i,j) for i,j in MEC.edges):
            if(not MEC.has_edge(j,i)):
                MEC.remove_edge(i,j)
        ChainCmp = ChainComponent(MEC)
        self.MEC = ChainCmp
        
        
    def Intervene(self,DAG,V):
        for k in range(len(self.MEC)):
            if(self.MEC[k].has_node(V)):
                ChainCmp = self.MEC[k].copy()
                break
            
        self.V.append(V)
        for i,j in list((i,j) for i,j in list(ChainCmp.edges) if (i==V or j == V)):
            ChainCmp.remove_edge(i,j)
        for i,j in list((i,j) for i,j in list(DAG.edges) if (i==V or j == V)):
            ChainCmp.add_edge(i,j)    
        MeekRule(ChainCmp)
        for i,j in list((i,j) for i,j in ChainCmp.edges):
            if(not ChainCmp.has_edge(j,i)):
                ChainCmp.remove_edge(i,j)
        ChainCmp = ChainComponent(ChainCmp)
        MEC = self.MEC.copy()
        MEC.remove(self.MEC[k])
        MEC = MEC + ChainCmp
        return MEC, self.CountUndirected(MEC)
        
    def CountUndirected(self,MEC):
        nUndirected = 0
        for k in range(len(MEC)):
            for i,j in list((i,j) for i,j in list(MEC[k].edges)):
                if(MEC[k].has_edge(i,j) and MEC[k].has_edge(j,i) ):
                    nUndirected = nUndirected + 1
        return nUndirected/2
    
    def Nodes(self):
        Node = list([])
        for M in self.MEC:
            Node = Node+list(M.nodes())
        return Node
        
        

######################################################################################################
#################### Meek Rules ######################################################################
def MeekRule(G):  
   Flag = True
   while(Flag):
       Flag = False
       Flag,G = MeekRule1(G,Flag)
       Flag,G = MeekRule2(G,Flag)
       Flag,G = MeekRule34(G,Flag)

   
def MeekRule1(G,F):
   V=list(G.nodes)
   for v1 in V: 
       for v2 in list(v2 for v2 in Neighbors(G,v1) if G.has_edge(v2,v1) and not(G.has_edge(v1,v2)) ):
           for v3 in list(v3 for v3 in Neighbors(G,v1) if v3 not in Neighbors(G,v2) ):
               if(G.has_edge(v1,v3) and G.has_edge(v3,v1)):
                   F = True
#                   print("Graph is Changed by Meek Rule 1")
                   G.remove_edge(v3,v1)
   return (F,G)


def MeekRule2(G,F):
   V=list(G.nodes)
   for v1 in V:   
       for v2 in Neighbors(G,v1):
           for v3 in list(v3 for v3 in Neighbors(G,v2) if v3 in Neighbors(G,v1)):
               if(G.has_edge(v2,v3) and G.has_edge(v3,v2)):
                   if(G.has_edge(v3,v1) and G.has_edge(v1,v2)) and not (G.has_edge(v1,v3) or G.has_edge(v2,v1)):
                       F = True
                       G.remove_edge(v2,v3)
                   if(G.has_edge(v1,v3) and G.has_edge(v2,v1)) and not (G.has_edge(v3,v1) or G.has_edge(v1,v2)):
                       F = True
                       G.remove_edge(v3,v2)               
   return (F,G)
               
def MeekRule34(G,F):
   V=list(G.nodes)
   for v1 in V:   
       for v2 in Neighbors(G,v1):
           for v3 in list(v3 for v3 in Neighbors(G,v2) if v3 in Neighbors(G,v1)):
               for v4 in list(v4 for v4 in Neighbors(G,v2) if v4 in Neighbors(G,v3) and (v4 != v1)):
                       if(G.has_edge(v1,v3) and G.has_edge(v3,v1)):
                           if(G.has_edge(v4,v3) and G.has_edge(v3,v4)):
                               if(G.has_edge(v2,v3) and G.has_edge(v3,v2)):
                                   if(G.has_edge(v1,v2) and not G.has_edge(v2,v1)):
                                       if(not G.has_edge(v1,v4) and not G.has_edge(v4,v1)):
                                           if(G.has_edge(v4,v2) and not G.has_edge(v2,v4)):
                                               if(G.has_edge(v4,v3) and G.has_edge(v3,v4)):
                                                   F = True
                                                   G.remove_edge(v2,v3)
                                           elif(G.has_edge(v2,v4) and not G.has_edge(v4,v2)):
                                               F = True
                                               G.remove_edge(v4,v3)
   
   return (F,G)
            

######################################################################################################
######################################################################################################
   

def Extract_V_Structures(G):
   V=list(G.nodes)
   V_Edges = list([])
   for v1 in V: 
       for v2 in list(v2 for v2 in Neighbors(G,v1) if G.has_edge(v2,v1) and not(G.has_edge(v1,v2)) ):
           for v3 in list(v3 for v3 in Neighbors(G,v1) if v3 not in Neighbors(G,v2) and v3 <v2):
               if G.has_edge(v3,v1):
                   V_Edges.append((v3,v1))
                   V_Edges.append((v2,v1))
   return V_Edges


