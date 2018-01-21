import socket
import mysql.connector
import pickle
import json
import re
from UserInformation import *
from threading import Thread

# CANT BE USED OUTSIDE CLASS, ADD AS METHOD TO ALL UserInfo class files
def printJSON(item):
	json.dumps(item,default=lambda o: o.__dict__, sort_keys=True, indent=4)

# finds and returns all the full json blocks
def jsonBlocksExtract(val):
	temp = re.findall(r'(\{.+?\})',val)
	return ''.join(temp)

# Removes all json blocks (non-greedy) after extraction
def jsonBlocksRemove(val):
	return re.sub(r'(\{.+?\})','',val)

# Returns a json structure representing data
def packageData(dataStruct):
	structure = {1:dataStruct.getId(),
				2:dataStruct.getEMG(),3:dataStruct.getRoll(),4:dataStruct.getPitch(),5:dataStruct.getYaw(),6:dataStruct.getShot(),
				7: dataStruct.getHeadXAxis(), 8: dataStruct.getHeadYAxis(), 9: dataStruct.getHeadZAxis(),10: dataStruct.getHeadHeading(), 11: dataStruct.getHeadDegrees(),
				12: dataStruct.getBodyXAxis(), 13: dataStruct.getBodyYAxis(), 14: dataStruct.getBodyZAxis(), 15: dataStruct.getBodyHeading(), 16: dataStruct.getBodyDegrees(),
				17: dataStruct.getLocationXAxis(),18:dataStruct.getLocationYAxis(),19:dataStruct.getLocationZAxis(),20:dataStruct.getHeartRate()}
	return json.dumps(structure)

# Handles a new connection and sends data to database
class AcceptThread(Thread):
	def __init__(self, addr, conn):
		Thread.__init__(self)
		self.addr = addr
		self.conn = conn
		print "[+] New thread started for " + str(addr)

	def run(self):
		print "FROM: ", addr
		accumulated = ""
		while (True):
			'''Loops continuously in blocks of 4096 until no more data is received.
			If many messages are sent (and received) from the same client, you can
			end up with a full buffer with partial json blocks, which is handled by
			the jsonBlocksExtract and jsonBlocksRemove methods.'''
			data = conn.recv(4096)
			if (not data): break
			# see if match is found, keep track of number
			accumulated += data
			fullBlocks = jsonBlocksExtract(accumulated)
			if (len(fullBlocks) >= 1):
				accumulated = jsonBlocksRemove(accumulated)
				storeData(fullBlocks)
			else:
				print "Warning: Partial json block received"
		conn.close()

# Saves received data from network to database
def storeData(jsonData):
	lastItemReceived = ""

	# sometimes multiple json structures are put together, this loop handles one by one
	try:
		lastItemReceived = jsonData
		items = jsonSplitMultiple(jsonData)
		for item in items:
			# turn json into object
			dataStruct = depackage(item)

			print packageData(dataStruct)

			# turn object into sql insert statements
			sql = convertToSqlInsert(dataStruct, "test")

			# execute sql queries
			databaseUpdate(sql)
	except Exception, e:
		print "Error: Could not store: *",lastItemReceived,"*"
		print "Exception: %s" % e

