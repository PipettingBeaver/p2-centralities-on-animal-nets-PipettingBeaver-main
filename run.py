## P2 Visualize Animal Social Networks
## Out: Friday Sept 20
## Due: Wednesday Oct 2
from pyvis.network import Network #from pyvis.network import Network
import matplotlib.pyplot as plt

def main():

    # File strings
    edgefile = str('files\zebra\zebra-edges.txt')   # Going with paper I picked before
    nodefile = str('files\zebra\zebra-nodes.txt')   # Going with paper I picked before

	## function calls
    print('1. Read Edges:')
    edgelist = read_edges(edgefile) # populate our edge list with output of edge file
    print(edgelist)

    print('2. Read Nodes:')
    nodes = read_nodes(nodefile)    # populate our dictionary with output of node file
    print(nodes)

    print('3. Calculate Degrees:')
    D = calculate_degree(edgelist)
    print(D)

    print('4. Calculate Clustering Coefficient:')
    C = calculate_clustering_coeff(edgelist)
    print(C)

    print('5. Calculate Closeness Centrality:')
    S = calculate_closeness(edgelist)
    print(S)

    return # done with main()


## write your functions here.
def read_edges(edgefile):
    # File format for edges is assumed to be two-category rows, like A B
    # we want to convert these to [A,B] tuple relationships in a list (edgelist)
    # Referenced Python wiki and Bio131 documents
    # Open file, query each line for contents (excluding whitespace),
    # consider tuple "A B" as parts 0 and 1 of a temporary array [A,B]
    # make sure they're consider integers, python....
    # add edge to list, iterate

    edgelist = set()  # Using a set to prevent duplicates (1,3) prevents (3,1)

    with open(edgefile, 'r') as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespace, no commas
            parts = line.split()  # Split line into parts

            edge = (int(parts[0]), int(parts[1]))  # Convert to integers
            edgelist.add(edge)

    return edgelist

def read_nodes(nodefile): ## NOTE this may have multiple inputs for the dolphin network.
    nodes = {} # Format: Node    Sex (Zebra)

    with open(nodefile, 'r') as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespace, no commas
            parts = line.split()  # Split line into parts
            #print("debug: ",parts)
            try:
                number = int(parts[0])
                node = (int(parts[0]), str(parts[1]))  # Convert to (integer, string) tuple
                nodes[node[0]] = node[1]            # integer is entry, string is key
            except ValueError:
                # Handle the case where parts[0] is not an integer, like the header
                #print("error reading line:",parts)
                pass
    return nodes

def calculate_degree(edgelist):
    # used adjmat_to_adjlist from P1 as framework of "for" loop
    # had to learn more about dictionary calls, incrementing integer key syntax
    D = {}

    for edge in edgelist:
        #parts = edge.split()
        aNode, bNode = edge
        #print("def D parts:",int(aNode)," and ",int(bNode))
        D[aNode] = 0	# Add aNode and bNode as empty terms to our dictionary
        D[bNode] = 0    # dictionary can not include duplicate terms, so no need to check

    for edge in edgelist:       #iterate through entries in edgelist
            aNode, bNode = edge # split [Integer, Integer] into [aNode] and [bNode]
            D[aNode] = int(D[aNode]) + 1  # get our term's current value as integer
            D[bNode] = int(D[bNode]) + 1  # for [A,B], increment A and B's value by 1
    return D

def calculate_clustering_coeff(edgelist):
    # Had my friend Kace tutor for me for writing this function
    # Create a dictionary to store the clustering coefficients, our output
    C = {}
    # Temporary dictionary to store the neighbors of each node
    neighbors = {}

    # Iterate through the edgelist and build the neighbor dictionary
    for edge in edgelist:
        u, v = edge         #split tuple
        neighbors[u] = neighbors.get(u, set()) | {v}
        neighbors[v] = neighbors.get(v, set()) | {u}

    # Calculate the clustering coefficient for each node
    for node, neighbors_set in neighbors.items():   # through every entry in neighbors
        degree = len(neighbors_set) # number of neighbors
        if degree < 2:  # Accounting for if a node has a single or zero neighbor
            C[node] = 0
        else:
            totalEdges = 0
            for neighbor1 in neighbors_set:
                for neighbor2 in neighbors_set:
                    if neighbor1 != neighbor2 and neighbor2 in neighbors[neighbor1]:
                        totalEdges += 1
            C[node] = totalEdges / (degree * (degree - 1) / 2)

    return C

def calculate_closeness(edgelist):
    S = {}  #shortest paths dictionary
    # breadth-first search

	# Template code from L2, had collaborated with Susan and Koko
	# s= StartingNode, given to function
	# Q= Queue, initially populated with A
	# X= Node being analyzed 
	# W= Distance (layers)

    # make a quick adj_list part 1
    adj_list = {}
    for edge in edgelist:
        #parts = edge.split()
        aNode, bNode = edge
        #print("def D parts:",int(aNode)," and ",int(bNode))
        adj_list[aNode] = 0	# Add aNode and bNode as empty terms to our dictionary
        adj_list[bNode] = 0    # dictionary can not include duplicate terms, so no need to check
    # make a quick adj_list part 2
    for i in range(len(edgelist)):
        for j in range(len(edgelist)):
            if adj_mat[i][j] == 1:	#jth entry of ith row
                adj_list[nodes[i]].append(nodes[j])

    for edge in edgelist:
        #parts = edge.split()
        aNode, bNode = edge
        #print("def D parts:",int(aNode)," and ",int(bNode))
        S[aNode] = float('inf')	# Add aNode and bNode as empty terms to our dictionary
        S[bNode] = float('inf')    # dictionary can not include duplicate terms, so no need to check

    for edge in edgelist:
        S[edge] = 0 #length from node to itself is 0
        Q = [edge] # initialize and populate queue of nodes to explore
        while len(Q) != 0: # while Q is nonempty:
            #print(Q," transfered to W")
            W = Q.pop(0)
            #print(W,"-->",adj_list[W]) # how to find entry for W in adj_list?
            for neighbor in adj_list[W]: #iterate over set or list
                #print(neighbor)
                if S[neighbor] == float('inf'):
                    S[neighbor] = S[W]+1
                    Q.append(neighbor)

    return S










# leave this at the bottom of the file
if __name__ == '__main__':
    main()
