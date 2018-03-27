import pygame
import sys
import time
import cx_Oracle
import pandas as pd
from Reactionalytics import *
# from Analysis.Reactionalytics import *
# from Server.UserInformation import *
from datetime import datetime

        # # # Control Panel Section # # #

# Set display width and height
display_width = 1500
display_height = 800

# Set Width and Height of Tracer Section
tracer_width = display_width*.6
tracer_heigth = display_height*.82

# Banner Width and Height
banner_width = 0
banner_height = 100

# frames per second
frame_rate = 10

# Database Information
user = 'SYSMAN'
password = 'System_Admin1'
host = 'localhost'
database_name = 'orcl'

# Set-up the colors for use in GUI
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GREY =(200, 200, 200)
LIGHT_RED =(180, 0, 0)
RED = (220,   0,   0)
BRIGHT_RED   = (255,   0,   0)
GREEN = (  0, 200,   0)
BRIGHT_GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
CYAN = ( 0, 255, 255)
TARGALYTICS = ( 28, 96, 230 )



# Class to store and manage X and Y coordinates
class Coordinate:
    def __init__(self, newX, newY):
        self.x = newX
        self.y = newY

    def setX(self,newX):
        self.x = newX

    def getX(self):
        return self.x

    def setY(self,newY):
        self.y = newY

    def getY(self):
        return self.y

# Class to store and manage coordinates associated with previous user located
class Tracer:
    originX = None
    originY = None
    width = None
    height = None
    scaleX = None
    scaleY = None
    tracer_list = []
    minX = None
    minY = None

    def __init__(self, x, y, w, h):
        self.originX = x
        self.originY = y
        self.width = w
        self.height = h

    def find_scale_factors(self,minX,maxX,minY,maxY):
        self.minX = minX
        self.minY = minY
        if(minX > 0):
            self.scaleX = self.width / (abs(maxX) - abs(minX))
        else:
            self.scaleX = self.width / (abs(maxX) + abs(minX))

        if(minY > 0):
            self.scaleY = self.height / (abs(maxY) - abs(minY))
        else:
            self.scaleY = self.height / (abs(maxY) + abs(minY))

    def convert_point_To_fit(self,x,y):
        newX = ((x - self.minX) * self.scaleX)
        newY = ((y - self.minY) * self.scaleY)
        newY = self.inverseY(newY)
        newX = self.inverseX(newX)
        newX += self.originX
        newY += self.originY
        return newX,newY

    def inverseY(self, y):
        newY = self.height - y
        return newY

    def inverseX(self, x):
        newX = self.width - x
        return newX

    def add_tracer(self,newTracer):
        self.tracer_list.append(newTracer)

    def get_tracer(self):
        return self.tracer_list

    def clear_tracer(self):
        self.tracer_list.clear()

    def set_target(self):
        self.target_visible = 1

    def clear_target(self):
        self.target_visible = 0

# Draws a symbol to the window
def placeSymbol(display_Surface,newImg, x, y):
    display_Surface.blit(newImg, (x, y))

def dbConnect(user, password, host, database):
    try:
        print("-> Connecting to database ", database, " located at ", host, " as ", user, " with password: ", password)
        dsn_tns = cx_Oracle.makedsn(host, "1521", database)
        database = cx_Oracle.connect(user, password, dsn_tns)
        cursor = database.cursor()
        print("-> Successfully connected to database - ", database, "\n")
    except Exception as err:
        print("-> Failed to connect to database - ", database)
        print("Database error - ", err,"\n")

    return database, cursor

# Sets up Pygame window
def GuiSetup():
    # Sets the pygame window dimensions with a width of 'display_width' and a height of 'display_height'
    # with a top left window location at 0,0 or top left of the display
    display_Surface = pygame.display.set_mode((display_width, display_height), 0,0) #, pygame.FULLSCREEN
    # Sets the title of the window
    pygame.display.set_caption('Targalytics')
    # Initialize Pygame window
    pygame.init()
    # Get a reference to the Pygame Clock
    clock = pygame.time.Clock()

    return display_Surface,clock

