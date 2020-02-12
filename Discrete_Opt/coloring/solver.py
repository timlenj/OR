from collections import defaultdict
from ortools.sat.python import cp_model


def solve_it(input_data):

    #instantiate model + solver
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    node_range = range(node_count)

    #create the data structure for the tree
    edges = defaultdict(list)
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges[int(parts[0])].append(int(parts[1]))

    #half baked attempt to find an upper bound for unique colors needed
    color_max = max(len(edges.get(n)) for n in edges)

    nodes = []
    #create decision variables for each node
    for i in node_range:
        nodes.append(model.NewIntVar(1, color_max, 'n' + str(i)))

    #constraints nodes != edges
    for n in edges:
        for e in edges.get(n):
            model.Add(nodes[n] != nodes[e])

    #add symmetry breaking and redundant constraints

    #objective - minimize sum(colors)
    model.Minimize(sum(nodes[i] for i in node_range))

    #solve it
    solver.Solve(model)

    #set solution for printing
    solution = [solver.Value(nodes[i]) for i in node_range]

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

