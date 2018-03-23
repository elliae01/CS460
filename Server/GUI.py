import pygame
import sys
import time
import cx_Oracle

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

# DATABASE INFORMATION
user = 'SYSMAN'
password = 'System_Admin1'
host = 'localhost'
database = 'orcl'

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (200,   0,   0)
BRIGHT_RED   = (255,   0,   0)
GREEN = (  0, 200,   0)
BRIGHT_GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
CYAN = ( 0, 255, 255)
TARGALYTICS = ( 28, 96, 230 )

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

class Tracer:
    originX = None
    originY = None
    width = None
    height = None
    scaleX = None
    scaleY = None
    tracer_list = []
    target_visible = 0
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

    def set_target(self):
        self.target_visible = 1

    def clear_target(self):
        self.target_visible = 0

    def check_target(self):
        for elements in self.get_tracer():
            if(elements.getTarget == 1):
                print()

def placeSymbol(display_Surface,newImg, x, y):
    display_Surface.blit(newImg, (x, y))

def dbConnect(user, password, host, database):
    try:
        print("-> Connecting to database ", database, " located at ", host, " as ", user, " with password: ", password)
        database = cx_Oracle.connect(user, password, host+"/"+database)
        cursor = database.cursor()
        print("-> Successfully connected to database - ", database, "\n")
    except Exception as err:
        print("-> Failed to connect to database - ", database)
        print("Database error - ", err,"\n")

    return database, cursor

