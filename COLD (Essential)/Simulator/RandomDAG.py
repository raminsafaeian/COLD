#import utils
import networkx as nx
from random import sample
from Simulator.LEX_BFS import LEX_BFS
from Simulator.GraphUtil import Extract_V_Structures
import random


def RandomDAG(nNodes,nEdges):
    
    
    MEC = RandomChainComp(nNodes,nEdges)
    Order = LEX_BFS(MEC[0],sample(list(MEC[0].nodes()), len(MEC[0].nodes())))
    
    for i,j in MEC[0].edges():
        if(Order.index(i) < Order.index(j)):
            MEC[0].remove_edge(j,i)     

    DAG = MEC[0]
    V_Edges = Extract_V_Structures(DAG)
    if(len(V_Edges) != 0 ):
        print("V Structure Detected")
    return DAG


def RandomChainComp(nNodes,nEdges):
    N = nNodes
    M = nEdges
    
    G = nx.random_tree(N)
#    print(nx.is_connected(G))
    
    edge_num = len(G.edges)
    
    available = set()
    for i in range(N):
        for j in range(i+1, N):
            if not G.has_edge(i, j):
                available.add((i, j))
    
#    print(available)
    # available = {(1,4)}
    Cnt = 0
    while edge_num < M:


        t = sample(available, 1)
        x, y = t[0]
    
        ca = []
        for i in range(N):
            if i != x and i != y:
                if G.has_edge(i, x) and G.has_edge(i, y):
                    ca.append(i)
    
        H = G.copy()
        for c in ca:
            H.remove_node(c)
        if not (nx.is_connected(H)):
            G.add_edge(x, y)
            edge_num += 1
            available.remove(t[0])
            Cnt = 0
        else:
            Cnt += 1
        if(Cnt == 2000):
            print("Error in DAG Generation functionality")
            G1 = RandomDAG(nNodes,nEdges)
            print('DAG Generation Halted')
            break;
#            print(edge_num, ": ", x, y, ca)

    G1 = nx.DiGraph()
    G1.add_edges_from(G.edges())
        
    MEC = nx.DiGraph()
    for i,j in list(G1.edges):
        MEC.add_edge(j,i)
        MEC.add_edge(i,j)
        
    return list([MEC])
