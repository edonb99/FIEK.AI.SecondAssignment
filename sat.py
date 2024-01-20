from ortools.sat.python import cp_model

num_guests = 100
num_tables = 10
guests_per_table = 10  

model = cp_model.CpModel()

# SAT Decision variables
seats = {}
for i in range(num_guests):
    for j in range(num_tables):
        seats[(i, j)] = model.NewBoolVar(f'guest_{i}_table_{j}')

# SAT Constraints
# Constraint 1: Each guest must sit at exactly one table
for i in range(num_guests):
    model.Add(sum(seats[(i, j)] for j in range(num_tables)) == 1)

# Constraint 2: Certain guests cannot sit together
cannot_sit_together = [(0, 1), (2, 3)]
for a, b in cannot_sit_together:
    for j in range(num_tables):
        model.AddBoolOr([seats[(a, j)].Not(), seats[(b, j)].Not()])

# Constraint 3: Certain guests must sit together
must_sit_together = [(4, 5), (6, 7)]
for a, b in must_sit_together:
    for j in range(num_tables):
        model.AddImplication(seats[(a, j)], seats[(b, j)])
        model.AddImplication(seats[(b, j)], seats[(a, j)])

# Constraint 4: Fixed number of guests per table
for j in range(num_tables):
    model.Add(sum(seats[(i, j)] for i in range(num_guests)) == guests_per_table)

# SAT Solver
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Output
if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    for j in range(num_tables):
        print(f"Table {j}: ", end="")
        for i in range(num_guests):
            if solver.Value(seats[(i, j)]):
                print(f"Guest {i} ", end="")
        print()  
else:
    print("No solution could be found.")
