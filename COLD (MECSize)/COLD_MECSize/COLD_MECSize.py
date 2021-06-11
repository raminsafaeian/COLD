from collections import deque
from ConnectedComponents import ConnectedComponents

    
def myfac(n):
    k=1
    for i in range(1,n+1):
        k*=i
    return(k)
def COLD_MECSize(RootOrientation,neighbor,HashLUT):   

    nedge=sum([len(neighbor[i])   for i in neighbor])/2  
    p=len(neighbor)
    vset=neighbor.keys()
    
    if nedge==p-1: 
        return(p)
    if nedge==p:
        return(2*p)   
    if nedge==p*(p-1)/2-1:
        return(2*myfac(p-1)-myfac(p-2))
    if nedge==p*(p-1)/2:
        return(myfac(p))
    if nedge==p*(p-1)/2-2:
        return((p*p-p-4)*myfac(p-3))

    ind = hash(str(vset))
    if ind in HashLUT:
        return HashLUT[ind]
    num1=0
    for kkk in vset:
         
        temneighbor = dict()
        for v in neighbor:
            tmp = neighbor[v]-RootOrientation[kkk][v]
            if tmp != set():
                temneighbor[v] = tmp
        ChainCompNodes = ConnectedComponents(temneighbor)     
        
        temcoun=1
        for CC in ChainCompNodes:
            temcoun*=COLD_MECSize(RootOrientation,CC,HashLUT)

        num1+=temcoun
    HashLUT[ind] = num1
    return(num1)
    
def countpdagLUT(RootOrientation,pdag,p1,p2,HashLUT):

    neighborsets=pdag['Neiset']
    noedges=list(pdag['ccedgeno'])
    out=1
    cnn=len(neighborsets)
    for ii in range(cnn):
        out*=COLD_MECSize(RootOrientation,neighborsets[ii],int(noedges[ii]),p1,p2,HashLUT)
    return out