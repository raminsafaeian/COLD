# Causal Orientation Learning with dynamic programming

## Main Reference
This is an implementation of the following paper:
**Safaeian, R., Salehkaleybar, S. and Tabandeh, M. (2021). Fast Causal Orientation in Directed Acyclic Graphs (submitted to JMLR).**

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


## Description
+ The code in COLD (Essential) folder recovers the essential graph from oriented v-structures.  
+ In COLD (LB) folder, the lower bound on a single node in a chordal chain component is computed. In this code, we compute the minimum number of edges that will be definitely oriented if we intervene on that node.  
+ We compute the number of DAGs in a Markov Equivalence class (MEC) with the codes in COLD (MECSize) folder. Codes in folder COLD (MinMax) select a node from a chordal chain component to perform an intervention. The property of the selected node is that the number of oriented edges after performing intervention is the maximum value that is achievable.  
+ We use the COLD (LB) Algorithm to solve the MinMax Problem. Codes in COLD (MinMax) versus COLD (LB) folder compare two algorithms COLD (MinMax) and COLD (LB) in the sense of execution time and performance. This comparison shows that using COLD (LB) decreases the execution time of solving MinMax Problem while maintaining the number of interventions that are needed for full identification.  
+ Furthermore, COLD (MinMaxPT) algorithm uses a practical trick that accelerates finding the solutions for MinMax problems. 
 


## Running a simple demo
In each of these folders, there are some files with names similar to Main.py, MainFixedEdgeDensity.py and MainFixedNode.py. Running each of these files, executes the codes and returns reported results in the paper. 
