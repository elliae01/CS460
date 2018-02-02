import pygame
import time
from Server import *
from UserInformation import *
import random

class coordinate:
    x = None
    y = None
    def __init__(self,originalX,originalY):
        self.x = originalX
        self.y = originalY
    def getX(self):
        return self.x
    def getY(self):
        return self.y

def guiMain(dataStruct):
    # Initialize Pygame
    pygame.init()

    # Set display width and height
    display_width = 700
    display_height = 700

    xAdjust = 5
    yAdjust = 5

    # Set the Pygame display
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Targamite Project')

    # Get a reference to the Pygame Clock
    clock = pygame.time.Clock()

    # Defines a symbol for Pygame window
    locSymbol = pygame.image.load('symbol.png')
    targetSymbol = pygame.image.load('target.png')

    topTarget = False
    bottomTarget = False
    leftTarget = False
    rightTarget = False

    tracers = []
    while dataStruct.getRun():
        xLoc = noneRemover(dataStruct.getLocationXAxis())
        yLoc = noneRemover(dataStruct.getLocationYAxis())
        heading = noneRemover(dataStruct.getHeadHeading())
        shot = noneRemover(dataStruct.getShot())

        newCoordinate = coordinate(xLoc*xAdjust+15,yLoc*yAdjust+15)
        tracers.append(newCoordinate)

        # Prints Shot Fired to Window if Shot is recieved as True
        if shot:
            message_display(gameDisplay, display_width, display_height, 'Shot Fired')

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dataStruct.setRun(False)
                if event.key == pygame.K_UP:
                    topTarget = True
                if event.key == pygame.K_DOWN:
                    bottomTarget = True
                if event.key == pygame.K_RIGHT:
                    rightTarget = True
                if event.key == pygame.K_LEFT:
                    leftTarget = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    topTarget = False
                if event.key == pygame.K_DOWN:
                    bottomTarget = False
                if event.key == pygame.K_RIGHT:
                    rightTarget = False
                if event.key == pygame.K_LEFT:
                    leftTarget = False

        display(locSymbol, gameDisplay, (xLoc*xAdjust), (yLoc*yAdjust), heading, targetSymbol, topTarget, bottomTarget, rightTarget,
                leftTarget, display_width, display_height,tracers)
        clock.tick(150)

    pygame.quit()
    sys.exit()

    # Defines the symbol we use to illustrate location within Pygame #
def placeSymbol(gameDisplay,newImg, x, y):
    gameDisplay.blit(newImg, (x, y))

    # Defines the text objects used in Pygame #
def text_objects(text, font):
    black = (0, 0, 0)
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

    # Displays text to the Pygame Screen #
def message_display(gameDisplay, display_width, display_height,text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    textSurf, textRect = text_objects(text, largeText)
    textRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(.1)
    # Rotates the symbol on the Pygame Window to reflect the heading supplied #
def orientation(originalSymbol,heading):
    facing = pygame.transform.rotate(originalSymbol, heading)
    return facing

    # Paints the symbols and messages to the Pygame window #
def display(locSymbol, gameDisplay, x, y, heading, targetSymbol, topTarget, bottomTarget, rightTarget,
            leftTarget, display_width, display_height, tracers):
    # Paints the background White
    white = (255, 255, 255)
    red = (255,0,0)
    gameDisplay.fill(white)

    for tracer in tracers:
        pygame.draw.circle(gameDisplay, red, [int(tracer.getX()), int(tracer.getY())], 5)

    # Defines a new symbol rotated to the proper heading
    locSymbol = orientation(locSymbol,heading)

    if(topTarget):
        placeSymbol(gameDisplay, targetSymbol, display_width/2, 20)
    if(bottomTarget):
        placeSymbol(gameDisplay, targetSymbol, display_width/2, display_height - 40)
    if(rightTarget):
        placeSymbol(gameDisplay, targetSymbol, display_width - 40, display_height/2)
    if(leftTarget):
        placeSymbol(gameDisplay, targetSymbol, 20, display_height/2)

    # Prints the new symbol in the x and y location supplied
    placeSymbol(gameDisplay,locSymbol, x, y)

    # Updates the Pygame Display
    pygame.display.update()