# Takes possible multiple json entries in same string (normal decoder cant handle), returns array of json objects
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
	Structure = item

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
def convertToSqlInsert(dataStruct, dataKind):
	emgData = dataStruct.getEMG()
	result = ""

	# locations
	result += sqlizerInsert(
		"insert into locations(id, people_id, time_stamp, locationXAxis, locationYAxis, locationZAxis, width, height)",
		["null", dataStruct.getId(), "now()", dataStruct.getLocationXAxis(),
		 dataStruct.getLocationYAxis(), dataStruct.getLocationZAxis(), "null", "null"]
	)

	# orientations
	result += sqlizerInsert(
		"insert into orientations(id, people_id, time_stamp, headXAxis, headYAxis, headZAxis, headHeading, headDegrees, bodyXAxis, bodyYAxis, bodyZAxis, bodyHeading, bodyDegrees)",
		["null", dataStruct.getId(), "now()", dataStruct.getHeadXAxis(), dataStruct.getHeadYAxis(),
		 dataStruct.getHeadZAxis(), dataStruct.getHeadHeading(), dataStruct.getHeadDegrees(), dataStruct.getBodyXAxis(),
		 dataStruct.getBodyYAxis(), dataStruct.getBodyZAxis(), dataStruct.getBodyHeading(), dataStruct.getBodyDegrees()]
	)

	# biometrics
	result += sqlizerInsert(
		"insert into biometrics(id, people_id, time_stamp, shot, roll, pitch, yaw, emg_1, emg_2, emg_3, emg_4, emg_5, emg_6, emg_7, emg_8)",
		["null", dataStruct.getId(), "now()", dataStruct.getShot(), dataStruct.getRoll(), dataStruct.getPitch(),
		 dataStruct.getYaw(), emgData[0], emgData[1], emgData[2], emgData[3], emgData[4], emgData[5], emgData[6],
		 emgData[7]]
	)

	# test
	result += sqlizerInsert(
		"insert into test(id, people_id, emg_1, emg_2, emg_3, emg_4, emg_5, emg_6, emg_7, emg_8, headXAxis, headYAxis, headZAxis, bodyXAxis, bodyYAxis, bodyZAxis, locationXAxis, locationYAxis, locationZAxis)",
		["null", dataStruct.getId(), emgData[0], emgData[1], emgData[2], emgData[3], emgData[4], emgData[5], emgData[6], emgData[7],
		 dataStruct.getHeadXAxis(), dataStruct.getHeadYAxis(), dataStruct.getHeadZAxis(), dataStruct.getBodyXAxis(), dataStruct.getBodyYAxis(),
		 dataStruct.getBodyZAxis(), dataStruct.getLocationXAxis(), dataStruct.getLocationYAxis(), dataStruct.getLocationZAxis()]
	)

	return result

# Takes input beginning sql statement and array of values. Turns input into sql insert statement.
def sqlizerInsert(sqlStatementBegin, values):
	result = sqlStatementBegin + "values("
	for i in range(len(values)):
		result += str(noneRemover(values[i]))
		if(i != (len(values)-1)):
			result += ", "
	result += ");"
	return result

# executes sql statements
def databaseUpdate(sql):
	# TODO: log errors
	cursor = cnx.cursor()
	for result in cursor.execute(sql,multi=True):
		if(printDatabaseStatement):
			if result.with_rows:
				print("Rows produced by statement '{}':".format(
					result.statement))
				print(result.fetchall())
			else:
				print("Number of rows affected by statement '{}': {}".format(
					result.statement, result.rowcount))
	cnx.commit()
	cursor.close()

# Automatically determine IP address or let user choose if multiple options available
def getIPAddress():
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

# Turns any Python Nones to 0, for playing nice with database
def noneRemover(item):
	if(item == None):
		return 0
	else:
		return item

if __name__ == '__main__':
	# Global variables
	global cnx
	global port

	# Setup Variables
	printDatabaseStatement = False	# prints each database statement if set to true
	port = 51212

	# Connect to database
	cnx = mysql.connector.connect(user='root', password='password',
								  host='127.0.0.1',
								  database='targalytics')

	ip = getIPAddress()		# automatically choose IP address or list options

	print "Server Started."
	print "IP - ", ip
	print "Port - ", port

	threads = []

	try:
		serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverTCP.bind((ip,port))
		while(True):
			print("-"*35)
			serverTCP.listen(4)
			conn,addr = serverTCP.accept()
			newThread = AcceptThread(addr,conn)
			newThread.start()
			threads.append(newThread)
		for t in threads:
			t.join()
	except Exception,e:
		print "ERROR: IP address ", ip, " not valid (is it already in use?)"
		print "Exception: ",e

	print("Server Ended.")
