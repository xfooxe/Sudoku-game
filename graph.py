import wx, wx.html, wx.grid   #Require to install wx by this command in cmd = pip install -U wxPython

class Sudoku(wx.Frame):
    # initialize a new sudoku game
    # input: the initial sudoku table 
    # output: no output 
    def __init__(self,StartBoard):
        wx.Frame.__init__(self, None, -1, "Sudoku") 
        self.StartBoard=StartBoard   
        
        #Create cell with range 1-9 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        self.board = wx.grid.Grid(self,-1)
        self.Editor = wx.grid.GridCellNumberEditor(1, 9) 


        numRows = numCols = 9
        cellSize = 50
        # creating the Sudoku square, grid , and set size
        self.board.CreateGrid(numRows, numCols)      
        self.board.SetRowLabelSize(0)
        self.board.SetColLabelSize(0)
        self.board.SetDefaultColSize(cellSize, resizeExistingCols=True)
        self.board.SetDefaultRowSize(cellSize, resizeExistingRows=True)
        self.board.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        self.board.SetDefaultEditor(self.Editor)

        self.sizer2 = wx.GridSizer(2, 3, 10, 10)

        #add to main sizer
        sizer.Add(self.board, 0, wx.EXPAND)
        sizer.Add(self.sizer2, 0, wx.EXPAND) 


        #draw background
        self.setBackground()
        #fill data in table
        self.fillBoard(self.StartBoard)
        
        # Set sizer and center
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.CenterOnScreen()
        self.Show()
        
        
    # fills the square with values 
    # input: the input sudoku table
    # output: no output 
    def fillBoard(self, sudoku):
        self.board.ClearGrid()
        self.board.SetDefaultCellFont(wx.Font(16, wx.SWISS,wx.NORMAL, wx.BOLD))
        
        # inserting numbers into cells of the table 
        for input in range(81): 
                column = input % 9
                row = abs(input // 9)
                #unlock cells
                self.board.SetReadOnly(row,column, isReadOnly=False)
                self.board.SetDefaultCellFont(wx.Font(16, wx.SWISS,wx.NORMAL, wx.NORMAL))
                # '0' and '.' inputs will be removed  
                if sudoku[input] in '.0':
                    self.board.SetCellValue(row, column,'')
                    self.board.SetDefaultCellFont(wx.Font(14, wx.SWISS,wx.NORMAL, wx.NORMAL))
                else:
                #fill data from input and lock cells    
                    self.board.SetCellValue(row, column,str(sudoku[input]))
                    self.board.SetReadOnly(row,column, isReadOnly=True)
                    self.board.SetCellFont(row,column, wx.Font(16, wx.SWISS,wx.NORMAL, wx.BOLD))


    # setting the background color with grey color
    # input: no input 
    # output: no output 
    def setBackground(self):
        
        # setting each cell with it's specific color 
        for row in range (9):
            for column in range (9):
                self.board.SetReadOnly(row,column, isReadOnly=False)
                #different each 3*3 box with different color
                self.backgroundColor(0,0,3,3,211,211,211)
                self.backgroundColor(0,6,3,9,211,211,211)
                self.backgroundColor(3,3,6,6,211,211,211)
                self.backgroundColor(6,0,9,3,211,211,211)
                self.backgroundColor(6,6,9,9,211,211,211)

    # setting the background color for each square (within the coordinates)
    # input: coordinates and colors 
    # output: no output 
    def backgroundColor(self, x1, y1, x2, y2, R, G, B):
        # setting each cell with it's specific color 
        for row in range (x1, x2):
            for column in range(y1,y2):
                self.board.SetCellBackgroundColour(row, column, (R,G,B)) 



