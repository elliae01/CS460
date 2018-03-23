from multiprocessing import Process, Manager
from multiprocessing.managers import *
from UserInformation import *
from Pozyx_Localize import *
from myo_raw import MyoRaw
import time
import socket
import pickle
import datetime


delay = .1

if __name__ == '__main__':
    BaseManager.register('UserInformation',UserInformation)
    manager = BaseManager()
    manager.start()
    dataStruct = manager.UserInformation('01')
    myoData = Process(target=MyoRaw.main, args=[dataStruct])
    LocationData = Process(target=GetLocData, args=[dataStruct])
    #BodyOrientData = Process(target=GetHeartData, args=[dataStruct])
    myoData.start()
    LocationData.start()
    #BodyOrientData.start()

    print("Setting initial configuration for client")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '192.168.1.6'
    port = 5001

    print("Attempting to connect to Ip - ", ip, "     Port - ", port)

    server.connect((ip, port))

    structure = {1: 0}
    stream = pickle.dumps(structure)
    server.send(stream)
    print("Connected to server at IP address - ", ip, "  port - ", port)


            #DATA THAT STILL NEEDS COLLECTED
    dataStruct.setHeartRate(0)
    dataStruct.setVisible(0)
    dataStruct.setHostile(0)
    dataStruct.setHit(0)



    while(True):
        time.sleep(delay)
        dataStruct.setTimestamp(str(datetime.datetime.now()))
            #DATA THAT STILL NEEDS COLLECTED
        dataStruct.setBodyXAxis(dataStruct.getHeadXAxis())
        dataStruct.setBodyYAxis(dataStruct.getHeadYAxis())
        dataStruct.setBodyZAxis(dataStruct.getHeadZAxis())
        dataStruct.setBodyHeading(dataStruct.getHeadHeading())
        dataStruct.setBodyDegrees(dataStruct.getHeadDegrees())


        structure = {1:dataStruct.getId(),
                    2:dataStruct.getEMG(),3:dataStruct.getRoll(),4:dataStruct.getPitch(),5:dataStruct.getYaw(),6:dataStruct.getShot(),
                    7: dataStruct.getHeadXAxis(), 8: dataStruct.getHeadYAxis(), 9: dataStruct.getHeadZAxis(),10: dataStruct.getHeadHeading(), 11: dataStruct.getHeadDegrees(),
                    12: dataStruct.getBodyXAxis(), 13: dataStruct.getBodyYAxis(), 14: dataStruct.getBodyZAxis(), 15: dataStruct.getBodyHeading(), 16: dataStruct.getBodyDegrees(),
                    17: dataStruct.getLocationXAxis(), 18:dataStruct.getLocationYAxis(), 19:dataStruct.getLocationZAxis(),
                    20:dataStruct.getHeartRate(), 21:dataStruct.getVisible(), 22:dataStruct.getHostile(), 23:dataStruct.getHit(), 24:dataStruct.getTimestamp()}

        stream = pickle.dumps(structure)
        server.send(stream)
        dataStruct.setShot(False)

    myoData.join()
    LocationData.join()
    #BodyOrientData.join()