def guiMain(cursor):
    # Set the Pygame display
    display_Surface = pygame.display.set_mode((display_width, display_height), 0,0) #, pygame.FULLSCREEN
    pygame.display.set_caption('Targalytics')

        # Initialize Pygame
    pygame.init()
        # Get a reference to the Pygame Clock
    clock = pygame.time.Clock()
    running = True

    cursor.execute('(SELECT s.S_INDEX,s.S_DATE AS time,s.S_SHOOTER.Id AS id,s.S_SHOOTER.Loc.x AS x,s.S_SHOOTER.Loc.y AS y,s.S_SHOOTER.shot AS shot, NULL AS hit, NULL AS visible, s.S_SHOOTER.head.heading AS heading,s.S_SHOOTER.arm.emg.emg0 AS emg0,s.S_SHOOTER.arm.emg.emg1 AS emg1,s.S_SHOOTER.arm.emg.emg2 AS emg2,s.S_SHOOTER.arm.emg.emg3 AS emg3,s.S_SHOOTER.arm.emg.emg4 AS emg4,s.S_SHOOTER.arm.emg.emg5 AS emg5,s.S_SHOOTER.arm.emg.emg6 AS emg6,s.S_SHOOTER.arm.emg.emg7 AS emg7,s.S_SHOOTER.arm.roll AS ARM_ROLL,s.S_SHOOTER.arm.pitch AS ARM_PITCH,s.S_SHOOTER.arm.heading AS ARM_YAW  FROM Shooter_Table s WHERE s.S_INDEX>15525) UNION ALL (SELECT t.T_INDEX,t.T_DATE AS time,t.T_TARGET.ID AS id,t.T_TARGET.Loc.x AS x, t.T_TARGET.Loc.y AS y,NULL AS shot, t.T_TARGET.hit AS hit, t.T_TARGET.visible AS visible, NULL AS heading, NULL AS emg0,NULL AS emg1,NULL AS emg2,NULL AS emg3,NULL AS emg4,NULL AS emg5,NULL AS emg6,NULL AS emg7, NULL AS ARM_ROLL, NULL AS ARM_PITCH, NULL AS ARM_YAW FROM Target_Table t WHERE  t.T_INDEX>1080) ORDER BY time')
    data_array = cursor.fetchall()

    cursor.execute('SELECT max(s.S_SHOOTER.Loc.x), max(t.T_TARGET.Loc.x), min(s.S_SHOOTER.Loc.x),min(t.T_TARGET.Loc.x),max(s.S_SHOOTER.Loc.y), max(t.T_TARGET.Loc.y), min(s.S_SHOOTER.Loc.y),min(t.T_TARGET.Loc.y) FROM Shooter_Table s, Target_Table t WHERE  t.T_INDEX>1080 AND s.S_INDEX>15525')
    calibration_array = cursor.fetchall()

    max_x = max(calibration_array[0][0], calibration_array[0][1])
    min_x = min(calibration_array[0][2], calibration_array[0][3])
    max_y = max(calibration_array[0][4], calibration_array[0][5])
    min_y = min(calibration_array[0][6], calibration_array[0][7])

    tracer = Tracer(20,banner_height+20,tracer_width,tracer_heigth)
    tracer.find_scale_factors(min_x,max_x,min_y,max_y)

    back_ground = pygame.image.load("BackGround.jpg")
    banner = pygame.image.load("Banner.jpg")
    locSymbol = pygame.image.load('symbol.png')
    targetSymbol = pygame.image.load('target.png')

    iterator = 0
    shotCount = 0
    hitCount = 0
    missCount = 0
    hitMiss = 0
    avgReact = 0
    distance = 0
    shotMarker = None
    reactionList = []
    score = 0
    past_x = []
    past_y = []
    targetVisible = None
    targetLocation = None
    emg = [-99,-99,-99,-99,-99,-99,-99,-99]
    arm_orient = [-99,-99,-99]

    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            display_Surface.fill(BLACK)
            display_Surface.blit(back_ground, (0, 0))
            display_Surface.blit(banner, (0, 0))
            DrawBorders(display_Surface)
            current = data_array[iterator]
            x,y = tracer.convert_point_To_fit(current[3],current[4])

                # THIS IS A TARGET
            if(current[2] > 100):
                if(current[7] == 1):
                    shotMarker = current[1]
                    targetVisible = 1
                    targetLocation = Coordinate(x, y)
                elif(current[6] == 1):
                    targetVisible = 0
                    reaction = current[1] - shotMarker
                    reactionList.append(to_float(reaction))
                    reactionSum=0
                    for records in reactionList:
                        reactionSum += records
                    avgReact = reactionSum / len(reactionList)


                # THIS IS A USER
            else:
                newPoint = Coordinate(x, y)
                tracer.add_tracer(newPoint)
                if(current[5] == 1):
                    shotCount = shotCount + 1
                    checkHitMissIterator = iterator-1
                    while checkHitMissIterator < iterator + 3:
                        nextRecords = data_array[checkHitMissIterator]
                        if(nextRecords[6] == 1):
                            hitCount += 1
                            break
                        elif (checkHitMissIterator == iterator + 2):
                            missCount += 1
                        checkHitMissIterator +=1
                emg = current[9:17]
                arm_orient = current[18:20]
            if(hitCount > 0):
                hitMiss = hitCount/(missCount+hitCount)
            if(avgReact > 0):
                score = hitMiss*(1000/avgReact)

            DisplayEMG(display_Surface,emg)
            DisplayArmOrient(display_Surface, arm_orient)

            DisplayTracer(display_Surface,tracer,current[8],targetVisible, targetLocation, targetSymbol,locSymbol)
            DisplayStats(display_Surface, shotCount, hitCount, missCount, avgReact, distance, score)

            pygame.display.update()
            clock.tick(frame_rate)
            iterator += 1

        except Exception as err:
            print(err)
            time.sleep(5)
            endHandler(display_Surface,cursor)
            break

def to_float(dt_time):
    return float(dt_time.seconds+(dt_time.microseconds/1000000))

def orientation(originalSymbol, heading):
	facing = pygame.transform.rotate(originalSymbol, heading)
	return facing

