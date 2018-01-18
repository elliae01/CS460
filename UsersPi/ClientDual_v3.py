from multiprocessing import Process, Manager
from multiprocessing.managers import *
from UserInformation import *
import time
import random
import socket
import pickle
import hashlib
import json

ip = '192.168.254.16'
port = 51212                   # The same port as used by the server
delay = 1
globalSend = 50


def myo(User):
	print "myo"
	while (not User.isDataSent()):
		if (User.willUseRealData()):
			'''
			code for pulling data from device

			code for storing into User object
			'''
		else:
			User.setEMG(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100),
						random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
		if(User.willPrintCollectedData()):
			tempEMG = User.getEMG()
			print("Myo - EMG Data = " + str(tempEMG))
		time.sleep(delay)
	print "DONE myo"


def headCompass(User):
	print "head"
	while (not User.isDataSent()):
		if (User.willUseRealData()):
			'''
			code for pulling data from device

			code for storing into User object
			'''
		else:
			User.setHeadXAxis(random.randint(0, 100))
			User.setHeadYAxis(random.randint(0, 100))
			User.setHeadZAxis(random.randint(0, 100))
		if(User.willPrintCollectedData()):
			tempXAxis = User.getHeadXAxis()
			tempYAxis = User.getHeadYAxis()
			tempZAxis = User.getHeadZAxis()
			print("Compass - HeadXAxis = " + str(tempXAxis) + "     HeadYAxis = " + str(
				tempYAxis) + "     HeadZAxis = " + str(tempZAxis))
		time.sleep(delay)
	print "DONE headCompass"


def bodyCompass(User):
	print "body"
	while (not User.isDataSent()):
		if (User.willUseRealData()):
			'''
			code for pulling data from device

			code for storing into User object
			'''
		else:
			User.setBodyXAxis(random.randint(0, 100))
			User.setBodyYAxis(random.randint(0, 100))
			User.setBodyZAxis(random.randint(0, 100))
		if(User.willPrintCollectedData()):
			tempXAxis = User.getBodyXAxis()
			tempYAxis = User.getBodyYAxis()
			tempZAxis = User.getBodyZAxis()
			print("Compass - BodyXAxis = " + str(tempXAxis) + "     BodyYAxis = " + str(
				tempYAxis) + "     BodyZAxis = " + str(tempZAxis))
		time.sleep(delay)
	print "DONE bodyCompass"


def locData(User):
	print "loc"
	while (not User.isDataSent()):
		if (User.willUseRealData()):
			'''
			code for pulling data from device

			code for storing into User object
			'''
		else:
			User.setLocationXAxis(random.randint(0, 100))
			User.setLocationYAxis(random.randint(0, 100))
			User.setLocationZAxis(random.randint(0, 100))
		if(User.willPrintCollectedData()):
			tempXAxis = User.getLocationXAxis()
			tempYAxis = User.getLocationYAxis()
			tempZAxis = User.getLocationZAxis()
			print("UWB Receiver - LocationXAxis = " + str(tempXAxis) + "     LocationYAxis = " + str(
				tempYAxis) + "     LocationZAxis = " + str(tempZAxis))
		time.sleep(delay)
	print "DONE locData"


def sendLoop(User):
	send = globalSend
	retryTime = 3
	isTCP = True
	# isTCP = False
	serverNotFoundError = False

	while(True):
		if(isTCP):
			sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				if(serverNotFoundError):
					print("Server not detected. Retrying in %d seconds..." % retryTime)
					time.sleep(retryTime)
					serverNotFoundError = False
					continue
				print "TCP connecting..."
				sockTCP.connect((ip, port))
				print "TCP connected"
				while(send > 0):
					data = packageData(User)
					sockTCP.sendall(data)
					print str((globalSend+1)-send) + ":\t" + str(checksum(data))
					# print data
					send -= 1
					time.sleep(delay)
				sockTCP.close()
				print "TCP socket closed"
				User.setDataSent(True)
				break
			except socket.error, exc:
				print "Error: %s" % exc
				serverNotFoundError = True
				continue
		else:
			sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			while(send > 0):
				time.sleep(delay)
				# data = "Data_" + str(send)
				# user = createTestUser(send)
				# data = user.printMe()
				sockUDP.sendto(data, (ip, port))
				print data
				send -= 1
			sockUDP.close()

# Takes UserInformation object as input, turns into json data
def packageData(dataStruct):
	structure = {1:dataStruct.getId(),
				2:dataStruct.getEMG(),3:dataStruct.getRoll(),4:dataStruct.getPitch(),5:dataStruct.getYaw(),6:dataStruct.getShot(),
				7: dataStruct.getHeadXAxis(), 8: dataStruct.getHeadYAxis(), 9: dataStruct.getHeadZAxis(),10: dataStruct.getHeadHeading(), 11: dataStruct.getHeadDegrees(),
				12: dataStruct.getBodyXAxis(), 13: dataStruct.getBodyYAxis(), 14: dataStruct.getBodyZAxis(), 15: dataStruct.getBodyHeading(), 16: dataStruct.getBodyDegrees(),
				17: dataStruct.getLocationXAxis(),18:dataStruct.getLocationYAxis(),19:dataStruct.getLocationZAxis(),20:dataStruct.getHeartRate()}
	return json.dumps(structure)

def checksum(item):
	h = hashlib.md5()
	h.update(item)
	return h.hexdigest()

if __name__ == '__main__':
	BaseManager.register('UserInformation',UserInformation)
	manager = BaseManager()
	manager.start()
	dataStruct = manager.UserInformation('01')
	sendLoopData = Process(target=sendLoop, args=[dataStruct])
	myoData = Process(target=myo, args=[dataStruct])
	headData = Process(target=headCompass, args=[dataStruct])
	bodyData = Process(target=bodyCompass, args=[dataStruct])
	locationData = Process(target=locData, args=[dataStruct])
	myoData.start()
	headData.start()
	bodyData.start()
	locationData.start()

	print "Sleeping for 1 second to let other processes fill data"
	time.sleep(1)
	sendLoopData.start()

	myoData.join()
	headData.join()
	bodyData.join()
	locationData.join()
	sendLoopData.join()
	

