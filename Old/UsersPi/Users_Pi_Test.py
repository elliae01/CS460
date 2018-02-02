from os import getpid
from multiprocessing import Process, Manager
from multiprocessing.managers import *
import time
import random

class UserInformation():
	Id = None
	emg = None
	location = None
	def __init__(self,Id):
		self.Id = Id
	def setId(self,newId):
		self.Id = newId
	def getId(self):
		return self.Id

	def setLocation(self,newLocation):
		self.location = newLocation
	def getLocation(self):
		return self.location

	def setEmg(self,newEmg):
		self.emg = newEmg
	def getEmg(self):
		return self.emg

def test1(User,delay):
	print("I am process number " + str( getpid()))
	while(True):
		User.setEmg(random.randint(0,100))
		time.sleep(delay)
def test2(User,delay):
	print("I am process number " + str(getpid()))
	while(True):
		User.setLocation(random.randint(0,100))
		time.sleep(delay)

if __name__ == '__main__':
	kill = 1
	delay = 1
	BaseManager.register('UserInformation',UserInformation)
	manager = BaseManager()
	manager.start()
	kyle = manager.UserInformation('01')
	print("Starting EMG = " + str(kyle.getEmg()))
	print("Starting Location = " + str(kyle.getLocation()))
	print("I am the main process")
	test1 = Process(target=test1, args=[kyle,delay])
	test2 = Process(target=test2, args=[kyle,delay])
	test1.start()
	test2.start()
	time.sleep(1)
	while(kill == 1):
		print("For user number: " + str(kyle.getId()) + " emg =  " + str(kyle.getEmg()))
		print("For user number: " +str(kyle.getId()) + " location = " + str(kyle.getLocation()))
		time.sleep(delay)
	test1.join()
	test2.join()
	

