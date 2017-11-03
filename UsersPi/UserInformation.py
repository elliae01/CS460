class UserInformation:
        # VARIABLE ASSIGNMENT
    numberOfUsers=0
    Id = None,
    emg = [None,None,None,None,None,None,None,None]
    roll = None
    pitch = None
    yaw = None
    shot = None
    headXAxis = None
    headYAxis = None
    headZAxis = None
    headHeading = None
    headDegrees = None
    bodyXAxis = None
    bodyYAxis = None
    bodyZAxis = None
    bodyHeading = None
    bodyDegrees = None
    locationXAxis = None
    locationYAxis = None
    locationZAxis = None

        # CONSTRUCTOR
    def __init__(self,Id):
        self.Id = Id
        UserInformation.numberOfUsers += 1

        # SETTERS
    def setId(self,newId):
        self.Id = newId
    def setEMG(self,emg1,emg2,emg3,emg4,emg5,emg6,emg7,emg8):
        self.emg = [emg1,emg2,emg3,emg4,emg5,emg6,emg7,emg8]
    def setRoll(self,newRoll):
        self.roll = newRoll
    def setPitch(self,newPitch):
        self.pitch = newPitch
    def setYaw(self,newYaw):
        self.yaw = newYaw
    def setShot(self,newShot):
        self.shot = newShot
    def setShot(self,newShot):
        self.shot = newShot
    def setHeadXAxis(self,newHeadXAxis):
        self.headXAxis = newHeadXAxis
    def setHeadYAxis(self,newHeadYAxis):
        self.headYAxis = newHeadYAxis
    def setHeadZAxis(self,newHeadZAxis):
        self.headZAxis = newHeadZAxis
    def setHeadHeading(self,newHeadHeading):
        self.headHeading = newHeadHeading
    def setHeadDegrees(self,newHeadDegrees):
        self.headDegrees = newHeadDegrees
    def setBodyXAxis(self,newBodyXAxis):
        self.bodyXAxis = newBodyXAxis
    def setBodyYAxis(self,newBodyYAxis):
        self.bodyYAxis = newBodyYAxis
    def setBodyZAxis(self,newBodyZAxis):
        self.bodyZAxis = newBodyZAxis
    def setBodyHeading(self,newBodyHeading):
        self.bodyHeading = newBodyHeading
    def setBodyDegrees(self,newBodyDegrees):
        self.bodyDegrees = newBodyDegrees
    def setLocationXAxis(self,newLocationXAxis):
        self.locationXAxis = newLocationXAxis
    def setLocationYAxis(self,newLocationYAxis):
        self.locationYAxis = newLocationYAxis
    def setLocationZAxis(self,newLocationZAxis):
        self.locationZAxis = newLocationZAxis

        # GETTERS
    def getId(self):
        return self.Id
    def getEMG(self):
        return self.emg
    def getRoll(self):
        return self.roll
    def getPitch(self):
        return self.pitch
    def getYaw(self):
        return self.yaw
    def getShot(self):
        return self.shot
    def getShot(self):
        return self.shot
    def getHeadXAxis(self):
        return self.headXAxis
    def getHeadYAxis(self):
        return self.headYAxis
    def getHeadZAxis(self):
        return self.headZAxis
    def getHeadHeading(self):
        return self.headHeading
    def getHeadDegrees(self):
        return self.headDegrees
    def getBodyXAxis(self):
        return self.bodyXAxis
    def getBodyYAxis(self):
        return self.bodyYAxis
    def getBodyZAxis(self):
        return self.bodyZAxis
    def getBodyHeading(self):
        return self.bodyHeading
    def getBodyDegrees(self):
        return self.bodyDegrees
    def getLocationXAxis(self):
        return self.locationXAxis
    def getLocationYAxis(self):
        return self.locationYAxis
    def getLocationZAxis(self):
        return self.locationZAxis