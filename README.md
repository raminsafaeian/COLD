# Causal Orientation Learning with dynamic programming

This is an implementation of the following paper:

Safaeian, R., Salehkaleybar, S. and Tabandeh, M. (2021). Fast Causal Exploration in Directed Acyclic Graphs (JMLR 2021).

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
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This Code finds the node which has will orient maximum number of undirected edges, in the worst case after performing single node intervention.  
+ COLD (MinMax) versus COLD (LB)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This Code Compares the running time of COLD (MinMax) and COLD (LB) for finding the best node for intervention in MinMax problem. Additionally, the number of interventions that are needed for full identification for both cases are computed.  
+ COLD (MinMax) versus COLD (MinMaxPT)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This Code shows how much we gain from using the practical trick in solving MinMax problem.  


## Deescription
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The code in COLD (Essential) folder recovers Essential graph from oriented v-structures. In COLD (LB) folder, we compute the lower bound on a single node in a chordal chain component. In this code we computes the minimum number of edges that will be surely oriented if we intervene on that node. We compute the number of DAGs in an Markov Equivalence class (MEC) with the codes in COLD (MECSize) folder.  



## Running a simple demo
