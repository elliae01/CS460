from multiprocessing import Process, Manager
from multiprocessing.managers import *
import pandas as pd
from pandas import DataFrame
import cx_Oracle
import os
from Server.UserInformation import *

def SetStructure(df,MyIndex):
    dataStruct.setId(df.loc[MyIndex, 'S_SHOOTER.ID'])
    dataStruct.setRoll(df.loc[MyIndex, 'S_SHOOTER.ARM.ROLL'])
    dataStruct.setEMG(df.loc[MyIndex, 'S_SHOOTER.ARM.EMG'])
    dataStruct.setPitch(df.loc[MyIndex, 'S_SHOOTER.ARM.PITCH'])
    #dataStruct.setYaw(df.loc[MyIndex, 'S_SHOOTER.ARM.YAW'])
    dataStruct.setShot(df.loc[MyIndex, 'S_SHOOTER.SHOT'])
    dataStruct.setHeadXAxis(df.loc[MyIndex, 'S_SHOOTER.HEAD.ROLL'])
    dataStruct.setHeadYAxis(df.loc[MyIndex, 'S_SHOOTER.HEAD.PITCH'])
    #dataStruct.setHeadZAxis(df.loc[MyIndex, 'S_SHOOTER.HEAD.YAW'])
    dataStruct.setHeadHeading(df.loc[MyIndex, 'S_SHOOTER.HEAD.HEADING'])
    #dataStruct.setHeadDegrees(df.loc[MyIndex, 'S_SHOOTER.HEAD.DEGREES'])
    dataStruct.setBodyXAxis(df.loc[MyIndex, 'S_SHOOTER.BODY.ROLL'])
    dataStruct.setBodyYAxis(df.loc[MyIndex, 'S_SHOOTER.BODY.PITCH'])
    #dataStruct.setBodyZAxis(df.loc[MyIndex, 'S_SHOOTER.BODY.YAW'])
    dataStruct.setBodyHeading(df.loc[MyIndex, 'S_SHOOTER.BODY.HEADING'])
    #dataStruct.setBodyDegrees(df.loc[MyIndex, 'S_SHOOTER.BODY.DEGREES'])
    dataStruct.setLocationXAxis(df.loc[MyIndex, 'S_SHOOTER.LOC.X'])
    dataStruct.setLocationYAxis(df.loc[MyIndex, 'S_SHOOTER.LOC.Y'])
    dataStruct.setLocationZAxis(df.loc[MyIndex, 'S_SHOOTER.LOC.Z'])
    dataStruct.setHeartRate(df.loc[MyIndex, 'S_SHOOTER.HR'])
    #dataStruct.setVisible(df.loc[MyIndex, 'S_SHOOTER.VISIBLE'])
    dataStruct.setHostile(df.loc[MyIndex, 'S_SHOOTER.HOSTILITY'])
    dataStruct.setHit(df.loc[MyIndex, 'S_SHOOTER.HIT'])


dataStruct = UserInformation("01")
dataStruct.setHeadDegrees(3)
print("before")
print(dataStruct.getHeadDegrees())
print("After")
dir_path = os.path.dirname(os.path.realpath("__file__"))
print (dir_path)
dir_path = dir_path + "\Targamite.csv"
#dir_path = dir_path + "\Yahoo.csv"
print (dir_path)
df = pd.read_csv(dir_path, index_col="S_INDEX")   # index_col="Date", parse_dates=True\
SetStructure(df,43)
#df.sort_values('S_DATE', inplace=True)




# x=df.loc[1,'S_DATE']
# S_SHOOTER_ID=df.loc[1,'S_SHOOTER.ID']
# S_SHOOTER_ARM_EMG=df.loc[1,'S_SHOOTER.ARM.EMG']
print (df.head())
# print (x+" "+str(S_SHOOTER_ID)+" "+str(S_SHOOTER_ARM_EMG))
MyIndex=2
print (dataStruct.getLocationZAxis())
print (dataStruct.getEMG())
# dataStruct.setEMG([Structure[2][0], Structure[2][1], Structure[2][2], Structure[2][3], Structure[2][4], Structure[2][5],
#                    Structure[2][6], Structure[2][7]])

#df.to_csv("MyOutput.csv")

# ip = 'localhost'
# port = 1521
# SID = 'orcl'
# dsn_tns = cx_Oracle.makedsn(ip, port, SID)
# print(dsn_tns)
#
# conn_str = u'SYSMAN/System_Admin1@localhost:1521/orcl'
# database = cx_Oracle.connect('SYSMAN', 'System_Admin1', dsn_tns)
# cursor = database.cursor()
#
# #connection = cx_Oracle.connect(conn_str)
# #df.to_sql("Shooter_Table","orcl" )
#
# sSQLCMD = 'Select s.S_INDEX,s.S_DATE,s.S_SHOOTER.Id,s.S_SHOOTER.Loc.x,s.S_SHOOTER.Loc.y,s.S_SHOOTER.Loc.z,'
# sSQLCMD = sSQLCMD +'s.S_SHOOTER.hostility,s.S_SHOOTER.hit,s.S_SHOOTER.hr,s.S_SHOOTER.arm.emg,s.S_SHOOTER.arm.roll,' \
#                    's.S_SHOOTER.arm.pitch,s.S_SHOOTER.arm.heading,s.S_SHOOTER.shot,s.S_SHOOTER.body.heading,' \
#                    's.S_SHOOTER.body.roll,s.S_SHOOTER.body.pitch,s.S_SHOOTER.head.heading,s.S_SHOOTER.head.roll,' \
#                    's.S_SHOOTER.head.pitch FROM Shooter_Table s'
# print(sSQLCMD)
# df_ora = pd.read_sql(sSQLCMD, database)
# print(df_ora.first_valid_index)
# database.close