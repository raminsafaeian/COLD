import utilityAli

#import ttictoc
#import chordal_graph_generator
import numpy as np

total_hash_time = [0, 0, 0, 0, 0, 0, 0, 0, 0]
#t = ttictoc.TicToc()


def f_count(adj_mat, neighbors, source, is_available, is_descendant, parents, sm, dp, verbose):

    n = len(adj_mat)

    chain_components = utilityAli.find_chain_components(adj_mat, neighbors, is_descendant)
    chain_components.append([x for x in list(range(n)) if is_available[x] and not is_descendant[x]])

    # if verbose:
    #     print("------------------Source:", source + 1, " Parents:", [p + 1 for p in parents],"\n",
    #           is_available,"\n", is_descendant,
    #       " Chain Components:", [[x + 1 for x in c] for c in chain_components])

    is_valid = [False] * n
    num = 1
    for cc in chain_components:
        for x in cc:
            is_valid[x] = True
        num *= count(adj_mat, neighbors, is_valid, dp, verbose=verbose)
        for x in cc:
            is_valid[x] = False

    sm[0] += num

    # if verbose:
    #     print("+++++++++++++++++++Source:", source + 1, " Parents:", [p + 1 for p in parents],
    #       " Chain Components:", [[x + 1 for x in c] for c in chain_components], " Count:", num)

    for node in neighbors[source]:
        if is_descendant[node] and (len(parents) is 0 or node > parents[len(parents)-1]):
            is_candidate = True
            for p in parents:
                if not adj_mat[p][node]:
                    is_candidate = False
            if is_candidate:

                # Find the Move List:
                v1 = is_descendant.copy()
                for j in neighbors[source]:
                    v1[j] = False
                v1[node] = True

                v2 = is_descendant.copy()
                v2[node] = False
                v2[source] = True

                _, can_reach_from_node = utilityAli.bfs(neighbors, node, v1)
                _, can_reach_from_others = utilityAli.bfs(neighbors, source, v2)

                move_list = []
                is_moved = [False] * n
                for i in range(n):
                    if can_reach_from_node[i] and not can_reach_from_others[i]:
                        move_list.append(i)
                        is_moved[i] = True

                removed_edges = []
                for i in move_list:
                    for j in neighbors[i]:
                        if is_moved[j] or (is_descendant[j] is False and is_available[j]):
                            if adj_mat[j][i] and not adj_mat[i][j]:
                                removed_edges.append((j, i))
                                adj_mat[i][j] = 1

                vn = [False] * n
                for i in neighbors[source]:
                    if is_descendant[i]:
                        vn[i] = True
                # 32254030
                added_edges = utilityAli.set_root(adj_mat, neighbors, node, vn)

                for i in move_list:
                    is_descendant[i] = False

                is_descendant[node] = False
                parents_new = parents.copy()
                parents_new.append(node)
                adj_mat[source][node] = 0
                adj_mat[node][source] = 1

                f_count(adj_mat, neighbors, source, is_available, is_descendant, parents_new, sm, dp, verbose=verbose)

                for s, e in added_edges:
                    adj_mat[e][s] = 1
                for i in move_list:
                    is_descendant[i] = True
                for s, e in removed_edges:
                    adj_mat[e][s] = 0
                is_descendant[node] = True
                adj_mat[source][node] = 1
                adj_mat[node][source] = 0
    return


def count(adj_mat, neighbors, is_valid, dp, verbose=False):
    ind = utilityAli.encode(is_valid)
    n = len(adj_mat)

    if verbose:
        print("Counting DAGs on ", [k + 1 for k in [i for i in list(range(n)) if is_valid[i]]])

    if ind in dp:
        return dp[ind]
    nodes = [i for i in list(range(n)) if is_valid[i]]
    if len(nodes) <= 1:
        return 1

    he_rules = utilityAli.check_he_rules(adj_mat, neighbors, nodes)
    if he_rules != -1:
        # dp[ind] = he_rules
        return he_rules


    # print([i for i in range(len(is_valid)) if is_valid[i]])

    best_node = nodes[0]
    for nd in nodes:
        if len(neighbors[nd]) < len(neighbors[best_node]):
            best_node = nd
    if 6 in nodes:
        best_node = 6
    added_edges = utilityAli.set_root(adj_mat, neighbors, best_node, is_valid)

    sm = [0]
    is_descendant = is_valid.copy()
    f_count(adj_mat, neighbors, best_node, is_valid, is_descendant, [], sm, dp, verbose=False)
    for s, e in added_edges:
        adj_mat[e][s] = 1
    dp[ind] = sm[0]

    if verbose:
        print("Counting DAGs on ", [k + 1 for k in nodes], " conditioned node is ", best_node+1, " answer is: ", dp[ind])

    return dp[ind]


