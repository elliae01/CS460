
from multiprocessing import Process, Manager
from multiprocessing.managers import *
from UserInformation import *
import time
import random
import socket
import pickle




delay = 1

def myo(User):
    while (True):
        time.sleep(delay)
        User.setEMG(random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),)
        tempEMG = User.getEMG()
        #print("Myo - EMG Data = " + str(tempEMG))

def headCompass(User):
    while(True):
        time.sleep(delay)
        User.setHeadXAxis(random.randint(0,100))
        User.setHeadYAxis(random.randint(0,100))
        User.setHeadZAxis(random.randint(0,100))
        tempXAxis = User.getHeadXAxis()
        tempYAxis = User.getHeadYAxis()
        tempZAxis = User.getHeadZAxis()
        #print("Compass - HeadXAxis = " + str(tempXAxis) + "     HeadYAxis = " + str(tempYAxis) + "     HeadZAxis = " + str(tempZAxis))

def bodyCompass(User):
    while(True):
        time.sleep(delay)
        User.setBodyXAxis(random.randint(0,100))
        User.setBodyYAxis(random.randint(0,100))
        User.setBodyZAxis(random.randint(0,100))
        tempXAxis = User.getBodyXAxis()
        tempYAxis = User.getBodyYAxis()
        tempZAxis = User.getBodyZAxis()
        #print("Compass - BodyXAxis = " + str(tempXAxis) + "     BodyYAxis = " + str(tempYAxis) + "     BodyZAxis = " + str(tempZAxis))

def locData(User):
    while(True):
        time.sleep(delay)
        User.setLocationXAxis(random.randint(0,100))
        User.setLocationYAxis(random.randint(0,100))
        User.setLocationZAxis(random.randint(0,100))
        tempXAxis = User.getLocationXAxis()
        tempYAxis = User.getLocationYAxis()
        tempZAxis = User.getLocationZAxis()
        #print("UWB Receiver - LocationXAxis = " + str(tempXAxis) + "     LocationYAxis = " + str(tempYAxis) + "     LocationZAxis = " + str(tempZAxis))

if __name__ == '__main__':
    BaseManager.register('UserInformation',UserInformation)
    manager = BaseManager()
    manager.start()
    dataStruct = manager.UserInformation('01')
    myoData = Process(target=myo, args=[dataStruct])
    headData = Process(target=headCompass, args=[dataStruct])
    bodyData = Process(target=bodyCompass, args=[dataStruct])
    locationData = Process(target=locData, args=[dataStruct])
    myoData.start()
    headData.start()
    bodyData.start()
    locationData.start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '192.168.1.4'
    port = 5454
    print"Connected to server at IP address - ", ip, "  port - ", port

    message = b"Hello Server"


    server.connect((ip, port))

    while(True):
        time.sleep(delay)

        print'Sending Data Structure to Server at IP address - ', ip, '  port - ', port
        structure = {1:dataStruct.getId(),
                    2:dataStruct.getEMG(),3:dataStruct.getRoll(),4:dataStruct.getPitch(),5:dataStruct.getYaw(),6:dataStruct.getShot(),
                    7: dataStruct.getHeadXAxis(), 8: dataStruct.getHeadYAxis(), 9: dataStruct.getHeadZAxis(),10: dataStruct.getHeadHeading(), 11: dataStruct.getHeadDegrees(),
                    12: dataStruct.getBodyXAxis(), 13: dataStruct.getBodyYAxis(), 14: dataStruct.getBodyZAxis(), 15: dataStruct.getBodyHeading(), 16: dataStruct.getBodyDegrees(),
                    17: dataStruct.getLocationXAxis(),18:dataStruct.getLocationYAxis(),19:dataStruct.getLocationZAxis(),20:dataStruct.getHeartRate()}
        stream = pickle.dumps(structure)

        server.send(stream)
    myoData.join()
    headData.join()


