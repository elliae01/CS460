def convertToSqlStatement(dataStruct):
    entireStatement = ""

    # User Status
    entireStatement += sqlizerInsert(
        "insert into status(id, people_id, time_stamp, heartRate, visible, hit, hostile, width, height) ",
        ["null", dataStruct.getId(), "now()", dataStruct.getHeartRate(), "null", "null", "null", "null", "null"])

    # User Location
    entireStatement += sqlizerInsert(
        "insert into locations(id, people_id, time_stamp, locationXAxis, locationYAxis, locationZAxis) ",
        ["null", dataStruct.getId(), "now()", dataStruct.getLocationXAxis(),
         dataStruct.getLocationYAxis(), dataStruct.getLocationZAxis()])

    # User Orientation
    entireStatement += sqlizerInsert(
        "insert into orientations(id, people_id, time_stamp, headXAxis, headYAxis, headZAxis, headHeading, headDegrees, bodyXAxis, bodyYAxis, bodyZAxis, bodyHeading, bodyDegrees) ",
        ["null", dataStruct.getId(), "now()", dataStruct.getHeadXAxis(), dataStruct.getHeadYAxis(),
         dataStruct.getHeadZAxis(), dataStruct.getHeadHeading(), dataStruct.getHeadDegrees(), dataStruct.getBodyXAxis(),
         dataStruct.getBodyYAxis(), dataStruct.getBodyZAxis(), dataStruct.getBodyHeading(),
         dataStruct.getBodyDegrees()])

    # User Biometrics
    emgData = dataStruct.getEMG()
    entireStatement += sqlizerInsert(
        "insert into biometrics(id, people_id, time_stamp, shot, roll, pitch, yaw, emg_1, emg_2, emg_3, emg_4, emg_5, emg_6, emg_7, emg_8) ",
        ["null", dataStruct.getId(), "now()", dataStruct.getShot(), dataStruct.getRoll(), dataStruct.getPitch(),
         dataStruct.getYaw(), emgData[0], emgData[1], emgData[2], emgData[3], emgData[4], emgData[5], emgData[6],
         emgData[7]])

    return entireStatement

def noneRemover(item):
	if(item == None):
		return 0
	else:
		return item

def sqlizerInsert(sqlStatementBegin, values):
	result = sqlStatementBegin + "values("
	for i in range(len(values)):
		result += str(noneRemover(values[i]))
		if(i != (len(values)-1)):
			result += ", "
	result += ");\n"
	return result


def insertStatementCreator(prefix, values):
    result = (prefix, " values (")

    LastElement = 0

    for eachValue in values:
        result += str(eachValue)

    if (LastElement + 1 < len(values)):
        result += ", "
        LastElement += 1
    else:
        result += ");\n"

    return result

def databaseUpdate(sql,database):
    cursor = database.cursor()
    for result in cursor.execute(sql, multi=True):
        pass
    #database.cmd_query_iter(sql)
    database.commit()
    cursor.close()
