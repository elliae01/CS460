from pandas import DataFrame
import cx_Oracle
import os
import math
from Server.UserInformation import *

print("Hello, Welcome to Reactionalytics.py")

class Reactionalytics:
    df = None

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
        self.df.rename(columns={0: "INDEX", 1: "Date", 2: "Id", 3: "Loc.x", 4: "Loc.y", 5: "Loc.z", 6: "Hostility", 7: "Hit",
                           8: "Heart Rate", 9: "Emg0", 10: "Emg1", 11: "Emg2", 12: "Emg3", 13: "Emg4", 14: "Emg5",
                           15: "Emg6", 16: "Emg7", 17: "Arm.Roll", 18: "Arm.Pitch", 19: "Arm.Heading", 20: "Shot",
                           21: "Hody.Heading", 22: "Body.Roll", 23: "Body.Pitch", 24: "Head.Heading", 25: "Head.Roll",
                           26: "Head.Pitch"}, inplace=True)
        dfCurrentEvent = (self.df['Date'] >= StartDate) & (self.df['Date'] <= EndDate)
        self.df=self.df[dfCurrentEvent]
        database.close
        return None

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
        return self.df.iat[row, self.cCol4LocX]

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
        #print("row=",row)
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

    def TotalDistanceTraveled(self,user):
        d=self.DistanceTraveled(user,self.classStartDate,self.classEndDate)
        return d

    def DistanceTraveled(self,user,startdate,finishdate):
        NotFirst=False
        count=self.rowcount()
        diff=finishdate-startdate
        #print("Count = ",count)
        #print("StartDate=", startdate, " --  Finish Date=", finishdate, " --> Elasped Time=",diff)
        d=0.0
        for i in range(count):
            if self.getID(i)==user:
                # print(self.getDate(i),startdate)
                #print("---",i)
                if (self.getDate(i)>=startdate) and (self.getDate(i)<=finishdate):
                    #print(self.getINDEX(i),self.getX(i),self.getY(i))
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
        count=self.rowcount()
        d=0.0
        for i in range(count-1):
            if self.getID(i)==user:
                if self.getShot(i)!=0:
                    d=d+1
        return d

    def getShotsBeforeRowByUser(self, row, user):
        count=self.rowcount()
        d=-1.0     # -1 reports a failure
        if row<=count:
            d = 0
            for i in range(row-1):
                if self.getID(i)==user:
                    if self.getShot(i)!=0:
                        d=d+1
        if d<0:
            print("Error ", d, " in getShotsBeforeRowByUser: Row = ", row, " Count = ", count)
        return d

    def getHitsBeforeRowByUser(self, row):
        return -1

    def getHitMissRatioBeforeRowByUser(self, row, user):
        return -1

    def getAvgReactionTimeBeforeRowByUser(self, row, user):
        return -1

    def getDistanceBeforeRowByUser(self, row, user):
        NotFirst=False
        count=self.rowcount()
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

    def getTotalNumberOfUsers(self):
        return -1

    def getTotalNumberOfTargets(self):
        return -1

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
        count = self.rowcount()
        MaxVal = -99999999
        for i in range(count):
            if MaxVal < self.getX(i):
                MaxVal = self.getX(i)
        return MaxVal

    def getMaxY(self):
        count = self.rowcount()
        MaxVal = -99999999
        for i in range(count):
            if MaxVal < self.getY(i):
                MaxVal = self.getY(i)
        return MaxVal

    def getMinX(self):
        count = self.rowcount()
        MinVal = 99999999
        for i in range(count):
            if MinVal > self.getX(i):
                MinVal = self.getX(i)
        return MinVal

    def getMinY(self):
        count = self.rowcount()
        MinVal = 99999999
        for i in range(count):
            if MinVal > self.getY(i):
                MinVal = self.getY(i)
        return MinVal


