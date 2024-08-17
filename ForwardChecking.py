
# The purpose of this function is to find all empty cells in the Sudoku puzzle. 
""" Finding the empty cell which are equal to zero is the first step to solving the Sudoko Puzzle, once we locate the empty cells we can determine the possible numbers
    we can still use in the same 3x3 box """
def isEmpty(board): # board is the Sudoko puzzle in the form of a 2D matrix
    emptyCells = [] # This variable will store the position of all the empty cells.

    # This loop will iterate through the whole board, if it finds any empty cells it will append/add it to the  emptycell list
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                emptyCells.append((i, j))
    return emptyCells




# The purpose of this function is to check if it's valid to place a number in a given cell
def check(board, position, number): # board = the current state of the board ; position = the cells that are being checked ; number = the possible number that we want to place in the cell
    
    """ We'll start by check the row specified by position to see if there is a matching number in the same row, it will accomplish this by iterating through each column
        and checking the each cell in the same row passed in the variable posistion. (It will check each cell except the cell where we want to place the number) """
    for i in range(len(board[0])):
        if position[1] != i and board[position[0]][i] == number:
            return False

    """ Then we'll check the column specified by position to see if there is a matching number in the same column, it will accomplish this by iterating through each row
        and checking the each cell in the same column passed in the variable posistion. (It will check each cell except the cell where we want to place the number) """
    for i in range(len(board)):
        if position[0] != i and board[i][position[1]] == number:
            return False

    # Check if the number we want to place in the cell is in the 3x3 box
    # The next two variables will identify the top-left cell of the box in which position is located.
    boxRow = (position[0] // 3) * 3
    boxCol = (position[1] // 3) * 3

    for i in range(boxRow, boxRow + 3):
        for j in range(boxCol, boxCol + 3):
            if (i, j) != position and board[i][j] == number:
                return False
            
    # Will only return True if all checks (Row, Column, and 3x3 box) pass, otherwise False.
    return True



# The purpose of this function is to perform Forward Checking and generate domains for the empty cells
def forwardChecking(board):
    emptyCells = isEmpty(board)
    domains = {} # This dictionary will hold all the possible values for each empty cell

    for i in emptyCells: # Iterate the empty cells
        domains[i] = [] # For each empty cell, a list is created in the domains dictionary to store its domain of candidate values.
        for j in range(1, len(board) + 1): # Iterate through numbers 1 to 9 (Possible numbers to be placed in empty cells)
            if check(board, i, j): # If the number doesn't violate the constraints it will be added to the domain of the empty cell
                domains[i].append(j)

        # If the empty cell doesn't have any numbers in the domain it means that the puzzle's configuration is not correct --> unsolveable puzzle
        if domains[i] == []:
            domains[i].pop
    return domains


# The purpose of this function is to select the cell with the fewest remaining possible values to fill this cell.
def mrv(domain, board):
    cells_with_min_values = []
    temp = 10 # Initialize temp with a large value (greater than the maximum possible number of candidates)
    """ Why? each cell can have at most 9 candidates (the numbers 1-9). Therefore, initializing temp to a value greater than 9 ensures that the first empty 
    cell will always have fewer candidates, and its position will be added to the list of cells with the minimum candidates. """

    for i in domain:
        if len(domain[i]) == temp:
            cells_with_min_values.append(i)
        elif len(domain[i]) < temp:
            cells_with_min_values.clear()
            cells_with_min_values.append(i)
            temp = len(domain[i]) # The value of the temp is changed to the number of possible values of the first empty cell, further comparisions will be compared to that number

    # wWhen there are multiple cells with the same minimum number of remaining possible values, a tie breaker is needed --> Most constraining variable (Highest degree)
    if len(cells_with_min_values) > 1:
        return degree(cells_with_min_values, board)

    return cells_with_min_values.pop() # Returns the position of the selected cell to be filled next

# The purpose of this function is to calculate the degree heuristic for cell selection in case of a tie breaker needed in MRV
def degree(cells_with_min_values, board):
    deg = {} # A dictionary that will store the degrees of each empty cell passed in the parameters
    counter = 0 # Temp variable that will be used to count the number of degrees

    # Check the row, for each cell it counts how many other empty cells are in the same row.
    for i in cells_with_min_values:
        for j in range(len(board)):
            if board[i[0]][j] == 0:
                counter += 1
        deg[i] = counter
        counter = 0

    # Check the column, for each cell it counts how many other empty cells are in the same column.
    for i in cells_with_min_values:
        for j in range(len(board)):
            if board[j][i[1]] == 0:
                deg[i] += 1

    # Check the 3x3 box and counts how many other empty cells are in the same box.
    for w in cells_with_min_values:
        boxRow = (w[0] // 3) * 3
        boxCol = (w[1] // 3) * 3

        for i in range(boxRow, boxRow + 3):
            for j in range(boxCol, boxCol + 3):
                if board[i][j] == 0:
                    deg[w] += 1

    # Find the cell with the highest degree
    result = ()
    for i in deg:
        if deg[i] > counter:
            counter = deg[i]
            result = i

    return result # Cell with the highest degree


# The purpose of this function is to solve the Sudoku puzzle using Forward Checking
def solveFC(board):
    domain = forwardChecking(board) # The domains of all the empty cells
    if not domain: # if the domain is empty then the puzzle is not solvable
        return True

    minimum = mrv(domain, board) # determine the next empty cell to fill using the Minimum Remaining Values heuristic

    for i in domain[minimum]:
        board[minimum[0]][minimum[1]] = i # Replace the cell with the possible value
        if solveFC(board): # Recursive call to try to solve the puzzle with the current possible value placed in the selected cell.
            return True # means the puzzle can be solved
        board[minimum[0]][minimum[1]] = 0
    return False # means the puzzle cannot be solved