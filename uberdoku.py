import numpy as np
from datetime import datetime
from ortools.sat.python import cp_model


def load_file(f_name: str) -> np.array:
    # create np.array of incoming file
    output = []
    with open(f_name, 'r') as infile:
        for line in infile:
            output.append([letter_to_num(l) for l in line.strip().split(',')])
    return np.array(output)


def print_board(board: np.array) -> None:
    for r in board:
        print(' '.join([num_to_letter(i) for i in r]))


def num_to_letter(i: int) -> str:
    # need to decrement by 1, so 1-G is out as 0-F
    if 1 <= i <= 10:
        return str(i-1)
    elif 11 <= i <= 16:
        return chr(i+86).upper()
    return " "


def letter_to_num(in_letter: str) -> int:
    # need to rotate by 1 so input is 0-F, output is 1-G
    letter = in_letter.lower()
    if letter in "012345678":
        return int(letter)+1
    if letter == "9":
        return 10
    elif letter in "abcdef":
        return ord(letter)-86
    return 0


def solve(board: np.array) -> (np.array, float):
    """Solve a 16x16 sudoku, returning its computational time as well as the
    solution"""
    assert board.shape == (16, 16)
    rows = cols = len(board)
    regions = 4
    model = cp_model.CpModel()

    values = {}
    for i in range(rows):
        for j in range(cols):
            if board[i, j] != 0:
                # defined by board
                values[i, j] = board[i, j]
            else:
                # place variables where holes are
                values[i, j] = model.NewIntVar(
                    1, rows, f"{i}, {j}",
                )

    # constraints!
    for i in range(rows):
        # rows are all different
        model.AddAllDifferent([values[i, j] for j in range(rows)])

    for j in range(cols):
        # cols are all different
        model.AddAllDifferent([values[i, j] for i in range(cols)])

    for r in range(0, rows, regions):
        for c in range(0, cols, regions):
            # all values in a region are different
            model.AddAllDifferent(
                [values[r+i, j] for j in range(
                    c, (c+regions)
                ) for i in range(regions)]
            )
    solver = cp_model.CpSolver()
    start = datetime.now()
    status = solver.Solve(model)
    elapsed = datetime.now() - start
    results = np.zeros((rows, cols)).astype(np.int)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(rows):
            for j in range(cols):
                results[i, j] = int(solver.Value(values[i, j]))
    else:
        raise RuntimeError(
            f"failed to solve, status: {solver.StatusName(status)}")

    return results, elapsed.total_seconds()


input_board = load_file('input.csv')
print("Your board:")
print_board(input_board)
solution, solve_time = solve(input_board)
print(f"Solution found in: {solve_time} seconds")
print_board(solution)
