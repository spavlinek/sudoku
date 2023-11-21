try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from PIL import Image, GifImagePlugin
from runAppWithScreens import *
##################################
# SplashScreen
##################################

def splash_screen_onScreenStart(app):
    app.stepsPerSecond = 5
    app.counter = 0
    app.button = CMUImage(Image.open('splashButton.png'))
    app.buttonWidth = Image.open('splashButton.png').width
    app.buttonHeight = Image.open('splashButton.png').height
    app.sprites = loadAnimatedGif(app, 'splashScreenGif.gif')
    app.spriteCounter = 0
    app.pausedMusic = False

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

def splash_screen_onKeyPress(app, key):
    if key == 'enter': setActiveScreen('sudoku')

def splash_screen_onMousePress(app, mouseX, mouseY):
    if (app.width//2 - app.buttonWidth//2 < mouseX <  app.width//2 + app.buttonWidth//2 and
        610 - app.buttonHeight//2 < mouseY < 610 + app.buttonHeight//2): #button is 300x45
        setActiveScreen('sudoku')

def splash_screen_redrawAll(app):
    drawRect(0,0, app.width, app.height, fill = rgb(181, 218, 225))
    # Draw the current sprite image:
    sprite = app.sprites[app.spriteCounter]
    drawImage(sprite, 430, 220, align='center')
    drawImage(app.button, app.width//2, 610, align='center')
    drawLabel("Click or press 'enter' to continue >", app.width//2, 610, size = 12, 
                align='center', font = 'monospace', bold = True, fill = 'black')
    drawLabel("SUDOKU", app.width//2, 290, size = 50, font = 'monospace', fill = 'black')

    
def splash_screen_onStep(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
    app.counter += 1
    if not app.pausedMusic:
          app.sound.play(loop=True)
    elif app.pausedMusic:
          app.sound.pause()