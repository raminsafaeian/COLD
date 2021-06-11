# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 19:11:12 2019

@author: Ramin
"""

class Meek:
    
    def __init__(self, neigh):
        self.LUT = dict()
        self.neighbor = neigh
        self.LUT = dict()
        self.OrientAllEdges()
    def OrientAllEdges(self):
        self.LUT['OrientedEdge'] = dict()          
        for v1 in list(self.neighbor.keys()):
            for v2 in list(self.neighbor[v1]):
                self.LUT['OrientedEdge'][(v1,v2)] = list([])
    
        for v1 in list(self.neighbor.keys()):
            for v2 in list(self.neighbor[v1]):
                if len(self.LUT['OrientedEdge'][(v1,v2)]) ==0:
                    self.OrientOneEdge(v1,v2,set([v1]))  
    
    
    
    def RootOrientation(self):
        self.LUT['Root'] = dict()
        for root in list(self.neighbor.keys()):
            self.LUT['Root'][root] = dict()
            tmp = []
            for v1 in self.neighbor[root]:
                tmp += self.LUT['OrientedEdge'][(root,v1)]
            tmp =  list(dict.fromkeys(list(tmp)))
            for Edge in tmp:
                if Edge[0] in self.LUT['Root'][root]:
                    self.LUT['Root'][root][Edge[0]] |= set([Edge[1]])
                else:
                    self.LUT['Root'][root][Edge[0]]  = set([Edge[1]])
                if Edge[1] in self.LUT['Root'][root]:
                    self.LUT['Root'][root][Edge[1]] |= set([Edge[0]])
                else:
                    self.LUT['Root'][root][Edge[1]]  = set([Edge[0]])
                
                               
            
    def OrientOneEdge(self,v1,v2,SetObs):
        
        if v2 in self.neighbor[v1]:
            SetObs1 = SetObs | self.neighbor[v1]
            for v3 in self.neighbor[v2]:
                if v3 not in SetObs1:
    
                    if len(self.LUT['OrientedEdge'][(v2,v3)]) ==0:
                        self.LUT['OrientedEdge'][(v1,v2)]   += self.OrientOneEdge(v2,v3,SetObs1)
                    else:
                        self.LUT['OrientedEdge'][(v1,v2)]   += self.LUT['OrientedEdge'][(v2,v3)]
                        
                    for v4 in self.neighbor[v1]:
                        if v4 in self.neighbor[v2]:
                            if v4 in self.neighbor[v3]:
                                if len(self.LUT['OrientedEdge'][(v4,v3)]) ==0:
                                    self.LUT['OrientedEdge'][(v1,v2)]   += self.OrientOneEdge(v4,v3,SetObs1)
                                else:
                                    self.LUT['OrientedEdge'][(v1,v2)]   += self.LUT['OrientedEdge'][(v4,v3)]
    
        self.LUT['OrientedEdge'][(v1,v2)] += list([(v1,v2)])
        self.LUT['OrientedEdge'][(v1,v2)] =  list(dict.fromkeys(list(self.LUT['OrientedEdge'][(v1,v2)])))
    
        return self.LUT['OrientedEdge'][(v1,v2)]

    
    
    def MeekResults(self,Centerv,Inv,neighborv):
        Oriented = list([])
        Outv = list([])
        
        for v1 in neighborv:
            if v1 not in Inv:
                Outv += list([v1])
         
            
        # Output Edges Results that are in a clique with input edges
        for v1 in Outv:
            flag = True;
            for v2 in Inv:
                if v1 not in self.neighbor[v2]:
                    flag = False;
                else:
                    Oriented += list([(v2,v1)])
            if(flag):
                Oriented += self.LUT['OrientedEdge'][(Centerv,v1)]
    
        for v1 in self.neighbor[Centerv]:
            if v1 not in Outv:
                Oriented += self.LUT['OrientedEdge'][(v1,Centerv)]

        return list(dict.fromkeys(Oriented))       
    