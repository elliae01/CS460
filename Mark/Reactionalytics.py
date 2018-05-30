from multiprocessing import Process, Manager
from multiprocessing.managers import *
import pandas as pd
from pandas import DataFrame
import cx_Oracle
import os
import math
from Server.UserInformation import *

print("Hello, Welcome to Reactionalytics.py")

class Reactionalytics:
    df = None

    def __init__(self,MyDataFrame):
        self.cCol4INDEX = 0
        self.cCol4Date = 1
        self.cCol4Id = 2
        self.cCol4LocX = 3
        self.cCol4LocY = 4
        self.cCol4LocZ = 5
        self.cCol4Hostility = 6
        self.cCol4Hit = 7
        self.cCol4HeartRate = 8
        self.cCol4Emg0 = 9
        self.cCol4Emg1 = 10
        self.cCol4Emg2 = 11
        self.cCol4Emg3 = 12
        self.cCol4Emg4 = 13
        self.cCol4Emg5 = 14
        self.cCol4Emg6 = 15
        self.cCol4Emg7 = 16
        self.cCol4ArmRoll = 17
        self.cCol4ArmPitch = 18
        self.cCol4ArmHeading = 19
        self.cCol4Shot = 20
        self.cCol4BodyHeading = 21
        self.cCol4BodyRoll = 22
        self.cCol4BodyPitch = 23
        self.cCol4HeadHeading = 24
        self.cCol4HeadRoll = 25
        self.cCol4HeadPitch = 26
        self.df = MyDataFrame

    def getDate(self, row):
        return self.df.iat[row, self.cCol4Date]

    def getINDEX(self, row):
        return self.df.iat[row, self.cCol4INDEX]

    def getID(self, row):
        return self.df.iat[row, self.cCol4Id]

    def getX(self, row):
        #print("Calculating X for index "+str(self.df.iat[row, self.cCol4INDEX]))
        return self.df.iat[row, self.cCol4LocX]

    def getY(self, row):
        return self.df.iat[row, self.cCol4LocY]

    def getZ(self, row):
        return self.df.iat[row, self.cCol4LocZ]

    def getHostility(self, row):
        return self.df.iat[row, self.cCol4Hostility]

    def getHit(self, row):
        return self.df.iat[row, self.cCol4Hit]

    def getHeartRate(self, row):
        return self.df.iat[row, self.cCol4HeartRate]

    def getEmg0(self, row):
        return self.df.iat[row, self.cCol4Emg0]

    def getEmg1(self, row):
        return self.df.iat[row, self.cCol4Emg1]

    def getEmg2(self, row):
        return self.df.iat[row, self.cCol4Emg2]

    def getEmg3(self, row):
        return self.df.iat[row, self.cCol4Emg3]

    def getEmg4(self, row):
        return self.df.iat[row, self.cCol4Emg4]

    def getEmg5(self, row):
        return self.df.iat[row, self.cCol4Emg5]

    def getEmg6(self, row):
        return self.df.iat[row, self.cCol4Emg6]

    def getEmg7(self, row):
        return self.df.iat[row, self.cCol4Emg7]

    def getArmRoll(self, row):
        return self.df.iat[row, self.cCol4ArmRoll]

    def getArmPitch(self, row):
        return self.df.iat[row, self.cCol4ArmPitch]

    def getArmHeading(self, row):
        return self.df.iat[row, self.cCol4ArmHeading]

    def getShot(self, row):
        return self.df.iat[row, self.cCol4Shot]

    def getBodyHeading(self, row):
        return self.df.iat[row, self.cCol4BodyHeading]

    def getBodyRoll(self, row):
        return self.df.iat[row, self.cCol4BodyRoll]

    def getBodyPitch(self, row):
        return self.df.iat[row, self.cCol4BodyPitch]

    def getHeadHeading(self, row):
        return self.df.iat[row, self.cCol4HeadHeading]

    def getHeadRoll(self, row):
        return self.df.iat[row, self.cCol4HeadRoll]

    def getHeadPitch(self, row):
        return self.df.iat[row, self.cCol4HeadPitch]

    def rowcount(self):
        return self.df['INDEX'].count()

    def columncount(self):
        return self.df.shape[1]

    def distanceFromLastPoint(self,row):
        d=0
        if row>0:
            xi = self.getX(row-1)
            xii = self.getX(row)
            yi = self.getY(row-1)
            yii = self.getY(row)
            sq1 = (xii-xi)*(xii-xi)
            sq2 = (yii-yi)*(yii-yi)
            d = math.sqrt(sq1 + sq2)
        return d

    # Distance function
    def distance2D(self,xii,xi,yii,yi):
        sq1 = (xi-xii)*(xi-xii)
        sq2 = (yi-yii)*(yi-yii)
        return math.sqrt(sq1 + sq2)

    def DistanceTraveled(self,user,startdate,finishdate):
        count=self.rowcount()
        d=0.0
        for i in range(count-1):
            if self.getID(i)==user:
                # print(self.getDate(i),startdate)
                # print("---")
                if self.getDate(i)>=startdate and self.getDate(i)<=finishdate:
                    #print(self.getINDEX(i))
                    x1 = self.getX(i)
                    y1 = self.getY(i)
                    x2 = self.getX(i+1)
                    y2 = self.getY(i+1)
                    d2 = self.distance2D(x1,x2,y1,y2)
                    d = d + self.distanceFromLastPoint(i+1)
            #print(d2,r.distanceFromLastPoint(i+1))
            #print(d2,r.getINDEX(i))
        return d

    def ShotCount(self,user):
        count=self.rowcount()
        d=0.0
        for i in range(count-1):
            if self.getID(i)==user:
                if self.getShot(i)!=0:
                    d=d+1
        return d
