import socket
import pickle
from UserInformation import *
import cx_Oracle
import sys
import threading
import time
import random
import datetime

#Target Deploy Speed
deploySpeed = 6             # 0-10  10 being fastest

    #TCP CONNECTION INFORMATION
numberOfConnections = 2
ip = '192.168.1.6'
port = 5001

    #DATABASE INFORMATION
user = 'SYSMAN'
password = 'System_Admin1'
host = 'localhost'
database = 'orcl'

def clientSpeaker(client,run,visible,hostile):
    structure = {1:run, 2:visible, 3:hostile}
    stream = pickle.dumps(structure)
    client.send(stream)
    #print("-> Data sent to target   Run - ", run, '   Visible - ',visible, '   hostile - ',hostile)

def tcpConnect(numberOfConnections, ip, port, cursor, database,targetList):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (ip, port)
    server.bind(address)
    numberOfConnected = 0

    server.listen(numberOfConnections)
    print("\n-> Started listening on     Ip - ", ip, "     Port - ", port, "       number of expected users - ",
          numberOfConnections)
    try:
        clientList = [numberOfConnections]
        for i in range(numberOfConnections):
            client, addr = server.accept()
            print("-> Made a connection with     IP - ", addr[0], "    Address - ", addr[1], "       number of connected users - ", numberOfConnected,"\n")
            numberOfConnected = numberOfConnected + 1

            t = threading.Thread(target=listen, args=(cursor,database,client,targetList))
            t.start()

            clientList.append(client)

    except Exception as err:
        print("-> Failed to make a connection with     IP - ", addr[0], "    Address - ", addr[1])
        print("Connection error - ", err, "\n")

    return server, clientList


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

def noneRemover(item):
    if(item == None):
        return -99
    return item

def booleanConvert(item):
    if(item == True):
        return 1
    else:
        return 0

