
import sys
import heapq
import queue
import numpy as np
import simplegraphs as sg

def shortestDirCycle(G):
    best_cost = np.Infinity #You should output this if you don't find any cycles
    best_node_list = [] #You should output this if you don't find any cycles

    def dijkstra(s):
        """
        get lightest path, return lightest cycle starting from s
        """

        visited = set() # keep track of nodes we've been to

        # keep track of the lightest paths to the nodes
        cost = {}
        cost[node] = 0

        parent = {} # keep track of parents in traversal
        min_cost = np.Infinity # init as infinite

        # set up priority queue
        Q = []
        heapq.heappush(Q, (cost[s], s))

        while len(Q) > 0:
            _, top = heapq.heappop(Q) # pop top item from heap

            if top not in visited:
                visited.add(top) # mark node as visited

                # iterate through neighbors of top
                for edge, w in G["adj"][top].items():
                    new_cost = w + cost[top] # get cost

                    # don't continue processing if same/more cost path
                    if new_cost >= best_cost:
                        continue
                    
                    # update node costs if they're less; add to queue
                    if edge not in cost or cost[edge] > new_cost:
                        cost[edge] = new_cost
                        parent[edge] = top
                        heapq.heappush(Q, (cost[edge], edge))
                    # the cycle has been completed, update its cost
                    elif new_cost < min_cost and edge == node:
                        min_cost = new_cost
                        parent[edge] = top
        
        # no cycles have been detected
        if min_cost == np.Infinity:
            return np.Infinity, []
        
        # setup traversal of cycle
        trav = parent[node]
        cycle = []

        # traverse and add nodes to cycle, until the cycle is completed
        while trav != s:
            cycle.append(trav)
            trav = parent[trav]

        cycle.append(s) # add source node to cycle

        return min_cost, cycle # return smallest cost + smallest cost cycle

    # process every node in the graph
    for node in G["adj"]:
        # run Dijkstra's on the given node, get results
        node_best_cost, node_best_node_list = dijkstra(node)

        # update the cost of the node if it's better than the current cost
        if node_best_cost < best_cost:
            best_cost = node_best_cost
            best_node_list = node_best_node_list

    # best_node_list in reverse order, since we originally traversed child->parent
    return best_cost, best_node_list[::-1]


############################################################
# input/output code. You shouldn't have to modify this. 
############################################################

def writeOutput(output_file, cost, node_list):
    # This takes the outputs of shortestHole and writes them
    # to a file with the name output_file
    with open(output_file, 'w') as f:
        f.write("{}\n{}\n".format(float(cost), node_list))
    return

def main(args=[]):
    # Expects two command-line arguments:
    # 1) name of a file describing the graph
    # 3) name of a file where the output should be written
    if len(args) != 2:
        print("Problem! There were {} arguments instead of 2.".format(len(args)))
        return
    graph_file = args[0]
    out_file = args[1]
    G = sg.readGraph(graph_file) # Read the graph from disk
    best_cost, best_node_list = shortestDirCycle(G) # Find the shortest hole!
    writeOutput(out_file, best_cost, best_node_list) # Write the output
    return     

if __name__ == "__main__":
    main(sys.argv[1:])    


