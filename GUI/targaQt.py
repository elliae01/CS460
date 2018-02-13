from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer
from GUI.targaQt_UI_ONLY import Ui_MainWindow
import pygame
from pygame.locals import *
import time
import atexit
import sys

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class ImageWidget(QtGui.QWidget):
	def __init__(self,surface,parent=None):
		super(ImageWidget,self).__init__(parent)
		self.surface = surface
		global timerPygame
		global timerQtUI

		timerPygame = QTimer()
		timerPygame.timeout.connect(self.updatePygame)
		timerPygame.start(20)

		timerQtUI = QTimer()
		timerQtUI.timeout.connect(self.updateQtUI)
		timerQtUI.start(20)

	def paintEvent(self,event):
		qp=QtGui.QPainter()
		qp.begin(self)

		displayLoop(locSymbol, self.surface, userX,100, 180,False)
		w=self.surface.get_width()
		h=self.surface.get_height()
		self.data=self.surface.get_buffer().raw
		self.image=QtGui.QImage(self.data,w,h,QtGui.QImage.Format_RGB32)
		qp.drawImage(0,0,self.image)

		qp.end()

	def updatePygame(self):
		# setup so that all mouse clicks are disabled
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				None
			if event.type == MOUSEBUTTONDOWN:
				None
			if event.type == pygame.QUIT:
				exit_handler()
		# pygame.event.post(manUpdateEvent)
		moveIt()
		clock.tick(60)
		print("pygame clock time ticked: {}".format(str(clock.get_time())))

	def updateQtUI(self):
		self.update()
		print("Updated QT UI")

def addPygameDisplay(self):
	global renderedScene
	renderedScene = ImageWidget(gameDisplay)
	self.graphicsView = renderedScene
	self.gridLayout_2.addWidget(self.graphicsView, 0, 0, 1, 1)

	# Defines the symbol we use to illustrate location within Pygame #
def placeSymbol(gameDisplay,newImg, x, y):
	gameDisplay.blit(newImg, (x, y))

	# Defines the text objects used in Pygame #
def text_objects(text, font):
	black = (0, 0, 0)
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

	# Displays text to the Pygame Screen #
def message_display(gameDisplay,text):
	largeText = pygame.font.Font('freesansbold.ttf', 115)
	textSurf, textRect = text_objects(text, largeText)
	textRect.center = ((pygame_display_width / 2), (pygame_display_height / 2))
	gameDisplay.blit(textSurf, textRect)
	pygame.display.update()
	time.sleep(.1)

	# Rotates the symbol on the Pygame Window to reflect the heading supplied #
def orientation(originalSymbol,heading):
	facing = pygame.transform.rotate(originalSymbol, heading)
	return facing

	# Paints the symbols and messages to the Pygame window #
def displayLoop(locSymbol, gameDisplay, x, y, heading, shot):
	# Display the data within the GUI
	# pygame.display.flip()

	# Handles cases for supplied data being None
	if x == None:
		x = 0
	if y == None:
		y = 0
	if heading == None:
		heading = 0

	# Paints the background White
	white = (0, 0, 0)	# made black to see pygame drawing area
	# white = (255, 255, 255)
	gameDisplay.fill(white)

	# Prints Shot Fired to Window if Shot is recieved as True
	if shot:
		message_display(gameDisplay,'Shot Fired')

	# Defines a new symbol rotated to the proper heading
	locSymbol = orientation(locSymbol,heading)

	# Prints the new symbol in the x and y location supplied
	placeSymbol(gameDisplay,locSymbol, x, y)

	# # Updates the Pygame Display
	# pygame.display.update()

	# clock.tick(60)
	

def exit_handler():
	pygame.display.quit()
	pygame.quit()
	print("exit_handler", flush=True)

def moveIt():
	global direction
	global userX
	if(userX < 0 or userX > (pygame_display_width - iconWidth)):
		if userX < 0:
			userX = 0
			direction = movement
		else:
			userX = (pygame_display_width - iconWidth)
			direction = -movement
	userX += direction


if __name__ == "__main__":
	global direction
	global userX
	global movement
	global pygame_display_width
	global pygame_display_height
	global iconWidth
	global renderedScene

	# Set display width and height
	pygame_display_width = 700
	pygame_display_height =700

	direction = -1
	userX = 0
	movement = 5
	iconWidth = 30

	# Pygame variables
	manUpdateEvent = pygame.event.Event(pygame.USEREVENT + 1)

	# Setup exit handler to close down everything open
	atexit.register(exit_handler)

	# Initialize Pygame
	pygame.init()

	# Set the Pygame display
	gameDisplay = pygame.Surface((700,700))
	# gameDisplay = pygame.display.set_mode((pygame_display_width, pygame_display_height))
	pygame.display.set_caption('Position locator')

	# Get a reference to the Pygame Clock
	clock = pygame.time.Clock()

	# Defines a symbol for Pygame window
	locSymbol = pygame.image.load('symbol.png')

	# Initialize the loop variable to true
	active = True

	# Defines a delay for the loop
	delay = 1

	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)

	# add method to insert pygame display into UI
	Ui_MainWindow.addPygameDisplay = addPygameDisplay
	ui.addPygameDisplay()

	try:
		MainWindow.show()
		sys.exit(app.exec_())
		print("Application window closed", flush=True)
	except Exception as e:
		print(e)
		pygame.display.quit()
		pygame.quit()
