
from multiprocessing import Process, Manager
from multiprocessing.managers import *
from UserInformation import *
from Pozyx_Localize import *
from myo_raw import MyoRaw
#from heartbeat_test import *
import time
import socket
import pickle
import random


delay = .2

if __name__ == '__main__':
    BaseManager.register('UserInformation',UserInformation)
    manager = BaseManager()
    manager.start()
    dataStruct = manager.UserInformation('01')
    myoData = Process(target=MyoRaw.main, args=[dataStruct])
    LocationData = Process(target=GetLocData, args=[dataStruct])
    #heartData = Process(target=GetHeartData, args=[dataStruct])
    myoData.start()
    LocationData.start()
    #heartData.start()

    print("Setting initial configuration for client")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '192.168.1.6'
    port = 5000

    print("Attempting to connect to Ip - ", ip, "     Port - ", port)

    server.connect((ip, port))

    print("Connected to server at IP address - ", ip, "  port - ", port)


            #DATA THAT STILL NEEDS COLLECTED
    dataStruct.setHeartRate(random.randint(60,90))
    dataStruct.setVisible(0)
    dataStruct.setHostile(0)
    dataStruct.setHit(0)



    while(True):
        time.sleep(delay)

            #DATA THAT STILL NEEDS COLLECTED
        dataStruct.setBodyXAxis(dataStruct.getHeadXAxis())
        dataStruct.setBodyYAxis(dataStruct.getHeadyAxis())
        dataStruct.setBodyZAxis(dataStruct.getHeadZAxis())
        dataStruct.setBodyHeading(dataStruct.getHeadHeading())
        dataStruct.setBodyDegrees(dataStruct.getHeadDegrees())
        dataStruct.setHeartRate(dataStruct.getHeartRate() + random.randint(-3,5))


        structure = {1:dataStruct.getId(),
                    2:dataStruct.getEMG(),3:dataStruct.getRoll(),4:dataStruct.getPitch(),5:dataStruct.getYaw(),6:dataStruct.getShot(),
                    7: dataStruct.getHeadXAxis(), 8: dataStruct.getHeadYAxis(), 9: dataStruct.getHeadZAxis(),10: dataStruct.getHeadHeading(), 11: dataStruct.getHeadDegrees(),
                    12: dataStruct.getBodyXAxis(), 13: dataStruct.getBodyYAxis(), 14: dataStruct.getBodyZAxis(), 15: dataStruct.getBodyHeading(), 16: dataStruct.getBodyDegrees(),
                    17: dataStruct.getLocationXAxis(), 18:dataStruct.getLocationYAxis(), 19:dataStruct.getLocationZAxis(),
                    20:dataStruct.getHeartRate(), 21:dataStruct.getVisible(), 22:dataStruct.getHostile(), 23:dataStruct.getHit()}

        print(structure)
        stream = pickle.dumps(structure)
        server.send(stream)
        dataStruct.setShot(False)

    myoData.join()
    LocationData.join()
    #heartData.join()


