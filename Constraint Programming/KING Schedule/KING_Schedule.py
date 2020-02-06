from __future__ import print_function
from ortools.sat.python import cp_model
import pandas as pd

#Trainers
#0 = G
#1 = R
#2 = C
#3 = Jan
#4 = Tiff

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_trainers, num_days, num_shifts, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_trainers = num_trainers
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._solutions = set(sols)
        self._solution_count = 0
        self._schedule = [[0 for c in range(num_days)] for r in range(num_shifts)]

    def on_solution_callback(self):
        trainers = ['G','R','C','J','T']
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in range(self._num_days):
                for s in range(self._num_shifts):
                    for n in range(self._num_trainers):
                        if self.Value(self._shifts[(n,d,s)]) == 1:
                            self._schedule[s][d] = trainers[n]
            print(pd.DataFrame(self._schedule))
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count


def main():
    # Data.
    num_trainers = 5
    num_shifts = 7
    num_days = 5
    all_trainers = range(num_trainers)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: trainer 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_trainers:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d,
                        s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    ##CONSTRAINTS##
    #One trainer per class
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_trainers) == 1)

    #No one works a full day
    for n in all_trainers:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 7)
    #Min 2 shifts
    for n in all_trainers:
        num_shifts_worked = sum(
            shifts[(n, d, s)] for d in all_days for s in all_shifts)
        model.Add(2 <= num_shifts_worked)
        model.Add(num_shifts_worked <= 15)
    
    #Gerrick does not work Wednesday, Thursday, Friday
    model.Add(sum(shifts[(0, 2, s)] for s in all_shifts) == 0)
    model.Add(sum(shifts[(0, 3, s)] for s in all_shifts) <= 1)
    model.Add(sum(shifts[(0, 4, s)] for s in all_shifts) <= 2)

    #Only Gerrick, Chris and Rob teach 5AM
    model.Add(sum(shifts[(3,d,0)] for d in all_days) == 0)
    model.Add(sum(shifts[(4,d,0)] for d in all_days) == 0)

    #Tiff only works nights
    for d in all_days:
        model.Add(sum(shifts[(4,d,s)] for s in range(5)) == 0)

    #But Rob only teaches up to 2
    model.Add(sum(shifts[(1,d,0)] for d in all_days) <= 2)
    #you can't work last class and first class right after more than 1 day a week
    for n in all_trainers:
        for d in range(num_days-1):
            model.Add(shifts[(n, d, 6)] + shifts[(n,d+1,0)]<=2)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first five solutions.
    a_few_solutions = range(5)
    solution_printer = SolutionPrinter(shifts, num_trainers,
                                                    num_days, num_shifts,
                                                    a_few_solutions)
    solver.SearchForAllSolutions(model, solution_printer)

    # Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main()