from multiprocessing import Process, Manager
from multiprocessing.managers import *
from datetime import datetime
import pandas as pd
from Reactionalytics import *

def __init_():
    print("hello from Analysis init")


if __name__ == '__main__':
    ip = 'localhost'
    port = 1521
    SID = 'orcl'
    UserName="SYSMAN"
    PassWord="System_Admin1"
    DatabaseInfo=[ip,port,SID,UserName,PassWord]

    # 2 lines in Database
    StartDate = pd.to_datetime("2018-02-09 15:53:26.376000")
    EndDate = pd.to_datetime('2018-02-09 15:59:11.8000000')

    #All of Database
    StartDate = pd.to_datetime(0)
    EndDate = datetime.now()
    r=Reactionalytics(DatabaseInfo, StartDate, EndDate)

    r.sortByDate()
    r.ExportToCSV("DataAfterSortDate")
    #r.printDF()
    # 2 lines in Database
    StartDate = pd.to_datetime("2018-02-09 15:53:26.376000")
    EndDate = pd.to_datetime('2018-02-09 15:59:11.8000000')
    print("Before subset")
    # r2=r.getSubSet(StartDate, EndDate)
    r2=r
    r.printHeadDF()
    print("After subset- r2=",r2.rowcount())
    print("After subset - r=",r.rowcount())
    print("Emg=",r.getEmgArray(0))
    # df2=r.getRawDF()
    # print(df2)
    d=r2.DistanceTraveled(1,StartDate,EndDate)
    print("Total Distance r = ", d)

    d=r2.DistanceTraveled(1,StartDate,EndDate)
    print("Total Distance r2 = ", d)

    FirstTimeStamp=r.getDate(0)
    print("Data from time index ",FirstTimeStamp)
    print(r.DistanceTraveled(1,FirstTimeStamp,datetime.now()))
    print("Total Shot count = ",r.getTotalShotCountForUser(1))
    print("Shot count in the sub set = ",r2.getTotalShotCountForUser(1))
    r3=Reactionalytics(DatabaseInfo, StartDate, EndDate)
    #r3.printDF()
    d=r3.DistanceTraveled(1,StartDate,EndDate)
    print("Total Distance r3 = ", d)
