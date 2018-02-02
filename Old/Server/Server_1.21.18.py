import socket
from UserInformation import *
import pickle
import pygame
import random
import time
import atexit

    # Defines the symbol we use to illustrate location within Pygame #
def placeSymbol(gameDisplay,newImg, x, y):
    gameDisplay.blit(newImg, (x, y))

    # Defines the text objects used in Pygame #
def text_objects(text, font):
    white = (0, 0, 0)
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

    # Displays text to the Pygame Screen #
def message_display(gameDisplay,text):
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
def displayLoop(locSymbol, gameDisplay, x, y, heading, shot):
    # Handles cases for supplied data being None
    if x == None:
        x = 0
    if y == None:
        y = 0
    if heading == None:
        heading = 0

    # Paints the background White
    white = (255, 255, 255)
    gameDisplay.fill(white)

    # Prints Shot Fired to Window if Shot is recieved as True
    if shot:
        message_display(gameDisplay,'Shot Fired')

    # Defines a new symbol rotated to the proper heading
    locSymbol = orientation(locSymbol,heading)

    # Prints the new symbol in the x and y location supplied
    placeSymbol(gameDisplay,locSymbol, x, y)

    # Updates the Pygame Display
    pygame.display.update()


def connectionSetup(ip, port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(ip)
        address = (ip, port)

        server.bind(address)
        server.listen(1)
        print("-> Started listening on     Ip - ", ip, "     Port - ", port)
        client, addr = server.accept()
        print("-> Made a connection with     IP - ", addr[0], "    Address - ", addr[1])
    except Exception as e:
        print(e)

    return client, addr


def collectionLoop(client):
    data = client.recv(4096)
    Structure = pickle.loads(data)

    dataStruct = UserInformation(Structure[1])
    dataStruct.setEMG(
        [Structure[2][0], Structure[2][1], Structure[2][2], Structure[2][3], Structure[2][4], Structure[2][5],
         Structure[2][6], Structure[2][7]])
    dataStruct.setRoll(Structure[3])
    dataStruct.setPitch(Structure[4])
    dataStruct.setYaw(Structure[5])
    dataStruct.setShot(Structure[6])
    dataStruct.setHeadXAxis(Structure[7])
    dataStruct.setHeadYAxis(Structure[8])
    dataStruct.setHeadZAxis(Structure[9])
    dataStruct.setHeadHeading(Structure[10])
    dataStruct.setHeadDegrees(Structure[11])
    dataStruct.setBodyXAxis(Structure[12])
    dataStruct.setBodyYAxis(Structure[13])
    dataStruct.setBodyZAxis(Structure[14])
    dataStruct.setBodyHeading(Structure[15])
    dataStruct.setBodyDegrees(Structure[16])
    dataStruct.setLocationXAxis(Structure[17])
    dataStruct.setLocationYAxis(Structure[18])
    dataStruct.setLocationZAxis(Structure[19])
    dataStruct.setHeartRate(Structure[20])

    return dataStruct

def storeData(dataStruct):
    print("Storing Data Now")


def exit_handler():
    client.close()
    pygame.display.quit()
    pygame.quit()
    print("Application closed")

if __name__ == '__main__':
    # Setup exit handler to close down everything open
    atexit.register(exit_handler)

    # Initialize Pygame
    pygame.init()

    # Set display width and height
    display_width = 1200
    display_height = 1000

    # Set the Pygame display
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Position locator')

    # Get a reference to the Pygame Clock
    clock = pygame.time.Clock()

    # Set the IP address and Port
    ip = '192.168.2.4'
    port = 5000

    # Defines a symbol for Pygame window
    locSymbol = pygame.image.load('symbol.png')

    # Call to Setup Connection passing IP and Port.  Store client information returned.
    client,addr = connectionSetup(ip, port)

    # Initialize the loop variable to true
    active = True

    # Defines a delay for the loop
    delay = .1

    try:
        # Main loop within the Server
        while(active):
            # Reconstruct the Data Structure from bytestream
            dataStruct = collectionLoop(client)
            # Store the Data Structure to Database
            storeData(dataStruct)
            # Display the data within the GUI
            displayLoop(locSymbol, gameDisplay, (dataStruct.getLocationXAxis() * 4),
                        (dataStruct.getLocationYAxis() * 4), dataStruct.getHeadHeading(),
                        dataStruct.getShot())
            # Delays the loop for time set in delay variable
            time.sleep(delay)

    except:
        print("Application Closed")
        client.close()
        pygame.display.quit()
        pygame.quit()
