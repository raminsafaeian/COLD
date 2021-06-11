
import time
import networkx as nx
from random import sample
import csv    
from enum import Enum


from Simulator.GraphUtil import Essential
from Simulator.RandomDAG import RandomDAG
from MemoMamo_MECSize.MemoMamo_MECSize import MemoMamo_MECSize
from MemoMamo_MECSize.MemoMamo_MECSize import cceg
from MarkovEquClasses import countpdag
from LazyIter_MECSize.LazyIter_MECSize import count_optimized
from COLD_MECSize.COLD_MECSize import COLD_MECSize

from MeekFastImp import Meek


class Algorithm(Enum):
    He2015   = 0
    MemoMamo = 1
    COLD_MECSize = 2
    LazyIter = 3

AlgorithmName = {}
AlgorithmName[Algorithm.He2015]   = "He2015"
AlgorithmName[Algorithm.MemoMamo] = 'MemoMamo'
AlgorithmName[Algorithm.COLD_MECSize] = 'COLD_MECSize'
AlgorithmName[Algorithm.LazyIter] = 'LazyIter'


Alg = [Algorithm.MemoMamo,Algorithm.COLD_MECSize,Algorithm.LazyIter]
nNodes = range(30,31,5)
nAvg   = 25
size = list([])
AvgTime = list([])
for AlgIdx in range(len(Alg)):
    size += [0]
    AvgTime += [dict()]



with open('Results.csv', 'w', newline='') as csvfile:
    CSVwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    CSVwriter.writerow(['Size of MEC',])
    String = list(['nNodes','nEdges']);
    for i in Alg:
        String.append(AlgorithmName[i])
    CSVwriter.writerow(String)
    

for p in nNodes:

    for AlgIdx in range(len(Alg)):
        AvgTime[AlgIdx][p] = dict()

    for e in range(50,int(p*(p-1)/2-3),25):

        nAvgCnter = 0
        print(time.ctime())

        for AlgIdx in range(len(Alg)):
            AvgTime[AlgIdx][p][e] = 0
			
        while(nAvgCnter<nAvg):
            nAvgCnter += 1
            print("nAvgCnter = ",nAvgCnter, end='')
    
            ##############################################################################
            ###
            ### Genrate DAG
            ###
            ##############################################################################
            dag = RandomDAG(p,e)   
            print(", DAG Generated")

            dag1 = list()
            for edge in list(dag.edges()):
                dag1 += list([list([edge[0],edge[1]])])
                    
            ##############################################################################
            ###
            ### He 2015
            ###
            ##############################################################################
            
            if Algorithm.He2015 in Alg:
                mec = cceg(dag1,len(dag.nodes()))
                start = time.perf_counter_ns()   
                size[Alg.index(Algorithm.He2015)] = countpdag(mec)
                end = time.perf_counter_ns()
                AvgTime[Alg.index(Algorithm.He2015)][p][e]+= (end-start) 
                
                
            ##############################################################################
            ###
            ### MemoMamo
            ###
            ##############################################################################
                
            if Algorithm.MemoMamo in Alg:
                mec = cceg(dag1,len(dag.nodes()))
                start = time.perf_counter_ns()   
                size[Alg.index(Algorithm.MemoMamo)] = MemoMamo_MECSize(mec,[0],[0],{})
                end = time.perf_counter_ns()
                AvgTime[Alg.index(Algorithm.MemoMamo)][p][e]+= (end-start)
                AlgIdx+=1
                
            ##############################################################################
            ###
            ### COLD (MECSize)
            ###
            ##############################################################################
            
            if Algorithm.COLD_MECSize in Alg:
                essential = Essential(dag)               
                MEC = essential.MEC[0].copy()
                mec = cceg(dag1,len(dag.nodes()))
                neighbor = mec['Neiset'][0]
                start = time.perf_counter_ns()   
                MeekObj = Meek(neighbor)
                size[Alg.index(Algorithm.COLD_MECSize)] = COLD_MECSize(MeekObj.LUT['Root'],neighbor,{}) 
                end = time.perf_counter_ns()
                AvgTime[Alg.index(Algorithm.COLD_MECSize)][p][e]+= (end-start) 
                AlgIdx+=1

                                
            ##############################################################################
            ###
            ### LazyIter
            ###
            ##############################################################################
            if Algorithm.LazyIter in Alg:
                mec = cceg(dag1,len(dag.nodes()))
                start = time.perf_counter_ns()   
                size[Alg.index(Algorithm.LazyIter)] = count_optimized(mec['Neiset'][0],{}) 
                end = time.perf_counter_ns()
                AvgTime[Alg.index(Algorithm.LazyIter)][p][e]+= (end-start) 
                AlgIdx+=1
                

        ##############################################################################
        ###
        ### Printing
        ###
        ##############################################################################
        
            for AlgIdx in range(len(Alg)-1):
                if(size[AlgIdx] != size[AlgIdx+1]):
                    print("Algorithm Does'nt work correctly")
                    print(size)
                    
                   
        String = list([p,e])
        for AlgIdx in range(len(Alg)):
            String.append(AvgTime[AlgIdx][p][e]/1e6/nAvg)

        with open('Results.csv', 'a+', newline='') as csvfile:
            CSVwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            CSVwriter.writerow(String)

        print("-------------------------------------------------------------")
        print("nNodes= ",p,", nEdges= ",e, ", nDAGs= ", size[0])
        print("-------------------------------------------------------------")

        print("Algorithm Name |  ",end="")
        for AlgId in Alg:
            print("%10s"%AlgId.name,end="")
            
        print("\n-------------------------------------------------------------")
        print("Average Time   | ",end="")
        for AlgIdx in range(len(Alg)):
            print("%10.2f"%(AvgTime[AlgIdx][p][e]/1e6/nAvg),end="")
        print("\n-------------------------------------------------------------\n\n")
        ##############################################################################
        ###
        ### End
        ###
        ##############################################################################
             