def count_iterate_optimized(neighbors, source, dp, parents, hidden_CC, children_CCs, descendants_CCs, undirected_graph, verbose=False):
    if verbose:
        print("SS============================")
        print(neighbors, "\nsource: ", source, "\nparents: ", parents, "\nhidden_CC: ", hidden_CC, "\nchildren_CCs: ", children_CCs, "\ndescendants_CCs: ", descendants_CCs)
    children = neighbors[source]-parents

    sum_res = 0
    mult_res = 1
    for ccmp in children_CCs:
        #TODO: can change this
        k = count_optimized({i: ccmp&undirected_graph[i] for i in ccmp}, dp, verbose=verbose)
        mult_res *= k

    for ccmp in descendants_CCs:
        k = count_optimized({i: ccmp&undirected_graph[i] for i in ccmp}, dp, verbose=verbose)
        mult_res *= k

    g_graph = parents.union(hidden_CC)
    k = count_optimized({i: g_graph&undirected_graph[i] for i in g_graph}, dp, verbose=verbose)
    mult_res *= k

    sum_res += mult_res

    for c in children:
        # print(parents, undirected_graph[c], c, "ASDF")
        if len(parents) == 0 or c > max(parents) and parents.issubset(undirected_graph[c]):
        # print("liolul", utilityAli.seperate_graph({i: neighbors[i]&children for i in children}))
            tmp = [set(j.keys()) for j in (utilityAli.seperate_graph({i: neighbors[i]&children for i in children}))]

            c_comp = {}

            for cc in tmp:
                if c in cc:
                    c_comp = cc
            tmp.remove(c_comp)
            # print(c_comp," :/ ")
            # print({i: neighbors[i]&c_comp for i in c_comp})
            
            new_children_CCs, new_neighbors = utilityAli.set_root_optimized(c, {i: neighbors[i]&c_comp for i in c_comp})
            new_children_CCs = [set(i) for i in new_children_CCs]
            new_children_CCs.extend(tmp)
            mult_res = 1
            cp = {i: neighbors[i].copy() for i in neighbors}
            for node in cp[c]:
                if c in cp[node]:
                    cp[node].remove(c)

            cp[source].remove(c)
            cp[c].add(source)
            reachable = utilityAli.bfs_optimized(cp, source)

            new_desc_ccs = []
            new_hidden_CC = hidden_CC.copy()
            for cc in descendants_CCs:
                if cc.issubset(reachable):
                    new_desc_ccs.append(cc.copy())
                else:
                    new_hidden_CC = new_hidden_CC.union(cc)

            for i in new_hidden_CC:
                for j in cp[i]:
                    cp[j].add(i)

            # print("----------child: ", c)
            # print("Reachable: ", reachable)
            # print("New hidden: ", new_hidden_CC)
            # print("New descs: ", new_desc_ccs)
            # print("New children: ", new_children_CCs)
            # print(children_CCs)

            new_parents = parents.copy()
            new_parents.add(c)
            k = count_iterate_optimized(cp, source, dp, new_parents, new_hidden_CC, new_children_CCs, new_desc_ccs, undirected_graph, verbose=verbose)
            # print(k)
            sum_res += k

    return sum_res


def count_optimized(neighbors, dp, verbose=False):

    if verbose:
        print("Count on: ", neighbors.keys(),"                   ", neighbors)

    num_of_edges = sum([len(neighbors[i]) for i in neighbors]) / 2

    all_nodes = neighbors.keys()
    p = len(all_nodes)

    if p <= 1:
        return 1
    elif num_of_edges == p - 1:
        return (p)
    elif num_of_edges == p:
        return (2 * p)
    elif num_of_edges == p * (p - 1) / 2 - 1:
        return (2 * utilityAli.fact[p - 1] - utilityAli.fact[p - 2])
    elif num_of_edges == p * (p - 1) / 2:
        return (utilityAli.fact[p])
    elif num_of_edges == p * (p - 1) / 2 - 2:
        return ((p * p - p - 4) * utilityAli.fact[p - 3])

    ind = hash(str(neighbors.keys()))
    # if p > 5:
    if ind in dp:
        return dp[ind]


    tmp = list(all_nodes)
    best_node = tmp[0]
    for node in all_nodes:
        if len(neighbors[node]) < len(neighbors[best_node]):
            # print(len(neighbors[node]), len(neighbors[best_node]))
            best_node = node
    # if 6 in neighbors.keys():
    #     best_node = 6
    CCs, new_neighbors = utilityAli.set_root_optimized(best_node, neighbors)
    for i in range(len(CCs)):
        CCs[i] = set(CCs[i])
    children_CCs = [neighbors[best_node]]

    descandant_CCs =  []
    for cc in CCs:
        if not cc == children_CCs[0]:
            descandant_CCs.append(cc)
#    print("########################")
    num = count_iterate_optimized(new_neighbors, best_node, dp, set(), set(), children_CCs, descandant_CCs, neighbors, verbose=verbose)

    # if p > 5:
    dp[ind] = num

    return num


#import MECSizeHe
#AdjMat = utilityAli.read_adj_mat_from_file("AdjMat")
#
#N = len(AdjMat)
#neighbors = {}
#for i in range(len(AdjMat)):
#    neighbors[i] = set()
#    for j in range(len(AdjMat)):
#        if AdjMat[i][j] == 1:
#            neighbors[i].add(j)
#
#dp = {}
#
#print("Running LazyIter...")
##t.tic()
#c_opt = count_optimized(neighbors, dp, verbose=False)
#print("Ans: ", c_opt)
#print("Time: ", t.toc())
#print("DP Size: ", len(dp))
#
## count_iterate_optimized(neighbors, 2, dp, parents=set())
## print(utilityAli.set_root_optimized(0, neighbors))
#
#print("==================================")
#dp = {}
#print("Running MemoMAO...")
#t.tic()
#c3 = MECSizeHe.count3(neighbors, dp)
#print("Ans: ", c3)
#print("Time: ", t.toc())
#print("DP Size: ", len(dp))


