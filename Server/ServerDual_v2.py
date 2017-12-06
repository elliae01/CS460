import socket
import mysql.connector
import pickle
import hashlib
import json
from UserInformation import *

# CANT BE USED OUTSIDE CLASS, ADD AS METHOD TO ALL UserInfo class files
def printJSON(item):
	json.dumps(item,default=lambda o: o.__dict__, sort_keys=True, indent=4)

def packageData(dataStruct):
	structure = {1:dataStruct.getId(),
				2:dataStruct.getEMG(),3:dataStruct.getRoll(),4:dataStruct.getPitch(),5:dataStruct.getYaw(),6:dataStruct.getShot(),
				7: dataStruct.getHeadXAxis(), 8: dataStruct.getHeadYAxis(), 9: dataStruct.getHeadZAxis(),10: dataStruct.getHeadHeading(), 11: dataStruct.getHeadDegrees(),
				12: dataStruct.getBodyXAxis(), 13: dataStruct.getBodyYAxis(), 14: dataStruct.getBodyZAxis(), 15: dataStruct.getBodyHeading(), 16: dataStruct.getBodyDegrees(),
				17: dataStruct.getLocationXAxis(),18:dataStruct.getLocationYAxis(),19:dataStruct.getLocationZAxis(),20:dataStruct.getHeartRate()}
	return json.dumps(structure)

# Saves received data from network to database
def storeData(jsonData):
	global numPacketsRec
	# sometimes multiple json structures are put together, this loop handles one by one
	try:
		items = jsonSplitMultiple(jsonData)
		# recNum = 1	#message number
		for item in items:
			# TODO: if hash/checksum is same as another, might be using UDP and received dup packet
			numPacketsRec += 1
			
			# turn json into object
			dataStruct = depackage(item)

			tempPrint = packageData(dataStruct)

			print str(numPacketsRec) + ": " + checksum(tempPrint)
			# print dataStruct

			# turn object into sql insert statement
			sql = convertToSqlInsert(dataStruct, "test")

			# execute sql queries
			databaseUpdate(sql)
	except:
		print "Error: Could not store data"

# Takes possible multiple json entries in same string (messes up normal decoder), returns array of json objects
def jsonSplitMultiple(jsonData):
	result = []
	dec = json.JSONDecoder()
	pos = 0
	while pos < len(str(jsonData)):
		j, jsonLen = dec.raw_decode(str(jsonData)[pos:])
		pos += jsonLen
		result.append(j)
	return result

# Takes json data as input, turns into UserInformation object
def depackage(item):
	# print jsonData
	# Structure = json.loads(item)
	Structure = item

	# Structure = json.loads(open("jsonData", "r").read())

	# for i in Structure:
	# 	print Structure["i"]

	# for received data from pi client
	dataStruct = UserInformation(Structure["1"])
	dataStruct.setEMG(Structure["2"][0],Structure["2"][1],Structure["2"][2],Structure["2"][3],Structure["2"][4],Structure["2"][5],Structure["2"][6],Structure["2"][7])
	dataStruct.setRoll(Structure["3"])
	dataStruct.setPitch(Structure["4"])
	dataStruct.setYaw(Structure["5"])
	dataStruct.setShot(Structure["6"])
	dataStruct.setHeadXAxis(Structure["7"])
	dataStruct.setHeadYAxis(Structure["8"])
	dataStruct.setHeadZAxis(Structure["9"])
	dataStruct.setHeadHeading(Structure["10"])
	dataStruct.setHeadDegrees(Structure["11"])
	dataStruct.setBodyXAxis(Structure["12"])
	dataStruct.setBodyYAxis(Structure["13"])
	dataStruct.setBodyZAxis(Structure["14"])
	dataStruct.setBodyHeading(Structure["15"])
	dataStruct.setBodyDegrees(Structure["16"])
	dataStruct.setLocationXAxis(Structure["17"])
	dataStruct.setLocationYAxis(Structure["18"])
	dataStruct.setLocationZAxis(Structure["19"])
	dataStruct.setHeartRate(Structure["20"])

	return dataStruct

