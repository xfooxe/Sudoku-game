#import pandas as pd                        # Importing pandas to read the 9 million sudoku puzzle
import time                                 # Importing the time library for measuring execution time
import random                               # Importing random library to choose randomly a board to run
from graph import *                         # Importing the graph file to represent the sudoku puzzle as visual simulator
from Backtracking import solveBT            
from ForwardChecking import solveFC         
from ac import solveAC3  
import os                  

# -- read sudoku puzzle from "sudoku.csv"
#sudokuList = pd.read_csv('sudoku.csv')


#------------- helping methods ----------------------


# The purpose of this function is to convert a Sudoku string into a 2D matrix.
def convertToMatrix(puzzle):
    mat = []
    
    #This loop will not stop until the puzzle string is empty
    while puzzle != []:
        mat.append(puzzle[:9])
        puzzle = puzzle[9:]
    # This loop will convert each character to an integer
    for i in range(0, len(mat)):
        for j in range(0, len(mat)):
            mat[i][j] = int(mat[i][j])
    return mat

# Convert the matrix elements into string to show it as GUI
def matrixToString(lst):
    x=''
    for i in range(len(lst)):
        for j in range(len(lst)):
            x+=str(lst[i][j])
    return x
            

#  to run a graph file to be GUI format for sudoku visual simulator
def runGUI(num):
    if  __name__ == "__main__":
        app = wx.App(False)
        frame = Sudoku(num)
        app.MainLoop()

def selectRandomVariable(variables):
    # Randomly choose a variable from the list
    selected_variable = random.choice(variables)
    return selected_variable

# read a specific line from file that contains 20 puzzle
def readFromFile(file_path, line_number):
    with open(file_path, 'r') as file:
        for i, line in enumerate(file, start=1):
            if i == line_number:
                return line.strip()
    return None



#---------------------------------------------------------------------

print("----Welcome to Sudoku game solver-----")
print("**note: \n**This program will choose the puzzles randomly then give the time in terminal \n**and show a visual simulator of puzzle game before and after the solution\n")
    

while(True):
        choice = input("Choose what search type to run:\n1-Backtracking   \n2-Forward checking   \n3- Arc consistency\n4- Exit\n")
        
        if choice=="1" or choice =="2" or choice=="3":
            choicePuzzle = input("Choose puzzle number from 1 to 20 to run\n")
            line = readFromFile("Puzzles.txt", int(choicePuzzle))
            if line:
                board = line
                runGUI(board)
                puzzle = (list(board))
                puzzle = convertToMatrix(puzzle) #Represent the puzzle as matrix to solve it using BT and FC
                solve = False
                
                #Backtracking
                if choice=="1":
                    startTime = time.time() # Measure the start time for the backtracking algorithm
                    solve = solveBT(puzzle)
                    Timing = time.time()-startTime    # Measure the execution time of the backtracking algorithm and add it to the total time.
                    print("Time taken by Backtracking is: ", Timing)            
                
                
                #ForwardChecking
                elif choice=="2":
                    startTime = time.time() # Measure the start time for the backtracking algorithm
                    solve = solveFC(puzzle)
                    Timing = time.time()-startTime   # Measure the execution time of the forwardChecking algorithm and add it to the total time.
                    print("Time taken by Forward checking is: ", Timing)            
                
                
                #Arc consistency
                elif choice=="3":
                    startTime = time.time() # Measure the start time for the backtracking algorithm
                    puzzle, solve  = solveAC3(puzzle)
                    Timing = time.time()-startTime
                    print("Time taken by ARC3 is: ", Timing)            
                elif choice=="4":
                    exit()
                
                
                x = matrixToString(puzzle)
                runGUI(x)
                
                if not solve:
                    print("no solution")
                print()
                
            else:
                print("Wrong entry! try again \n")
        
        else:
            if choice =="4":
                exit()
            print("Try again!!")
    