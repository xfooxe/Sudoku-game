import copy

class CSP:
    def __init__(self, cell, domains, arcs, constraints):
        self.cell = cell
        self.domains = domains
        self.constraints = constraints
        self.arcs = arcs

# to checks if there are any empty cells and return it's coordinates if empty
def isEmpty(sudoku):
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0:
                return False 
    return True

#calculate the range of a 3x3 box in a Sudoku puzzle based on the given index x
def boxRange(x): 
    return range((x//3)*3,(x//3)*3+3)


# generates arcs  list vij if it is in same row or column, or in same grid
def generateArc(x,y):
    l = []
    for i in range(0,9):
        for j in range(0,9):
            if  (i != x or y != j) and (i == x or j == y or (i in boxRange(x) and j in boxRange(y))):
                l.append('X'+str(i)+str(j))
    return l

# check if constraint is satisfied
def constraints(x,y):
    return x != y


# identify the unassigned variable with the fewest remaining domain values 
def unassignedVariable(csp):
    unassigned_variables = filter(lambda y: len(y[1]) > 1, csp.domains.items())
    variable_with_fewest_values = min(unassigned_variables, key=lambda x: len(x[1]))
    return variable_with_fewest_values


#least constraining value heuristic
def orderDomain(csp, var, domain):
    def neighbor(val): #number of neighboring variables
        num = 0
        neighbours = generateArc(int(var[1]), int(var[2])) 
        for n in neighbours:
            if val in csp.domains[n]:
                num += 1
        return num
    domain.sort(key = lambda x: neighbor(x)) #sorts the domain based on the number of neighbor.
    return domain


#checks if there is a conflict with any neighbors whose domain size = 1
def consistentAssignment(csp, var, value):
    neighbors = generateArc(int(var[1]), int(var[2]))
    for n in neighbors:
        if ((len(csp.domains[n]) == 1) and (value in csp.domains[n])):
            return False
    return True


#checks if there exist any values in the domain of Xi that are inconsistent with the values in the domain of Xj
def revise(csp, Xi, Xj):
    revised = False
    for x in csp.domains[Xi]:
        # Checks if there is any value y in the domain of Xj that violates the constraint between x and y
        if all(not csp.constraints(x, y) for y in csp.domains[Xj]):
            # Removes the inconsistent value x from the domain of Xi
            csp.domains[Xi].remove(x)
            revised = True
    return revised


#iteratively removes inconsistent values from the domains of variables until the sudoku becomes arc consistent or problem detected.
def AC3(csp):
    queue = [(Xi, Xj) for Xi in csp.domains for Xj in csp.arcs[Xi]]
    while queue:
        Xi, Xj = queue.pop()
        # Apply revise function to remove inconsistent values from the domain of Xi
        if revise(csp, Xi, Xj):
            if (len(csp.domains[Xi]) == 0):
                return False
            # Add the arcs (Xd, Xi) to the queue for further processing, excluding the current arc (Xj, Xi)
            for Xd in csp.arcs[Xi]:
                if Xd != Xj:
                    queue.append((Xd, Xi))
    return True


#explore the search space, assigning values to variables, enforcing arc consistency, and backtracking when necessary to find a valid solution.
def AC3_with_BT(csp):
    #Base state: if all variables in the CSP have only one possible value in their domains, it constructs the solution grid by extracting the assigned values from the domains and returns it as the solution.
    if all(len(csp.domains[k]) == 1 for k in csp.domains):
        solution = [[0 for i in range(9)] for j in range(9)]
        i, j = 0, 0
        for row in solution:
            for cells in row:
                    solution[i][j] = csp.domains['X'+str(i)+str(j)][0]
                    j += 1
                    if j == 9:
                        i += 1
                        j = 0
        return solution
    # If the base case is not met, the algorithm proceeds to the backtracking phase.
    #If an empty domain is found, it means the assignment so far is inconsistent, and the algorithm backtracks by returning None
    if not any([len(csp.domains[k]) == 0 for k in csp.domains]): 
        unassignedVar, unassignedDomain = unassignedVariable(csp)
        
        # Try all possible values for the unassigned variable
        for value in orderDomain(csp, unassignedVar, unassignedDomain):
            # Create a copy of the CSP to explore this branch of the search space
            next_CSP = copy.deepcopy(csp)
            next_CSP.domains[unassignedVar] = [value]
            if consistentAssignment(next_CSP, unassignedVar, value):
                # Enforce arc consistency on the CSP with the new assignment
                if AC3(next_CSP):    
                    # Recursively solve the CSP with the new assignment                
                    sol = AC3_with_BT(next_CSP)
                    if sol is not None:
                        return sol
    return None


def solveAC3(puzzle):
    # each cell as (Xij, value) 
    cell = [('X'+str(i)+str(j), X) for i, row in enumerate(puzzle) for j, X in enumerate(row)]    
    #values domain are 0-9
    domains ={}
    
    #If a cell has a value of 0, indicating an empty cell, its domain is set to be a list of numbers from 1 to 9. Otherwise, if the cell has a non-zero value, its domain is set to be a list containing only that value
    for (key, X) in cell:
        if X == 0: #Has not domain
            domains[key] = [x for x in range(1,10)]
        else: #Has one domain
            domains[key] = [X]
        
        
    #form arc with key value is a list of variables
    arcs = {}
    for (key, X) in cell:
        arcs[key] = generateArc(int(key[1]), int(key[2]))
    puzzle = AC3_with_BT(CSP(cell, domains, arcs, constraints))
    
    
    return puzzle, isEmpty(puzzle)

