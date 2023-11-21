try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

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
    
    def __repr_(self):
        return self.name

    def mousePress(self, x, y):
        if self.left <= x <= self.left + self.width and self.top <= y <= self.top + self.height:
            return True
        return False
    def drawButton(self, fill = 'white', size = 16, borderWidth = 1):
        drawRect(self.left, self.top, self.width, self.height, border='black', fill = fill, borderWidth = borderWidth)
        drawLabel(self.name, self.left+self.width//2, self.top+self.height//2, font = 'monospace', size = size)

def settings_screen_onScreenStart(app):
    app.backButton = Button('Back',160,70,140,40)
    app.normalModeButton = Button('Normal Mode', 85, 200,210,30)
    app.keyModeButton = Button('Key-only Mode', 85, 240,210,30)
    app.mouseModeButton = Button('Mouse-only Mode', 85, 280,210,30)
    app.musicOnButton = Button('On', 85, 370, 105, 30)
    app.musicOffButton = Button('Off', 190, 370, 105, 30)
    app.highlightRegionsButton = Button('Highlight Regions', 85, 410, 210, 30)
    app.highlightSameValuesButton = Button('Highlight same values', 85, 450, 210, 30)
    app.highlightRegions = True
    app.highlightSameValues = True

    app.selectedCellColor = 'lavender'
    app.selectedGreenButton = Button('', 650, 200, 40, 30)
    app.selectedLavenderButton = Button('', 850, 200, 40, 30)
    app.selectedPinkButton = Button('', 700, 200, 40, 30)
    app.selectedBlueButton = Button('', 800, 200, 40, 30)
    app.selectedLightBlueButton = Button('', 750, 200, 40, 30)
    app.selectedGrayButton = Button('', 550, 200, 40, 30)
    app.selectedMossGreenButton = Button('', 600, 200, 40, 30)
    app.selectedPurpleButton = Button('', 900, 200, 40, 30)
    app.selectedButtons = [(app.selectedGreenButton, rgb(187, 214, 108)),
                        (app.selectedLavenderButton, 'lavender'),
                        (app.selectedPinkButton,rgb(241,142,155)),
                        (app.selectedGrayButton,rgb(237, 237, 237)),
                        (app.selectedLightBlueButton, 'lightblue'),
                        (app.selectedBlueButton, rgb(197, 231, 237)), 
                        (app.selectedMossGreenButton, rgb(224, 236, 223)),
                        (app.selectedPurpleButton, rgb(134, 151, 193))
                        ]
    app.initialValuesColor = rgb(197, 231, 237)
    app.initialGreenButton = Button('', 650, 250, 40, 30)
    app.initialLavenderButton = Button('', 850, 250, 40, 30)
    app.initialPinkButton = Button('', 700, 250, 40, 30)
    app.initialBlueButton = Button('', 800, 250, 40, 30)
    app.initialLightBlueButton = Button('', 750, 250, 40, 30)
    app.initialGrayButton = Button('', 550, 250, 40, 30)
    app.initialMossGreenButton = Button('', 600, 250, 40, 30)
    app.initialPurpleButton = Button('', 900, 250, 40, 30)
    app.initialButtons = [(app.initialGreenButton, rgb(187, 214, 108)),
                        (app.initialLavenderButton, 'lavender'),
                        (app.initialPinkButton,rgb(241,142,155)),
                        (app.initialGrayButton,rgb(237, 237, 237)),
                        (app.initialLightBlueButton, 'lightblue'),
                        (app.initialBlueButton, rgb(197, 231, 237)), 
                        (app.initialMossGreenButton, rgb(224, 236, 223)),
                        (app.initialPurpleButton, rgb(134, 151, 193))
                        ]

    app.userInputValuesColor = rgb(237, 237, 237)
    app.inputGreenButton = Button('', 650, 300, 40, 30)
    app.inputLavenderButton = Button('', 850, 300, 40, 30)
    app.inputPinkButton = Button('', 700, 300, 40, 30)
    app.inputBlueButton = Button('', 800, 300, 40, 30)
    app.inputLightBlueButton = Button('', 750, 300, 40, 30)
    app.inputGrayButton = Button('', 550, 300, 40, 30)
    app.inputMossGreenButton = Button('', 600, 300, 40, 30)
    app.inputPurpleButton = Button('', 900, 300, 40, 30)
    app.inputButtons = [(app.inputGreenButton, rgb(187, 214, 108)),
                        (app.inputLavenderButton, 'lavender'),
                        (app.inputPinkButton,rgb(241,142,155)),
                        (app.inputGrayButton,rgb(237, 237, 237)),
                        (app.inputLightBlueButton, 'lightblue'),
                        (app.inputBlueButton, rgb(197, 231, 237)), 
                        (app.inputMossGreenButton, rgb(224, 236, 223)),
                        (app.inputPurpleButton, rgb(134, 151, 193))
                        ]

    app.redDotColor = rgb(241,142,155)
    app.dotGreenButton = Button('', 650, 350, 40, 30)
    app.dotLavenderButton = Button('', 850, 350, 40, 30)
    app.dotPinkButton = Button('', 700, 350, 40, 30)
    app.dotBlueButton = Button('', 800, 350, 40, 30)
    app.dotLightBlueButton = Button('', 750, 350, 40, 30)
    app.dotGrayButton = Button('', 550, 350, 40, 30)
    app.dotMossGreenButton = Button('', 600, 350, 40, 30)
    app.dotPurpleButton = Button('', 900, 350, 40, 30)
    app.dotButtons = [(app.dotGreenButton, rgb(187, 214, 108)),
                        (app.dotLavenderButton, 'lavender'),
                        (app.dotPinkButton,rgb(241,142,155)),
                        (app.dotGrayButton,rgb(237, 237, 237)),
                        (app.dotLightBlueButton, 'lightblue'),
                        (app.dotBlueButton, rgb(197, 231, 237)), 
                        (app.dotMossGreenButton, rgb(224, 236, 223)),
                        (app.dotPurpleButton, rgb(134, 151, 193))
                        ]

    app.hintColor = rgb(187, 214, 108)
    app.hintGreenButton = Button('', 650, 400, 40, 30)
    app.hintLavenderButton = Button('', 850, 400, 40, 30)
    app.hintPinkButton = Button('', 700, 400, 40, 30)
    app.hintBlueButton = Button('', 800, 400, 40, 30)
    app.hintLightBlueButton = Button('', 750, 400, 40, 30)
    app.hintGrayButton = Button('', 550, 400, 40, 30)
    app.hintMossGreenButton = Button('', 600, 400, 40, 30)
    app.hintPurpleButton = Button('', 900, 400, 40, 30)
    app.hintButtons = [(app.hintGreenButton, rgb(187, 214, 108)),
                        (app.hintLavenderButton, 'lavender'),
                        (app.hintPinkButton,rgb(241,142,155)),
                        (app.hintGrayButton,rgb(237, 237, 237)),
                        (app.hintLightBlueButton, 'lightblue'),
                        (app.hintBlueButton, rgb(197, 231, 237)), 
                        (app.hintMossGreenButton, rgb(224, 236, 223)),
                        (app.hintPurpleButton, rgb(134, 151, 193))
                        ]

    app.highlightingRegionsColor = rgb(224, 236, 223)
    app.regionGreenButton = Button('', 650, 450, 40, 30)
    app.regionLavenderButton = Button('', 850, 450, 40, 30)
    app.regionPinkButton = Button('', 700, 450, 40, 30)
    app.regionBlueButton = Button('', 800, 450, 40, 30)
    app.regionLightBlueButton = Button('', 750, 450, 40, 30)
    app.regionGrayButton = Button('', 550, 450, 40, 30)
    app.regionMossGreenButton = Button('', 600, 450, 40, 30)
    app.regionPurpleButton = Button('', 900, 450, 40, 30)
    app.regionButtons = [(app.regionGreenButton, rgb(187, 214, 108)),
                        (app.regionLavenderButton, 'lavender'),
                        (app.regionPinkButton,rgb(241,142,155)),
                        (app.regionGrayButton,rgb(237, 237, 237)),
                        (app.regionLightBlueButton, 'lightblue'),
                        (app.regionBlueButton, rgb(197, 231, 237)), 
                        (app.regionMossGreenButton, rgb(224, 236, 223)),
                        (app.regionPurpleButton, rgb(134, 151, 193))
                        ]
    app.highlightingValuesColor = rgb(134, 151, 193)
    app.valuesGreenButton = Button('', 650, 500, 40, 30)
    app.valuesLavenderButton = Button('', 850, 500, 40, 30)
    app.valuesPinkButton = Button('', 700, 500, 40, 30)
    app.valuesBlueButton = Button('', 800, 500, 40, 30)
    app.valuesLightBlueButton = Button('', 750, 500, 40, 30)
    app.valuesGrayButton = Button('', 550, 500, 40, 30)
    app.valuesMossGreenButton = Button('', 600, 500, 40, 30)
    app.valuesPurpleButton = Button('', 900, 500, 40, 30)
    app.valuesButtons = [(app.valuesGreenButton, rgb(187, 214, 108)),
                        (app.valuesLavenderButton, 'lavender'),
                        (app.valuesPinkButton,rgb(241,142,155)),
                        (app.valuesGrayButton,rgb(237, 237, 237)),
                        (app.valuesLightBlueButton, 'lightblue'),
                        (app.valuesBlueButton, rgb(197, 231, 237)), 
                        (app.valuesMossGreenButton, rgb(224, 236, 223)),
                        (app.valuesPurpleButton, rgb(134, 151, 193))
                        ]

    app.modes = 'Normal Mode'
    app.pausedMusic = False
def settings_screen_onKeyPress(app, key):
    if key == 'b': setActiveScreen('sudoku')
def settings_screen_onMousePress(app, mouseX, mouseY):
    if app.backButton.mousePress(mouseX, mouseY): setActiveScreen('sudoku')
    selectedMode = getModeButton(app, mouseX, mouseY)
    if selectedMode != None:
        app.modes = selectedMode
    elif app.musicOnButton.mousePress(mouseX, mouseY):
        app.pausedMusic = False
    elif app.musicOffButton.mousePress(mouseX, mouseY):
        app.pausedMusic = True
    elif app.highlightRegionsButton.mousePress(mouseX, mouseY):
        app.highlightRegions = not app.highlightRegions
    elif app.highlightSameValuesButton.mousePress(mouseX, mouseY):
        app.highlightSameValues = not app.highlightSameValues

    for button in app.selectedButtons:
        if button[0].mousePress(mouseX, mouseY):
            app.selectedCellColor = button[1]
    for button in app.hintButtons:
        if button[0].mousePress(mouseX, mouseY):
            app.hintColor = button[1]
    for button in app.dotButtons:
        if button[0].mousePress(mouseX, mouseY):
            app.redDotColor = button[1]
    for button in app.inputButtons:
        if button[0].mousePress(mouseX, mouseY):
            app.userInputValuesColor = button[1]
    for button in app.initialButtons:
        if button[0].mousePress(mouseX, mouseY):
            app.initialValuesColor = button[1]
    for button in app.valuesButtons:
        if button[0].mousePress(mouseX, mouseY):
            app.highlightingValuesColor = button[1]
    for button in app.regionButtons:
        if button[0].mousePress(mouseX, mouseY):
            app.highlightingRegionsColor = button[1]
                

def getModeButton(app, x, y):
    if app.normalModeButton.mousePress(x, y):
        return app.normalModeButton.name
    elif app.keyModeButton.mousePress(x, y):
        return app.keyModeButton.name
    elif app.mouseModeButton.mousePress(x, y):
        return app.mouseModeButton.name

def settings_screen_redrawAll(app):
    drawLabel('SUDOKU',
              app.width/2, 30, size=40, font = 'monospace')
    drawLabel('GamePlay Mode',
              190, 170, size=20, font = 'monospace', bold = True)
    app.backButton.drawButton()
    drawModeButtons(app)
    if not app.pausedMusic:
        fillOn = 'lavender'
        fillOff = 'white'
    else:
        fillOff = 'lavender'
        fillOn = 'white'
    app.musicOffButton.drawButton(fillOff)
    app.musicOnButton.drawButton(fillOn)
    
    if app.highlightRegions:
        fill = 'lavender'
    else:
        fill = 'white'
    app.highlightRegionsButton.drawButton(fill = fill)
    
    if app.highlightSameValues:
        fill = 'lavender'
    else:
        fill = 'white'
    app.highlightSameValuesButton.drawButton(fill = fill)
    drawLabel('Music', 190, 350, size=20, font = 'monospace', bold = True)
    drawLabel('Color Preferences', 530, 170, size = 20, font = 'monospace', bold = True)
    drawLabel('Selected Cell:', 530, 215, size = 17, font = 'monospace', align = 'right' )
    drawLabel('Initial Values:', 530, 265, size = 17, font = 'monospace',align = 'right' )
    drawLabel('User input:', 530, 315, size = 17, font = 'monospace', align = 'right')
    drawLabel('Error dot:', 530, 365, size = 17, font = 'monospace', align = 'right')
    drawLabel('Hints:', 530, 415, size = 17, font = 'monospace', align = 'right')
    drawLabel('Highlight Regions:', 530, 465, size = 17, font = 'monospace', align = 'right')
    drawLabel('Highlight Same Values:', 530, 515, size = 17, font = 'monospace', align = 'right')
    
    for button in app.selectedButtons:
        if app.selectedCellColor == button[1]:
            borderWidth = 3
        else:
            borderWidth = 1
        button[0].drawButton(fill = button[1], borderWidth = borderWidth)
    
    for button in app.hintButtons:
        if app.hintColor == button[1]:
            borderWidth = 3
        else:
            borderWidth = 1
        button[0].drawButton(fill = button[1], borderWidth = borderWidth)
    
    for button in app.dotButtons:
        if app.redDotColor == button[1]:
            borderWidth = 3
        else:
            borderWidth = 1
        button[0].drawButton(fill = button[1], borderWidth = borderWidth)
    
    for button in app.inputButtons:
        if app.userInputValuesColor == button[1]:
            borderWidth = 3
        else:
            borderWidth = 1
        button[0].drawButton(fill = button[1], borderWidth = borderWidth)
    
    for button in app.initialButtons:
        if app.initialValuesColor == button[1]:
            borderWidth = 3
        else:
            borderWidth = 1
        button[0].drawButton(fill = button[1], borderWidth = borderWidth)
    
    for button in app.valuesButtons:
        if app.highlightingValuesColor == button[1]:
            borderWidth = 3
        else:
            borderWidth = 1
        button[0].drawButton(fill = button[1], borderWidth = borderWidth)

    for button in app.regionButtons:
        if app.highlightingRegionsColor == button[1]:
            borderWidth = 3
        else:
            borderWidth = 1
        button[0].drawButton(fill = button[1], borderWidth = borderWidth)




def drawModeButtons(app):
    modes = [app.normalModeButton, app.keyModeButton, app.mouseModeButton]
    for button in modes:
        if app.modes == button.name: 
            fill = 'lavender'
        else: 
            fill = 'white'
        button.drawButton(fill)
    
 