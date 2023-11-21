try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from splash_screen import *
from help_screen import *
from enterBoard_screen import *
from settings_screen import *
from PIL import Image, GifImagePlugin

from boards import *
import math
import random
import copy 
import os
import time
import itertools
import pyscreenshot

#EXTRA FEATURES: preferences, convert to pdf file, more advanced ban
#citations
    # CS academy sudoku hints: https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html
    #new york times sudoku: https://www.nytimes.com/puzzles/sudoku/easy
    #music provided by Lofi Girl. Listen: https://lofigirl.com/blogs/releases/enchantments

class State:
    def __init__(self, initialBoard):
        self.board = [[0]*9 for i in range(9)] #2dlist of integers that are all zero at start
        self.legals = [[set(range(1,10))]*9 for i in range(9)] #2dlist of sets that is full of 1-9 at start
        for row in range(9):
            for col in range(9):
                value = initialBoard[row][col]
                self.set(row,col,value)
        self.legalsCopy = copy.deepcopy(self.legals)
        self.boardCopy = copy.deepcopy(self.board)

    # CS academy sudoku hints: https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html
    #debug printing
    def printBoard(self): print2dList(self.board)
    def printLegals(self):
        colWidth = 4
        for col in range(9):
            colWidth = max(colWidth, 1+max([len(self.legals[row][col]) for row in range(9)]))
        for row in range(9):
            for col in range(9):
                label = ''.join([str(v) for v in sorted(self.legals[row][col])])
                if label == '': label = '-'
                print(f"{' '*(colWidth - len(label))}{label}", end='')
            print()
    def printLegalsCopy(self):
        colWidth = 4
        for col in range(9):
            colWidth = max(colWidth, 1+max([len(self.legalsCopy[row][col]) for row in range(9)]))
        for row in range(9):
            for col in range(9):
                label = ''.join([str(v) for v in sorted(self.legalsCopy[row][col])])
                if label == '': label = '-'
                print(f"{' '*(colWidth - len(label))}{label}", end='')
            print()
    def print(self): self.printBoard(); self.printLegals()
    def set(self, row, col, value):
        self.board[row][col] = value #sets value
        if value != 0:
            self.legals[row][col] = set() #ban all the values in the current spot
        #ban the one value in the block, row, col
            targetBlock = self.getBlock(row, col)
            for r in range(9):
                for c in range(9):
                    currBlock = self.getBlock(r,c)
                    if r == row:
                        self.ban(r, c, {value})
                    elif c == col:
                        self.ban(r, c, {value})
                    elif currBlock == targetBlock:
                        self.ban(r,c,{value})
    def ban(self, row, col, values):
            self.legals[row][col] = self.legals[row][col] - values
    
    def unban(self, row, col, values, oldState):
        self.legals[row][col] = self.legalsCopy[row][col]
        for r, c in self.getCellRegions(row, col):
            num = list(values)[0]
            if self.board[r][c] == 0:
                if self.isLegal(num, r, c):
                    self.legals[r][c] = self.legals[r][c]|values
    def isLegal(self, num, row, col):
        values = set()
        for r, c in self.getCellRegions(row, col):
            values.add(self.board[r][c])
        if num in values:
            return False
        return True

    #A region is a list of 9 (row,col) tuples
    def getRowRegion(self, row):
        #loop through and create a list for block, colRegion and rowRegion
        rows = len(self.board)
        cols = len(self.board[0])
        rowRegion = []
        for r in range(rows):
            for c in range(cols):
                if r == row:
                    rowRegion.append((r,c))
        return rowRegion
    def getColRegion(self, col):
        #loop through and create a list for block, colRegion and rowRegion
        rows = len(self.board)
        cols = len(self.board[0])
        colRegion = []
        for r in range(rows):
            for c in range(cols):
                if c == col:
                    colRegion.append((r,c))
        return colRegion


    def getBlockRegion(self, block):
        # 0 1 2
        # 3 4 5
        # 6 7 8
        if block == 0:
            blockR = blockC = 0
        elif  block == 1:
            blockR = 0
            blockC = 3
        elif  block == 2:
            blockR = 0
            blockC = 6
        elif  block == 3:
            blockR = 3
            blockC = 0
        elif  block == 4:
            blockR = 3
            blockC = 3
        elif  block == 5:
            blockR = 3
            blockC = 6
        elif  block == 6:
            blockR = 6
            blockC = 0
        elif  block == 7:
            blockR = 6
            blockC = 3
        elif  block == 8:
            blockR = 6
            blockC = 6
        rows = len(self.board)
        cols = len(self.board[0])
        blockRegion = []
        for r in range(rows):
            for c in range(cols):
                if (blockR <= r < blockR+3) and (blockC <= c < blockC+3):
                    blockRegion.append((r,c))
        return blockRegion
    def getBlock(self, row, col):
        # 0 1 2
        # 3 4 5
        # 6 7 8
        if row < 3 and col < 3:
            return 0
        elif  3 <= row <= 5 and 3 <= col <= 5:
            return 4  
        elif  6 <= row <= 8 and 6 <= col <= 8:
            return 8  
        elif 3 <= row <= 5 and col < 3:
            return 3
        elif row < 3 and 3 <= col <= 5:
            return 1
        elif 6 <= row <= 8 and col < 3:
            return 6
        elif row < 3 and 6 <= col <= 8:
            return 2
        elif 6 <= row <= 8 and 3 <= col <= 5:
            return 7
        elif 3 <= row <= 5 and 6 <= col <= 8:
            return 5
    def getBlockRegionByCell(self, row, col):
        block = self.getBlock(row, col)
        return self.getBlockRegion(block)
    def getCellRegions(self, row, col):
        allRegions = []
        #returns a list of three regions
        colRegion = self.getColRegion(col)
        rowRegion = self.getRowRegion(row)
        blockRegion = self.getBlockRegionByCell(row,col)
        allRegions = allRegions + colRegion + rowRegion + blockRegion
        return allRegions
    def getAllRegions(self):
        allRegions = []
        for i in range(0,9):
            allRegions.append(self.getBlockRegion(i))
        for r in range(9):
            for c in range(9):
                allRegions.append(self.getColRegion(c))
                allRegions.append(self.getRowRegion(r))
        return allRegions
    def getAllRegionsThatContainTargets(self, targets):
        #targets is a tuple containing row, col pairs
        #gets a set of targets (row,col), goes through all the regions and returns 
        #the regions that contains the targets
        sharedRegions = []
        for region in self.getAllRegions():#loop through colRegions, rowRegions, blockRegions
            region = set(region)
            if self.allTargetsInRegion(targets, region):
                sharedRegions.append(region)   
        return sharedRegions
    def allTargetsInRegion(self, targets, region):
        for target in targets:
            if target not in region:
                return False
        return True 
        #BACKTRACKING SOLVER
        ##SUDOKU SOLVER
    #find the cell with least legals
    def findNextLeastLegals(self):
        rows = len(self.board)
        cols = len(self.board[0])
        leastLegalsC = leastLegalsR = None
        for row in range(rows):
            for col in range(cols):
                if len(self.legals[row][col]) != 0:
                    if leastLegalsC == None and leastLegalsR == None:
                        leastLegalsR = row
                        leastLegalsC = col
                    elif len(self.legals[row][col]) < len(self.legals[leastLegalsR][leastLegalsC]):
                        leastLegalsR = row
                        leastLegalsC = col
        return leastLegalsR, leastLegalsC
    
    #find the zero in the board
    def findNextZero(self, board):
        rows = len(board.board)
        cols = len(board.board[0])
        for row in range(rows):
            for col in range(cols):
                if board.board[row][col] == 0:
                    return row, col
        return None, None
        
    def willCreatePermanentZero(self, num,row,col,board):
        board = copy.deepcopy(board)
        board.set(row, col, num)
        rows = len(board.board)
        cols = len(board.board[0])
        for r in range(rows):
            for c in range(cols):
                if len(board.legals[r][c]) ==  0 and board.board[r][c] == 0:
                    return True
        return False

    def sudokuSolver(self):
        boardSol = State(copy.deepcopy(self.board))
        return self.solver(boardSol)

    def solver(self, boardSol):
        row, col = self.findNextLeastLegals()
        if row == None and col == None: #no more full legal
            return boardSol.board
        else:
            for num in boardSol.legals[row][col]: #try all the legal values
                if boardSol.isLegalMove(num, row, col, boardSol):
                    #set the value and update the legals as well
                    oldStateLegals = copy.deepcopy(boardSol.legals)
                    oldStateBoard = copy.deepcopy(boardSol.board)
                    boardSol.set(row, col, num)
                    solution = boardSol.solver(boardSol)
                    if solution != None:
                        return solution
                    #undo move
                    #unset the move 
                    #unban all the legals
                    boardSol.board = oldStateBoard
                    boardSol.legals = oldStateLegals
                    #boardSol.ban(row,col, {num})
            return None
            
    def isLegalMove(self,num, row, col, board):
        for r, c in self.getCellRegions(row, col):
            if board.board[r][c] == num:
                return False
        if self.willCreatePermanentZero(num,row,col,board):
            return False
        return True

    #HINTS
    #Hint 1: obvious (naked) single
    def getHint1(self):
        for row in range(9):
            for col in range(9):
                if len(self.legals[row][col]) == 1:
                    return row, col
        return None
    def applyHint1(self):
        hint = self.getHint1()
        if hint != None:
            hintR, hintC = hint
            self.set(hintR, hintC, list(self.legals[hintR][hintC])[0])
        return None

    #Hint 2: obvious (naked) tuple (pair, triple, quad, quint)
    def getHint2(self):
        for region in self.getAllRegions():
            for N in range(2, 6):
                result = self.findHint2(region, N)
                if result != None:
                    return result
        return None

    def findHint2(self, region, N):
        for targetCells in itertools.combinations(region, N):
            for valueCombo in itertools.combinations(range(1,9), N):
                if self.valuesAreOnlyLegals(valueCombo, targetCells):
                    values = set(valueCombo)
                    bans = self.getBansForAllRegions(values, targetCells)
                    if bans == []:
                        return None
                    return targetCells

    def applyHint2(self):
        targetCells = self.getHint2()
        if targetCells != None:
            values = set()
            for targetCell in targetCells:
                row, col = targetCell
                values = values.union(self.legals[row][col])
            #create list of cells that contain the values in the targetCells regions
            bans = self.getBansForAllRegions(values, targetCells)
            if bans == []:
                return 'No more bans'
            for ban in bans:
                self.ban(ban[0], ban[1], values)
        return None

    def valuesAreOnlyLegals(self, values, targets):
        values = set(values)
        for cell in targets:
            row, col = cell
            if self.legals[row][col] != set():
                for legal in self.legals[row][col]:
                    if legal not in values:
                        return False
            else:
                return False
        return True

    def getBansForAllRegions(self, values, targets):
            # The values (to ban) can stay in the targets, but they must be
            # banned from all other cells in all regions that contain all
            # the targets
        bans = [ ]
        for region in self.getAllRegionsThatContainTargets(targets):
            for cell in region:
                for value in values:
                    if value in self.legals[cell[0]][cell[1]] and cell not in set(targets):
                        bans.append(cell)
        return bans

