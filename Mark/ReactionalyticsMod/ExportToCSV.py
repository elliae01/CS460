from multiprocessing import Process, Manager
from multiprocessing.managers import *
import pandas as pd
from pandas import DataFrame
import cx_Oracle
import os
from Server.UserInformation import *

def __init_():
    print("hello from ExportToCSV init")

def pExportToCSV():
    ip = 'localhost'
    port = 1521
    SID = 'orcl'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    print(dsn_tns)

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

    sColumnNames =  'INDEX','DATE' \
                    ',Id,' \
                    'Loc.x,Loc.y,Loc.z,' \
                    'hostility,hit,Heart Rate,' \
                    'emg0,emg1,emg2,emg3,emg4,emg5,emg6,emg7,' \
                    'arm.roll,arm.pitch,arm.heading,' \
                    'shot,' \
                    'body.heading,body.roll,body.pitch,' \
                    'head.heading,head.roll,head.pitch'

    cursor.execute(sSQLCMD)

    df = DataFrame(cursor.fetchall())
    print(sColumnNames)
    df.rename(columns={0:"INDEX", 1: "Date", 2: "Id", 3: "Loc.x", 4: "Loc.y", 5: "Loc.z", 6: "Hostility", 7: "hit", 8: "Heart Rate", 9: "emg0", 10: "emg1", 11: "emg2", 12: "emg3", 13: "emg4",14: "emg5",15: "emg6",16: "emg7",17: "arm.roll",18: "arm.pitch",19: "arm.heading",20: "Shot",21: "body.heading", 22: "body.roll", 23: "body.pitch",24: "head.heading",25: "head.roll", 26: "head.pitch"}, inplace=True)

    print(df.head())

    dir_path = os.path.dirname(os.path.realpath("__file__"))
    print (dir_path)
    dir_path = dir_path + "\DataFrame.csv"
    df.to_csv(dir_path)
    #sSQLCMD='select * from shooter_table'

    #cursor.execute(sSQLCMD)
    # cursor.execute(sSQLCMD)
    #
    # for row in cursor:
    #     print (row[0], row[1], row[2])
    #

    #connection = cx_Oracle.connect(conn_str)
    #df.to_sql("Shooter_Table","orcl" )

    # print(sSQLCMD)
    #df_ora = pd.read_sql(sSQLCMD, database)
    #print(df_ora.first_valid_index)
    database.close
    return 0

if __name__ == '__main__':
    print("Running main program in Export to CSV")
    pExportToCSV()