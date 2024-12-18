## P2 Visualize Animal Social Networks
## Out: Friday Sept 20
## Due: Wednesday Oct 2
from pyvis.network import Network #from pyvis.network import Network
import matplotlib.pyplot as plt

def main():

    # File strings
    edgefile = str('files/zebra/zebra-edges.txt')   # Going with paper I picked before
    nodefile = str('files/zebra/zebra-nodes.txt')   # Going with paper I picked before

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

    viz_graph(edgelist,nodes,C, S,'ZebraNetwork.html')

    CompareMeasures(nodes, D, C, S, "NodeData.txt")

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

    with open(edgefile, 'r') as f:  #
        for line in f:
            line = line.strip()     # Remove leading/trailing whitespace, no commas
            parts = line.split()    # Split line into parts

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
            C[node] = totalEdges / (degree * (degree - 1) / 1)

    return C

def calculate_closeness(edgelist):
    S = {}  #closeness dictionary
    # found via breadth-first search near end of function

    # Template code from L2, had collaborated with Susan and Koko
    # s= StartingNode, given to function
    # Q= Queue, initially populated with A
    # X= Node being analyzed 
    # W= Distance (layers)

    # make a quick adj_list - Code sourced from my P3 and Gabe's help
    adjlist = {}
    for aNode, bNode in edgelist:
            # Adjlist - Dictionary
            # We are assuming undirected, so Add B to A, A to B
            # With dictionary, we do not have to worry about duplicate keys, but second if is about duplicate values
            if aNode not in adjlist: adjlist[aNode] = []
            if bNode not in adjlist[aNode]: adjlist[aNode].append(bNode)

            if bNode not in adjlist: adjlist[bNode] = []
            if aNode not in adjlist[bNode]: adjlist[bNode].append(aNode)

    # # make a quick adj_list part 2
    # for i in range(len(edgelist)):
    #     for j in range(len(edgelist)):
    #         if adj_mat[i][j] == 1:	#jth entry of ith row
    #             adj_list[nodes[i]].append(nodes[j])

    # Shortest paths algorithm
    print(adjlist)
    for Node in adjlist:
        #print(Node)
        DistanceToNode = {}
        for edge in edgelist:
            #parts = edge.split()
            aNode, bNode = edge
            #print("def D parts:",int(aNode)," and ",int(bNode))
            DistanceToNode[aNode] = float('inf')	# Add aNode and bNode as empty terms to our dictionary
            DistanceToNode[bNode] = float('inf')    # dictionary can not include duplicate terms, so no need to check

        DistanceToNode[Node] = 0 #length from node to itself is 0
        Q = [Node] # initialize and populate queue of nodes to explore
        while len(Q) != 0: # while Q is nonempty:
            #print(Q," transfered to W")
            W = Q.pop(0)
            #print(W,"-->",adj_list[W]) # how to find entry for W in adj_list?
            for neighbor in adjlist[W]: #iterate over set or list
                #print(neighbor)
                if DistanceToNode[neighbor] == float('inf'):
                    DistanceToNode[neighbor] = DistanceToNode[W]+1
                    Q.append(neighbor)
        #finished looking at queue, now need to put S through equation
        PathTotal = 0
        for Node2 in DistanceToNode:             # DistanceToNode[A: 0, 2, 2, 2, 3]
            PathTotal += DistanceToNode[Node2]
        S[Node] = ((len(adjlist) - 1)/(PathTotal))
        print(S)

    return S

def viz_graph(edgelist,nodelist,C, S,outfile):

    # Refer to Lab 1 for instructions about visualizing a graph.

    G = Network() # create undirected graph

    # when Tnodelist is finished, switch the "for" line:
    #for n, Name, src in Tnodelist:

    for Node in nodelist:
        # line to convert n from Ensemble to Common Gene Name
        #Name = n # comment out when Tnodelist Finished
        #
        if nodelist[Node] == "male": # This is the starting node
            G.add_node(Node,label=Node,shape="square", size=10,color=rgb_to_hex(0,C[Node],0))
        elif nodelist[Node] == "female": 
            G.add_node(Node,label=Node,shape="circle", size=3, color=rgb_to_hex(C[Node],0,0))
        else:
            G.add_node(Node,label=Node,shape="triangle",size=10, color=rgb_to_hex(C[Node],C[Node],C[Node]))

    for u,v in edgelist:
        G.add_edge(u,v,width=1.0)

    G.toggle_physics(True)
    G.show_buttons(filter_=('physics'))
    G.write_html(outfile)

    print("viz_graph done, ",outfile)
    return

def rgb_to_hex(red,green,blue): # pass in three values between 0 and 1
  maxHexValue= 255  ## max two-digit hex value (0-indexed)
  r = int(red*maxHexValue)    ## rescale red
  g = int(green*maxHexValue)  ## rescale green
  b = int(blue*maxHexValue)   ## rescale blue
  RR = format(r,'02x') ## two-digit hex representation
  GG = format(g,'02x') ## two-digit hex representation
  BB = format(b,'02x') ## two-digit hex representation
  return '#'+RR+GG+BB



    # Finally, compare the node measures in your network.
    # For this, you will either need to print a table to the terminal or write the values to a file.
    # In the comments (lines starting with #), write a description of this comparison.

    # :bulb: You can choose to write a separate compare() function or write this code directly in the main() function.

    # :bulb: I encourage you to plot these values for each node in any way you'd like (a spreadsheet, in R, or in Python - see the first challenge below). This will help you get a broad sense of the relationships among these three measures.

    # Plot the degree, clustering coefficient, and the closeness centrality for every node using matplotlib functions (e.g., scatter plots, line plots, or bar plots). Take a look at L1 code, as well as this matplotlib gallery with different visualization options.
    # 
def CompareMeasures(nodelist, D, C, S, outfile):

  # Analysis of nodes and measures
  # Review of NodeData.txt :
  # There's a tendency for nodes with higher degree centrality to also have higher closeness centrality.
  # This suggests nodes that are more connected are likely to have shorter paths to other nodes.

    combined = {}
    # search through each dictionary for node, they're call in [Node, Value] format so should match
    for entry in [D, C, S]:
        for key, value in entry.items():
            if key not in combined:
                combined[key] = []
            combined[key].append(value)


    with open(outfile, "w") as file:
        file.write("Node, Degree, Centrality, Closeness")
        for node, values in combined.items():
            file.write(f"\n{node}, {','.join(map(str, values))}")

    print(f"{outfile} created")



    return

# leave this at the bottom of the file
if __name__ == '__main__':
    main()