# Main Gui Method
def guiMain(display_Surface,cursor,clock,T):
            # # # Database Section # # #
    # Executes the main SQL query and assigns the list to 'data_array'
    cursor.execute('(SELECT s.S_INDEX,s.S_DATE AS time,s.S_SHOOTER.Id AS id,s.S_SHOOTER.Loc.x AS x,s.S_SHOOTER.Loc.y AS y,s.S_SHOOTER.shot AS shot, NULL AS hit, NULL AS visible, s.S_SHOOTER.head.heading AS heading,s.S_SHOOTER.arm.emg.emg0 AS emg0,s.S_SHOOTER.arm.emg.emg1 AS emg1,s.S_SHOOTER.arm.emg.emg2 AS emg2,s.S_SHOOTER.arm.emg.emg3 AS emg3,s.S_SHOOTER.arm.emg.emg4 AS emg4,s.S_SHOOTER.arm.emg.emg5 AS emg5,s.S_SHOOTER.arm.emg.emg6 AS emg6,s.S_SHOOTER.arm.emg.emg7 AS emg7,s.S_SHOOTER.arm.roll AS ARM_ROLL,s.S_SHOOTER.arm.pitch AS ARM_PITCH,s.S_SHOOTER.arm.heading AS ARM_YAW  FROM Shooter_Table s WHERE s.S_INDEX>15525) UNION ALL (SELECT t.T_INDEX,t.T_DATE AS time,t.T_TARGET.ID AS id,t.T_TARGET.Loc.x AS x, t.T_TARGET.Loc.y AS y,NULL AS shot, t.T_TARGET.hit AS hit, t.T_TARGET.visible AS visible, NULL AS heading, NULL AS emg0,NULL AS emg1,NULL AS emg2,NULL AS emg3,NULL AS emg4,NULL AS emg5,NULL AS emg6,NULL AS emg7, NULL AS ARM_ROLL, NULL AS ARM_PITCH, NULL AS ARM_YAW FROM Target_Table t WHERE  t.T_INDEX>1080) ORDER BY time')
    data_array = cursor.fetchall()
    # Executes an SQL query to find the minimum and maximum values for both X and Y coordinates of the target and user
    # Then assigns it to 'calibration_array'
    cursor.execute('SELECT max(s.S_SHOOTER.Loc.x), max(t.T_TARGET.Loc.x), min(s.S_SHOOTER.Loc.x),min(t.T_TARGET.Loc.x),max(s.S_SHOOTER.Loc.y), max(t.T_TARGET.Loc.y), min(s.S_SHOOTER.Loc.y),min(t.T_TARGET.Loc.y) FROM Shooter_Table s, Target_Table t WHERE  t.T_INDEX>1080 AND s.S_INDEX>15525')
    calibration_array = cursor.fetchall()

    # Finds the maximum and minimum values for X and Y taking into consideration the target and the user
    # Then assigns them
    max_x = max(calibration_array[0][0], calibration_array[0][1])
    if max_x!=T.getMaxX():
        print("MaxX error")
    min_x = min(calibration_array[0][2], calibration_array[0][3])
    if min_x!=T.getMinX():
        print("MinX error: min_x = ",min_x, " and getMinX=", T.getMinX())
    max_y = max(calibration_array[0][4], calibration_array[0][5])
    if max_y!=T.getMaxY():
        print("MaxY error")
    min_y = min(calibration_array[0][6], calibration_array[0][7])
    if min_y != T.getMinY():
        print("MinY error: min_y = ",min_y, " and getMinY=", T.getMinY())

    max_x = T.getMaxX()
    min_x = T.getMinX()
    max_y = T.getMaxY()
    min_y = T.getMinY()

