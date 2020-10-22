from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import timeit
from ortools.sat.python import cp_model

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print solutions."""

    def __init__(self, variables, rows):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__rows = rows
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for row in self.__rows:
            r = [self.Value(v) for v in row]
            print(r)

    def solution_count(self):
        return self.__solution_count


def solve(puzzle):
    
    model = cp_model.CpModel()

    int_vars = []
    rows = []
    cols = []
    blks = []

    for _ in range(9):
        rows.append([])
        cols.append([])
        blks.append([])

    for row in range(9):
        for col in range(9):
            if puzzle[col + 9*row] == '.':
                new_var = model.NewIntVar(1, 9, "item_"+str(row)+str(col))
            else:
                new_var = model.NewConstant(int(puzzle[col + 9*row]))
            
            int_vars.append(new_var)
            rows[row].append(new_var)
            cols[col].append(new_var)

            if (0 <= row < 3) and (0 <= col < 3): blks[0].append(new_var)
            if (0 <= row < 3) and (3 <= col < 6): blks[1].append(new_var)
            if (0 <= row < 3) and (6 <= col < 9): blks[2].append(new_var)

            if (3 <= row < 6) and (0 <= col < 3): blks[3].append(new_var)
            if (3 <= row < 6) and (3 <= col < 6): blks[4].append(new_var)
            if (3 <= row < 6) and (6 <= col < 9): blks[5].append(new_var)

            if (6 <= row < 9) and (0 <= col < 3): blks[6].append(new_var)
            if (6 <= row < 9) and (3 <= col < 6): blks[7].append(new_var)
            if (6 <= row < 9) and (6 <= col < 9): blks[8].append(new_var)

    # Rows
    for row in rows: model.AddAllDifferent(row)
    for col in cols: model.AddAllDifferent(col)
    for blk in blks: model.AddAllDifferent(blk)

    solver = cp_model.CpSolver()
    solution_printer = SolutionPrinter(int_vars, rows)

    status = solver.SearchForAllSolutions(model, solution_printer)
    print('\nSolver status:', solver.StatusName(status))


if __name__ == "__main__":
    
    # https://qqwing.com/generate.html

    puzzle = '..9.7.....7.1....5......7.835.7..1.6.....3...61.8..4.7......8.4.6.5....1..1.2....'

    print('\nSolve:', puzzle)
    print()

    start = timeit.default_timer()
    solve(puzzle)   
    print('\nTime required:', round(timeit.default_timer() - start, 4))
    