import socket
import pickle
from UserInformation import *
import mysql.connector
from multiprocessing import Process, Manager
from multiprocessing.managers import *
import sys
from DatabaseStorage import *
from Display import *

def tcpConnect(numberOfConnections,ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (ip, port)
    server.bind(address)
    server.listen(numberOfConnections)
    print("\n-> Started listening on     Ip - ", ip, "     Port - ", port, "       number of expected users - ",
          numberOfConnections)
    try:
        client, addr = server.accept()
        print("-> Made a connection with     IP - ", addr[0], "    Address - ", addr[1], "\n")
    except Exception as err:
        print("-> Failed to make a connection with     IP - ", addr[0], "    Address - ", addr[1])
        print("Connection error - ", err, "\n")

    return server, client


def dbConnect(user, password, host, databaseName):
    try:
        print("-> Connecting to database ", databaseName, " located at ", host, " as ", user, " with password: ", password)
        database = mysql.connector.connect(user=user, password=password, host=host, database=databaseName)
        cursor = database.cursor()
        print("-> Successfully connected to database - ", databaseName, "\n")
    except Exception as err:
        print("-> Failed to connect to database - ", databaseName)
        print("Database error - ", err,"\n")

    return database, cursor

def guiConnect():
    try:
        print("-> Attempting to create graphical user interface process")
        BaseManager.register('UserInformation', UserInformation)
        manager = BaseManager()
        manager.start()
        dataStruct = manager.UserInformation('01')
        gui = Process(target=guiMain, args=[dataStruct])
        gui.start()
        print("-> Successfully created graphical user interface process\n")

    except Exception as err:
        print("-> Failed to create graphical user interface process")
        print("Multiprocess error - ", err, "\n")

    return dataStruct, gui

if __name__ == '__main__':
        # TCP CONNECTION
    numberOfConnections = 1
    ip = '192.168.1.6'
    port = 5000
    server, client = tcpConnect(numberOfConnections, ip, port)

        # DATABASE CONNECTION
    user = 'root'
    password = 'System_Admin1'
    host = '127.0.0.1'
    databaseName = 'targamite_project'
    database, cursor = dbConnect(user, password, host, databaseName)

        # GUI CONNECTION
    dataStruct, gui = guiConnect()

        # MAIN LOOP
    print("-> Beginning main collection process\n")
    dataStruct.setRun(True)
    while(dataStruct.getRun()):
        try:
            data = client.recv(4096)
            Structure = pickle.loads(data)

            dataStruct.setId(Structure[1])
            dataStruct.setEMG([Structure[2][0],Structure[2][1],Structure[2][2],Structure[2][3],Structure[2][4],Structure[2][5],Structure[2][6],Structure[2][7]])
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

                # PRODUCE SQL STATEMENT
            sql = convertToSqlStatement(dataStruct)
            print("SQL insert statement: \n",sql)
                # STORE SQL INTO DATABASE
            # Delays the loop for time set in delay variable
            databaseUpdate(sql, database)

        except Exception as err:
            print("Main collection process failed")
            print("Main process error - ",err)

    client.close()
    database.close()
    server.close()
    gui.join()
    print("-> Closed all connections and exiting now.")
    sys.exit()