def listen(cursor,database,client,targetList):
    ident = client.recv(4096)
    Structure = pickle.loads(ident)

    if (Structure[1] == 1):
        targetList.append(client)
        print('Target Added')

        # MAIN LOOP
    print("-> Beginning main collection process\n")

    dataStruct.setRun(True)
    while(dataStruct.getRun()):
        try:
            data = client.recv(4096)
            Structure = pickle.loads(data)

            while(dataStruct.getWriting() == 1):
                time.sleep(.001)
            dataStruct.setWriting(1)

            dataStruct.setId(noneRemover(Structure[1]))
            dataStruct.setEMG([noneRemover(Structure[2][0]),noneRemover(Structure[2][1]),noneRemover(Structure[2][2]),noneRemover(Structure[2][3]),noneRemover(Structure[2][4]),noneRemover(Structure[2][5]),noneRemover(Structure[2][6]),noneRemover(Structure[2][7])])
            dataStruct.setRoll(noneRemover(Structure[3]))
            dataStruct.setPitch(noneRemover(Structure[4]))
            dataStruct.setYaw(noneRemover(Structure[5]))
            dataStruct.setShot(booleanConvert(Structure[6]))
            dataStruct.setHeadXAxis(noneRemover(Structure[7]))
            dataStruct.setHeadYAxis(noneRemover(Structure[8]))
            dataStruct.setHeadZAxis(noneRemover(Structure[9]))
            dataStruct.setHeadHeading(noneRemover(Structure[10]))
            dataStruct.setHeadDegrees(noneRemover(Structure[11]))
            dataStruct.setBodyXAxis(noneRemover(Structure[12]))
            dataStruct.setBodyYAxis(noneRemover(Structure[13]))
            dataStruct.setBodyZAxis(noneRemover(Structure[14]))
            dataStruct.setBodyHeading(noneRemover(Structure[15]))
            dataStruct.setBodyDegrees(noneRemover(Structure[16]))
            dataStruct.setLocationXAxis(noneRemover(Structure[17]))
            dataStruct.setLocationYAxis(noneRemover(Structure[18]))
            dataStruct.setLocationZAxis(noneRemover(Structure[19]))
            dataStruct.setHeartRate(noneRemover(Structure[20]))
            dataStruct.setVisible(noneRemover(Structure[21]))
            dataStruct.setHostile(noneRemover(Structure[22]))
            dataStruct.setHit(noneRemover(Structure[23]))
            #dataStruct.setTimestamp(noneRemover(datetime.strptime(Structure[24], "%d-%b-%Y %I.%M.%S.%f %p")))
            dataStruct.setTimestamp(noneRemover(Structure[24]))

            #print(Structure)
            if(dataStruct.getShot() == 1):
                print('-> Shot detected')

            if(dataStruct.getVisible() == 1):
                print('-> Target is visible')

            if(dataStruct.getHit() == 1):
                print('-> Target has been hit')

            if(dataStruct.getHostile() < 10):
                rawEMG = dataStruct.getEMG()

                sql = (
                    "INSERT INTO Shooter_Table VALUES(shooter_index_seq.nextval,dataStruct.getTimestamp(),SHOOTER(" + str(
                        dataStruct.getId()) + "," + "Loc_Obj(" + str(dataStruct.getLocationXAxis()) + "," + str(
                        dataStruct.getLocationYAxis()) + "," + str(dataStruct.getLocationZAxis()) + ")," + str(
                        dataStruct.getHostile()) + "," + str(dataStruct.getHit()) + "," + str(
                        dataStruct.getHeartRate()) + "," + "Arm_Obj(Emg_Obj(" + str(rawEMG[0]) +"," + str(rawEMG[1]) +"," + str(
                        rawEMG[2]) +"," + str(rawEMG[3]) +"," + str(rawEMG[4]) +"," + str(rawEMG[5]) +"," + str(rawEMG[6]) +"," + str(
                        rawEMG[7]) + ")," + str(dataStruct.getRoll()) + "," + str(dataStruct.getPitch()) + "," + str(
                        dataStruct.getYaw()) + ")," + str(dataStruct.getShot()) + "," + "Orient_Obj(" + str(
                        dataStruct.getBodyHeading()) + "," + str(dataStruct.getBodyXAxis()) + "," + str(
                        dataStruct.getBodyYAxis()) + "),Orient_Obj(" + str(dataStruct.getHeadHeading()) + "," + str(
                        dataStruct.getHeadXAxis()) + "," + str(dataStruct.getHeadYAxis()) + ")))")
                cursor.execute(sql)
            else:
                sql = (
                    "INSERT INTO Target_Table VALUES(target_index_seq.nextval,dataStruct.getTimestamp(,TARGET(" + str(
                        dataStruct.getId()) + "," + "Loc_Obj(" + str(dataStruct.getLocationXAxis()) + "," + str(
                        dataStruct.getLocationYAxis()) + "," + str(dataStruct.getLocationZAxis()) + ")," + str(
                        dataStruct.getHostile()) + "," + str(dataStruct.getHit()) + "," + str(
                        dataStruct.getVisible()) + "))")
                cursor.execute(sql)
            database.commit()
            dataStruct.setWriting(0)

        except Exception as err:
            print("Main collection process failed")
            print("Main process error - ",err)

    client.close()
    database.close()


if __name__ == '__main__':
    # DATABASE CONNECTION
    database, cursor = dbConnect(user, password, host, database)

        # GUI CONNECTION
    #dataStruct, gui = guiConnect()

    dataStruct = UserInformation(0)

    targetList = []
        # TCP CONNECTION
    server,clientList = tcpConnect(numberOfConnections, ip, port, cursor, database,targetList)

    while(dataStruct.getRun() != 0):
        time.sleep(5)
        if(random.randint(0,10) < deploySpeed):
            if targetList:
                randomTarget = random.randint(1,len(targetList))
                clientSpeaker(targetList[randomTarget-1], 1, 1, 11)

    for client in clientList:
        clientSpeaker(client,0,0,0)
        client.close()

    server.close()
    print("-> Closed all connections and exiting now.")
    sys.exit()