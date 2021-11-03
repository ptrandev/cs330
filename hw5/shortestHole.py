#
# Collaborators:
# Dominic Maglione
# Mikayla Steinberg
# Huy Phan
# Malik Baker
# Daniel Melchor
#

import sys
import numpy as np
import simplegraphs as sg


def shortestHole(G,s):
    ########################################
    # Write code that finds the shortest hole containing s if one exists
    # If one exists, set 'found' to True
    # Set hole_length to be the length of the shortest hole
    # Set hole_nodes to be a list of the nodes in the hole in order,
    #    starting from s (and not repeating s)
    ########################################
    
    d, parents, layers = sg.BFS(G, s) # get shortest paths from BFS
    verified_nodes = set() # keep track of nodes we've verified via memoization

    def getNodes(node, p1, p2):
        """
            return 2 nodes w/ different parents, allows us to traverse both ways
            through a cycle w/ out going through the same path
        """

        if parents[node] == p1:
            return [node, p2]
        return [node, p1]

    def checkCycle(nodes, parents, s):
        """
            verifies that a cycle contains the source node s
        """

        # generate keys for verifying nodes
        k = f"{nodes[0]},{nodes[1]}"
        k2 = f"{nodes[1]},{nodes[0]}"

        # already verified these nodes, return early
        if k in verified_nodes or k2 in verified_nodes:
            return False, -1, []

        # keep track of length and nodes of hole
        hole_length = 0
        hole_nodes = []

        # verify if paths form a cycle to the s node
        # 0 = neither reached, 1 = one reached, 2 = both reached
        reached_s = 0

        trav = nodes[0] # start traversing at node 0

        # add nodes to the right side of the list
        while trav:
            # the trav node is not the source node
            if trav != s:
                # increment len by 1, add trav node to array
                hole_length += 1
                hole_nodes += [trav]

            trav = parents[trav] # go onto next node

            # we have reached the source node, increment reached_s by 1
            if trav == s:
                reached_s += 1

        trav = nodes[1] # start traversing at node 1

        # add nodes to the left side of the list
        while trav:
            # the trav node is not the source node
            if trav != s:
                # increment len by 1, add trav node to array
                hole_length += 1
                hole_nodes = [trav] + hole_nodes

            trav = parents[trav] # go onto next node

            # we have reached the source node, increment reached_s by 1
            if trav == s:
                reached_s += 1

        hole_length += 1 # hole becomes 1 longer due to adding start node
        hole_nodes = [s] + hole_nodes # add start node to hole_nodes

        unique_nodes = np.unique(hole_nodes) # get unique nodes from hole_nodes

        # if not all nodes unique or both paths didn't reach s...
        if not len(unique_nodes) == len(hole_nodes) or reached_s != 2:
            verified_nodes.add(k) # add key of nodes to verified_nodes
            return False, -1, [] # return falsy values

        return True, hole_length, hole_nodes # checks passed, s is part of hole

    # find connected nodes
    for i, layer in enumerate(layers):
        shared_nodes = {} # keep track of nodes in common

        # keep track of shortest cycle length and path in layer
        layer_shortest_len = len(G['adj'].keys()) + 1
        layer_shortest_path = []

        # iterate through every node v in layer
        for v in layer:
            shared_nodes[v] = parents[v]

            # get neighbors u of node v
            for u in G['adj'][v]:
                if u != parents[v]:
                    # nodes in same layer have mutual edge
                    if u in shared_nodes:
                        nodes = getNodes(u, shared_nodes[u], v)

                        # check if cycle contains s
                        found, hole_length, hole_nodes = checkCycle(nodes, parents, s)

                        # update values if found cycle is shorter
                        if found and hole_length < layer_shortest_len:
                            layer_shortest_path = hole_nodes
                            layer_shortest_len = hole_length
                    
                    shared_nodes[u] = v # set node in common
        
        # shortest cycle found, return
        if len(layer_shortest_path) > 0:
            return True, layer_shortest_len, layer_shortest_path

    return False, -1, [] # unable to find a hole, return falsy values

#########################################################
# Don't modify the stuff below this line for submission
# (Of course you can change it while you're
#    doing your own testing if you want)
#########################################################


def readSource(start_file):
    # The source vertex is listed in its own file
    # It is an integer on a line by itself.
    with open(start_file, 'r') as f:
        raw_start = f.readline()
        s = int(raw_start)
    return s



def writeOutput(output_file, hole_found, hole_length, hole_list):
    # This takes the outputs of shortestHole and writes them
    # to a file with the name output_file
    with open(output_file, 'w') as f:
        f.write("{}\n".format(hole_found))
        f.write("{}\n".format(hole_length))
        f.write("{}\n".format(hole_list))
    return



def main(args=[]):
    # Expects three command-line arguments:
    # 1) name of a file describing the graph
    # 2) name of a file with the ID of the start node
    # 3) name of a file where the output should be written
    if len(args) != 3:
        print("Problem! There were {} arguments instead of 3.".format(len(args)))
        return
    graph_file = args[0]
    start_file = args[1]
    out_file = args[2]
    G = sg.readGraph(graph_file) # Read the graph from disk
    s = readSource(start_file) # Read the source from disk
    hole_found, hole_length, hole_list = shortestHole(G,s) # Find the shortest hole!
    writeOutput(out_file, hole_found, hole_length, hole_list) # Write the output
    return 

if __name__ == "__main__":
    main(sys.argv[1:])    

    