# Extracts data from objects and converts to sql insert statements
# TODO: make if statements so that multiple datakinds will be saved if they are passed
def convertToSqlInsert(dataStruct, dataKind):
	result = ""
	if(dataKind == "people"):
		result += sqlizerInsert(
			"insert into people(id, name)",
			["null", dataStruct.getId()]
			)
	elif(dataKind == "locations"):
		result += sqlizerInsert(
			"insert into locations(id, people_id, time_stamp, signature, locationXAxis, locationYAxis, locationZAxis, width, height)",
			["null", dataStruct.getId(), "now()", dataStruct.getSignature(), dataStruct.getLocationXAxis(), dataStruct.getLocationYAxis(), dataStruct.getLocationZAxis(), "null", "null"]
			)
	elif(dataKind == "orientations"):
		result += sqlizerInsert(
			"insert into orientations(id, people_id, time_stamp, headXAxis, headYAxis, headZAxis, headHeading, headDegrees, bodyXAxis, bodyYAxis, bodyZAxis, bodyHeading, bodyDegrees)",
			["null", dataStruct.getId(), "now()", dataStruct.getHeadXAxis(), dataStruct.getHeadYAxis(), dataStruct.getHeadZAxis(), dataStruct.getHeadHeading(), dataStruct.getHeadDegrees(), dataStruct.getBodyXAxis(), dataStruct.getBodyYAxis(), dataStruct.getBodyZAxis(), dataStruct.getBodyHeading(), dataStruct.getBodyDegrees()]
			)
	elif(dataKind == "biometrics"):
		# emgData = ['''make sure data is actually here and not missing values...will cause out of bounds''']
		emgData = dataStruct.getEMG()
		result += sqlizerInsert(
			"insert into biometrics(id, people_id, time_stamp, shot, roll, pitch, yaw, emg_1, emg_2, emg_3, emg_4, emg_5, emg_6, emg_7, emg_8)",
			["null", dataStruct.getId(), "now()", dataStruct.getShot(), dataStruct.getRoll(), dataStruct.getPitch(), dataStruct.getYaw(), emgData[0], emgData[1], emgData[2], emgData[3], emgData[4], emgData[5], emgData[6], emgData[7]]
			)
	else:
		# else(dataKind == "test"):
		emgData = dataStruct.getEMG()
		# print("null", dataStruct.getId(), emgData[0], emgData[1], emgData[2], emgData[3], emgData[4], emgData[5], emgData[6], emgData[7], dataStruct.getHeadXAxis(), dataStruct.getHeadYAxis(), dataStruct.getHeadZAxis(), dataStruct.getBodyXAxis(), dataStruct.getBodyYAxis(), dataStruct.getBodyZAxis(), dataStruct.getLocationXAxis(), dataStruct.getLocationYAxis(), dataStruct.getLocationZAxis())
		result += sqlizerInsert(
			"insert into test(id, people_id, emg_1, emg_2, emg_3, emg_4, emg_5, emg_6, emg_7, emg_8, headXAxis, headYAxis, headZAxis, bodyXAxis, bodyYAxis, bodyZAxis, locationXAxis, locationYAxis, locationZAxis)",
			[str(noneRemover("null")), str(noneRemover(dataStruct.getId())), str(noneRemover(emgData[0])), str(noneRemover(emgData[1])), str(noneRemover(emgData[2])), str(noneRemover(emgData[3])), str(noneRemover(emgData[4])), str(noneRemover(emgData[5])), str(noneRemover(emgData[6])), str(noneRemover(emgData[7])), str(noneRemover(dataStruct.getHeadXAxis())), str(noneRemover(dataStruct.getHeadYAxis())), str(noneRemover(dataStruct.getHeadZAxis())), str(noneRemover(dataStruct.getBodyXAxis())), str(noneRemover(dataStruct.getBodyYAxis())), str(noneRemover(dataStruct.getBodyZAxis())), str(noneRemover(dataStruct.getLocationXAxis())), str(noneRemover(dataStruct.getLocationYAxis())), str(noneRemover(dataStruct.getLocationZAxis()))]
			)
	return result

# Takes input beginning sql statement and array of values. Turns input into sql insert statement.
def sqlizerInsert(sqlStatementBegin, values):
	result = sqlStatementBegin + "values("
	for i in range(len(values)):
		result += str(noneRemover(values[i]))
		if(i != (len(values)-1)):
			result += ", "
	result += ")"
	return result

# def databaseUpdateMany():
	# cursor.executemany()

# executes sql statements
def databaseUpdate(sql):
	# TODO: log errors
	cursor = cnx.cursor()
	cursor.execute(sql)
	cnx.commit()
	cursor.close()

def checksum(item):
	h = hashlib.md5()
	h.update(item)
	return h.hexdigest()

def noneRemover(item):
	if(item == None):
		return 0
	else:
		return item

if __name__ == '__main__':
	global numPacketsRec
	global cnx
	cnx = mysql.connector.connect(user='root', password='password',
											  host='127.0.0.1',
											  database='targalytics')

	isTCP = True
	# isTCP = False

	ip = '192.168.254.24'
	port = 51212

	print "Starting listening"
	print "IP - ", ip
	print "Port - ", port

	if(isTCP):
		serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverTCP.bind((ip,port))
		while(True):
			print("-"*35)
			serverTCP.listen(1)
			conn,addr = serverTCP.accept()
			numPacketsRec = 0
			while(True):
				data = conn.recv(4096)
				if not data: break
				# print "=============PACKET============="
				storeData(data)	#will be called until connection closes

			conn.close()
		else:
			serverUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			serverUDP.bind((ip,port))

			while(True):
				data,addr = serverUDP.recvfrom(4096)
				if not data: break
				print("Data: ", data, ", from: ", addr)

	print("Server Ended.")
