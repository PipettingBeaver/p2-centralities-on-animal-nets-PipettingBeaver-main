import run

# values for toy dataset
edgelist = [['A', 'B'], ['B', 'C'], ['B', 'D'], ['D', 'E'], ['D', 'G'], ['E', 'G'], ['E', 'F']]
nodes = ['A','B','C','D','E','F','G']
degrees = {'A': 1, 'B': 3, 'C': 1, 'D': 3, 'E': 3, 'G': 2, 'F': 1}
clustcoeff = {'A': 0, 'B': 0.0, 'C': 0, 'D': 0.3333333333333333, 'E': 0.3333333333333333, 'G': 1.0, 'F': 0}
closeness = {'A': 0.4, 'B': 0.6, 'C': 0.4, 'D': 0.6666666666666666, 'E': 0.5454545454545454, 'G': 0.5, 'F': 0.375}
test_degrees = run.calculate_degree(edgelist)
test_clustcoeff = run.calculate_clustering_coeff(edgelist)
test_closeness = run.calculate_closeness(edgelist)

def test_read_edges():
    test = run.read_edges('files/toy/toy-edges.txt')
    assert len(edgelist) == len(test)
    for edge in edgelist:
        assert edge in test
    return

def test_degree_A():
    assert degrees['A'] == test_degrees['A']
    
def test_degree_B():
    assert degrees['B'] == test_degrees['B']

def test_degree_C():
    assert degrees['C'] == test_degrees['C']

def test_degree_D():
    assert degrees['D'] == test_degrees['D']

def test_degree_E():
    assert degrees['E'] == test_degrees['E']

def test_degree_F():
    assert degrees['F'] == test_degrees['F']

def test_degree_G():
    assert degrees['G'] == test_degrees['G']

def test_clustcoeff_A():
    assert clustcoeff['A'] == test_clustcoeff['A']
    
def test_clustcoeff_B():
    assert clustcoeff['B'] == test_clustcoeff['B']

def test_clustcoeff_C():
    assert clustcoeff['C'] == test_clustcoeff['C']

def test_clustcoeff_D():
    assert clustcoeff['D'] == test_clustcoeff['D']

def test_clustcoeff_E():
    assert clustcoeff['E'] == test_clustcoeff['E']

def test_clustcoeff_F():
    assert clustcoeff['F'] == test_clustcoeff['F']

def test_clustcoeff_G():
    assert clustcoeff['G'] == test_clustcoeff['G']

def test_closeness_A():
    assert closeness['A'] == test_closeness['A']
    
def test_closeness_B():
    assert closeness['B'] == test_closeness['B']

def test_closeness_C():
    assert closeness['C'] == test_closeness['C']

def test_closeness_D():
    assert closeness['D'] == test_closeness['D']

def test_closeness_E():
    assert closeness['E'] == test_closeness['E']

def test_closeness_F():
    assert closeness['F'] == test_closeness['F']

def test_closeness_G():
    assert closeness['G'] == test_closeness['G']