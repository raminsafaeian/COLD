from itertools import combinations
import copy


def uDAG2pDAG(pdag):

    def rule1(pdag,Flag):
        
        edgeSet = list([])
        for row in range(0,len(pdag)):
            for col in range(0,len(pdag)):
                if pdag[row][col] == 1 and pdag[col][row] == 0:
                    edgeSet += list([list([row,col])])
                    
        for i in range(0,len(edgeSet)):
            a = edgeSet[i][0]
            b = edgeSet[i][1]
            for c in range(0,len(pdag)):
                if pdag[a][c]==0 and pdag[c][a]==0:
                    if pdag[b][c]==1 and pdag[c][b]==1:
                        pdag[c][b]=0
                        Flag = True

                        
        return Flag
       
    def rule2(pdag,Flag):
        
        edgeSet = list([])
        for row in range(0,len(pdag)):
            for col in range(0,len(pdag)):
                if pdag[row][col] == 1 and pdag[col][row] == 1:
                    edgeSet += list([list([row,col])])
                    
        
        for i in range(0,len(edgeSet)):
            a = edgeSet[i][0]
            b = edgeSet[i][1]
            for c in range(0,len(pdag)):
                if pdag[a][c]==1 and pdag[c][a]==0:
                    if pdag[b][c]==0 and pdag[c][b]==1:
                        if pdag[a][b]==1 and pdag[b][a]==1:
                            pdag[b][a]=0
                            Flag = True

                    
        return Flag
       
                    
    def rule3(pdag,Flag):
        
        edgeSet = list([])
        for row in range(0,len(pdag)):
            for col in range(0,len(pdag)):
                if pdag[row][col] == 1 and pdag[col][row] == 1:
                    edgeSet += list([list([row,col])])
                    
        remEdge = list([])
        for i in range(0,len(edgeSet)):
            a = edgeSet[i][0]
            b = edgeSet[i][1]
            cSet = list([])
            for c in range(0,len(pdag)):
                if pdag[a][c]==1 and pdag[c][a]==1:
                    if pdag[b][c]==0 and pdag[c][b]==1:
                        cSet += list([c])

                          
            for (c1, c2) in combinations(cSet, 2):
                if pdag[c1][c2]==0 and pdag[c2][c1]==0:
                    pdag[b][a] = 0
                    Flag = True
        
        return Flag
  
    
    Flag = True
    while Flag:
        
        Flag = False
        Flag = rule1(pdag,Flag)
        Flag = rule2(pdag,Flag)
        Flag = rule3(pdag,Flag)


    return pdag      

