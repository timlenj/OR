from ortools.sat.python import cp_model
import pandas as pd
from random import seed
from random import randint
from random import choice
from datetime import datetime

class sudoku():
    def __init__(self):
        self.board =  [[0 for c in range(9)] for r in range(9)]
        
    def randboard(self):
        #crude Sudoku board generator
        x = [[0 for c in range(9)] for r in range(9)]
        nums = list(range(10))
        
        #seed the rand # gen
        seed(datetime.now())
        
        #insert #s
        while len(nums)>0:
            #select an index at random
            i = randint(0,8)
            j = randint(0,8)
            #insert random element from nums if index has not been selected already
            if x[i][j] == 0:
                sel = choice(nums)
                x[i][j] = sel
                nums.remove(sel)
        #set the board
        self.board = x
        
    def solve(self):
        #solve self.board
        solver = cp_model.CpSolver()
        model = cp_model.CpModel()
        
        #create data structure to hold variables
        x = [[0 for c in range(9)] for r in range(9)]
        #create the variables and assign to the data structure
        for i in range(9):
            for j in range(9):
                x[i][j] = model.NewIntVar(1, 9, 'x' + str(i) + str(j))
        #constraints
        #assign values from the start board
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    model.Add(x[i][j] == self.board[i][j])
        #rows all different
        for i in range(9):
            model.AddAllDifferent(x[i])
        #columns all different
        for j in range(9):
            consvars = []
            for i in range(9):
                consvars.append(x[i][j])
            model.AddAllDifferent(consvars)
        #3x3 squares all different
        for z in range(3):
            for m in range(3):
                consvars = []
                for j in range(3):
                    for i in range(3):
                        consvars.append(x[i+z*3][j+m*3])
                model.AddAllDifferent(consvars)
        #solve
        solver.Solve(model)
        solved = [[0 for c in range(9)] for r in range(9)]
        #print result
        for i in range(9):
            for j in range(9):
                solved[i][j] = solver.Value(x[i][j])
        print(pd.DataFrame(solved))
    
s = sudoku()
s.randboard()
s.solve()