# Initializes a tracer object with the parameters ( window starting X, window starting Y, width of tracer window, height of tracer window)
    tracer = Tracer(20,banner_height+20,tracer_width,tracer_heigth)
    tracer.clear_tracer()

    # Calls to find the scale factor to apply to the X and Y to scale input to fit in the window.
    tracer.find_scale_factors(min_x,max_x,min_y,max_y)



    # # # Image Assignment Section # # #

    # Assigns the background image
    back_ground = pygame.image.load("..\\server\BackGround.jpg")
    # Assigns the banner at the top of the window
    banner = pygame.image.load("..\\server\\Banner.jpg")
    # Assings the symbol used for the user in the tracer window
    locSymbol = pygame.image.load('..\\server\\symbol.png')
    # Assigns the symbol used for the target in the tracer window
    targetSymbol = pygame.image.load('..\\server\\target.png')



    # # # Initialization Section # # #

    # initializes the the iterator that is iterated with each main display loop
    iterator = 0
    shotCount = 0
    hitCount = 0
    missCount = 0
    hitMiss = 0
    avgReact = 0
    distance = 0
    # Marks when the target becomes visible
    visibleMarker = None
    reactionList = []
    score = 0
    targetVisible = None
    targetLocation = None
    emg = []
    arm_orient = []

    #Set the running variable to true to allow the main loop to run
    running = True

    while running:
        try:
            if(iterator + 1 == len(data_array)):
                running = False
                endHandler(display_Surface,clock,cursor)
                    # # # Handles events in this section # # #

            for event in pygame.event.get():
                # Checks if the pygame detects a quit event.
                if event.type == pygame.QUIT:
                    # Sets running to False to exit main loop
                    running = False
                    sys.exit(0)


                    # # # Drawing operations to setup window # # #

            # Fills the background with BLACK prior to drawing anything
            display_Surface.fill(BLACK)
            # Fills the background with the background image
            display_Surface.blit(back_ground, (0, 0))
            # Draws the banner to the top of the window
            display_Surface.blit(banner, (0, 0))
            # Draw borders on the window to split each section
            DrawBorders(display_Surface)

            # assigns 'current' with the record that takes place at the 'iterator'
            current = data_array[iterator]
            # Converts the location X and Y at the current record to the scaled location
            # of X and Y that fit the tracer window
            x,y = tracer.convert_point_To_fit(current[3],current[4])


                # # # Target Handling Section # # #
            # Checks if the ID of the record is greater than 100 which indicates a target
            if(current[2] > 100):

                # Checks if the target reports that it became visible
                if(current[7] == 1):
                    # Sets the 'visibleMarker' variable to the time stamp of the record
                    visibleMarker = current[1]
                    # Sets the 'targetVisible' variable to True
                    targetVisible = 1
                    # Sets the target Location to the Coordinate object storing the X and Y location to draw the target
                    targetLocation = Coordinate(x, y)

                # Checks if the targets reports that it was hit
                elif(current[6] == 1):
                    # Sets the 'targetVisible' variable to False
                    targetVisible = 0
                    # sets 'reaction' to the current reaction speed of the shooter to hit the target
                    reaction = current[1] - visibleMarker
                    # Adds the new reaction to the list of reactions
                    reactionList.append(to_float(reaction))
                    # Sets the 'reactionSum' variable to 0 to clear it.
                    reactionSum = 0

                    # Loops through all the reaction speeds to find the sum then divide by the number of records
                    # to find an average reaction speed for the user.
                    for records in reactionList:
                        reactionSum += records
                    avgReact = reactionSum / len(reactionList)


                # # # User Handling Section # # #
            else:
                # Sets the scaled location of the user to 'newPoint'
                newPoint = Coordinate(x, y)
                # Adds the new point to the tracer array within the tracer object
                tracer.add_tracer(newPoint)
                # Checks if the user fired a shot
                if(current[5] == 1):
                    # Adds one to the 'shotCount' variable
                    shotCount = shotCount + 1

                    #This section checks the next few records to find if the user hit or missed the target
                    checkHitMissIterator = iterator-1
                    while checkHitMissIterator < iterator + 3:
                        nextRecords = data_array[checkHitMissIterator]
                        if(nextRecords[6] == 1):
                            hitCount += 1
                            break
                        elif (checkHitMissIterator == iterator + 2):
                            missCount += 1
                        checkHitMissIterator +=1

                # Sets the emg values
                emg = current[9:17]
                # Sets the arm orientation values
                arm_orient = current[18:20]

            # Sets the hit miss ratio
            if(hitCount > 0):
                hitMiss = hitCount/(missCount+hitCount)
            if(avgReact > 0):
                score = hitMiss*(1000/avgReact)

            # Call to display the EMG Values ( surface to draw on, emg list)
            DisplayEMG(display_Surface,emg)
            # Call to display the Arm Orientation Values ( surface to draw on, arm orientation list)
            DisplayArmOrient(display_Surface, arm_orient)
            # Call to display the tracer window ( surface to draw on, tracer object, heading, target visible variable,
            # target location Coordinate, target Symbol, location symbol)
            DisplayTracer(display_Surface,tracer,current[8],targetVisible, targetLocation, targetSymbol,locSymbol)
            # Call to display the stats of the user ( surface to draw on, shot count, hit count, average reaction speed,
            # distance traveled, score)
            DisplayStats(display_Surface, shotCount, hitCount, missCount, avgReact, distance, score)

            # Update the pygame display
            pygame.display.update()
            # Call to set frame rate to 'frame_rate' in Control Panel
            clock.tick(frame_rate)
            # Add one to the iterator variable
            iterator += 1

        except Exception as err:
            print(err)
            break