def DisplayEMG(display_Surface,newEMG):
    startingRow = banner_height+50
    spacing_off_tracer = 80
    horizontal_spacing = 180
    verticle_spacing = 30
    emg_color = WHITE
    font_size = 25

    display_Surface.fill(BLACK, [tracer_width+spacing_off_tracer, startingRow-40, 480, startingRow+(verticle_spacing)-20])

    headerFont = pygame.font.Font(None, font_size+20)
    emgHeader = headerFont.render('MYO DATA', 1, emg_color)
    emgHeaderpos = emgHeader.get_rect(topleft=(tracer_width+230, startingRow-40))

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

    display_Surface.blit(emgHeader, emgHeaderpos)
    display_Surface.blit(emg1, emg1pos)
    display_Surface.blit(emg2, emg2pos)
    display_Surface.blit(emg3, emg3pos)
    display_Surface.blit(emg4, emg4pos)
    display_Surface.blit(emg5, emg5pos)
    display_Surface.blit(emg6, emg6pos)
    display_Surface.blit(emg7, emg7pos)
    display_Surface.blit(emg8, emg8pos)

def DisplayArmOrient(display_Surface,newArm):
    startingRow = banner_height+50
    spacing_off_tracer = 400
    horizontal_spacing = 250
    verticle_spacing = 40
    arm_color = WHITE
    font_size = 25

    font = pygame.font.Font(None, font_size)
    arm1 = font.render('Arm Roll - ' + str(newArm[0]), 1, arm_color)
    arm1pos = arm1.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow))

    arm2 = font.render('Arm Pitch - ' + str(newArm[0]), 1, arm_color)
    arm2pos = arm2.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow + verticle_spacing))

    arm3 = font.render('Arm Yaw - ' + str(newArm[0]), 1, arm_color)
    arm3pos = arm3.get_rect(topleft=(tracer_width+spacing_off_tracer, startingRow + verticle_spacing*2))

    display_Surface.blit(arm1, arm1pos)
    display_Surface.blit(arm2, arm2pos)
    display_Surface.blit(arm3, arm3pos)

def DisplayTracer(display_Surface,tracer,heading,targetVisible, targetLocation, targetSymbol,locSymbol):
    display_Surface.fill(WHITE,[20,banner_height+20,tracer_width,tracer_heigth])
    list = tracer.get_tracer()
    pastElement = None
    for element in list:
        if(pastElement == None):
                pastElement = element
        else:
            pygame.draw.line(display_Surface, RED, [pastElement.getX(), pastElement.getY()],[element.getX(), element.getY()], 4)
            pastElement = element

    if(heading != None):
        locSymbol = orientation(locSymbol, float(heading))
        placeSymbol(display_Surface, locSymbol, element.getX(), element.getY())

    if(targetVisible == 1):
        placeSymbol(display_Surface, targetSymbol, targetLocation.getX()+40, targetLocation.getY()-520)

def DisplayStats(display_Surface, shotCount, hits, misses, avgReact, distance, score):
    startingRow = banner_height+300
    spacing_off_tracer = 80
    horizontal_spacing = 180
    verticle_spacing = 60
    Stat_color = WHITE
    font_size = 40

    display_Surface.fill(BLACK, [tracer_width+spacing_off_tracer, startingRow-90, 450, startingRow+(verticle_spacing)-20])

    headerFont = pygame.font.Font(None, font_size+10)
    statHeader = headerFont.render('Stat Summary', 1, Stat_color)
    statHeaderpos = statHeader.get_rect(topleft=(tracer_width+190, startingRow-70))

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


    display_Surface.blit(statHeader, statHeaderpos)
    display_Surface.blit(shot, shotpos)
    display_Surface.blit(hits, hitspos)
    display_Surface.blit(misses, missespos)
    display_Surface.blit(avgReact, avgReactpos)
    display_Surface.blit(distance, distancepos)
    display_Surface.blit(score, scorepos)

def DrawBorders(display_Surface):
    pygame.draw.line(display_Surface, WHITE, [tracer_width+40, banner_height], [tracer_width+40, display_height], 2)
    pygame.draw.line(display_Surface, WHITE, [tracer_width+40, banner_height+170], [display_width, banner_height+170], 2)

def orientation(originalSymbol,heading):
    facing = pygame.transform.rotate(originalSymbol, heading)
    return facing

def endHandler(display_Surface,cursor):
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
                    pygame.quit()
                    guiMain(cursor)
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
    # DATABASE CONNECTION
    database, cursor = dbConnect(user, password, host, database)

    guiMain(cursor)
