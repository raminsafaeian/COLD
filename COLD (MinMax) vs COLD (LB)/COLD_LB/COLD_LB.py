from MeekLUT import Meek
from GraphTools import nEdges
from ConnectedComponents import ConnectedComponents
from Clique import MaximalCliques

def FullIdentificationLowerBound(neigh,MAXnIntervention):

    Dict = {"IntSet":list([])}
    E = nEdges(neigh["graph"])
    
    while E > 0:
        
        MeekObj = Meek(neigh["graph"])
        _,v = LowerBoundOfOrientationNewMethod(neigh["graph"])   
        
        if(MAXnIntervention == len(Dict["IntSet"])):
            break;
            
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

def LowerBoundOfOrientationNewMethod(neigh):


    CliqueSet = dict()
    LowerBoundOriented = dict()
    LowerBoundClique = dict()
    
    ChainComp = ConnectedComponents(neigh)

    for CC in ChainComp:
        MeekObj = Meek(CC)
        CliqueSet =list(MaximalCliques(CC))

        for v in list(CC.keys()):
            LowerBoundOriented[v] = float("inf")

            for c in list(CliqueSet):
                if v in c:
                    c = c.copy()
                    c.remove(v)
                    Len = 0
                    Cnt = 0
                    
                    ##############################################################################
                    # All Edges Are Input
                    oriented1 = set()
                    for v1 in MeekObj.neighbor[v]:
                        if v1 not in c:
                            oriented1  |= set(MeekObj.LUT['OrientedEdge'][(v,v1)])
                        else:
                            oriented1  |= set(MeekObj.LUT['OrientedEdge'][(v1,v)])
                    
                    oriented1 = list(dict.fromkeys(oriented1))
                    Len = len(oriented1)
                    ##############################################################################
                    
                    ##############################################################################
                    # One Input and One Output
                    oriented2 = set()
                    for v1 in MeekObj.neighbor[v]:
                        if v1 not in c:
                            oriented2  |= set(MeekObj.LUT['OrientedEdge'][(v,v1)])
                    
                    
                    TableInput = list([])
                    TableOutput =  list([])
                    for v1 in c:
                        orientedtmp = set()
                        for v2 in list(set(neigh[v]&neigh[v1]) - set(c)):
                            orientedtmp  |= set((v1,v2))
                        TableInput.append(len((set(MeekObj.LUT['OrientedEdge'][(v1,v)]) | orientedtmp)  - oriented2))

                    for v1 in c:
                        TableOutput.append(len(set(MeekObj.LUT['OrientedEdge'][(v,v1)])  - oriented2))


                                
                                
                    TableInput.sort()
                    TableOutput.sort()

                    MinOriented = float("inf")
                    for Iedges in range(1,len(c)-1,1):
                        tmp = TableInput[Iedges-1] + TableOutput[len(c)-1-Iedges] + (len(c)-Iedges)*Iedges
                        if(MinOriented > tmp):
                            MinOriented = tmp

                    MinOriented += len(oriented2)

                    if(Len > MinOriented + len(c)-2 ):
                        Cnt = 1
                        Len = MinOriented + len(c)-2


                    ##############################################################################

                        
                    if(LowerBoundOriented[v] >Len):
                        LowerBoundOriented[v]  = Len
                        LowerBoundClique[v] = Cnt


                        
            ##############################################################################
            # All Edges Are Output
            oriented3 = set()
            for v1 in MeekObj.neighbor[v]:
                oriented3  |= set(MeekObj.LUT['OrientedEdge'][(v,v1)])
            oriented3 = list(dict.fromkeys(oriented3))
            
            if(Len > len(oriented3)):
                Cnt = 2
                Len = len(oriented3)
                
            if(LowerBoundOriented[v] >Len):
                LowerBoundOriented[v]  = Len
                LowerBoundClique[v] = Cnt
            ##############################################################################

    zVal = float("inf")
    zIdx = -1
    V = list(LowerBoundOriented.keys())
    V.sort()
    for v in V:
        LowerBoundOriented[v] = nEdges(neigh) - LowerBoundOriented[v]
        if(zVal>=LowerBoundOriented[v]):
            zIdx = v
            zVal = LowerBoundOriented[v]
    return LowerBoundOriented,zIdx




