from Simulator.GraphUtil import Neighbors


def LEX_BFS(G,InitOrder):
 
    S = list([InitOrder.copy()])
    s = list([])
       
    while(1==1):
        v = S[0].pop(0)
        if(len(S[0])==0):
            S.pop(0)
            
        s.append(v)

        if(len(S) ==0):
            break
        N = Neighbors(G,v);   

        S1 = list([])
        for c in S:
            Grp1 = list([])
            Grp2 = list([])
            for b in c:
                if b in N:
                    Grp1.append(b)
                else:
                    Grp2.append(b)
                
            if len(Grp1) !=0:
                S1.append(Grp1)            
            if len(Grp2) !=0:
                S1.append(Grp2)
            
        S=S1.copy()
#        print(S)
     
    return s
