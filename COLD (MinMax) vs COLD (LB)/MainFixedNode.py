

import networkx as nx
from Simulator.RandomDAG import RandomDAG
from Simulator.GraphUtil import Essential

from COLD_MinMax.COLD_MinMax import FullIdentificationHauserLUT
from COLD_LB.COLD_LB import FullIdentificationLowerBound
import time
import csv    
import copy

    
from enum import Enum
class Algorithm(Enum):
    COLD_MinMax = 0
    COLD_LB = 1

AlgorithmName = {}
AlgorithmName[Algorithm.COLD_MinMax] = 'COLD_MinMax'
AlgorithmName[Algorithm.COLD_LB] = 'COLD_LB'


Alg = [Algorithm.COLD_MinMax,Algorithm.COLD_LB]
nNodes = range(35,36,5)
nAvg   = 100
nIntervention = list([])
AvgTime = list([])
IntSet = list([])
for AlgIdx in range(len(Alg)):
    nIntervention += [0]
    AvgTime += [dict()]
    IntSet  += [dict()]

with open('ResultFixedNode.csv', 'w', newline='') as csvfile:
    CSVwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    CSVwriter.writerow(['Hauser',])
    String = list(['nNodes','nEdges']);
    for i in Alg:
        String.append(AlgorithmName[i]+' Time')
        
    for i in Alg:
        String.append(AlgorithmName[i]+' N INtervention')
        
    CSVwriter.writerow(String)
    
for p in nNodes:
    
    for AlgIdx in range(len(Alg)):
        AvgTime[AlgIdx][p] = dict()
        IntSet[AlgIdx][p]  = dict()
        

    for e in range(50,int(p*(p-1)/2-3),50):
        nAvgCnter = 0
        for AlgIdx in range(len(Alg)):
            AvgTime[AlgIdx][p][e] = 0
            nIntervention[AlgIdx] = 0
            IntSet[AlgIdx][p][e]  = list([])
          

        while(nAvgCnter<nAvg):
                       
            
            ##############################################################################
            ###
            ### Genrate DAG
            ###
            ##############################################################################
            dag = RandomDAG(p,e)   
            if(nx.is_connected(dag.to_undirected()) == False):
                print("Unconnected")
            if(nx.is_chordal(dag.to_undirected()) == False):
                print("Not Chordal")
            
            
            neigh = {"dag":{} , "graph":{}}
            for v in dag:
                neigh["dag"][v]   = set()
                neigh["graph"][v] = set()
            
            for v1,v2 in list((v1,v2) for v1,v2 in dag.edges):
                neigh["dag"][v2]   |= set([v1])
                neigh["graph"][v1] |= set([v2])
                neigh["graph"][v2] |= set([v1])
#            print(neigh["dag"])
 
            
            ##############################################################################
            ###
            ### Accelerated Hauser
            ###
            ##############################################################################
            if Algorithm.COLD_MinMax in Alg:
                neightmp = copy.deepcopy(neigh)
                start = time.perf_counter_ns()   
    #           SingleOptMeekLUT(essential.MEC,essential.nUndirected,p1)  
                IntSet[Alg.index(Algorithm.COLD_MinMax)][p][e] += list([FullIdentificationHauserLUT(neightmp,'AllCliques',30)])
                end  = time.perf_counter_ns()   
                AvgTime[Alg.index(Algorithm.COLD_MinMax)][p][e]+= (end-start) 
                nIntervention[Alg.index(Algorithm.COLD_MinMax)] += len(IntSet[Alg.index(Algorithm.COLD_MinMax)][p][e][nAvgCnter]["IntSet"])


            
            ##############################################################################
            ###
            ### Lower Bound Algorihtm
            ###
            ##############################################################################
            if Algorithm.COLD_LB in Alg:
                neightmp = copy.deepcopy(neigh)
                start = time.perf_counter_ns() 
                IntSet[Alg.index(Algorithm.COLD_LB)][p][e] += list([FullIdentificationLowerBound(neightmp,30)])                  
                end  = time.perf_counter_ns()   
                AvgTime[Alg.index(Algorithm.COLD_LB)][p][e]+= (end-start) 
                nIntervention[Alg.index(Algorithm.COLD_LB)] += len(IntSet[Alg.index(Algorithm.COLD_LB)][p][e][nAvgCnter]["IntSet"])
  



            nAvgCnter += 1
            

        ##############################################################################
        ###
        ### Printing
        ###
        ##############################################################################

                    
        String = list([p,e])
        for AlgIdx in range(len(Alg)):
            String.append(AvgTime[AlgIdx][p][e]/1e6/nAvg)
        for AlgIdx in range(len(Alg)):
            String.append(nIntervention[AlgIdx]/nAvg)

        with open('ResultFixedNode.csv', 'a+', newline='') as csvfile:
            CSVwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            CSVwriter.writerow(String)

        print("-------------------------------------------------------------")
        print("nNodes= ",p,", nEdges= ",e)
        print("-------------------------------------------------------------")

        print("Algorithm Name |  ",end="")
        for AlgId in Alg:
            print("%14s"%AlgId.name,end="")
            
        print("\n-------------------------------------------------------------")
        print("Average Time   | ",end="")
        for AlgIdx in range(len(Alg)):
            print("%14.2f"%(AvgTime[AlgIdx][p][e]/1e6/nAvg),end="")
        print("\n-------------------------------------------------------------\n\n")
        ##############################################################################
        ###
        ### End
        ###
        ##############################################################################
#             