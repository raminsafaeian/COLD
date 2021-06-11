import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import queue
import itertools
#import ttictoc

def read_adj_mat_from_file(file_name):

    inp = open(file_name, 'r').read()

    inp = inp.split('\n')
    if len(inp[-1]) == 0:
        inp = inp[:-1]

    n = len(inp)
    m = np.zeros((n, n)).astype('int')

    for row in range(n):
        nums = inp[row].split()
        for i in range(n):
            m[row, i] = int(nums[i])

    return m

def get_all_subsets(st):
    ret = []
    for i in range(len(st) + 1):
        lst = list(itertools.combinations(st, i))
        for item in lst:
            ret.append(list(item))
    return ret

def plot_graph(adj_mat):
    plt.figure(figsize=(20, 20))
    g = nx.DiGraph(adj_mat)
    options = {
        'node_color': 'pink',
        'edge_color': 'gray',
        'node_size': 300,
        'width': 3,
    }
    labels = {}
    for i in range(adj_mat.shape[0]):
        labels[i] = str(i)
    nx.draw(g, labels=labels, **options)
    plt.show()


def get_accessible_nodes(adj, source, valid_nodes):
    n = adj.shape[0]
    q = queue.Queue(maxsize=n)
    seen = [False] * n

    q.put(source)
    seen[source] = True

    while not q.empty():
        node = q.get()
        for i in valid_nodes:
            if adj[node, i] and seen[i] is False:
                q.put(i)
                seen[i] = True
    res = []
    for i in range(n):
        if seen[i]:
            res.append(i)

    return res


def bfs_optimized(neighbors, start):
    n = len(neighbors)
    q = queue.Queue()
    seen = {i: False for i in neighbors.keys()}
    seen[start] = True
    q.put(start)
    while not q.empty():
        node = q.get()
        for i in neighbors[node]:
            if not seen[i]:
                q.put(i)
                seen[i] = True

    res = []
    for i in seen:
        if seen[i]:
            res.append(i)

    return set(res)


def bfs(neighbors, start, is_valid):
    n = len(neighbors)
    q = queue.Queue()
    seen = [False] * n
    seen[start] = True
    q.put(start)

    while not q.empty():
        node = q.get()
        for i in neighbors[node]:
            if not seen[i] and is_valid[i]:
                q.put(i)
                seen[i] = True

    res = []
    for i in range(n):
        if seen[i]:
            res.append(i)
    return res, seen


def set_root(adj_mat, neighbors, root, is_valid):

    # t = ttictoc.TicToc()
    # t.tic()

    added_edges = []
    q = queue.Queue()


    for i in neighbors[root]:
        if is_valid[i] and adj_mat[root][i] == 1 and adj_mat[i][root] == 1:
            added_edges.append((root, i))
            q.put((root, i))
            adj_mat[i][root] = 0
    # total_hash_time[4] += t.toc()
    """
    If the graph is not chordal, direction of the root's edges might be overwritten in the following while-loop! 
    """
    # t.tic()
    while not q.empty():
        s, e = q.get()
        for i in neighbors[e]:
            if is_valid[i] and adj_mat[e][i] == 1 and adj_mat[i][e] == 1 and adj_mat[s][i] == 0 and adj_mat[i][s] == 0:
                added_edges.append((e, i))
                q.put((e, i))
                adj_mat[i][e] = 0

    # total_hash_time[5] += t.toc()
    return added_edges


def test(a, b):
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] != b[i][j]:
                print(i, j)
                return False
    return True


def encode(lst):
    w = 1
    sm = 0
    for i in lst:
        if i:
            sm += w
        w *= 2
    return sm


