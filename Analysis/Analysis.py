from multiprocessing import Process, Manager
from multiprocessing.managers import *
from datetime import datetime
import pandas as pd
from pandas import DataFrame
import cx_Oracle
import os
import math
from Server.UserInformation import *
from Reactionalytics import *

def __init_():
    print("hello from Analysis init")

#getDataFrame from Database
def getDataFrame():
    ip = 'localhost'
    port = 1521
    SID = 'orcl'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    #print(dsn_tns)
    conn_str = u'SYSMAN/System_Admin1@localhost:1521/orcl'
    database = cx_Oracle.connect('SYSMAN', 'System_Admin1', dsn_tns)
    cursor = database.cursor()

    sSQLCMD = 'Select s.S_INDEX,s.S_DATE,s.S_SHOOTER.Id,s.S_SHOOTER.Loc.x,s.S_SHOOTER.Loc.y,s.S_SHOOTER.Loc.z,'
    sSQLCMD = sSQLCMD +'s.S_SHOOTER.hostility,s.S_SHOOTER.hit,s.S_SHOOTER.hr,s.S_SHOOTER.arm.emg.emg0,' \
                       's.S_SHOOTER.arm.emg.emg1,s.S_SHOOTER.arm.emg.emg2,' \
                       's.S_SHOOTER.arm.emg.emg3,s.S_SHOOTER.arm.emg.emg4,s.S_SHOOTER.arm.emg.emg5,' \
                       's.S_SHOOTER.arm.emg.emg6,s.S_SHOOTER.arm.emg.emg7,s.S_SHOOTER.arm.roll,' \
                       's.S_SHOOTER.arm.pitch,s.S_SHOOTER.arm.heading,s.S_SHOOTER.shot,s.S_SHOOTER.body.heading,' \
                       's.S_SHOOTER.body.roll,s.S_SHOOTER.body.pitch,s.S_SHOOTER.head.heading,s.S_SHOOTER.head.roll,' \
                       's.S_SHOOTER.head.pitch FROM Shooter_Table s'
    cursor.execute(sSQLCMD)
    df = DataFrame(cursor.fetchall())
    df.rename(columns={0:"INDEX", 1: "Date", 2: "Id", 3: "Loc.x", 4: "Loc.y", 5: "Loc.z", 6: "Hostility", 7: "Hit", 8: "Heart Rate", 9: "Emg0", 10: "Emg1", 11: "Emg2", 12: "Emg3", 13: "Emg4",14: "Emg5",15: "Emg6",16: "Emg7",17: "Arm.Roll",18: "Arm.Pitch",19: "Arm.Heading",20: "Shot",21: "Hody.Heading", 22: "Body.Roll", 23: "Body.Pitch",24: "Head.Heading",25: "Head.Roll", 26: "Head.Pitch"}, inplace=True)
    database.close
    return df

def pExportToCSV(df,sFileName):
    dir_path = os.path.dirname(os.path.realpath("__file__"))
    #print (dir_path)
    dir_path = dir_path+"\\"+sFileName+".csv"
    #print(df.head())
    try:
        df.to_csv(dir_path)
        print("Saved " + sFileName)
    except:
        print("Could not save " + sFileName)
        pass
    return 0

# Distance function
def distance2D(xii,xi,yii,yi):
    sq1 = (xi-xii)*(xi-xii)
    sq2 = (yi-yii)*(yi-yii)
    return math.sqrt(sq1 + sq2)

def DistanceTraveled(df,user,startdate,finishdate):
    count=df.rowcount()
    d=0.0
    for i in range(count-1):
        if df.getID(i)==user:
            # print(df.getDate(i),startdate)
            # print("---")
            if df.getDate(i)>=startdate and df.getDate(i)<=finishdate:
                print(df.getINDEX(i))
                x1 = df.getX(i)
                y1 = df.getY(i)
                x2 = df.getX(i+1)
                y2 = df.getY(i+1)
                d2 = distance2D(x1,x2,y1,y2)
                d = d + d2
        #print(d2,r.distanceFromLastPoint(i+1))
        #print(d2,r.getINDEX(i))
    return d

if __name__ == '__main__':
    df=getDataFrame()
    #print(df.head())
    pExportToCSV(df,"DataBeforeSort")
    dfSortedByIndex=df.sort_values('INDEX', ascending=True)
    pExportToCSV(dfSortedByIndex,"DataAfterSort")
    dfSortedByDate=df.sort_values('Date', ascending=True)
    pExportToCSV(dfSortedByIndex,"DataAfterSortDate")

    r=Reactionalytics(dfSortedByDate)

    StartDate = pd.to_datetime("2018-02-09 15:53:26.376000")
    EndDate = pd.to_datetime('2018-02-09 15:59:11.8000000')
    print(dfSortedByDate['Date'])
    print('End of print and start of new df')
    dfCurrentEvent = (dfSortedByDate['Date']>=StartDate)&(dfSortedByDate['Date']<=EndDate)
    r2=Reactionalytics(dfSortedByDate[dfCurrentEvent])
    print(dfSortedByDate[dfCurrentEvent])
    d=DistanceTraveled(r,1,StartDate,EndDate)
    print("Total Distance = ", d)
    d=DistanceTraveled(r2,1,StartDate,EndDate)
    print("Total Distance = ", d)