# takes a date time and converts it to a float
def to_float(dt_time):
    return float(dt_time.seconds+(dt_time.microseconds/1000000))

# takes a symbol and a heading and returns a rotated symbol matching that heading
def orientation(originalSymbol, heading):
	facing = pygame.transform.rotate(originalSymbol, heading)
	return facing

# Draws EMG information to the window
def DisplayEMG(display_Surface,newEMG):
    # Values to position and format the components
    startingRow = banner_height+50
    spacing_off_tracer = 80
    horizontal_spacing = 180
    verticle_spacing = 30
    emg_color = WHITE
    font_size = 25

    # fills the background behind the information with black
    display_Surface.fill(BLACK, [tracer_width+spacing_off_tracer, startingRow-40, 480, startingRow+(verticle_spacing)-20])

    # Formats and locates the header text
    headerFont = pygame.font.Font(None, font_size+20)
    emgHeader = headerFont.render('MYO DATA', 1, emg_color)
    emgHeaderpos = emgHeader.get_rect(topleft=(tracer_width+230, startingRow-40))

    # Formats and locates the emg text
    font = pygame.font.Font(None, font_size)
    emg1 = font.render('EMG 1 - ' + str(newEMG[0]), 1, emg_color)
    emg1pos = emg1.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow))

    emg2 = font.render('EMG 2 - ' + str(newEMG[1]), 1, emg_color)
    emg2pos = emg1.get_rect(topleft=(tracer_width+spacing_off_tracer + horizontal_spacing, startingRow))

    emg3 = font.render('EMG 3 - ' + str(newEMG[2]), 1, emg_color)
    emg3pos = emg1.get_rect(topleft=(tracer_width+spacing_off_tracer, (startingRow+(verticle_spacing*1))))

    emg4 = font.render('EMG 4 - ' + str(newEMG[3]), 1, emg_color)
    emg4pos = emg1.get_rect(topleft=(tracer_width+spacing_off_tracer + horizontal_spacing, (startingRow+(verticle_spacing*1))))

    emg5 = font.render('EMG 5 - ' + str(newEMG[4]), 1, emg_color)
    emg5pos = emg1.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow+(verticle_spacing*2)))

    emg6 = font.render('EMG 6 - ' + str(newEMG[5]), 1, emg_color)
    emg6pos = emg1.get_rect(topleft=(tracer_width+spacing_off_tracer + horizontal_spacing, startingRow+(verticle_spacing*2)))

    emg7 = font.render('EMG 7 - ' + str(newEMG[6]), 1, emg_color)
    emg7pos = emg1.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow+(verticle_spacing*3)))

    emg8 = font.render('EMG 8 - ' + str(newEMG[7]), 1, emg_color)
    emg8pos = emg1.get_rect(topleft=(tracer_width+spacing_off_tracer + horizontal_spacing, startingRow+(verticle_spacing*3)))

    # Draws the header and emg text to the window
    display_Surface.blit(emgHeader, emgHeaderpos)
    display_Surface.blit(emg1, emg1pos)
    display_Surface.blit(emg2, emg2pos)
    display_Surface.blit(emg3, emg3pos)
    display_Surface.blit(emg4, emg4pos)
    display_Surface.blit(emg5, emg5pos)
    display_Surface.blit(emg6, emg6pos)
    display_Surface.blit(emg7, emg7pos)
    display_Surface.blit(emg8, emg8pos)

# Draws the Arm Orientation to the window
def DisplayArmOrient(display_Surface,newArm):
    # Values to position and format the components
    startingRow = banner_height+50
    spacing_off_tracer = 400
    horizontal_spacing = 250
    verticle_spacing = 40
    arm_color = WHITE
    font_size = 25

    # Formats and locates the orientation text
    font = pygame.font.Font(None, font_size)
    arm1 = font.render('Arm Roll - ' + str(newArm[0]), 1, arm_color)
    arm1pos = arm1.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow))

    arm2 = font.render('Arm Pitch - ' + str(newArm[0]), 1, arm_color)
    arm2pos = arm2.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow + verticle_spacing))

    arm3 = font.render('Arm Yaw - ' + str(newArm[0]), 1, arm_color)
    arm3pos = arm3.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow + verticle_spacing*2))

    # Draws the orientation text to the window
    display_Surface.blit(arm1, arm1pos)
    display_Surface.blit(arm2, arm2pos)
    display_Surface.blit(arm3, arm3pos)

