import sys
import pygame
from pygame.locals import *
import time
import atexit
import sys


def runPygame(x, y):
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
	while True:  # dataStruct.getRun()
		# xLoc = noneRemover(dataStruct.getLocationXAxis())
		# yLoc = noneRemover(dataStruct.getLocationYAxis())
		# heading = noneRemover(dataStruct.getHeadHeading())
		# shot = noneRemover(dataStruct.getShot())

		xLoc = x
		yLoc = y
		heading = 30
		shot = False

		newCoordinate = coordinate(xLoc * xAdjust + 15, yLoc * yAdjust + 15)
		tracers.append(newCoordinate)

		# Prints Shot Fired to Window if Shot is recieved as True
		if shot:
			message_display(gameDisplay, display_width, display_height, 'Shot Fired')

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					# dataStruct.setRun(False)
					pass
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
			if event.type == MOUSEBUTTONUP:
				None
			if event.type == MOUSEBUTTONDOWN:
				None
			if event.type == pygame.QUIT:
				exit_handler()

		display(locSymbol, gameDisplay, x, y, heading, targetSymbol, topTarget,
				bottomTarget, rightTarget,
				leftTarget, display_width, display_height, tracers)
		clock.tick(150)

	print("Pygame window closing", flush=True)
	exit_handler()

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
	pygame.display.update()  # Rotates the symbol on the Pygame Window to reflect the heading supplied #

# Defines the text objects used in Pygame #
def text_objects(text, font):
	black = (0, 0, 0)
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

# Displays text to the Pygame Screen #
def message_display(gameDisplay, display_width, display_height, text):
	largeText = pygame.font.Font('freesansbold.ttf', 115)
	textSurf, textRect = text_objects(text, largeText)
	textRect.center = ((display_width / 2), (display_height / 2))
	gameDisplay.blit(textSurf, textRect)
	pygame.display.update()
	time.sleep(.1)

def orientation(originalSymbol, heading):
	facing = pygame.transform.rotate(originalSymbol, heading)
	return facing

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

def exit_handler():
	pygame.display.quit()
	pygame.quit()
	print("exit_handler", flush=True)
	sys.exit()

	# Defines the symbol we use to illustrate location within Pygame #
def placeSymbol(gameDisplay,newImg, x, y):
	area = TargaPlotter(0, 0, 700 - 20, 700 - 20)
	gameDisplay.blit(newImg, area.plot(x,y))

class TargaPlotter:
	# By default:
	# the origin is the center of the defined area, and
	# the plotting will be limited to the closest edge if the value goes out of bounds
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.doLimitBounds = True
		self.setOrigin(self.x+(self.w/2), self.y+(self.h/2))

	def setOrigin(self, x, y):
		self.origin = (x, y)

	def setDoLimitBounds(self, val):
		self.doLimitBounds = val

	def limitBounds(self, x, y):
		if(self.doLimitBounds):
			if(x <= self.x):
				x = self.x
			if(x >= (self.x+self.w)):
				x = (self.x+self.w)
			if(y <= self.y):
				y = self.y
			if(y >= (self.y+self.h)):
				y = (self.y+self.h)
		return (x,y)

	def plot(self, x, y):
		x = self.origin[0]+x
		y = self.origin[1]-y
		return self.limitBounds(x,y)

if __name__ == '__main__':
	# Examples

	# set the plotting area top left corner to (20,100) in pygame coordinates and set width and height
	area1 = TargaPlotter(20, 120, 60, 400)
	print(area1.plot(40, 300))	# The function "plot" takes in coordinates relative to the origin you
								# set (by default the center of the plotting rectangle if you don't set) and
								# outputs a point pygame understands.

	# Check console for output of above

	# Implemented in pygame to limit display within a box.
	# Change doLimitBounds = False if want symbols able to move outside of edges.
	runPygame(900,900)	# change x and y to move symbol
	# notice how the TargaPlotter is implemented in the PlaceSymbol method so
	# that everything drawn in that "area' automatically is converted

