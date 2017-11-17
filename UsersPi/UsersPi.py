from UserInformation import *
from multiprocessing import Process, Manager
from multiprocessing.managers import *
import time
import random

delay = .01

def myo(User):
    while (True):
        time.sleep(delay)
        User.setEMG(random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),)
        tempEMG = User.getEMG()
        print("Myo - EMG Data = " + str(tempEMG))

def headCompass(User):
    while(True):
        time.sleep(delay)
        User.setHeadXAxis(random.randint(0,100))
        User.setHeadYAxis(random.randint(0,100))
        User.setHeadZAxis(random.randint(0,100))
        tempXAxis = User.getHeadXAxis()
        tempYAxis = User.getHeadYAxis()
        tempZAxis = User.getHeadZAxis()
        print("Compass - HeadXAxis = " + str(tempXAxis) + "     HeadYAxis = " + str(tempYAxis) + "     HeadZAxis = " + str(tempZAxis))

def bodyCompass(User):
    while(True):
        time.sleep(delay)
        User.setBodyXAxis(random.randint(0,100))
        User.setBodyYAxis(random.randint(0,100))
        User.setBodyZAxis(random.randint(0,100))
        tempXAxis = User.getBodyXAxis()
        tempYAxis = User.getBodyYAxis()
        tempZAxis = User.getBodyZAxis()
        print("Compass - BodyXAxis = " + str(tempXAxis) + "     BodyYAxis = " + str(tempYAxis) + "     BodyZAxis = " + str(tempZAxis))

def locData(User):
    while(True):
        time.sleep(delay)
        User.setLocationXAxis(random.randint(0,100))
        User.setLocationYAxis(random.randint(0,100))
        User.setLocationZAxis(random.randint(0,100))
        tempXAxis = User.getLocationXAxis()
        tempYAxis = User.getLocationYAxis()
        tempZAxis = User.getLocationZAxis()
        print("UWB Receiver - LocationXAxis = " + str(tempXAxis) + "     LocationYAxis = " + str(tempYAxis) + "     LocationZAxis = " + str(tempZAxis))

if __name__ == '__main__':
    BaseManager.register('UserInformation',UserInformation)
    manager = BaseManager()
    manager.start()
    kyle = manager.UserInformation('01')
    myoData = Process(target=myo, args=[kyle])
    headData = Process(target=headCompass, args=[kyle])
    bodyData = Process(target=bodyCompass, args=[kyle])
    locationData = Process(target=locData, args=[kyle])
    myoData.start()
    headData.start()
    bodyData.start()
    locationData.start()
    while(True):
        time.sleep(delay)
        print("\nPi - EMG DATA = " + str(kyle.getEMG()))
        print("Pi - HeadXAxis = " + str(kyle.getHeadXAxis()) + "     HeadYAxis = " + str(kyle.getHeadYAxis()) + "     HeadZAxis = " + str(kyle.getHeadZAxis()))
        print("Pi - BodyXAxis = " + str(kyle.getBodyXAxis()) + "     BodyYAxis = " + str(kyle.getBodyYAxis()) + "     BodyZAxis = " + str(kyle.getBodyZAxis()))
        print("Pi - LocationXAxis = " + str(kyle.getLocationXAxis()) + "     LocationYAxis = " + str(kyle.getLocationYAxis()) + "     LocationZAxis = " + str(kyle.getLocationZAxis()) +"\n")
    myoData.join()
    headData.join()


