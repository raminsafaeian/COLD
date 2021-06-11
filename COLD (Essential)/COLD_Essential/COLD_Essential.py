from itertools import combinations



def COLD_Essential(pdag,neigh):

      
    def OrientOneEdgeAddEdge(v1,v2,SetObs,pdag,neigh, forbidden=[]):
        if v1 in pdag[v2] and v2 in pdag[v1]:
            SetObs1 = SetObs | neigh[v1]
            for v3 in neigh[v2]:
                if v3 not in SetObs1:
                    if (v3,v2) not in forbidden:
                        pdag = OrientOneEdgeAddEdge(v2,v3,SetObs1,pdag,neigh,forbidden)
            
            pdag[v1] -= set([v2])
        return pdag
    
    
    
    def rule1(pdag,neigh,newOrientedEdges,forbidden,Flag):
        
        for v1,v2 in newOrientedEdges:
            pdag = OrientOneEdgeAddEdge(v1,v2,set([v1]),pdag,neigh,forbidden)
            Flag = True
                
        return pdag,Flag
       
        
    
    def rule2(pdag,neigh,Flag):
        Otiented = list([])
        for v1 in list(neigh.keys()):
            for v2 in pdag[v1]:
                if v1 not in pdag[v2]:
                    for v3 in neigh[v1].intersection(neigh[v2]):
                        if v2 in pdag[v3] and v3 in pdag[v2]:
                            if v1 in pdag[v3] and v3 not in pdag[v1]:
                                Otiented += list([(v2,v3)])
                                Flag = True
                                break;
                                
        return Otiented,Flag
       
        

    def rule3(pdag,neigh):
        Otiented = list([])
        forbidden = list([])
        for v1 in list(neigh.keys()):
            for v2 in neigh[v1]:
                if v1 in pdag[v2] and v2 in pdag[v1]:
                    candidate = neigh[v1].intersection(neigh[v2] )
                    for (v3, v4) in combinations(candidate, 2):
                        if v3 in pdag[v2] and v2 not in pdag[v3]:
                            if v4 in pdag[v2] and v2 not in pdag[v4]:
                                if v4 not in neigh[v3] and v3 not in neigh[v4]:
                                    Otiented += list([(v1,v2)])
                                    break;
  
        return forbidden,Otiented



    forbidden,Otiented = rule3(pdag,neigh)
    
    for v1 in list(neigh.keys()):
        for v2 in neigh[v1]:
            if v1 in pdag[v2] and v2 not in pdag[v1]:
                pdag[v1] |= set([v2])
                Otiented += list([(v1,v2)])
                forbidden += list([(v1,v2)])


    Flag = True

    while Flag:

        Flag = False
        pdag,Flag = rule1(pdag,neigh,Otiented,forbidden,Flag)
        Otiented,Flag = rule2(pdag,neigh,Flag)

    return pdag      