def find_chain_components(adj_mat, neigbors, is_valid):
    n = len(adj_mat)
    component_id = [-1] * n
    current_id = 0
    for i in range(n):
        if is_valid[i]:
            if component_id[i] == -1:
                q = queue.Queue()
                q.put(i)
                while not q.empty():
                    node = q.get()
                    component_id[node] = current_id
                    for v in neigbors[node]:
                        if component_id[v] == -1 and is_valid[v] and adj_mat[v][node] == 1 and adj_mat[node][v] == 1:
                            # print(node+1, v+1, component_id[v])
                            q.put(v)
                current_id += 1

    return [[num for num in list(range(n)) if component_id[num] == id] for id in range(current_id)]
    # for id in range(current_id):
    #     print([num+1 for num in list(range(n)) if component_id[num] == id])


fact = [1] * 5000
for i in range(1,5000):
    fact[i] = fact[i-1] * i


def check_he_rules(AdjMat, neighbors, nodes):
    num_of_edges = 0
    n = len(AdjMat)
    is_in_nodes = [False] * n
    for i in nodes:
        is_in_nodes[i] = True
    for i in nodes:
        for j in neighbors[i]:
            if j > i and is_in_nodes[j] and AdjMat[i][j] and AdjMat[j][i]:
                num_of_edges += 1
    n = len(nodes)

    if num_of_edges == n-1:
        return n
    if num_of_edges == n:
        return 2 * n
    if num_of_edges == ((n * (n-1))/2-2):
        return (n*n -n - 4) * fact[n-3]
    if num_of_edges == ((n * (n-1))/2-1):
        return 2 * fact[n-1] - fact[n-2]
    if num_of_edges == (n * (n-1)/2):
        return fact[n]

    return -1


def seperate_graph(G):
    left=set(G.keys())
    H=[]
    while len(left)>0:
        current=left.pop()
        visited={current}
        tovisit=G[current].copy()
        Tg={}
        Tg[current]=G[current].copy()
        while len(tovisit)>0:
            tem=tovisit.pop()
            visited.add(tem)
            Tg[tem]=G[tem].copy()
            tovisit.update(G[tem].difference(visited))
            left.remove(tem)
        H.append(Tg)
        # print("GG: ", G, "\nHH:", H)
        # print(H[0] == G)
    return H


def set_root_optimized(root, neighbors):
    nodes = set(neighbors.keys())
    # total_edges = sum(len(neighbors[i]) for i in neighbors)/2
    directed_edges = []

    if root not in nodes:
        print("Missing root!")

    current_nodes = {root}
    CCs = list()
    left = nodes - current_nodes
    while len(left) != 0:
        res = set()
        fathers = {}
        for i in current_nodes:
            nodestem = neighbors[i].intersection(left)
            res |= nodestem
            for nodesi in nodestem:
                if nodesi in fathers:
                    fathers[nodesi].add(i)
                else:
                    fathers[nodesi] = {i}
                directed_edges.append((i, nodesi))
        residual_graph = {i: neighbors[i]&res for i in res}

        is_done = False
        while not is_done:
            is_done = True
            for i in residual_graph:
                removed_edges = []
                for j in residual_graph[i]:
                    if not fathers[i].issubset(neighbors[j]):
                        fathers[j].add(i)
                        removed_edges.append((i, j))
                        directed_edges.append((i, j))
                        is_done = False
                for x, y in removed_edges:
                    residual_graph[x].remove(y)
                    residual_graph[y].remove(x)

            residual_graph = {i:residual_graph[i] for i in residual_graph}
            #TODO: changed sth here (len(resg[i]) > 0)
        CCs.extend(seperate_graph(residual_graph))
        current_nodes = res
        left -= res
    # ccnodesn = [0 for i in range(CC_num)]
    # ccedgesn = [0 for i in range(CC_num)]

    #     undirected += sum(len(CC[i]) for i in CC)/2
    #     ccnodesn[i] = len(CCs[i])
    #     tem = set([j for j in CCs[i]])
    #     while len(tem) != 0:
    #         ss = tem.pop()
    #         ccedgesn[i] += len(neighbors[ss] & tem)
    new_neighbors = {i: set() for i in nodes}
    for x, y in directed_edges:
        new_neighbors[x].add(y)
    for CC in CCs:
        for i in CC:
            new_neighbors[i] = new_neighbors[i]|CC[i]
    return [item.keys() for item in CCs], new_neighbors

