# Causal Orientation Learning with dynamic programming

## Main Reference
This is an implementation of the following paper:  
**Safaeian, R., Salehkaleybar, S. and Tabandeh, M. (2021). Fast Causal Orientation in Directed Acyclic Graphs (JMLR 2021).**

## Citing information
For citing this paper, please use the following:

@inproceedings{Safaeian2021COLD,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; author = {Safaeian, Ramin and SalehKaleybar, Saber and Tabandeh, Mahmoud.},  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; title = {Fast Causal Exploration in Directed Acyclic Graphs},  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; year = {2021}  
}


## Requirements
+ Python 3.7+
+ networkx
+ itertools
+ random
+ collections


## Contents
+ COLD (Essential)  
+ COLD (LB)  
+ COLD (MECSize)  
+ COLD (MinMax)  
+ COLD (MinMax) versus COLD (LB)  
+ COLD (MinMax) versus COLD (MinMaxPT)  


## Deescription
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The code in COLD (Essential) folder recovers Essential graph from oriented v-structures. In COLD (LB) folder, the lower bound on a single node in a chordal chain component is computed. In this code we compute the minimum number of edges that will be surely oriented if we intervene on that node. We compute the number of DAGs in an Markov Equivalence class (MEC) with the codes in COLD (MECSize) folder. Codes in folder COLD (MinMax) select a node from a chordal chain component to perform intervention. The property of selected node is that the number of oriented edges after performing intervention is maximum value that is achievable. We use the COLD (LB) Algorithm to solve the MinMax Problem. Codes in COLD (MinMax) versus COLD (LB) folder compares two algorithms COLD (MinMax) and COLD (LB) in the sence of execution time and performance. This comparison shows that using  COLD (LB) decreases the execution time of solving MinMax Problem while maintaining the number of interventions that are needed for full identifacation. Furthermore, COLD (MinMaxPT) algorithm uses a practial trick which accelerates finding the solutions of MinMax problems. 



## Running a simple demo
In each of these folders, there are some files with names similar to Main.py, MainFixedEdgeDensity.py and MainFixedNode.py. Running each of these files, executes the codes and returns reported results in the paper. 
