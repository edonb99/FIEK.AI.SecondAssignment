import heapq

class State:
    def __init__(self, queens, size):
        self.queens = queens  # positions of already placed queens: list of tuples (row, col)
        self.size = size  # size of the board (size x size)

    def is_goal(self):
        return len(self.queens) == self.size

    def successors(self):
        if self.is_goal():
            return []  # No successors from goal state

        next_col = len(self.queens)
        successors = []

        for next_row in range(self.size):
            if self.is_safe(next_row, next_col):
                # Copy current queens and add the new one
                new_queens = self.queens[:]
                new_queens.append((next_row, next_col))
                successors.append(State(new_queens, self.size))

        return successors

    def is_safe(self, row, col):
        for q_row, q_col in self.queens:
            # Check same row, diagonal, or same column (shouldn't need to check column in this setup)
            if q_row == row or q_col == col or abs(q_row - row) == abs(q_col - col):
                return False
        return True

    def __lt__(self, other):
        return len(self.queens) < len(other.queens)

def heuristic(state):
    # Number of remaining queens to place
    return state.size - len(state.queens)

def a_star(size):
    initial_state = State([], size)
    frontier = []
    heapq.heappush(frontier, (0, initial_state))  # (priority, state)

    while frontier:
        _, state = heapq.heappop(frontier)

        if state.is_goal():
            return state

        for successor in state.successors():
            # In this case, the cost is the number of queens placed + estimated queens remaining
            cost = len(successor.queens) + heuristic(successor)
            heapq.heappush(frontier, (cost, successor))

    return None  

def print_solution(state):
    board = [["." for _ in range(state.size)] for _ in range(state.size)]

    for row, col in state.queens:
        board[row][col] = "Q"

    for row in board:
        print(" ".join(row))

solution = a_star(8)  # Adjust size for different board sizes
if solution:
    print_solution(solution)
else:
    print("No solution found.")
