try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from PIL import Image, GifImagePlugin
from runAppWithScreens import *

##################################
# Helper Screen
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

def help_screen_onScreenStart(app):
    app.backButton = Button('Back',160,70,140,40)
    app.helpImageCounter = 1
    app.helpImage = CMUImage(Image.open(getHelpImage(app)))
    app.arrowRightButton = Button('>', 900, 360, 30, 80)
    app.arrowLeftButton = Button('<', 100, 360, 30, 80)

def getHelpImage(app):
    return f'helpIm{app.helpImageCounter}.png'
def help_screen_onKeyPress(app, key):
    if key == 'b': setActiveScreen('sudoku')
    elif key == 'right':
        if app.helpImageCounter < 5:
            app.helpImageCounter += 1
        app.helpImage = CMUImage(Image.open(getHelpImage(app)))
    elif key == 'left':
        if app.helpImageCounter > 1:
            app.helpImageCounter -= 1
        app.helpImage = CMUImage(Image.open(getHelpImage(app)))
def help_screen_onMousePress(app, mouseX, mouseY):
    if app.backButton.mousePress(mouseX, mouseY): setActiveScreen('sudoku')
    if app.arrowRightButton.mousePress(mouseX, mouseY):
        if app.helpImageCounter < 6:
            app.helpImageCounter += 1
        app.helpImage = CMUImage(Image.open(getHelpImage(app)))
    if app.arrowLeftButton.mousePress(mouseX, mouseY):
        if app.helpImageCounter > 1:
            app.helpImageCounter -= 1
        app.helpImage = CMUImage(Image.open(getHelpImage(app)))

def help_screen_redrawAll(app):
    drawImage(app.helpImage, app.width//2, app.height//2-10, align='center')
    drawLabel('SUDOKU',
            app.width/2, 30, size=40, font = 'monospace')
    app.backButton.drawButton()
    app.arrowRightButton.drawButton()
    app.arrowLeftButton.drawButton()
    
    #singleton keys 'a' for all and 'n' for next
    #

    