# Averages a list of Coordinates
def averageTracer(list):
    if(len(list) < 2):
        newList = [list[0]]
        return newList
    else:
        newList = []
        firstElement = None
        secondElement = None
        for element in list:
            if(firstElement and secondElement != None):
                averageX = (firstElement.getX() + secondElement.getX() + element.getX()) / 3
                averageY = (firstElement.getY() + secondElement.getY() + element.getY()) / 3
                newCoordinate = Coordinate(averageX,averageY)
                newList.append(newCoordinate)
                firstElement = secondElement
                secondElement = element
            elif(firstElement == None):
                firstElement = element
            else:
                secondElement = element

    return newList

# Draws the tracer window and its components to the window
def DisplayTracer(display_Surface,tracer,heading,targetVisible, targetLocation, targetSymbol,locSymbol):
    # Fills the section of the window with a white background
    display_Surface.fill(WHITE,[20,banner_height+20,tracer_width,tracer_heigth])
    # Assigns list to the list stored in the tracer object
    list = tracer.get_tracer()
    # Calls to average the location of the user
    list = averageTracer(list)
    # Initializes 'pastElement' to None
    pastElement = None
    # Iterator counts the loop
    iterator = 0
    # Loops through each element in the tracer list
    for element in list:
        # If it is the first element
        if(pastElement == None):
                # Assign the previous element to the current element
                pastElement = element
                # increment iterator
                iterator += 1
        # This is not the first element
        else:
                # Draws the line of the tracer in 4 different colors depending on where it exists in order
            if(iterator > len(list) - 4):
                # Draw a line between the previous point and the current point
                pygame.draw.line(display_Surface, BRIGHT_RED, [pastElement.getX(), pastElement.getY()],[element.getX(), element.getY()], 4)
            elif(iterator > len(list) - 7):
                # Draw a line between the previous point and the current point
                pygame.draw.line(display_Surface, RED, [pastElement.getX(), pastElement.getY()],[element.getX(), element.getY()], 4)
            elif(iterator > len(list) - 10):
                # Draw a line between the previous point and the current point
                pygame.draw.line(display_Surface, LIGHT_RED, [pastElement.getX(), pastElement.getY()],[element.getX(), element.getY()], 4)
            else:
                # Draw a line between the previous point and the current point
                pygame.draw.line(display_Surface, GREY, [pastElement.getX(), pastElement.getY()],[element.getX(), element.getY()], 4)

            # Assign the previous element to the current element
            pastElement = element
            # increment iterator
            iterator += 1

    # Checks if there is a heading
    # If there is a heading it is a user we can place the symbol for
    if(heading != None and pastElement != None):
        # Orient the symbol to the proper heading
        locSymbol = orientation(locSymbol, float(heading))
        # Place the symbol for the user
        placeSymbol(display_Surface, locSymbol, pastElement.getX()-30, pastElement.getY()-30)

    # Checks if the target is visible
    if(targetVisible == 1):
        # Places the symbol of the target
        placeSymbol(display_Surface, targetSymbol, targetLocation.getX()+40, targetLocation.getY()-520)

