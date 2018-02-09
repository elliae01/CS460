import socket
import pickle
from UserInformation import *
import cx_Oracle
from multiprocessing import Process, Manager
from multiprocessing.managers import *
import sys
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

def noneRemover(item):
	if(item == None):
		return 0
	else:
		return item

# Automatically determine IP address or let user choose if multiple options available
def getIPAddress(port):
    validIPs = socket.getaddrinfo(socket.gethostname(), port, socket.AF_INET, socket.SOCK_STREAM)
    options = []
    # store all valid IPs
    for val in validIPs:
        options.append(val[4][0])

    chosen = 0
    try:
        if(len(options) >= 2):
            i = 0
            for val in options:
                print "[", i, "]: ", options[i]
                i += 1
            chosen = int(raw_input("Enter index of IP to use for server: "))
    except Exception,e:
        print "ERROR: trouble parsing index for IP"
        print "Exception: ",e
    return options[chosen]


def dbConnect(user, password, host, database):
    try:
        print("-> Connecting to database ", database, " located at ", host, " as ", user, " with password: ", password)
        database = cx_Oracle.connect(user, password, host + "/" + database)
        cursor = database.cursor()
        print("-> Successfully connected to database - ", database, "\n")
    except Exception as err:
        print("-> Failed to connect to database - ", database)
        print("Database error - ", err, "\n")

    return database, cursor

if __name__ == '__main__':
        # TCP CONNECTION
    numberOfConnections = 1
    port = 5000
    ip = getIPAddress(port)
    server, client = tcpConnect(numberOfConnections, ip, port)

        # DATABASE CONNECTION
    user = 'SYSMAN'
    password = 'System_Admin1'
    host = 'localhost'
    database = 'orcl'
    database, cursor = dbConnect(user, password, host, database)

        # GUI CONNECTION
    dataStruct, gui = guiConnect()

        # MAIN LOOP
    print("-> Beginning main collection process\n")
    dataStruct.setRun(True)
    User = True
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
            dataStruct.setHeartRate(Structure[20])
            dataStruct.setVisible(Structure[21])
            dataStruct.setHostile(Structure[22])
            dataStruct.setHit(Structure[23])

            if(User):
                rawEMG = dataStruct.getEMG()
                cursor.execute(
                    "INSERT INTO Shooter_Table VALUES(shooter_index_seq.nextval,CURRENT_TIMESTAMP,SHOOTER(" + str(
                        dataStruct.getId()) + "," + "Loc_Obj(" + str(dataStruct.getLocationXAxis()) + "," + str(
                        dataStruct.getLocationYAxis()) + "," + str(dataStruct.getLocationZAxis()) + ")," + str(
                        dataStruct.getHostile()) + "," + str(dataStruct.getHit()) + "," + str(
                        dataStruct.getHeartRate()) + "," + "Arm_Obj(Emg_Obj(" + str(rawEMG[0]) + str(rawEMG[1]) + str(
                        rawEMG[2]) + str(rawEMG[3]) + str(rawEMG[4]) + str(rawEMG[5]) + str(rawEMG[6]) + str(
                        rawEMG[7]) + ")," + str(dataStruct.getRoll()) + "," + str(dataStruct.getPitch()) + "," + str(
                        dataStruct.getYaw()) + ")," + str(dataStruct.getShot()) + "," + "Orient_Obj(" + str(
                        dataStruct.getBodyHeading()) + "," + str(dataStruct.getBodyXAxis()) + "," + str(
                        dataStruct.getBodyYAxis()) + "),Orient_Obj(" + str(dataStruct.getHeadHeading()) + "," + str(
                        dataStruct.getHeadXAxis()) + "," + str(dataStruct.getHeadYAxis()) + ")))")
            else:
                cursor.execute(
                    "INSERT INTO Target_Table VALUES(target_index_seq.nextval,CURRENT_TIMESTAMP,TARGET(" + str(
                        dataStruct.getId()) + "," + "Loc_Obj(" + str(dataStruct.getLocationXAxis()) + "," + str(
                        dataStruct.getLocationYAxis()) + "," + str(dataStruct.getLocationZAxis()) + ")," + str(
                        dataStruct.getHostile()) + "," + str(dataStruct.getHit()) + "," + str(
                        dataStruct.getVisible()) + "))")

            database.commit()


        except Exception as err:
            print("Main collection process failed")
            print("Main process error - ",err)

    client.close()
    database.close()
    server.close()
    gui.join()
    print("-> Closed all connections and exiting now.")
    sys.exit()