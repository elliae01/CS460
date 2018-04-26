from pandas import DataFrame, Timedelta
import cx_Oracle
import os
import math
import numpy as np
from Server.UserInformation import *

print("Hello, Welcome to Targalytics.py")

class Targalytics:
    df = None
    dfReaction = None
    aTargetVisibleTimes={}       #self.aTargetVisibleTimes.update({9999:'end'})  to add more dict items
    dfNoteworthyEvents=None
    aReactionTimes=[]            #use append to add more array items
    HitCount = 0
    ShotCount = 0
    Miss = 0

    def __init__(self, DatabaseInfo, StartDate, EndDate):
        self.classStartDate=StartDate
        self.classEndDate=EndDate
        self.cDB_IPPos=0
        self.cDB_portPos=1
        self.cDB_SIDPos=2
        self.cDB_UserPos=3
        self.cDB_PWPos=4
        self.cCol4INDEX = 0
        self.cCol4Date = 1
        self.cCol4Id = 2
        self.cCol4LocX = 3
        self.cCol4LocY = 4
        self.cCol4LocZ = 5
        self.cCol4TargetVisible = 6
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

        dsn_tns = cx_Oracle.makedsn(DatabaseInfo[self.cDB_IPPos], DatabaseInfo[self.cDB_portPos], DatabaseInfo[self.cDB_SIDPos])
        print(dsn_tns)
        # conn_str = u'SYSMAN/System_Admin1@localhost:1521/orcl'

        database = cx_Oracle.connect(DatabaseInfo[self.cDB_UserPos], DatabaseInfo[self.cDB_PWPos], dsn_tns)
        cursor = database.cursor()

        sSQLCMD = '(Select s.S_INDEX,s.S_DATE as time, s.S_SHOOTER.Id,s.S_SHOOTER.Loc.x,s.S_SHOOTER.Loc.y,s.S_SHOOTER.Loc.z,'
        sSQLCMD = sSQLCMD + 's.S_SHOOTER.hostility,s.S_SHOOTER.hit,s.S_SHOOTER.hr,s.S_SHOOTER.arm.emg.emg0,' \
                            's.S_SHOOTER.arm.emg.emg1,s.S_SHOOTER.arm.emg.emg2,' \
                            's.S_SHOOTER.arm.emg.emg3,s.S_SHOOTER.arm.emg.emg4,s.S_SHOOTER.arm.emg.emg5,' \
                            's.S_SHOOTER.arm.emg.emg6,s.S_SHOOTER.arm.emg.emg7,s.S_SHOOTER.arm.roll,' \
                            's.S_SHOOTER.arm.pitch,s.S_SHOOTER.arm.heading,s.S_SHOOTER.shot,s.S_SHOOTER.body.heading,' \
                            's.S_SHOOTER.body.roll,s.S_SHOOTER.body.pitch,s.S_SHOOTER.head.heading,s.S_SHOOTER.head.roll,' \
                            's.S_SHOOTER.head.pitch ' \
                            'FROM Shooter_Table s )' \
                            'UNION ALL' \
                            '(SELECT t.T_INDEX, t.T_DATE AS time, t.T_TARGET.ID AS id, t.T_TARGET.Loc.x AS x, t.T_TARGET.Loc.y AS y, ' \
                            't.T_TARGET.Loc.Z AS z, ' \
                            't.T_TARGET.visible AS visible, t.T_TARGET.hit AS hit, NULL AS Hostility, ' \
                            'NULL AS emg0, NULL AS emg1, NULL AS emg2, NULL AS emg3, NULL AS emg4, NULL AS emg5, NULL AS emg6, NULL AS emg7, ' \
                            'NULL AS ARM_ROLL, NULL AS ARM_PITCH, NULL AS ARM_Heading, ' \
                            'NULL AS Body_ROLL, NULL AS Body_PITCH, NULL AS Body_Heading, ' \
                            'NULL AS Head_ROLL, NULL AS Head_PITCH, NULL AS Head_Heading, ' \
                            'NULL AS HR ' \
                            'FROM Target_Table t) ORDER BY time'
                            # 'WHERE s.S_DATE > ''17-MAR-18 04.00.00.00'' AND s.S_DATE < ''01-MAR-18 04.00.00.00'' '
        # 'WHERE s.S_DATE > ' + str(StartDate) + ' AND s.S_DATE < ' + str(EndDate) + ''
        # print(sSQLCMD)
        cursor.execute(sSQLCMD)
        self.df = DataFrame(cursor.fetchall())
        self.df.rename(columns={0: "INDEX", 1: "Date", 2: "Id", 3: "Loc.x", 4: "Loc.y", 5: "Loc.z", 6: "Hostility",
                7: "Hit", 8: "Heart Rate", 9: "Emg0", 10: "Emg1", 11: "Emg2", 12: "Emg3", 13: "Emg4", 14: "Emg5",
                15: "Emg6", 16: "Emg7", 17: "Arm.Roll", 18: "Arm.Pitch", 19: "Arm.Heading", 20: "Shot",
                21: "Body.Heading", 22: "Body.Roll", 23: "Body.Pitch", 24: "Head.Heading", 25: "Head.Roll",
                26: "Head.Pitch"}, inplace=True)
        dfCurrentEvent = (self.df['Date'] >= StartDate) & (self.df['Date'] <= EndDate)
        self.df=self.df[dfCurrentEvent]
        database.close
        # return None	# Commented...seems to have no use!

    @classmethod
    def NewFromDF(self,df2):
        self.cCol4INDEX = 0
        self.cCol4Date = 1
        self.cCol4Id = 2
        self.cCol4LocX = 3
        self.cCol4LocY = 4
        self.cCol4LocZ = 5
        self.cCol4TargetVisible = 6
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

        self.df = df2
        return None

    def getSubSet(self, StartDate, EndDate):
        if StartDate<self.classStartDate:
            StartDate=self.classStartDate
        if EndDate>self.classEndDate:
            EndDate=self.classEndDate
        dfCurrentEvent = (self.df['Date'] >= StartDate) & (self.df['Date'] <= EndDate)
        #self.__class__.NewFromDF(self.df[dfCurrentEvent])
        # print(MyDataFrame)
        return self.__class__.NewFromDF(self.df[dfCurrentEvent])

    def printDF(self):
        print(self.df)
        return None

    def printHeadDF(self):
        print(self.df.head())
        return None

    def isBadDateSelection(self):
        if(math.isnan(self.df['Loc.x'].max())):
            # Location column for this date has a problem
            return True
        else:
            return False

    def getRawDF(self):
        return self.df

    def getDate(self, row):
        return self.df.iat[row, self.cCol4Date]

    def getINDEX(self, row):
        #flaw until target and shooter get same index sequence  -- i.e there could be 2 indentical indices in the df
        return self.df.iat[row, self.cCol4INDEX]


    def getID(self, row):
        return self.df.iat[row, self.cCol4Id]

    def getX(self, row):
        #print("Calculating X for index "+str(self.df.iat[row, self.cCol4INDEX]))
        return (self.df.iat[row, self.cCol4LocX]) * (-1)

    def getY(self, row):
        return self.df.iat[row, self.cCol4LocY]

    def getZ(self, row):
        return self.df.iat[row, self.cCol4LocZ]

    def getHostility(self, row):
        return self.df.iat[row, self.cCol4Hostility]

    def getTargetVisible(self, row):
        return self.df.iat[row, self.cCol4TargetVisible]


    def getHit(self, row):
        return self.df.iat[row, self.cCol4Hit]

    def getHeartRate(self, row):
        return self.df.iat[row, self.cCol4HeartRate]

    def getEmgArray(self, row):
        a=[self.df.iat[row,self.cCol4Emg0],
            self.df.iat[row,self.cCol4Emg1],
            self.df.iat[row,self.cCol4Emg2],
            self.df.iat[row,self.cCol4Emg3],
            self.df.iat[row,self.cCol4Emg4],
            self.df.iat[row,self.cCol4Emg5],
            self.df.iat[row,self.cCol4Emg6],
            self.df.iat[row,self.cCol4Emg7]]
        return a

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

    def getArmArray(self, row):
        a=[self.df.iat[row,self.cCol4ArmRoll],
            self.df.iat[row,self.cCol4ArmPitch],
            self.df.iat[row,self.cCol4ArmHeading]]
        return a

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

    def getLength(self):
        # size or number of rows
        return self.df['INDEX'].count()

    def rowCount(self):
        #size or length
        return self.df['INDEX'].count()

    def columnCount(self):
        return self.df.shape[1]

    def distanceFromLastPoint(self,row):
        CurrentUser=self.getID(row)
        RolledBackRow=row-1
        d=0
        if CurrentUser > 100:
            return 0
        if row>0 and CurrentUser<100:
            CheckUser = self.getID(RolledBackRow)
            if CheckUser!=CurrentUser:
                while (RolledBackRow>=0 and CheckUser!=CurrentUser):
                    # print(row, RolledBackRow,CurrentUser, CheckUser, "rolling back")
                    RolledBackRow=RolledBackRow-1
                    CheckUser=self.getID(RolledBackRow)
                if RolledBackRow<0 or CheckUser!=CurrentUser:
                    return 0
            xi = self.getX(RolledBackRow)
            xii = self.getX(row)
            yi = self.getY(RolledBackRow)
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

    def TotalDistanceTraveled(self,user):
        d=self.DistanceTraveled(user,self.classStartDate,self.classEndDate)
        return d

    def DistanceTraveled(self,user,startdate,finishdate):
        NotFirst=False
        count=self.rowCount()
        diff=finishdate-startdate
        d=0.0
        for i in range(count):
            if self.getID(i)==user:
                if (self.getDate(i)>=startdate) and (self.getDate(i)<=finishdate):
                    if NotFirst:
                        x1 = self.getX(i-1)
                        y1 = self.getY(i-1)
                        x2 = self.getX(i)
                        y2 = self.getY(i)
                        d2 = self.distance2D(x1,x2,y1,y2)
                        d = d + self.distanceFromLastPoint(i)
                    NotFirst=True
            #print(d2,r.distanceFromLastPoint(i+1))
            #print(d2,r.getINDEX(i))
        return d

    def getTotalShotCountForUser(self,user):
        count=self.rowCount()
        d=0.0
        for i in range(count-1):
            if self.getID(i)==user:
                if self.getShot(i)!=0:
                    d=d+1
        return d

    def getShotsBeforeRowByUser(self, row, user):
        count=self.rowCount()
        d=-1.0     # -1 reports a failure
        if row<=count:
            d = 0
            for i in range(row):
                if self.getID(i)==user:
                    if self.getShot(i)!=0:
                        d=d+1
        if d<0:
            print("Error ", d, " in getShotsBeforeRowByUser: Row = ", row, " Count = ", count)
        return d

    def getHitsBeforeRowByUser(self, row, user):
        count=self.rowCount()
        d=-1.0     # -1 reports a failure
        if row<=count:
            d = 0
            for i in range(row):
                if self.getID(i)==user:
                    if self.getHit(i)!=0:
                        d=d+1
        if d<0:
            print("Error ", d, " in getShotsBeforeRowByUser: Row = ", row, " Count = ", count)
        return d

    def getHitMissRatioBeforeRowByUser(self, row, user):
        count=self.rowCount()
        if row > count:
            print("Error ", -1 , " in getHitMissRatioBeforeRowByUser: Row = ", row, " Count = ", count)
            return -1
        hits=self.getHitsBeforeRowByUser(row,user)
        miss=self.getShotsBeforeRowByUser(row,user)
        if miss==0:
            if hits>0:
                return 1
            return 0
        return hits/miss

    def getDistanceBeforeRowByUser(self, row, user):
        NotFirst=False
        count=self.rowCount()
        d=-1.0     # -1 reports a failure
        if row<=count:
            d = 0
            for i in range(row):
                if self.getID(i)==user:
                    #print(self.getINDEX(i),self.getX(i),self.getY(i))
                    if NotFirst:
                        x1 = self.getX(i-1)
                        y1 = self.getY(i-1)
                        x2 = self.getX(i)
                        y2 = self.getY(i)
                        d2 = self.distance2D(x1,x2,y1,y2)
                        d = d + self.distanceFromLastPoint(i)
                    NotFirst=True
        if d<0:
            print("Error ", d, " in getDistanceBeforeRowByUser: Row = ", row, " Count = ", count)
        return d

    def sortByDate(self):
        self.df = self.df.sort_values('Date', ascending=True)

    def sortByIndex(self):
        self.df = self.df.sort_values('INDEX', ascending=True)

    def getTotalNumberOfActors(self):
        return self.df['Id'].nunique()

    def getTotalNumberOfShooters(self):
        dfCurrentEvent = (self.df['Id'] < 100)
        df=self.df[dfCurrentEvent]
        return df['Id'].nunique()

    def getTotalNumberOfTargets(self):
        dfCurrentEvent = (self.df['Id'] > 100)
        df=self.df[dfCurrentEvent]
        return df['Id'].nunique()

    def ExportToCSV(self,sFileName):
        dir_path = os.path.dirname(os.path.realpath("__file__"))
        dir_path = dir_path+"\\"+sFileName+".csv"
        #print (dir_path)
        #print(df.head())
        try:
            self.df.to_csv(dir_path)
            print("Saved " + dir_path)
        except:
            print("Could not save " + sFileName)
            pass
        return 0

    def getMaxX(self):
        if(self.df.empty):
            print("WARNING [getMaxX]: Dataframe empty!")
            return 10
        else:
            return (self.df['Loc.x'].min()) * (-1)

    def getMaxY(self):
        if(self.df.empty):
            print("WARNING [getMaxY]: Dataframe empty!")
            return 10
        else:
            return self.df['Loc.y'].max()

    def getMinX(self):
        if(self.df.empty):
            print("WARNING [getMinX]: Dataframe empty!")
            return -10
        else:
            return (self.df['Loc.x'].max()) * (-1)

    def getMinY(self):
        if(self.df.empty):
            print("WARNING [getMinY]: Dataframe empty!")
            return -10
        else:
            return self.df['Loc.y'].min()

    def getTargetLocationByID(self,user):
        dfCurrentEvent = (self.df['Id'] == user)
        df=self.df[dfCurrentEvent]
        x=df.iat[0, self.cCol4LocX]
        y=df.iat[0, self.cCol4LocY]
        # print(df.iat[0, self.cCol4LocX],df.iat[0, self.cCol4LocY])
        return x,y

    def getReactionTimeBeforeRowByUser(self, row, user):
        count=self.rowCount()
        dfCurrentEvent = (self.df['Id'] == user)
        df=self.df[dfCurrentEvent]
        x=df.iat[0, self.cCol4LocX]
        y=df.iat[0, self.cCol4LocY]

        return -1

    # Returns a list of lists, each session separated by sessionGapMinutes. Uses Pandas Timedelta.
    def getSessions(self, sessionGapMinutes):
        # List to return results
        result = []
        # Start at index 1 so that prevDateTime gets index 0 date
        index = 1
        # Init start date for first saved start date
        savedStart = self.getDate(0)
        # There are different time libraries being used, uncomment below to see
        # print(type(savedStart))
        while(index < self.rowCount()):
            prevDateTime = self.getDate(index - 1)
            currDateTime = self.getDate(index)

            # If the current time and previous time have a gap of more than the "sessionGapMinutes",
            # we need to append the session to the list of other sessions
            if((currDateTime - prevDateTime) > Timedelta(sessionGapMinutes,unit="m")):
                # start datetime, end datetime, distance
                result.append([str(savedStart), str(prevDateTime), str(round(self.DistanceTraveled(1, savedStart, prevDateTime)))])

                # save current time as the start, for the next session
                savedStart = currDateTime
            index += 1
        return result

    def getAvgReactionTimeBeforeRowByUser(self, row, user):

        aEvent=[]

        # b.append("a")
        # b.append("2")
        # print(b)
        # print("length=",len(b), "one=",b[0],b[1])

        return -1

        count=self.rowCount()
        d=-1.0     # -1 reports a failure
        if row<=count:
            d = 0
            for i in range(row):
                if self.getID(i)==user:
                    #print(self.getINDEX(i),self.getX(i),self.getY(i))
                    x1 = self.getX(i-1)
                    y1 = self.getY(i-1)
                    x2 = self.getX(i)
                    y2 = self.getY(i)
                    d2 = self.distance2D(x1,x2,y1,y2)
                    d = d + self.distanceFromLastPoint(i)
        if d<0:
            print("Error ", d, " in getAvgReactionTimeBeforeRowByUser: Row = ", row, " Count = ", count)
        return d

    def totalTargetVisibleCount(self):
        dfCurrentEvent = (self.df['Id'] > 100) & (self.df['Hostility'] > 0)
        df2=self.df[dfCurrentEvent]
        return df2['Id'].count()

    def TargetVisibleEventTimes(self):
        aEvents=[]
        dfCurrentEvent = (self.df['Id'] > 100) & (self.df['Hostility'] > 0)
        df2=self.df[dfCurrentEvent]
        self.aTargetVisibleTimes=(df2['Date'].to_dict())    # =  {2576: Timestamp('2018-03-17 16:08:05.755000'), 2625: Timestamp('2018-03-17 16:08:15.762000'), 2699: Timestamp('2018-03-17 16:08:30.764000')}
        #self.aTargetVisibleTimes.update({9999:'end'})      # =  {2576: Timestamp('2018-03-17 16:08:05.755000'), 2625: Timestamp('2018-03-17 16:08:15.762000'), 2699: Timestamp('2018-03-17 16:08:30.764000'), 9999: 'end'}
        #print("internal = ",self.aTargetVisibleTimes)      # This output is shown above ^
        for item in df2['Date']:
            aEvents.append(item)                            # Array[1] =  2018-03-17 16:08:15.762000
        return aEvents                                      #=  [Timestamp('2018-03-17 16:08:05.755000'), Timestamp('2018-03-17 16:08:15.762000'), Timestamp('2018-03-17 16:08:30.764000')]

    def getReactionEvents(self):
        #list all the times associated with an event that is required to calculate response time or hit/miss
        dfCurrentEvent = (self.df['Id'] > 100) ^ ( (self.df['Id'] <= 100) & (self.df['Shot'] > 0))
        self.dfNoteworthyEvents=self.df[dfCurrentEvent]
        try:
            self.dfNoteworthyEvents.to_csv("ReactionTimes.csv")
            print("Saved ReactionTimes.csv")
        except:
            print("Could not save ReactionTimes.csv")
            pass

        #        self.aTargetVisibleTimes.append(df2['Date'].to_string(index=False))           #self.df.iat[row, self.cCol4LocX]
        # self.dfNoteworthyEvents=(df2['Date'].to_dict())    # =  {2576: Timestamp('2018-03-17 16:08:05.755000'), 2625: Timestamp('2018-03-17 16:08:15.762000'), 2699: Timestamp('2018-03-17 16:08:30.764000')}
        # self.dfNoteworthyEvents.update({9999:'end'})       # =  {2576: Timestamp('2018-03-17 16:08:05.755000'), 2625: Timestamp('2018-03-17 16:08:15.762000'), 2699: Timestamp('2018-03-17 16:08:30.764000'), 9999: 'end'}
        #print("internal = ",self.dfNoteworthyEvents)      # This output is shown above ^
        return self.dfNoteworthyEvents

    def listReactionTimes(self,user):
        if self.dfNoteworthyEvents is None:
            dfReactionEvents=self.getReactionEvents()
        keys=[]
        self.aReactionTimes.clear()
        for key in self.dfNoteworthyEvents:
            keys.append(key)
        # print(keys, "array of length ",len(keys))
        count=self.dfNoteworthyEvents[keys[self.cCol4Hit]].count()
        i=0
        Visible=0
        TargetVisibleTime=0
        ShotTime=0
        ReactionSum=0
        while (i <= count-1):
            # print("------------i of count : ",i,"/",count)
            TimeOfAction=self.dfNoteworthyEvents.iat[i,self.cCol4Date]
            UserID=self.dfNoteworthyEvents.iat[i,self.cCol4Id]
            Visible = self.dfNoteworthyEvents.iat[i, self.cCol4Hostility]
            Hit = self.dfNoteworthyEvents.iat[i, self.cCol4Hit]
            Shot = self.dfNoteworthyEvents.iat[i, self.cCol4Shot]
            # print("Time=", TimeOfAction)
            # print("UserID=", UserID)
            # print("Visible=", Visible)
            # print("Hit=", Hit)
            # print("Shot=", Shot)
            if Visible:
                TargetVisibleTime=TimeOfAction
            if Shot==1:
                ShotTime=TimeOfAction
                self.ShotCount=self.ShotCount+1
            if Hit:
                TargetHitTime=TimeOfAction
                self.HitCount=self.HitCount+1
                ReactionTime=TargetHitTime-TargetVisibleTime
                print(ReactionTime._s)
                ReactionSum=ReactionSum+(ReactionTime.delta)
                self.aReactionTimes.append(ReactionTime)
            i=i+1
            self.Miss=self.ShotCount-self.HitCount
        AveReactionTime=(ReactionSum/len(self.aReactionTimes))/1000000000.0
        print(self.aReactionTimes)
        # print("Number of Shots = ", self.ShotCount, ", Hits=", self.HitCount, ", Misses=", self.Miss)
        HitMissRatio=0
        if (self.Miss+self.HitCount)>0:
            HitMissRatio=self.HitCount/(self.Miss+self.HitCount)
            # print("Hit/Miss Ratio=",HitMissRatio)
        # print("Length of list=",len(self.aReactionTimes))
        # print("Average Reaction Time=",AveReactionTime, " seconds.")
        # print("Average Reaction Time=",AveReactionTime, " seconds.")
        score =0
        if AveReactionTime>0:
            score = HitMissRatio*(1000/AveReactionTime)
        return AveReactionTime, self.HitCount, self.Miss, HitMissRatio, self.ShotCount, score

    def listReactionTimesUpToRow(self, row, user):
        ShotCount=0
        HitCount=0
        Miss=0
        if self.dfNoteworthyEvents is None:
            dfReactionEvents=self.getReactionEvents()
        keys=[]
        self.aReactionTimes.clear()
        for key in self.dfNoteworthyEvents:
            keys.append(key)
        # print(keys, "array of length ",len(keys))
        row=np.int32(row)
        count=self.dfNoteworthyEvents[keys[self.cCol4Hit]].count()
        count=self.df['INDEX'].count()
        if count < row:
            print("Error: row > data count (Not enough data or view past end of data) Max=",count)
            return -1
        count=row
        i=0
        Visible=0
        TargetVisibleTime=0
        ShotTime=0
        ReactionSum=0
        while (i <= count-1):
            # print("------------i of count : ",i,"/",count)
            TimeOfAction=self.df.iat[i,self.cCol4Date]
            UserID=self.df.iat[i,self.cCol4Id]
            Hit=0
            Visible=0
            if UserID>100:
                Visible = self.df.iat[i, self.cCol4Hostility]
                Hit = self.df.iat[i, self.cCol4Hit]
            Shot = self.df.iat[i, self.cCol4Shot]
            # print("Time=", TimeOfAction)
            # print("UserID=", UserID)
            # print("Visible=", Visible)
            # print("Hit=", Hit)
            # print("Shot=", Shot)
            if Visible>0:
                TargetVisibleTime=TimeOfAction
            if Shot==1:
                ShotTime=TimeOfAction
                ShotCount=ShotCount+1
            if Hit>0:
                TargetHitTime=TimeOfAction
                HitCount=HitCount+1
                ReactionTime=TargetHitTime-TargetVisibleTime
                # print("ReactionTime._s=",ReactionTime._s)
                ReactionSum=ReactionSum+(ReactionTime.delta)
                self.aReactionTimes.append(ReactionTime)
            i=i+1
            Miss=ShotCount-HitCount
        AveReactionTime=0
        if len(self.aReactionTimes)>0:
            AveReactionTime=(ReactionSum/len(self.aReactionTimes))/1000000000.0

        # print(self.aReactionTimes)
        # print("Number of Shots = ", ShotCount, ", Hits=", HitCount, ", Misses=", Miss)
        HitMissRatio=0
        if (Miss+HitCount)>0:
            HitMissRatio=HitCount/(Miss+HitCount)
            # print("Hit/Miss Ratio=",HitMissRatio)
        # print("Length of list=",len(self.aReactionTimes))
        # print("Average Reaction Time=",AveReactionTime, " seconds.")
        score =0
        if AveReactionTime>0:
            score = HitMissRatio*(1000/AveReactionTime)
        return AveReactionTime, HitCount, Miss, HitMissRatio, ShotCount,score
