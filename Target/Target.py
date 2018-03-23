from __future__ import division
import time
import socket
import pickle
import threading
from UserInformation import *
import spidev
import sys
import datetime
# Import the PCA9685 module.
import Adafruit_PCA9685



### SERVO INFORMATION ###
# Configure min and max servo pulse lengths
servo_min = 300  # Min pulse length out of 4096
servo_max = 520  # Max pulse length out of 4096
servo_delay = .8


### TARGET INFORMATION ###
identifier = 101            # THE ID THE TARGET IS KNOWN AS
initialHostility = 11       # THE HOSTILITY LEVEL THE TARGET IS KNOWN AS 10 - 20 FOR HOSTILE.

### TCP CONNECTION INFORMATION ###
ip = '192.168.1.6'
port = 5001

### LOCATION INFORMATION ###
x = 27
y = 190
z = 32

### PIEZO SETTINGS ###
piezo_channel = 0


def multiProcessSetup(dataStruct,server,pwm,spi):
    try:
        print("\nBeginning to send and receive data\n")
        t2 = threading.Thread(target=targetSettings, args=(dataStruct, server, pwm))
        t3 = threading.Thread(target=checkHits, args=(dataStruct,spi,server))
        t2.start()
        t3.start()

    except Exception as err:
        print("-> Failed to send and receive data")
        print("Error - ", err, "\n")

    return t2,t3

def cleanUp(t2,t3,pwm):
    t2.join()
    t3.join()
    sys.exit


def connectTCP(ip, port):
    try:
        print("-> Attempting to connect to Ip - ", ip, "     Port - ", port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((ip, port))
        structure = {1:1}
        stream = pickle.dumps(structure)
        server.send(stream)
        print("-> Connected to server at IP address - ", ip, "  port - ", port)
    except Exception as err:
        print("-> Failed to make a connection")
        print("-> Connection error - ", err, "\n")

    return server

def sendData(dataStruct, server):
    if(dataStruct.getHit() == 1):
        dataStruct.setVisible(0)
    print('starting time')
    dataStruct.setTimestamp(datetime.datetime.now().format("%d-%b-%Y %I.%M.%S.%f %p"))
    print(dataStruct.getTimestamp())
    structure = {1:dataStruct.getId(),
                2:dataStruct.getEMG(),3:dataStruct.getRoll(),4:dataStruct.getPitch(),5:dataStruct.getYaw(),6:dataStruct.getShot(),
                7: dataStruct.getHeadXAxis(), 8: dataStruct.getHeadYAxis(), 9: dataStruct.getHeadZAxis(),10: dataStruct.getHeadHeading(), 11: dataStruct.getHeadDegrees(),
                12: dataStruct.getBodyXAxis(), 13: dataStruct.getBodyYAxis(), 14: dataStruct.getBodyZAxis(), 15: dataStruct.getBodyHeading(), 16: dataStruct.getBodyDegrees(),
                17: dataStruct.getLocationXAxis(), 18:dataStruct.getLocationYAxis(), 19:dataStruct.getLocationZAxis(),
                20:dataStruct.getHeartRate(), 21:dataStruct.getVisible(), 22:dataStruct.getHostile(), 23:dataStruct.getHit(), 24:dataStruct.getTimestamp()}
    stream = pickle.dumps(structure)
    server.send(stream)
    print("-> Data sent to server ",structure)
    dataStruct.setHit(0)                #SETS THE HIT BACK TO FALSE.


def checkHits(dataStruct,spi,server):
    while(dataStruct.getRun() == 1):
        if dataStruct.getVisible():
            piezo = ReadChannel(piezo_channel,spi)
            if(piezo < 20):
                dataStruct.setHit(1)
                print('-> Target hit detected Sending Data to server')
                sendData(dataStruct, server)



def deployTarget(pwm):
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, servo_max)
    time.sleep(1)
    pwm.set_pwm(0, 0, servo_min)

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000  # 1,000,000 us per second
    pulse_length //= 60  # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096  # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)


def targetSettings(dataStruct, server, pwm):
    while(dataStruct.getRun() == 1):
        data = server.recv(1020)
        structure = pickle.loads(data)
        if(dataStruct.getVisible() == 1):
            dataStruct.setRun(structure[1])
            dataStruct.setVisible(structure[2])
            dataStruct.setHostile(structure[3])

        else:
            dataStruct.setRun(structure[1])
            dataStruct.setVisible(structure[2])
            dataStruct.setHostile(structure[3])
            if(dataStruct.getVisible() == 1):
                deployTarget(pwm)
                sendData(dataStruct, server)
                print('-> Deployed Target with a hostility level of ', structure[3])
                time.sleep(servo_delay)

        # Open SPI bus
def spiSetup():
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000

    return spi

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel,spi):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

if __name__ == '__main__':
        #CONNECT TO SERVER USING TCP CONNECTION
    server = connectTCP(ip, port)

        #INSTATIATE A DATA STRUCTURE OF USERINFORMATION USING THE IDENTIFIER SPECIFIED AT THE TOP.
    dataStruct = UserInformation(identifier)
    dataStruct.setRun(1)
    dataStruct.setHostile(initialHostility)
    dataStruct.setLocationXAxis(x)
    dataStruct.setLocationYAxis(y)
    dataStruct.setLocationZAxis(z)
    dataStruct.setHit(0)
    dataStruct.setVisible(0)

        # Initialise the PCA9685 using the default address (0x40).
    pwm = Adafruit_PCA9685.PCA9685()

        # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)

        # Initializes an SPI
    spi = spiSetup()

        # SETS THE PROCESSES FOR COMMUNICATION AND DETECTION UP
    t2,t3 = multiProcessSetup(dataStruct,server,pwm, spi)

    while(True):
        if(dataStruct.getRun != 1):
            cleanUp(t2,t3, pwm)
        time.sleep(1)