#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd

def trivialGreedy(items, capacity):
    #greedy algorithm - goes through items in order and adds to bag if it fits
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    a = (value, taken)
    return a

def optimisticEstimate(items, capacity):
    #optimistic estimate by linear relaxation
    value = 0
    weight = 0
    taken = [0]*len(items)
    
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
            
    for item in items:
        if taken[item.index] == 0 and weight < capacity:
            value += item.value*((capacity-weight)/item.weight)
            weight += capacity-weight
            
    return value
    
def dynamicProgramming(items, capacity):
    #dynamic programming model
    value = 0
    taken = [0]*len(items)
    
    table = [[0 for c in range(len(items))] for r in range(capacity)]
    weights = [[0 for c in range(len(items))] for r in range(capacity)]
    takenTable = [[[0 for i in range(len(items))] for c in range(len(items))] for r in range(capacity)]
    
    for c in range(len(items)):
        #reset firstEntry for the column/new item
        firstEntry = 0
        for r in range(capacity):
            #evaluate first column and set value where item passes constraint
            if c == 0 and items[0].weight <= r+1:
                table[r][c] = items[0].value
                weights[r][c] = items[0].weight
                takenTable[r][c][c] = 1 
            else:
                
            #for all other columns
                
                #set cell in table to be equal to previous best
                table[r][c] = table[r][c-1]
                weights[r][c] = weights[r][c-1]
                takenTable[r][c] = list(takenTable[r][c-1])
                  
                #if current item > previous best
                if items[c].weight <= r+1 and items[c].value > table[r][c]:
                    table[r][c] = items[c].value
                    weights[r][c] = items[c].weight
                    takenTable[r][c][c] = 1
                    takenTable[r][c][c-1] = 0
                    
                #try to find first entry point
                if (r > 0 and table[r][c] != 0 and table[r-1][c] == 0) or (r==0 and table[r][c] != 0):
                        firstEntry = r
                        
                
                #see if any combination of new item with old item values trumps previous best (same row, one column over)
                if items[c].weight <= r+1 and firstEntry > 0 and items[c].value + table[r-(firstEntry+1)][c-1] > table[r][c] \
                and items[c].weight + weights[r-(firstEntry+1)][c-1] <= r+1:
                    table[r][c] = items[c].value + table[r-(firstEntry+1)][c-1]
                    weights[r][c] = items[c].weight + weights[r-(firstEntry+1)][c-1]
                    takenTable[r][c] = list(takenTable[r-(firstEntry+1)][c-1])
                    takenTable[r][c][c] = 1
                    #print("added:", items[c].value , table[r-(firstEntry+1)][c-1], "FE:", firstEntry)
                
                #print(pd.DataFrame(table))
                
    #set value to be last (bottom right) cell in table
    value = table[capacity-1][len(items)-1]
    taken = takenTable[capacity-1][len(items)-1]
    a = (value, taken)
    return a

from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
        
    #optimistic estimate
    print("Optimistic Estimate (Linear Relaxation):", optimisticEstimate(items, capacity))
    
    #call algo and output results
    algoResult = dynamicProgramming(items, capacity)
    value = algoResult[0]
    taken = algoResult[1]
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

