try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
import math
##################################
# Enter a board Screen
##################################
class Button(): 
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

def enterBoard_screen_onScreenStart(app):
    app.newBoard = [[0]*9 for i in range(9)]
    app.saveButton = Button('Save Board', 310,70,120,40)
    app.enterPathButton = Button('Enter Board Path', 440, 70, 180, 40)
    app.path = None
    app.keysEnterBoard = []
def enterBoard_screen_onKeyPress(app, key):
    if key == 'b': setActiveScreen('sudoku')
    if key == 'h': setActiveScreen('help_screen')
    elif app.modes != 'Mouse-only Mode':
        #move the user's cell selection with keys
        if key == 'left':  moveSelection(app, 0, -1)
        elif key == 'right': moveSelection(app, 0, +1)
        elif key == 'up':    moveSelection(app ,-1, 0)
        elif key == 'down':  moveSelection(app, +1, 0)
        
        elif app.selectedCell != None:
            sRow = app.selectedCell[0]
            sCol = app.selectedCell[1]
            if key.isdigit() and app.newBoard[sRow][sCol] == 0: 
                app.newBoard[sRow][sCol] = int(key)

def enterBoard_screen_onMousePress(app, mouseX, mouseY):
    if app.backButton.mousePress(mouseX, mouseY): setActiveScreen('sudoku')
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        if selectedCell == app.selectedCell:
            app.selectedCell = None
        else:
            app.selectedCell = selectedCell
    if app.modes != 'Key-only Mode':
        selectedKey = getKey(app, mouseX, mouseY)
        if selectedKey != None and app.selectedCell != None:
            sRow = app.selectedCell[0]
            sCol = app.selectedCell[1]
            if app.newBoard[sRow][sCol] == 0:
                app.newBoard[sRow][sCol] = selectedKey
    
    if app.helpButton.mousePress(mouseX, mouseY):
        setActiveScreen('help_screen')
    elif app.enterPathButton.mousePress(mouseX, mouseY):
        app.path = app.getTextInput('Enter the path to your board:')
        if app.path == '':
            app.path = None
    elif app.saveButton.mousePress(mouseX, mouseY):
        writeBoard(app.newBoard)

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

def moveSelection(app, drow, dcol):
    if app.selectedCell != None:
        selectedRow, selectedCol = app.selectedCell
        newSelectedRow = (selectedRow + drow) % app.rows
        newSelectedCol = (selectedCol + dcol) % app.cols
        app.selectedCell = (newSelectedRow, newSelectedCol)

#returns the value of the selected key
def getKey(app, x, y):
    keyCount = 0
    xButtonLeft,xButtonTop, xButtonWidth,xButtonHeight = 700, 375, 225, 63
    if xButtonLeft <= x <= xButtonLeft + xButtonWidth and xButtonTop <= y <= xButtonTop + xButtonHeight:
        return keyCount
    else:
        for keyLeft, keyTop in app.keysEnterBoard:
            keyCount += 1
            if keyLeft <= x <= keyLeft + app.keyWidth and keyTop <= y <= keyTop + app.keyHeight:
                return keyCount
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

def enterBoard_screen_redrawAll(app):
    drawLabel('ENTER OWN BOARD',
              app.width/2, 30, size=40, font = 'monospace')
    drawBoard(app)
    drawBlocks(app)
    drawBoardBorder(app)
    drawKeypad(app)
    app.helpButton.drawButton()
    app.backButton.drawButton()
    app.saveButton.drawButton()
    app.enterPathButton.drawButton()

def getLevel(app, x, y):
    buttonsTop = 178
    buttonsLeft = 380
    buttonWidth = 280
    buttonHeight = 44
    if 373 <= x <= 668 and 500 <= y <= 548:
        return "evil"
    for i in range(0,4):
        if (buttonsLeft <= x <= buttonsLeft+buttonWidth and 
            buttonsTop+i*(buttonHeight+31)<= y <= buttonsTop+buttonHeight+i*(buttonHeight+31)):
            return app.levels[i]

def drawKeypad(app):
    rows = 3
    cols = 3
    count = 0
    keyPadLeft = 700
    keyPadTop = 150
    xButtonTop = 0
    xButtonLeft = 0
    for col in range(cols):
        for row in range(rows):
            count += 1
            keyLeft = keyPadLeft+row*(app.keyWidth+12)
            keyTop = keyPadTop+col*(app.keyHeight+12)
            app.keysEnterBoard.append((keyLeft,keyTop))
            drawRect(keyLeft, keyTop, app.keyWidth, app.keyHeight, fill = rgb(237, 237, 237), border = 'black')
            drawLabel(str(count), keyLeft + app.keyWidth//2, keyTop+app.keyHeight//2, size = 20, 
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

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    #color starting cells
    if (row,col) == app.selectedCell:
        fill = 'lavender'
    elif app.newBoard[row][col] != 0:
        fill = rgb(197, 231, 237)
    else: fill =  None

    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill= fill, border='black',
             borderWidth=app.cellBorderWidth)
    if app.newBoard[row][col] != 0:
        drawLabel(app.newBoard[row][col], cellLeft+cellWidth//2, 
                    cellTop + cellHeight//2, size = 25, font = 'monospace', bold = True)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