# Draws the stats to the window
def DisplayStats(display_Surface, shotCount, hits, misses, avgReact, distance, score):
    # Values to position and format the components
    startingRow = banner_height+300
    spacing_off_tracer = 80
    horizontal_spacing = 180
    verticle_spacing = 60
    Stat_color = WHITE
    font_size = 40

    # Fills the space behind stats with a black background
    display_Surface.fill(BLACK, [tracer_width+spacing_off_tracer, startingRow-90, 450, startingRow+(verticle_spacing)-20])

    # Formats and locates the header text
    headerFont = pygame.font.Font(None, font_size+10)
    statHeader = headerFont.render('Stat Summary', 1, Stat_color)
    statHeaderpos = statHeader.get_rect(topleft=(tracer_width+190, startingRow-70))

    # Formats and locates the stat text
    font = pygame.font.Font(None, font_size)
    shot = font.render('Shot Count - ' + str(shotCount), 1, Stat_color)
    shotpos = shot.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow))

    hits = font.render('Hit Count - ' + str(hits), 1, Stat_color)
    hitspos = shot.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow+(verticle_spacing)))

    misses = font.render('Miss Count - ' + str(misses), 1, Stat_color)
    missespos = shot.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow+(verticle_spacing*2)))

    avgReact = font.render('Average Reaction Speed - ' + str(avgReact), 1, Stat_color)
    avgReactpos = shot.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow+(verticle_spacing*3)))

    distance = font.render('Distance traveled - ' + str(distance), 1, Stat_color)
    distancepos = shot.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow+(verticle_spacing*4)))

    score = font.render('Score - ' + str(score), 1, Stat_color)
    scorepos = shot.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow+(verticle_spacing*5)))

    # Draws the stats to the window
    display_Surface.blit(statHeader, statHeaderpos)
    display_Surface.blit(shot, shotpos)
    display_Surface.blit(hits, hitspos)
    display_Surface.blit(misses, missespos)
    display_Surface.blit(avgReact, avgReactpos)
    display_Surface.blit(distance, distancepos)
    display_Surface.blit(score, scorepos)

# Draws the borders to the window
def DrawBorders(display_Surface):
    pygame.draw.line(display_Surface, WHITE, [tracer_width+40, banner_height], [tracer_width+40, display_height], 2)
    pygame.draw.line(display_Surface, WHITE, [tracer_width+40, banner_height+170], [display_width, banner_height+170], 2)

# Orients a symbol to the correct heading
def orientation(originalSymbol,heading):
    facing = pygame.transform.rotate(originalSymbol, heading)
    return facing

