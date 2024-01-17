from ortools.sat.python import cp_model

def solve_sudoku(puzzle):
    model = cp_model.CpModel()

    # Create a 9x9 matrix of integer variables
    cells = [[model.NewIntVar(1, 9, f'cell{i}{j}') for j in range(9)] for i in range(9)]

    # Add constraints for each row and column to be different
    for i in range(9):
        model.AddAllDifferent([cells[i][j] for j in range(9)])  # Rows
        model.AddAllDifferent([cells[j][i] for j in range(9)])  # Columns

    # Add constraints for each 3x3 subgrid to be different
    for block_i in range(3):
        for block_j in range(3):
            model.AddAllDifferent([
                cells[i][j]
                for i in range(block_i * 3, (block_i + 1) * 3)
                for j in range(block_j * 3, (block_j + 1) * 3)
            ])

    # Add constraints for pre-filled cells
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                model.Add(cells[i][j] == puzzle[i][j])

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        for i in range(9):
            print([solver.Value(cells[i][j]) for j in range(9)])
    else:
        print("No solution found!")

# Sudoku puzzle
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solve_sudoku(puzzle)
