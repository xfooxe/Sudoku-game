# this code to implement a backtracking algorithm to solve Sudoku puzzles.


# to checks if there are any empty cells and return it's coordinates if empty
def isEmpty(sudoku):
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0:
                return (i, j) 
    return None



# To determine whether the number is in the correct place or not according to Sudoku
def check(sudoku, position, number):
    # Check the row for the given position
    for i in range(len(sudoku[0])):
        if position[1] != i and sudoku[position[0]][i] == number:
            return False

    #Check the column for the given position
    for i in range(len(sudoku)):
        if position[0] != i and sudoku[i][position[1]] == number:
            return False

    # Check the box containing the specified position
    boxRow = (position[0] // 3) *3
    boxCol = (position[1] // 3) *3

    for i in range(boxRow, boxRow + 3):
        for j in range(boxCol, boxCol + 3):
            if (i,j) != position and sudoku[i][j] == number:
                return False
    return True



# implementation of a backtracking algorithm
def solveBT(sudoku):
    if isEmpty(sudoku):
        row, col = isEmpty(sudoku)
    else:
        return True

    for i in range(1,10):
        if check(sudoku, (row, col), i):
            sudoku[row][col] = i

            if solveBT(sudoku):
                return True

            sudoku[row][col] = 0

    return False