class Button:
    def __init__(self, name, left, top, width, height):
        self.name = name
        self.top = top
        self.left = left
        self.width = width
        self.height = height
    
    def mousePress(self, x, y):
        if self.left <= x <= self.left + self.width and self.top <= y <= self.top + self.height:
            return True
        return False
    def drawButton(self, fill = 'white', size = 16):
        drawRect(self.left, self.top, self.width, self.height, border='black', fill = fill)
        drawLabel(self.name, self.left+self.width//2, self.top+self.height//2, font = 'monospace', size = size)

def sudoku_onScreenStart(app):
    print(app.hintColor, 'hint')
    #choosing a level
    app.level = None
    app.levels = ['easy', 'medium','hard','expert','evil']
    app.stepsPerSecond = 5
    app.levelsGif = loadAnimatedGif(app, 'levelsGif.gif')
    app.levelSpriteCounter = 0
    url = 'https://audio.jukehost.co.uk/98pPgWIK8u5ZruzH3QsGalxtuwlTfo8b'
    app.sound = Sound(url)
    #drawing the board
    app.width = 1000
    app.height = 700
    app.rows = 9
    app.cols = 9
    app.boardLeft = 80
    app.boardTop = 120
    app.boardWidth = 540
    app.boardHeight = 540
    app.cellBorderWidth = 1
    #boards
    app.board = None
    app.boardSolution = None
    app.showSudokuSolution = False
    app.selectedCell = (0,0)
    app.usersBoard = None
    app.manualModeLegals = [[set() for i in range(9)] for i in range(9)]#when the user is setting all the legals himself
    app.keys = []
    app.undoRedoList = [] #keeps track of all the states from start to current
    app.undoRedoPosition = None #keeps track of what state is currently showing 
    #keeps track of what to unban, row, col
    app.lastValueEntered = dict()
    #In automatic mode, each time a value is placed in a cell, that value is 
    #automatically removed from all the legals in that cell's row, column, and block. 
    #In manual mode, the user is responsible for updating all the legals
    app.automaticLegalsMode = False 
    app.modes = 'Normal Mode'
    app.showHoveringLegal = (None, None)
    app.hoveringCounter = 0
    app.noMoreSingletonsCounter = 0
    app.showHintCellsCounter = 0
    app.showNoMoreSingletons = False
    app.showNoMoreHints = False
    app.hintCells = None #a tuple of tuples of row, col pairs
    app.hintCounter = 0 
    app.competitionMode = False
    #buttons
    keyWidth, keyHeight = getCellSize(app)
    app.keyWidth, app.keyHeight = keyWidth+3, keyHeight+3
    app.xButtonHeight = app.keyHeight
    app.xButtonWidth = app.keyWidth*3+12*2
    app.helpButton = Button('Help', 80,70, 70, 40)
    app.createBoardButton = Button('Create Board',160,70,160,40)
    app.playSingletonsButton = Button('Play All Singletons', 700,540,210,30)
    app.playNextSingletonButton = Button('Play Singleton', 700, 500, 210, 30)
    app.manualLegalsButton = Button('Normal', 700, 120, 105,30)
    app.automaticLegalsButton = Button('Show Legals', 805, 120, 105,30)
    app.enterLegalsButton = Button('Enter Legals',700, 160, 210,30)
    app.enterKeysButton = Button('Enter Keys',700, 160, 210,30)
    app.changeLevelButton = Button('Change Level', 330,70,160,40)
    app.settingsButton = Button('Preferences', 500, 70, 120, 40)
    app.showHintButton = Button('Show Hint', 700, 580, 210, 30)
    app.playHintButton = Button('Play Hint', 700, 620, 210, 30)
    app.undoButton = Button('Undo <-', 700, 70, 100, 40)
    app.redoButton = Button('Redo ->', 810, 70, 100, 40)
    app.enterLegalsMode = False
    app.isGameOver = False
    app.showGameOverCounter = 0
    app.drawBoardCount = 0
    app.takeScreenshotCounter = 0
    app.gameOverCounter = 0
    app.image1 = None
    app.image2 = None

def sudoku_onStep(app):
    app.levelSpriteCounter = (1 + app.levelSpriteCounter) % len(app.levelsGif)
    app.hoveringCounter += 1
    if app.showNoMoreSingletons or app.showNoMoreHints:
        app.noMoreSingletonsCounter += 1
        if app.noMoreSingletonsCounter >= 5:
            app.showNoMoreSingletons = False
            app.showNoMoreHints = False
            app.noMoreSingletonsCounter = 0
    if app.hintCells != None:
        app.showHintCellsCounter += 1
        if app.showHintCellsCounter >= 15:
            app.hintCells = None
            app.showHintCellsCounter = 0
    if app.isGameOver:
        app.showGameOverCounter += 1
        if app.showGameOverCounter == 3:
            app.image2 = pyscreenshot.grab(bbox=(295,215,845,764))
                # To save the screenshot
            app.image2.save("endSudokuBoard.png")

            #SAVE AS PDF
            #cite:https://datatofish.com/images-to-pdf-python/
            #https://www.geeksforgeeks.org/taking-screenshots-using-pyscreenshot-in-python/
            image_1 = Image.open("startSudokuBoard.png")
            image_2 = Image.open("endSudokuBoard.png")   
            im_1 = image_1.convert('RGB')
            im_2 = image_2.convert('RGB')
            image_list = [im_2]
            im_1.save("sudokuBoard.pdf", save_all=True, append_images=image_list)


        elif app.showGameOverCounter >= 25:
            app.isGameOver = False
            app.showGameOverCounter = 0 
    
    if not app.pausedMusic:
          app.sound.play(loop=True)
    elif app.pausedMusic:
          app.sound.pause()
    if app.level != None:
        app.takeScreenshotCounter += 1
    if app.takeScreenshotCounter == 5:
        # im=pyscreenshot.grab(bbox=(x1,x2,y1,y2))
        app.image1 = pyscreenshot.grab(bbox=(295,215,845,764))
            # To save the screenshot
        app.image1.save("startSudokuBoard.png")



#Board loading
def loadBoardPaths(filters):
    boardPaths = [ ]
    for filename in os.listdir(f'boards/'):
        if filename.endswith('.txt'):
            if hasFilters(filename, filters):
                boardPaths.append(f'boards/{filename}')
    return boardPaths

def hasFilters(filename, filters=None):
    if filters == None: return True
    for filter in filters:
        if filter not in filename:
            return False
    return True

def loadRandomBoard(filters=None):
    boardPath = random.choice(loadBoardPaths(filters))
    return boardPath

#returns a 2d list board from the text files
def getBoard(app):
    if app.level != None:
        if app.path == None: #app.path created in enterBoard screen
            contents = readFile(loadRandomBoard(app.level))
        else:
            contents = readFile(app.path)
        board = [[0]*9 for i in range(9)]
        countRow = 0
        for line in contents.splitlines():
            countCol = 0
            for num in line:
                if num != ' ':
                    board[countRow][countCol] = int(num)
                    countCol += 1
            countRow += 1
        return board

def sudoku_onKeyPress(app, key):
    if not app.isGameOver:
        if key == 's' and not app.competitionMode:
            #toggle showing solution
            app.showSudokuSolution = not app.showSudokuSolution
        elif key == 'n' and app.automaticLegalsMode and not app.competitionMode:
            playSingleton(app)
        elif key == 'a' and app.automaticLegalsMode and not app.competitionMode:
            playAllSingletons(app)
        elif key == 'l':
            app.enterLegalsMode = not app.enterLegalsMode
        elif key == 'h' and not app.competitionMode:
            hint = app.usersBoard.getHint1()
            if hint != None:
                app.hintCells = hint
        elif key == 'H' and not app.competitionMode:
            hint = app.usersBoard.applyHint1()
            if hint != None:
                app.hintCells = hint
        elif key == 't' and app.automaticLegalsMode and not app.competitionMode:
            hint = app.usersBoard.getHint2()
            if hint != None:
                app.hintCells = hint
        elif key == 'T' and app.automaticLegalsMode and not app.competitionMode:
            hint = app.usersBoard.getHint2()
            if hint != None:
                app.hintCells = hint
                app.usersBoard.applyHint2()
        elif app.modes != 'Mouse-only Mode':
            #move the user's cell selection with keys
            if key == 'left':  moveSelection(app, 0, -1)
            elif key == 'right': moveSelection(app, 0, +1)
            elif key == 'up':    moveSelection(app ,-1, 0)
            elif key == 'down':  moveSelection(app, +1, 0)
            
            elif app.selectedCell != None:
                sRow = app.selectedCell[0]
                sCol = app.selectedCell[1]
                if key.isdigit() and app.board.board[sRow][sCol] == 0 and not app.enterLegalsMode: 
                    if app.automaticLegalsMode:
                        oldState = State(copy.deepcopy(app.usersBoard.board))
                        app.usersBoard.set(sRow, sCol, int(key))
                        if app.undoRedoPosition != len(app.undoRedoList)-1 and app.undoRedoPosition != 0 :
                            app.undoRedoList = app.undoRedoList[0:app.undoRedoPosition+1]
                        app.undoRedoList.append(copy.deepcopy(app.usersBoard))
                        app.undoRedoPosition = len(app.undoRedoList)-1

                        if app.lastValueEntered != None:
                            for row, col in app.lastValueEntered:
                                if row == sRow and col == sCol:
                                    app.usersBoard.unban(sRow, sCol, {app.lastValueEntered[(row, col)]}, oldState)
                        app.lastValueEntered[(sRow, sCol)] = int(key)
                        if app.usersBoard.board == app.boardSolution:
                            app.isGameOver = True
                            writeBoard(app.usersBoard.board)
                            
                    else: 
                        #if not in automatic legals mode, user updates legals himself
                        app.usersBoard.board[sRow][sCol] = int(key)
                        if app.undoRedoPosition != len(app.undoRedoList)-1 and app.undoRedoPosition != 0:
                            app.undoRedoList = app.undoRedoList[0:app.undoRedoPosition+1]
                        app.undoRedoList.append(copy.deepcopy(app.usersBoard))
                        app.undoRedoPosition = len(app.undoRedoList)-1
                        if app.usersBoard.board == app.boardSolution:
                            app.isGameOver = True
                            writeBoard(app.usersBoard.board)
                #entering legal values instead of keys
                elif key.isdigit() and app.board.board[sRow][sCol] == 0 and app.enterLegalsMode:
                    if not app.automaticLegalsMode:
                        app.manualModeLegals[sRow][sCol].add(int(key))
                    else:   
                        app.usersBoard.legals[sRow][sCol].add(int(key))
                if (key == 'delete' or key == 'backspace') and app.board.board[sRow][sCol] == 0:
                    if app.automaticLegalsMode:
                        oldState = State(copy.deepcopy(app.usersBoard.board))
                        app.usersBoard.set(sRow, sCol, 0)
                        if app.undoRedoPosition != len(app.undoRedoList)-1 and app.undoRedoPosition != 0:
                            app.undoRedoList = app.undoRedoList[0:app.undoRedoPosition+1]
                        app.undoRedoList.append(copy.deepcopy(app.usersBoard))
                        app.undoRedoPosition = len(app.undoRedoList)-1
                        if (app.lastValueEntered != None and 
                            app.lastValueEntered[1] == sRow and app.lastValueEntered[2] == sCol):
                                app.usersBoard.unban(sRow, sCol, {app.lastValueEntered[0]}, oldState)         
                    else: 
                        #if not in automatic legals mode, user updates legals himself
                        app.usersBoard.board[sRow][sCol] = int(key)
                        if app.undoRedoPosition != len(app.undoRedoList)-1 and app.undoRedoPosition != 0:
                            app.undoRedoList = app.undoRedoList[0:app.undoRedoPosition+1]
                        app.undoRedoList.append(copy.deepcopy(app.usersBoard))
                        app.undoRedoPosition = len(app.undoRedoList)-1

def playSingleton(app):
    for row in range(9):
        for col in range(9):
            legals = app.usersBoard.legals[row][col]
            if len(legals) == 1:
                app.usersBoard.set(row, col, list(legals)[0])
                if app.undoRedoPosition != len(app.undoRedoList)-1 and app.undoRedoPosition != 0:
                            app.undoRedoList = app.undoRedoList[0:app.undoRedoPosition+1]
                app.undoRedoList.append(copy.deepcopy(app.usersBoard))
                app.undoRedoPosition = len(app.undoRedoList)-1
                return #set only one
    app.showNoMoreSingletons = True
    if app.usersBoard.board == app.boardSolution:
        app.isGameOver = True
        writeBoard(app.usersBoard.board)
def playAllSingletons(app):
    count = 0
    for row in range(9):
        for col in range(9):
            legals = app.usersBoard.legals[row][col]
            if len(legals) == 1:
                count += 1
                app.usersBoard.set(row, col, list(legals)[0])
                if app.undoRedoPosition != len(app.undoRedoList)-1 and app.undoRedoPosition != 0:
                            app.undoRedoList = app.undoRedoList[0:app.undoRedoPosition+1]
                app.undoRedoList.append(copy.deepcopy(app.usersBoard))
                app.undoRedoPosition = len(app.undoRedoList)-1
    if count == 0: #none are singletons
        app.showNoMoreSingletons = True
    if app.usersBoard.board == app.boardSolution:
        app.isGameOver = True
        writeBoard(app.usersBoard.board)
def moveSelection(app, drow, dcol):
    if app.selectedCell != None:
        selectedRow, selectedCol = app.selectedCell
        newSelectedRow = (selectedRow + drow) % app.rows
        newSelectedCol = (selectedCol + dcol) % app.cols
        app.selectedCell = (newSelectedRow, newSelectedCol)

def sudoku_onMouseMove(app, mouseX, mouseY):
    if not app.isGameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        if selectedCell == app.selectedCell and app.selectedCell != None:
            row, col = selectedCell
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            legalCount = 1
            for r in range(3):
                for c in range(3):
                    minX = cellLeft+r*cellWidth//3
                    maxX = cellLeft+(r+1)*cellWidth//3
                    minY = cellTop+c*(cellHeight)//3
                    maxY = cellTop+(c+1)*cellHeight//3
                    if minX < mouseX < maxX and minY < mouseY < maxY:
                        app.showHoveringLegal = (r,c)
                    legalCount += 1
        else:
            app.showHoveringLegal = (None,None)
        
def sudoku_onMousePress(app, mouseX, mouseY):
    if app.level == None:
        selectedLevel = getLevel(app, mouseX, mouseY)
        if selectedLevel != None:
            app.level = selectedLevel
            #testBacktracker(filters=['easy'])
            randBoard = getBoard(app)
            app.board = State(randBoard)
            app.board.print()
            app.usersBoard = State(randBoard)
            app.undoRedoList.append(copy.deepcopy(app.usersBoard))
            app.undoRedoPosition = 0
            app.boardSolution = app.board.sudokuSolver()
            if app.level == 'easy':
                app.automaticLegalsMode = False
            else:
                app.automaticLegalsMode = True
    if not app.isGameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        if selectedCell != None:
            if selectedCell == app.selectedCell:
                #if the user clicked inside the selected cell then he is choosing a legal
                hoveringLegal = getClickedLegal(app, mouseX, mouseY) #returns legal
                row, col = app.selectedCell
                if not app.automaticLegalsMode:
                    if hoveringLegal not in app.manualModeLegals[row][col]:
                        app.manualModeLegals[row][col].add(hoveringLegal)
                        app.usersBoard.legals[row][col].add(hoveringLegal)
                    else: #user already added the legal and is clicking again to remove it
                        app.manualModeLegals[row][col].remove(hoveringLegal)
                        app.usersBoard.legals[row][col].remove(hoveringLegal)
                else:
                    if hoveringLegal not in app.usersBoard.legals[row][col]:
                        app.usersBoard.legals[row][col].add(hoveringLegal)
                    else: #user already added the legal and is clicking again to remove it
                        app.usersBoard.legals[row][col].remove(hoveringLegal)
            else:
                app.selectedCell = selectedCell
        if app.modes != 'Key-only Mode':
            selectedKey = getKey(app, mouseX, mouseY)
            if selectedKey != None and app.selectedCell != None:
                sRow = app.selectedCell[0]
                sCol = app.selectedCell[1]
                if app.board.board[sRow][sCol] == 0 and not app.enterLegalsMode:
                    if app.automaticLegalsMode:
                        oldState = State(copy.deepcopy(app.usersBoard.board))
                        app.usersBoard.set(sRow, sCol, selectedKey)
                        if app.undoRedoPosition != len(app.undoRedoList)-1 and app.undoRedoPosition != 0:
                            app.undoRedoList = app.undoRedoList[0:app.undoRedoPosition+1]
                        app.undoRedoList.append(copy.deepcopy(app.usersBoard))
                        app.undoRedoPosition = len(app.undoRedoList)-1
                        if app.lastValueEntered != None:
                            for row, col in app.lastValueEntered:
                                if row == sRow and col == sCol:
                                    app.usersBoard.unban(sRow, sCol, {app.lastValueEntered[(row, col)]}, oldState)
                        app.lastValueEntered[(sRow, sCol)] = selectedKey
                        if app.usersBoard.board == app.boardSolution:
                            app.isGameOver = True
                            writeBoard(app.usersBoard.board)
                    else: 
                        #if not in automatic legals mode, user updates legals himself
                        app.usersBoard.board[sRow][sCol] = selectedKey
                        if app.undoRedoPosition != len(app.undoRedoList)-1 and app.undoRedoPosition != 0:
                            app.undoRedoList = app.undoRedoList[0:app.undoRedoPosition+1]
                        app.undoRedoList.append(copy.deepcopy(app.usersBoard))
                        app.undoRedoPosition = len(app.undoRedoList)-1
                        if app.usersBoard.board == app.boardSolution:
                            app.isGameOver = True
                            writeBoard(app.usersBoard.board)
                        
                elif app.board.board[sRow][sCol] == 0 and app.enterLegalsMode:
                    if app.automaticLegalsMode:
                        app.usersBoard.legals[sRow][sCol].add(selectedKey)
                    else:
                        app.manualModeLegals[sRow][sCol].add(selectedKey)
    if app.helpButton.mousePress(mouseX, mouseY):
        setActiveScreen('help_screen')
    elif app.createBoardButton.mousePress(mouseX, mouseY):
        setActiveScreen('enterBoard_screen')
    elif app.manualLegalsButton.mousePress(mouseX, mouseY):
         app.automaticLegalsMode = False
    elif app.automaticLegalsButton.mousePress(mouseX, mouseY):
         app.automaticLegalsMode = True
    elif app.enterLegalsButton.mousePress(mouseX, mouseY):
        app.enterLegalsMode = not app.enterLegalsMode
    elif app.changeLevelButton.mousePress(mouseX, mouseY):
        app.level = None
    elif app.playSingletonsButton.mousePress(mouseX, mouseY):
        if not app.competitionMode:
            playAllSingletons(app)
    elif app.playNextSingletonButton.mousePress(mouseX, mouseY):
        if not app.competitionMode:
            playSingleton(app)
    elif app.playHintButton.mousePress(mouseX, mouseY) and not app.competitionMode:
        hint1 = app.usersBoard.applyHint1()
        if hint1 != None:
            app.hintCells = {hint1}
        else:
            if app.automaticLegalsMode:
                hint2 = app.usersBoard.getHint2()
                if hint2 != None:
                    if app.usersBoard.applyHint2() != 'No more bans':
                        app.hintCells = set(hint2)
                    else:
                        app.showNoMoreHints = True
    elif app.showHintButton.mousePress(mouseX, mouseY) and not app.competitionMode:
        hint1 = app.usersBoard.getHint1()
        if hint1 != None:
            app.hintCells = {hint1}
        else:
            if app.automaticLegalsMode:
                hint2 = app.usersBoard.getHint2()
                if hint2 != None:
                    app.hintCells = set(hint2)
                else:
                    app.showNoMoreHints = True
    elif app.settingsButton.mousePress(mouseX, mouseY):
        setActiveScreen('settings_screen')
    elif app.redoButton.mousePress(mouseX, mouseY):
        if app.undoRedoPosition < len(app.undoRedoList)-1:
            app.undoRedoPosition += 1 #keeps track of what state is currently showing
        app.usersBoard = copy.deepcopy(app.undoRedoList[app.undoRedoPosition])
    elif app.undoButton.mousePress(mouseX, mouseY):
        if app.undoRedoPosition >= 1:
            app.undoRedoPosition -= 1 #keeps track of what state is currently showing 
        app.usersBoard = copy.deepcopy(app.undoRedoList[app.undoRedoPosition]) #keeps track of all the states from start to current
def getClickedLegal(app, x, y):
    legalCount = 1
    for c in range(3):
        for r in range(3):
            if app.showHoveringLegal == (r,c):
                return legalCount
            legalCount += 1
#returns the value of the selected key
def getKey(app, x, y):
    count = 0
    xButtonLeft,xButtonTop, xButtonWidth,xButtonHeight = 700, 430, 225, 63
    if xButtonLeft <= x <= xButtonLeft + xButtonWidth and xButtonTop <= y <= xButtonTop + xButtonHeight:
        return count
    else:
        for keyLeft, keyTop in app.keys:
            count += 1
            if keyLeft <= x <= keyLeft + app.keyWidth and keyTop <= y <= keyTop + app.keyHeight:
                return count

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:   
      return None

def sudoku_redrawAll(app):
    drawLabel('SUDOKU',
            app.width/2, 30, size=40, font = 'monospace')
    if app.level == None:
        buttonsTop = 173
        buttonsLeft = 336
        buttonWidth = 280
        buttonHeight = 44
        sprite = app.levelsGif[app.levelSpriteCounter]
        drawRect(0,0, app.width, app.height, fill = rgb(191,221,243))
        drawImage(sprite, app.width//2, app.height//2, align='center')
        for i in range(0,4):
            drawLabel(app.levels[i], buttonsLeft+buttonWidth//2, 
                        buttonsTop+buttonHeight//2+i*(buttonHeight+31),
                        font = 'monospace', size = 16)
        drawLabel('evil',471,523, font = 'monospace', size = 16)
        drawLabel('Select a difficulty!', 471, 100, size = 20, font = 'monospace')

    else:
        drawBoard(app)
        drawBlocks(app)
        drawBoardBorder(app)
        drawKeypad(app)
        app.helpButton.drawButton()
        app.createBoardButton.drawButton()
        app.changeLevelButton.drawButton()
        if app.automaticLegalsMode == False:
            fillAutomatic = 'white'
            fillManual = 'lavender'
        else:
            fillAutomatic = 'lavender'
            fillManual = 'white'
        app.manualLegalsButton.drawButton(fillManual, size = 12)
        app.automaticLegalsButton.drawButton(fillAutomatic, size = 12)
        app.playSingletonsButton.drawButton()
        app.playNextSingletonButton.drawButton()
        app.settingsButton.drawButton()
        app.showHintButton.drawButton()
        app.playHintButton.drawButton()
        app.undoButton.drawButton()
        app.redoButton.drawButton()
        if app.enterLegalsMode: app.enterKeysButton.drawButton()
        else: app.enterLegalsButton.drawButton()
        if app.showNoMoreSingletons:
            drawWarningMessage(app, 'No more singletons to play!')
        if app.showNoMoreHints:
            drawWarningMessage(app, 'No more hints available!')
        if app.isGameOver and app.competitionMode:
            drawWarningMessage(app, 'GAME OVER')
        elif app.isGameOver and app.showGameOverCounter > 3:
            drawSolvedPuzzle(app)
def drawSolvedPuzzle(app):
    drawRect(app.width//2 - 200, app.height//2-100, 400, 200, fill = 'lavender', border = 'black')
    drawLabel('Yayy! Good job you solved it.', app.width//2, app.height//2, size = 16, font = 'monospace')
def drawWarningMessage(app, message):
    drawRect(app.width//2 - 160, app.height//2 - 30, 320, 60, fill = 'white', border = 'black')
    drawLabel(message, app.width//2, app.height//2, fill = 'red',
                font = 'monospace', size = 16, bold = True)

def getLevel(app, x, y):
    buttonsTop = 173
    buttonsLeft = 336
    buttonWidth = 280
    buttonHeight = 44
    if 373 <= x <= 668 and 500 <= y <= 548:
        return "evil"
    for i in range(0,4):
        if (buttonsLeft <= x <= buttonsLeft+buttonWidth and 
            buttonsTop+i*(buttonHeight+31)<= y <= buttonsTop+buttonHeight+i*(buttonHeight+31)):
            return app.levels[i]
    return None
def drawKeypad(app):
    rows = 3
    cols = 3
    count = 0
    keyPadLeft = 700
    keyPadTop = 200
    xButtonTop = 0
    xButtonLeft = 0
    for col in range(cols):
        for row in range(rows):
            count += 1
            keyLeft = keyPadLeft+row*(app.keyWidth+12)
            keyTop = keyPadTop+col*(app.keyHeight+12)
            app.keys.append((keyLeft,keyTop))
            drawRect(keyLeft, keyTop, app.keyWidth, app.keyHeight, fill = rgb(237, 237, 237), border = 'black')
            if not app.enterLegalsMode:
                drawLabel(str(count), keyLeft + app.keyWidth//2, keyTop+app.keyHeight//2, size = 20, 
                            font = 'monospace')
            else:
                drawLabel(str(count), keyLeft + 10, keyTop+10, size = 15, 
                            font = 'monospace')
            if row == 0 and col == 2:
                xButtonTop = keyTop + app.keyHeight+12
                xButtonLeft = keyLeft
    drawRect(xButtonLeft,xButtonTop, app.xButtonWidth,app.xButtonHeight, fill = rgb(237, 237, 237), border = 'black')
    drawLabel('X', xButtonLeft+app.xButtonWidth//2, xButtonTop+app.xButtonHeight//2, size = 20,
                font = 'monospace')

def drawBlocks(app):
    for row in range(1, app.rows//3):
        cellWidth,cellHeight = getCellSize(app)
        blockWidth, blockHeight = (cellWidth*3), (cellHeight*3)
        boardBottom = app.boardTop + app.boardHeight
        boardRight = app.boardLeft + app.boardWidth
        drawLine(app.boardLeft + blockWidth*row, app.boardTop,
                app.boardLeft + blockWidth*row, boardBottom,
                   lineWidth = 5*app.cellBorderWidth)
        drawLine(app.boardLeft, app.boardTop + blockHeight*row, boardRight,
                    app.boardTop + blockHeight*row, 
                    lineWidth = 5*app.cellBorderWidth)    

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=5*app.cellBorderWidth)

def drawRedDot(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    #user enters a wrong value or user bans the correct value
    if app.usersBoard.board[row][col] != app.board.board[row][col] and app.usersBoard.board[row][col] != 0:
        if app.usersBoard.board[row][col] != app.boardSolution[row][col]:
            if not app.competitionMode:
                drawCircle(cellLeft+10, cellTop+10, 6, fill = app.redDotColor)
            else:
                app.isGameOver = True
            
    if (app.boardSolution[row][col] not in app.usersBoard.legals[row][col]) and app.usersBoard.board[row][col] == 0:
        if not app.competitionMode:
            drawCircle(cellLeft+10, cellTop+10, 6, fill = app.redDotColor)
        else:
            app.isGameOver = True

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    selectedCellRegions = set(app.usersBoard.getCellRegions(app.selectedCell[0], app.selectedCell[1]))
    #color starting cells
    if app.hintCells != None and (row, col) in app.hintCells:
        fill = app.hintColor
    elif (row,col) == app.selectedCell:
        fill = app.selectedCellColor
    elif app.usersBoard.board[row][col] != app.board.board[row][col]:
        #the values user inputs are gray
        fill = app.userInputValuesColor
        #hint cells start out green
    elif (row,col) in selectedCellRegions and app.highlightRegions:
        fill = app.highlightingRegionsColor
    elif app.board.board[row][col] != 0:
        selectedCellVal = app.usersBoard.board[app.selectedCell[0]][app.selectedCell[1]]
        print(selectedCellVal)
        #if a user clicks on a value, it will highlight all other values
        if (app.usersBoard.board[row][col] == selectedCellVal) and app.highlightSameValues:
            fill = app.highlightingValuesColor
        else:
            #starting values are blue
            fill = app.initialValuesColor
    else: fill = None

    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill= fill, border='black',
             borderWidth=app.cellBorderWidth)
    
    #draw only numbers that are filled in
    if not app.showSudokuSolution:
        if app.usersBoard.board[row][col] != 0:
            drawLabel(app.usersBoard.board[row][col], cellLeft+cellWidth//2, 
                        cellTop + cellHeight//2, size = 25, font = 'monospace', bold = True)
        else:
            if (row,col) == app.selectedCell:
                drawHoveringLegals(app, row, col)
                drawLegals(app, row, col)
            else:
                drawLegals(app, row, col)
        drawRedDot(app, row, col)
            
    else:
        drawLabel(app.boardSolution[row][col], cellLeft+cellWidth//2, 
                       cellTop + cellHeight//2, size = 25, font = 'monospace')
def drawHoveringLegals(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    legalCount = 1
    for c in range(3):
        for r in range(3):
            legalX = cellLeft+10+r*cellWidth//3
            legalY = cellTop+11+c*(cellHeight-10)//3
            if app.showHoveringLegal[0] == r and app.showHoveringLegal[1] == c:
                drawLabel(str(legalCount), legalX, legalY, size = 14, font = 'monospace', fill = 'purple', bold = True)
            legalCount += 1
def drawLegals(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    legalCount = 1
    for c in range(3):
        for r in range(3):
            legalX = cellLeft+10+r*cellWidth//3
            legalY = cellTop+11+c*(cellHeight-10)//3
            if app.automaticLegalsMode != False:
                legals = app.usersBoard.legals[row][col]
            else:
                legals = app.manualModeLegals[row][col]
            for legal in legals:
                if legal == legalCount:
                    drawLabel(str(legalCount), legalX, legalY, size = 14, font = 'monospace', bold = True)
            legalCount += 1


def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def loadAnimatedGif(app, path):
    pilImages = Image.open(path)
    if pilImages.format != 'GIF':
        raise Exception(f'{path} is not an animated image!')
    if not pilImages.is_animated:
        raise Exception(f'{path} is not an animated image!')
    cmuImages = [ ]
    for frame in range(pilImages.n_frames):
        pilImages.seek(frame)
        pilImage = pilImages.copy()
        cmuImages.append(CMUImage(pilImage))
    return cmuImages

def readFile(path):
    with open(path, "rt") as f:
        return f.read()
def print2dList(list):
    for l in list:
        print(l)

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def writeBoard(board):
    rows = len(board)
    cols = len(board[0])
    result = ''
    for row in range(rows):
        for col in range(cols):
            result = result +  str(board[row][col]) + ' '
        result = result + '\n'
    print(result)
    writeFile('/Users/sapavlinek/Desktop/mySudoku.txt', result)

def testBacktracker(filters):
    time0 = time.time()
    boardPaths = sorted(loadBoardPaths(filters))
    failedPaths = [ ]
    for boardPath in boardPaths:
        board = getBoard(boardPath)
        testBoard = State(board)
        print(boardPath)
        solution = testBoard.sudokuSolver()
        if not solution:
            failedPaths.append(boardPath)
    print()
    totalCount = len(boardPaths)
    failedCount = len(failedPaths)
    okCount = totalCount - failedCount
    time1 = time.time()
    if len(failedPaths) > 0:
        print('Failed boards:')
        for path in failedPaths:
            print(f'    {path}')
    percent = round(100 * okCount/totalCount)
    print(f'Success rate: {okCount}/{totalCount} = {percent}%')
    print(f'Total time: {round(time1-time0, 1)} seconds')

def main():
    runAppWithScreens(initialScreen='splash_screen', width=700)
    runApp()

main()
