from multiprocessing import Process, Manager
from multiprocessing.managers import *
from UserInformation import *
import time
import random
import socket
import pickle
import hashlib
import json


ip = '127.0.0.1'
port = 51212                   # The same port as used by the server
delay = 0.1
globalSend = 10

def myo(User):
	send = globalSend
	while(send > 0):
		time.sleep(delay)
		User.setEMG(random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100))
		tempEMG = User.getEMG()
		# print("Myo - EMG Data = " + str(tempEMG))
		send -= 1

def headCompass(User):
	send = globalSend
	while(send > 0):
		time.sleep(delay)
		User.setHeadXAxis(random.randint(0,100))
		User.setHeadYAxis(random.randint(0,100))
		User.setHeadZAxis(random.randint(0,100))
		tempXAxis = User.getHeadXAxis()
		tempYAxis = User.getHeadYAxis()
		tempZAxis = User.getHeadZAxis()
		# print("Compass - HeadXAxis = " + str(tempXAxis) + "     HeadYAxis = " + str(tempYAxis) + "     HeadZAxis = " + str(tempZAxis))
		send -= 1

def bodyCompass(User):
	send = globalSend
	while(send > 0):
		time.sleep(delay)
		User.setBodyXAxis(random.randint(0,100))
		User.setBodyYAxis(random.randint(0,100))
		User.setBodyZAxis(random.randint(0,100))
		tempXAxis = User.getBodyXAxis()
		tempYAxis = User.getBodyYAxis()
		tempZAxis = User.getBodyZAxis()
		# print("Compass - BodyXAxis = " + str(tempXAxis) + "     BodyYAxis = " + str(tempYAxis) + "     BodyZAxis = " + str(tempZAxis))
		send -= 1

def locData(User):
	send = globalSend
	while(send > 0):
		time.sleep(delay)
		User.setLocationXAxis(random.randint(0,100))
		User.setLocationYAxis(random.randint(0,100))
		User.setLocationZAxis(random.randint(0,100))
		tempXAxis = User.getLocationXAxis()
		tempYAxis = User.getLocationYAxis()
		tempZAxis = User.getLocationZAxis()
		# print("UWB Receiver - LocationXAxis = " + str(tempXAxis) + "     LocationYAxis = " + str(tempYAxis) + "     LocationZAxis = " + str(tempZAxis))
		send -= 1

def sendLoop(User):
	send = globalSend
	isTCP = True
	# isTCP = False

	if(isTCP):
		sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sockTCP.connect((ip, port))
			print "TCP connected"
			while(send > 0):
				time.sleep(delay)
				data = readyData(User)		#MAY HAVE POTENTIAL PROBLEM HERE
				sockTCP.sendall(data)
				print str(11-send) + " " + str(checksum(data))
				# print data
				send -= 1
			sockTCP.close()
			print "TCP socket closed"
		except socket.error, exc:
			print("Error: %s" % exc)
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

def readyData(dataStruct):
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
	sendLoopData.start()
	myoData.start()
	headData.start()
	bodyData.start()
	locationData.start()


	# old version
	# myoData.join()
	# headData.join()

	# new
	print "myoData.join(@@@@@@@)"
	myoData.join()

	print "headData.join(@@@@@@@)"
	headData.join()

	print "bodyData.join(@@@@@@@)"
	bodyData.join()

	print "locationData.join(@@@@@@@)"
	locationData.join()

	sendLoopData.join()
	

