import time
import os
import pandas as pd

if __name__ == '__main__':
    ip = 'localhost'
    port = 1521
    SID = 'orcl'
    UserName="SYSMAN"
    PassWord="System_Admin1"
    DatabaseInfo=[ip,port,SID,UserName,PassWord]


    StartDate = pd.to_datetime('2018-03-17 16:07:56.164')
    EndDate = pd.to_datetime('2018-03-17 16:59:12.000')

    file = open('DBInfo.txt', 'w')
    for item in DatabaseInfo:
        file.write(str(item))
        file.write('\n')
    file.close()

    file = open('Times.txt', 'w')
    file.write(str(StartDate))
    file.write("\n")
    file.writelines(str(EndDate))
    file.close()

    os.system("C:\\Python36\\python DBGUI.py")

    exit(0)

# the following code will get the info into DBGUI.py

    DatabaseInfo=[]
    file = open('DBInfo.txt', 'r')
    for line in file:
        DatabaseInfo.append(line)
    file.close()
    print(DatabaseInfo)

    file = open('Times.txt', 'r')
    StartDate=pd.to_datetime(file.readline())
    EndDate=pd.to_datetime(file.readline())
    file.close()

    print(StartDate)
    print(EndDate)
