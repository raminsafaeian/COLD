"""
@ Author : Ramin Safaeian
  Date   : 06/11/2021

"""

import networkx as nx
from Simulator.RandomDAG import RandomDAG
from Simulator.GraphUtil import Essential
from GraphTools import nEdges
from HauserLUT.HauserLUT import BestNodeHauserLUT
from LowerBound.LowerBoundOfOrientation import LowerBoundOfOrientationNewMethod


from MeekLUT import Meek
import time
import csv    
import copy

    
from enum import Enum
class Algorithm(Enum):
    AccHauser    = 0
    LowBoundNew    = 1

AlgorithmName = {}
AlgorithmName[Algorithm.AccHauser] = 'AccHauser'
AlgorithmName[Algorithm.LowBoundNew] = 'LowBoundNew'

Alg = [Algorithm.AccHauser,Algorithm.LowBoundNew]
nNodes = range(20,61,10)
nAvg   = 100
nIntervention = list([])
AvgTime = list([])
MinOrientation = list([])
for AlgIdx in range(len(Alg)):
    nIntervention += [0]
    AvgTime += [dict()]
    MinOrientation  += [dict()]

with open('ResultFixedEdgeDensity.csv', 'w', newline='') as csvfile:
    CSVwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    CSVwriter.writerow(['Lower Bound Comparison',])
    String = list(['nNodes','nEdges','Node number','Number of average']);
    for i in Alg:
        String.append(AlgorithmName[i])
        
    for i in Alg:
        String.append(AlgorithmName[i]+' Time')

    CSVwriter.writerow(String)
    
for p in nNodes:
    
    for AlgIdx in range(len(Alg)):
        AvgTime[AlgIdx][p] = dict()
        MinOrientation[AlgIdx][p]  = dict()


    for e in range(int(p*(p-1)/2*.4),1+int(p*(p-1)/2*.4),25):
        nAvgCnter = 0
        for AlgIdx in range(len(Alg)):
            AvgTime[AlgIdx][p][e] = 0
            MinOrientation[AlgIdx][p][e] = 0
            nIntervention[AlgIdx] = 0
          
        Error = list([0])
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
            if Algorithm.AccHauser in Alg:
                neightmp = copy.deepcopy(neigh)
                start = time.perf_counter_ns()   
                MeekObj = Meek(neightmp["graph"])
                MinOrientation[Alg.index(Algorithm.AccHauser)][p][e],_ =BestNodeHauserLUT(neightmp["graph"],nEdges(neightmp["graph"]),MeekObj,'AllCliques')
                end  = time.perf_counter_ns()   
                AvgTime[Alg.index(Algorithm.AccHauser)][p][e]+= (end-start) 




            ##############################################################################
            ###
            ### Lower Bound New Algorihtm
            ###
            ##############################################################################
            if Algorithm.LowBoundNew in Alg:
                neightmp = copy.deepcopy(neigh)
                start = time.perf_counter_ns() 
                MinOrientation[Alg.index(Algorithm.LowBoundNew)][p][e],_ = LowerBoundOfOrientationNewMethod(neightmp["graph"])                  
                end  = time.perf_counter_ns()   
                AvgTime[Alg.index(Algorithm.LowBoundNew)][p][e]+= (end-start) 


            nAvgCnter +=1
            print("nAvgCnter = ",nAvgCnter)


            ##############################################################################
            ###
            ### Printing
            ###
            ##############################################################################
                                   
            with open('ResultFixedEdgeDensity.csv', 'a+', newline='') as csvfile:
                CSVwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                
                for v in list(MinOrientation[AlgIdx][p][e].keys()):
                    String = list([p,e,v,nAvgCnter])                   
                    for AlgIdx in range(len(Alg)):
                        String.append(MinOrientation[AlgIdx][p][e][v])
                        
                    for AlgIdx in range(len(Alg)):
                        String.append(AvgTime[AlgIdx][p][e]/1e6/nAvgCnter)
                    CSVwriter.writerow(String)

        ##############################################################################
        ###
        ### End
        ###
        ##############################################################################
