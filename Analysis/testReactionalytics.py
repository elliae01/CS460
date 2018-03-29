from multiprocessing import Process, Manager
from multiprocessing.managers import *
from Targalytics import *
from datetime import datetime
import pandas as pd

"""
Note that all expected results require the TestDB tables to be the only events in the Database. 
    Or you can limit your tests to the following Dates...
    2018-02-06 19:57:26.376000
    2018-03-17 16:08:34.975000
Find SQL insert statements in the "TestDB" folder.

--Mark Erickson
--3/19/2018
"""

if __name__ == '__main__':
    ip = 'localhost'
    port = 1521
    SID = 'orcl'
    UserName="SYSMAN"
    PassWord="System_Admin1"
    DatabaseInfo=[ip,port,SID,UserName,PassWord]

    #All in Database
    StartDate = pd.to_datetime(0)
    EndDate = datetime.now()

    # Create Event 1
    print("testEvent1...Created using Dates ",StartDate," through ",EndDate,"  --> Elasped Time=",(EndDate-StartDate))
    testEvent1=Targalytics(DatabaseInfo, StartDate, EndDate)
    testEvent1.ExportToCSV("Test DB Before Sort")
    testEvent1.sortByDate()
    testEvent1.ExportToCSV("Test DB After Sort")
    FirstTimeStamp=testEvent1.getDate(0)
    LastTimeStamp=testEvent1.getDate(testEvent1.rowCount()-1)
    TotalDistanceUser1=testEvent1.TotalDistanceTraveled(1)
    TotalCount=testEvent1.rowCount()
    print("First Event in Database occurred on ",FirstTimeStamp, "(Expected: 2018-02-06 19:57:26.376000 )")
    print("Last Event in Database occurred on ",LastTimeStamp,"(Expected: 2018-03-17 16:08:34.975000 )")
    print("Elapsed time = ",(LastTimeStamp-FirstTimeStamp), "(Expected: 38 days 20:11:08.599000 )")
    print("Total distance Traveled by user 1 = ", TotalDistanceUser1, "(Expected: 18955.3292083872 )")
    print("Total NUmber of Rows in DB = ",TotalCount, "(Expected: 2720 )")

    DistUptoRow30=testEvent1.getDistanceBeforeRowByUser(30, 1)
    DistUptoRow39=testEvent1.getDistanceBeforeRowByUser(39, 1)
    ShotsUptoRow30=testEvent1.getShotsBeforeRowByUser(30,1)
    ShotsUptoRow39=testEvent1.getShotsBeforeRowByUser(39,1)
    HitsUptoRow30 = testEvent1.getHitsBeforeRowByUser(30,1)
    HitsUptoRow39 = testEvent1.getHitsBeforeRowByUser(39,1)
    print("Distance traveled during playback up to row 30 = ", DistUptoRow30,
          "(Expected: 2.8284271247461903 -- H16)")
    print("Distance traveled during playback up to row 39 = ", DistUptoRow39,
          "(Expected: 144.2497833620557 -- H39)")
    totalShotCount=testEvent1.getTotalShotCountForUser(1)
    print("Total Shot count for user = ", totalShotCount)
    print("Shot count before row 30 = ", ShotsUptoRow30)
    print("Shot count before row 39 = ", ShotsUptoRow39)
    print("Hit count before row 30 = ", HitsUptoRow30)
    print("Hit count before row 39 = ", HitsUptoRow39)
    HitMissRatioUptoRow30=testEvent1.getHitMissRatioBeforeRowByUser(30,1)
    HitMissRatioUptoRow39=testEvent1.getHitMissRatioBeforeRowByUser(39,1)
    print("Hit/miss ratio before row 30 = ", HitMissRatioUptoRow30)
    print("Hit/miss ratio before row 39 = ", HitMissRatioUptoRow39)
    print("Max X",testEvent1.getMaxX())
    print("Min X",testEvent1.getMinX())
    print("Max Y",testEvent1.getMaxY())
    print("Min Y",testEvent1.getMinY())
    print("Total Number of actors in event = ", testEvent1.getTotalNumberOfActors())
    print("Total Number of Targets = ", testEvent1.getTotalNumberOfTargets())
    print("Total Number of Shooters = ", testEvent1.getTotalNumberOfShooters())

    # Test 2 - showing 2 lines in Database
    StartDate = pd.to_datetime('2018-02-09 15:53:36.070')
    EndDate = pd.to_datetime('2018-02-09 15:59:11.789')

    # EndDate = StartDate
    # StartDate = pd.to_datetime('2018-02-09 15:52:56.963')

    # Create Event 2
    print("------------------------------------------------------------")
    print("testEvent2...Created using Dates ",StartDate," through ",EndDate,"  --> Elasped Time=",(EndDate-StartDate))
    testEvent2=Targalytics(DatabaseInfo, StartDate, EndDate)
    testEvent2.ExportToCSV("Test2 DB Before Sort")
    testEvent2.sortByDate()
    testEvent2.ExportToCSV("Test2 DB After Sort")
    FirstTimeStamp=testEvent2.getDate(0)
    LastTimeStamp=testEvent2.getDate(testEvent2.rowCount()-1)
    TotalDistanceUser1=testEvent2.TotalDistanceTraveled(1)
    TotalCount=testEvent2.rowCount()
    print("First Event in Database occurred on ",FirstTimeStamp, "(Expected: 2018-02-09 15:53:36.070000 )")
    print("Last Event in Database occurred on ",LastTimeStamp,"(Expected: 2018-02-09 15:59:11.789000 )")
    print("Elapsed time = ",(LastTimeStamp-FirstTimeStamp), "(Expected: 0 days 00:05:35.719000 )")
    print("Total distance Traveled by user 1 = ", TotalDistanceUser1, "(Expected: 1.4142135623730951 )")
    print("Total NUmber of Rows in DB = ",TotalCount, "(Expected: 2 )")
    DistUptoRow30=testEvent2.getDistanceBeforeRowByUser(30,1)
    DistUptoRow39=testEvent2.getDistanceBeforeRowByUser(39, 1)
    DistUptoRow2=testEvent2.getDistanceBeforeRowByUser(2, 1)
    print("Distance traveled during playback up to row 30 = ", DistUptoRow30,
          "(Expected: -1 )")
    print("Distance traveled during playback up to row 39 = ", DistUptoRow39,
          "(Expected: -1 )")
    print("Distance traveled during playback up to row 2 = ", DistUptoRow2,
          "(Expected: 1.4142135623730951 -- G16)")
    totalShotCount=testEvent2.getTotalShotCountForUser(1)
    ShotsUptoRow30=testEvent2.getShotsBeforeRowByUser(30,1)
    ShotsUptoRow39=testEvent2.getShotsBeforeRowByUser(39,1)
    ShotsUptoRow2=testEvent2.getShotsBeforeRowByUser(2,1)
    print("Total Shot count for user = ", totalShotCount)
    print("Shot count before row 30 = ", ShotsUptoRow30)
    print("Shot count before row 39 = ", ShotsUptoRow39)
    print("Shot count before row 2 = ", ShotsUptoRow2)
    HitsUptoRow30 = testEvent2.getHitsBeforeRowByUser(30,1)
    HitsUptoRow39 = testEvent2.getHitsBeforeRowByUser(39,1)
    HitsUptoRow1 = testEvent2.getHitsBeforeRowByUser(1,1)
    HitsUptoRow2 = testEvent2.getHitsBeforeRowByUser(2,1)
    print("Hit count before row 30 = ", HitsUptoRow30)
    print("Hit count before row 39 = ", HitsUptoRow39)
    print("Hit count before row 1 = ", HitsUptoRow1)
    print("Hit count before row 2 = ", HitsUptoRow2)
    HitMissRatioUptoRow30=testEvent2.getHitMissRatioBeforeRowByUser(30,1)
    HitMissRatioUptoRow39=testEvent2.getHitMissRatioBeforeRowByUser(39,1)
    HitMissRatioUptoRow2=testEvent2.getHitMissRatioBeforeRowByUser(2,1)
    print("Hit/miss ratio before row 30 = ", HitMissRatioUptoRow30)
    print("Hit/miss ratio before row 39 = ", HitMissRatioUptoRow39)
    print("Hit/miss ratio before row 2 = ", HitMissRatioUptoRow2)
    print("Max X",testEvent2.getMaxX())
    print("Min X",testEvent2.getMinX())
    print("Max Y",testEvent2.getMaxY())
    print("Min Y",testEvent2.getMinY())
    print("Total Number of actors in event = ", testEvent2.getTotalNumberOfActors())
    print("Total Number of Targets = ", testEvent2.getTotalNumberOfTargets())
    print("Total Number of Shooters = ", testEvent2.getTotalNumberOfShooters())

    # Test 3 - showing 2 lines in Database
    StartDate = pd.to_datetime('2018-03-17 16:07:00.000')
    EndDate = pd.to_datetime('2018-03-17 16:59:12.000')

    # Create Event 3
    print("------------------------------------------------------------")
    print("testEvent3...Created using Dates ",StartDate," through ",EndDate,"  --> Elasped Time=",(EndDate-StartDate))
    testEvent3=Targalytics(DatabaseInfo, StartDate, EndDate)
    print("Total Number of actors in event = ", testEvent3.getTotalNumberOfActors())
    print("Total Number of Targets = ", testEvent3.getTotalNumberOfTargets())
    print("Total Number of Shooters = ", testEvent3.getTotalNumberOfShooters())
    print(testEvent3.getAvgReactionTimeBeforeRowByUser(191,1))

