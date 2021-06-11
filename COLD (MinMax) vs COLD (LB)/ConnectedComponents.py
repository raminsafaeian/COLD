 

def DFSUtil(neighbor, temp, v, visited): 
  
        # Mark the current vertex as visited 
        visited[v] = True
  
        # Store the vertex to list 
        temp[v] = neighbor[v] 
  
        # Repeat for all vertices adjacent 
        # to this vertex v 
        for i in neighbor[v]: 
            if visited[i] == False: 
                  
                # Update the list 
                temp = DFSUtil(neighbor,temp, i, visited) 
        return temp 
    
    
    
def ConnectedComponents(neighbor): 
    visited = dict() 
    cc = [] 
    for i in list(neighbor.keys()): 
        visited[i] = False
    for v in neighbor: 
        if visited[v] == False: 
            temp = dict() 
            cc.append(DFSUtil(neighbor,temp, v, visited)) 
            
    return cc 