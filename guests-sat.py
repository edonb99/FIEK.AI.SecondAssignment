from ortools.sat.python import cp_model


num_guests = 100
num_tables = 10
guests_per_table = 10  

model = cp_model.CpModel()

# Decision variables
# seats[i][j]=true if guest 'i' is at table 'j'
seats = {}
for i in range(num_guests):
    for j in range(num_tables):
        seats[(i, j)] = model.NewBoolVar(f'guest_{i}_table_{j}')

#each guest must sit at exactly one table
for i in range(num_guests):
    model.Add(sum(seats[(i, j)] for j in range(num_tables)) == 1)

cannot_sit_together = [(0, 1), (2, 3)] 
must_sit_together = [(4, 5), (6, 7)]
#guests who cannot sit together check
for a, b in cannot_sit_together:
    for j in range(num_tables):
        model.AddBoolOr([seats[(a, j)].Not(), seats[(b, j)].Not()])

#guests that must sit together check
for a, b in must_sit_together:
    for j in range(num_tables):
        # If guest a is at table j, then guest b must also be at table j
        model.AddImplication(seats[(a, j)], seats[(b, j)])
        model.AddImplication(seats[(b, j)], seats[(a, j)])

#nr of guests per table to the desired amount
for j in range(num_tables):
    model.Add(sum(seats[(i, j)] for i in range(num_guests)) == guests_per_table)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    for j in range(num_tables):
        print(f"Table {j}: ", end="")
        for i in range(num_guests):
            if solver.Value(seats[(i, j)]):
                print(f"Guest {i} ", end="")
        print()  
else:
    print("No solution could be found.")