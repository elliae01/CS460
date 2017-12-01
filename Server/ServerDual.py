import socket
import mysql.connector
import pickle
import hashlib
import json
from UserInformation import *

cnx = mysql.connector.connect(user='root', password='password',
											  host='127.0.0.1',
											  database='targalytics')
cnx.start_transaction(isolation_level='READ COMMITTED')
cursor = cnx.cursor()

def databaseUpdate(sql):
	query = (sql)
	cursor.execute(query)
	# rows = cursor.fetchall()

	# print(cursor.rowcount)

	# for row in rows:
	#     print(row)

	cnx.commit()
	# cursor.close()
	# cnx.close()

def checksum(item):
	h = hashlib.md5()
	h.update(item)
	return h.hexdigest()

def noneRemover(item):
    if(item == None):
        return 0
    else:
        return item

isTCP = True
# isTCP = False


ip = '127.0.0.1'
port = 51212

print("Starting listening on     Ip - ", ip, "     Port - ", port)

while(True):
	print("-"*20)
	if(isTCP):
		serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverTCP.bind((ip,port))
		serverTCP.listen(1)
		conn,addr = serverTCP.accept()

		while(True):
			data = conn.recv(4096)
			if not data: break
			# print("Data: ", h.hexdigest(), ", from: ", addr)
			print checksum(data)
			# print data
			Structure = pickle.loads(data)
			print Structure[1]
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
	
			emgData = dataStruct.getEMG()
			sql = "insert into test(id, people_id, emg_1, emg_2, emg_3, emg_4, emg_5, emg_6, emg_7, emg_8, headXAxis, headYAxis, headZAxis, bodyXAxis, bodyYAxis, bodyZAxis, locationXAxis, locationYAxis, locationZAxis)" \
			+"values("+"null"+", "+noneRemover(dataStruct.getId())+", " \
			+str(noneRemover(emgData[0]))+", "+str(noneRemover(emgData[1]))+", "+str(noneRemover(emgData[2]))+", "+str(noneRemover(emgData[3]))+", "+str(noneRemover(emgData[4]))+", "+str(noneRemover(emgData[5]))+", "+str(noneRemover(emgData[6]))+", "+str(noneRemover(emgData[7]))+", " \
			+str(noneRemover(dataStruct.getHeadXAxis()))+", "+str(noneRemover(dataStruct.getHeadYAxis()))+", "+str(noneRemover(dataStruct.getHeadZAxis()))+", " \
			+str(noneRemover(dataStruct.getBodyXAxis()))+", "+str(noneRemover(dataStruct.getBodyYAxis()))+", "+str(noneRemover(dataStruct.getBodyZAxis()))+", " \
			+str(noneRemover(dataStruct.getLocationXAxis()))+", "+str(noneRemover(dataStruct.getLocationYAxis()))+", "+str(noneRemover(dataStruct.getLocationZAxis()))+")"
			print sql
			databaseUpdate(sql)

		conn.close()
	else:
		serverUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		serverUDP.bind((ip,port))

		while(True):
			data,addr = serverUDP.recvfrom(4096)
			if not data: break
			print("Data: ", data, ", from: ", addr)

print("Server Ended.")