# Is called when the end of analysis is detected
def endHandler(display_Surface, clock, cursor):
    end_color = BLACK
    font_size = 30
    start_of_window_width = display_width/4
    start_of_window_height = banner_height + 180
    end_window_height = 400
    end_window_width = 700
    button_width = 180
    button_height = 100
    drop_to_button = 180
    space_to_first_button = 120
    space_to_second_button = 400

    display_Surface.fill(WHITE, [start_of_window_width, start_of_window_height, end_window_width, end_window_height])
    pygame.draw.line(display_Surface, BLACK, [start_of_window_width, start_of_window_height], [start_of_window_width, start_of_window_height+end_window_height], 2)
    pygame.draw.line(display_Surface, BLACK, [start_of_window_width, start_of_window_height], [start_of_window_width+end_window_width, start_of_window_height], 2)
    pygame.draw.line(display_Surface, BLACK, [start_of_window_width+end_window_width, start_of_window_height], [start_of_window_width+end_window_width, start_of_window_height+end_window_height], 2)
    pygame.draw.line(display_Surface, BLACK, [start_of_window_width, start_of_window_height+end_window_height], [start_of_window_width+end_window_width, start_of_window_height+end_window_height], 2)

    headerFont = pygame.font.Font(None, font_size+10)
    endHeader = headerFont.render('Would you like to view analysis again or exit?', 1, end_color)
    endHeaderpos = endHeader.get_rect(topleft=(start_of_window_width+50, start_of_window_height+80))
    display_Surface.blit(endHeader, endHeaderpos)

    display_Surface.fill(BLACK, [start_of_window_width+space_to_first_button, start_of_window_height+drop_to_button, button_width, button_height])
    display_Surface.fill(GREEN, [start_of_window_width+space_to_first_button+5, start_of_window_height+drop_to_button+5, button_width-10, button_height-10])

    display_Surface.fill(BLACK, [start_of_window_width+space_to_second_button, start_of_window_height+drop_to_button, button_width, button_height])
    display_Surface.fill(RED, [start_of_window_width+space_to_second_button+5, start_of_window_height+drop_to_button+5, button_width-10, button_height-10])

    font = pygame.font.Font(None, font_size+15)
    analyze = font.render('Analyze', 1, end_color)
    analyzepos = analyze.get_rect(topleft=(start_of_window_width+space_to_first_button+25, start_of_window_height+drop_to_button+32))

    exit = font.render('Exit', 1, end_color)
    exitpos = exit.get_rect(topleft=(start_of_window_width+space_to_second_button+54, start_of_window_height+drop_to_button+32))

    display_Surface.blit(analyze, analyzepos)
    display_Surface.blit(exit, exitpos)

    pygame.display.update()
    answered = False
    while not answered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                answered = False
                sys.exit()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

                # Analyze Button
            if(start_of_window_width+space_to_first_button+button_width) > mouse[0] > (start_of_window_width+space_to_first_button) and (start_of_window_height+drop_to_button+button_height) > mouse[1] > (start_of_window_height+drop_to_button):
                display_Surface.fill(BLACK, [start_of_window_width + space_to_first_button,
                                             start_of_window_height + drop_to_button, button_width, button_height])
                display_Surface.fill(BRIGHT_GREEN, [start_of_window_width + space_to_first_button + 5,
                                             start_of_window_height + drop_to_button + 5, button_width - 10,
                                             button_height - 10])
                analyze = font.render('Analyze', 1, end_color)
                analyzepos = analyze.get_rect(topleft=(
                start_of_window_width + space_to_first_button + 25, start_of_window_height + drop_to_button + 32))
                display_Surface.blit(analyze, analyzepos)
                pygame.display.update()
                if(click[0] == 1):
                    guiMain(display_surface, cursor, clock, T)
            else:
                display_Surface.fill(BLACK, [start_of_window_width + space_to_first_button,
                                             start_of_window_height + drop_to_button, button_width, button_height])
                display_Surface.fill(GREEN, [start_of_window_width + space_to_first_button + 5,
                                             start_of_window_height + drop_to_button + 5, button_width - 10,
                                             button_height - 10])
                analyze = font.render('Analyze', 1, end_color)
                analyzepos = analyze.get_rect(topleft=(
                start_of_window_width + space_to_first_button + 25, start_of_window_height + drop_to_button + 32))
                display_Surface.blit(analyze, analyzepos)
                pygame.display.update()


                # Exit Button
            if (start_of_window_width + space_to_second_button + button_width) > mouse[0] > (start_of_window_width + space_to_second_button) and (start_of_window_height + drop_to_button + button_height) > mouse[1] > (start_of_window_height + drop_to_button):
                display_Surface.fill(BLACK, [start_of_window_width + space_to_second_button,
                                             start_of_window_height + drop_to_button, button_width, button_height])
                display_Surface.fill(BRIGHT_RED, [start_of_window_width + space_to_second_button + 5,
                                           start_of_window_height + drop_to_button + 5, button_width - 10,
                                           button_height - 10])
                exit = font.render('Exit', 1, end_color)
                exitpos = exit.get_rect(topleft=(start_of_window_width + space_to_second_button + 54, start_of_window_height + drop_to_button + 32))
                display_Surface.blit(exit, exitpos)
                pygame.display.update()
                if(click[0] == 1):
                    sys.exit(0)
            else:
                display_Surface.fill(BLACK, [start_of_window_width + space_to_second_button,
                                             start_of_window_height + drop_to_button, button_width, button_height])
                display_Surface.fill(RED, [start_of_window_width + space_to_second_button + 5,
                                           start_of_window_height + drop_to_button + 5, button_width - 10,
                                           button_height - 10])
                exit = font.render('Exit', 1, end_color)
                exitpos = exit.get_rect(topleft=(start_of_window_width + space_to_second_button + 54, start_of_window_height + drop_to_button + 32))
                display_Surface.blit(exit, exitpos)
                pygame.display.update()

if __name__ == '__main__':
    ip = 'localhost'
    port = 1521
    SID = 'orcl'
    UserName = "SYSMAN"
    PassWord = "System_Admin1"
    DatabaseInfo = [ip, port, SID, UserName, PassWord]

    # All in Database
    StartDate = pd.to_datetime(0)
    EndDate = datetime.now()

    # Date time of Kyle's test
    StartDate = pd.to_datetime('2018-03-17 16:07:56.164')
    EndDate = pd.to_datetime('2018-03-17 16:59:12.000')
    T = Reactionalytics(DatabaseInfo, StartDate, EndDate)
    T.ExportToCSV('Kyle')

    display_surface,clock = GuiSetup()
    # Connects to the database using parameters in 'Control Panel' at top
    database, cursor = dbConnect(user, password, host, database_name)
    guiMain(display_surface,cursor, clock,T)
