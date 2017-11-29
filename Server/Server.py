import socket
import pickle
from User_Information_Pi import *

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip = '192.168.1.4'
#ip = socket.gethostbyname(socket.gethostname())
port = 5454
address = (ip,port)

server.bind(address)
server.listen(1)

print("Started listening on     Ip - ",ip,"     Port - ",port)
client,addr = server.accept()
print("-> Made a connection with     IP - ", addr[0],"    Port - ",addr[1])

while(True):
    data = client.recv(4096)
    Structure = pickle.loads(data)

    dataStruct = UserInformation(Structure[1])
    dataStruct.setEMG(Structure[2][0],Structure[2][1],Structure[2][2],Structure[2][3],Structure[2][4],Structure[2][5],Structure[2][6],Structure[2][7])
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

    print("\nServer - EMG DATA = " + str(dataStruct.getEMG()))
    print("Server - HeadXAxis = " + str(dataStruct.getHeadXAxis()) + "     HeadYAxis = " + str(dataStruct.getHeadYAxis()) + "     HeadZAxis = " + str(dataStruct.getHeadZAxis()))
    print("Server - BodyXAxis = " + str(dataStruct.getBodyXAxis()) + "     BodyYAxis = " + str(dataStruct.getBodyYAxis()) + "     BodyZAxis = " + str(dataStruct.getBodyZAxis()))
    print("Server - LocationXAxis = " + str(dataStruct.getLocationXAxis()) + "     LocationYAxis = " + str(dataStruct.getLocationYAxis()) + "     LocationZAxis = " + str(dataStruct.getLocationZAxis()) +"\n")

client.close()
