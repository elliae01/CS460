from multiprocessing import Process, Manager
from multiprocessing.managers import *
import pandas as pd
from pandas import DataFrame
import cx_Oracle
import os
from Server.UserInformation import *

cCol4INDEX = 0
cCol4Date = 1
cCol4Id = 2
cCol4LocX = 3
cCol4LocY = 4
cCol4LocZ = 5
cCol4Hostility = 6
cCol4Hit = 7
cCol4HeartRate = 8
cCol4Emg0 = 9
cCol4Emg1 = 10
cCol4Emg2 = 11
cCol4Emg3 = 12
cCol4Emg4 = 13
cCol4Emg5 = 14
cCol4Emg6 = 15
cCol4Emg7 = 16
cCol4ArmRoll = 17
cCol4ArmPitch = 18
cCol4ArmHeading = 19
cCol4Shot = 20
cCol4BodyHeading = 21
cCol4BodyRoll = 22
cCol4BodyPitch = 23
cCol4HeadHeading = 24
cCol4HeadRoll = 25
cCol4HeadPitch = 26


print("Hello, Welcome to Reactionalytics-result of import in __INIT__.py")


class Reactionalytics:
    df=None

    def __init__(self,MyDataFrame):
        self.df = MyDataFrame
        print("Hello2, Welcome to Reactionalytics init")
        #return self


    def getX(self, df, row):
        return df.iat[row, cCol4LocX]


    def getY(self, df, row):
        return df.iat[row, cCol4LocY]



    print("Main Body of file Reactionalytics.py - Code Running Here")

