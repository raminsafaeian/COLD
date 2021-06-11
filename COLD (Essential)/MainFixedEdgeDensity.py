"""
Python Code For obtaining Essential graph from skeleton and v-structures:
    
    1 - COLD (Essential)
    2 - PCAlg
    
@ Author : Ramin Safaeian
  Date   : 1400/03/12

"""


###################################################################
###       Import       ############################################
import networkx as nx
from Simulator.RandomDAG import RandomDAG
from Simulator.GraphUtil import Essential
from CPDAG.uDAG2pDAG_R2Py import uDAG2pDAG
from Simulator.GraphUtil import Extract_V_Structures
from COLD_Essential.COLD_Essential import COLD_Essential
import time
import csv    
import sys    



###################################################################
###       Algorithms      #########################################
from enum import Enum
class Algorithm(Enum):
    COLD   = 0
    PCAlg = 1

AlgorithmName = {}
AlgorithmName[Algorithm.COLD]   = 'COLD'
AlgorithmName[Algorithm.PCAlg] = 'PCAlg'



###################################################################
###       Choose Algorithms for Execution      ####################
Alg = [Algorithm.COLD,Algorithm.PCAlg]




###################################################################
###       Setting #################################################
nNodes = range(20,51,10)
nAvg   = 100
AvgTime = list([])
for AlgIdx in range(len(Alg)):
    AvgTime += [dict()]
    

###################################################################
###       Open CSV file for writing results #######################
with open('ResultFixedEdge.csv', 'w', newline='') as csvfile:
    CSVwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    CSVwriter.writerow(['Hauser',])
    String = list(['nNodes','nEdges']);
    for i in Alg:
        String.append(AlgorithmName[i]+' Time')
    CSVwriter.writerow(String)




###################################################################
###       Algorithm Execution #####################################    
for p in nNodes:
    
    for AlgIdx in range(len(Alg)):
        AvgTime[AlgIdx][p] = dict()
        
        
    for e in range(int(.25*p*(p-1)/2),int(.51*p*(p-1)/2),int(.8*p*(p-1)/2)):
        nAvgCnter = 0
        for AlgIdx in range(len(Alg)):
            AvgTime[AlgIdx][p][e] = 0
          

        while(nAvgCnter<nAvg):
                       
            ##############################################################################
            ###
            ### Genrate DAG
            ###
            ##############################################################################
            dag = RandomDAG(p,e)   
            print("")
            print("")
            print("")
            print("---------------------------------------------------------------------------------")
            print("---------------------------------------------------------------------------------")

    
            neigh = dict()
            for v in dag:
                neigh[v] = set()
            
            for v1,v2 in list((v1,v2) for v1,v2 in dag.edges):
                neigh[v1] |= set([v2])
                neigh[v2] |= set([v1])
                
                
                
            V_Edges = Extract_V_Structures(dag)
            V_Edges =  list(dict.fromkeys(list(V_Edges)))
            if V_Edges ==[]:
                continue


            newDAG = nx.DiGraph()
            for v1,v2 in list(dag.edges):
                newDAG.add_edge(v1,v2)
                if (v1,v2) not in V_Edges:
                    newDAG.add_edge(v2,v1)

           ##############################################################################
            ###
            ### COLD 
            ###
            ##############################################################################
            print("COLD algorithm Running...")


            dag2 = newDAG.copy()
            
            pdag = dict()
            for v in dag2:
                pdag[v]   = set()
                
            for v1,v2 in list((v1,v2) for v1,v2 in dag2.edges):
                if (v2,v1) not in dag2.edges():
                    pdag[v2] |= set([v1])
                else:
                    pdag[v1] |= set([v2])
                    pdag[v2] |= set([v1])
                        
                
            
            start1  = time.perf_counter_ns()  
            pdag11 = COLD_Essential(pdag,neigh)
            end1  = time.perf_counter_ns()   
            
            
            OrientedEdgeCOL = list([])
            for  v1 in range(len(pdag11)):
                for  v2 in range(len(pdag11)):
                    if v1 in  pdag11[v2] and v2 not in pdag11[v1]:
                        OrientedEdgeCOL += [(v1,v2)]


#            print("OrientedEdges")
#            print(OrientedEdges)
#            print("Time: ",end1-start1)
            AvgTime[Alg.index(Algorithm.COLD)][p][e]= (end1-start1) 

            
             ##############################################################################
            ###
            ### PCAlg
            ###
            ##############################################################################
            print("PC Alg algorithm Running...")
            dag1 = newDAG.copy()
            
            pdag = [[0 for col in list(dag1.nodes())] for row in list(dag1.nodes())]

            for ee in dag1.edges():
                pdag[ee[0]][ee[1]] = 1

            start2  = time.perf_counter_ns()   
            dag2 = uDAG2pDAG(pdag)
            end2  = time.perf_counter_ns()   

    
            OrientedEdgePC = list([])
            for  v1 in range(len(dag2)):
                for  v2 in range(len(dag2)):
                    if dag2[v1][v2] == 1 and dag2[v2][v1] == 0:
                        OrientedEdgePC += [(v1,v2)]

            AvgTime[Alg.index(Algorithm.PCAlg)][p][e]= (end2-start2) 

       

            nAvgCnter += 1


        ##############################################################################
        ###
        ### Printing
        ###
        ##############################################################################
      

                    
            String = list([p,e])
            for AlgIdx in range(len(Alg)):
                String.append(AvgTime[AlgIdx][p][e]/1e6)
    
            with open('ResultFixedEdge.csv', 'a+', newline='') as csvfile:
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
                print("%14.2f"%(AvgTime[AlgIdx][p][e]/1e6),end="")
            print("\n-------------------------------------------------------------\n\n")
            ##############################################################################
            ###
            ### End
            ###
            ##############################################################################
    #             