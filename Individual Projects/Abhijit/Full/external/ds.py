from wpilib import DriverStation

ds = None

def init():
    global ds
    ds = DriverStation.getInstance()

def getVoltage():
    return ds.getBatteryVoltage()

def getGameData():
    return ds.getGameSpecificMessage()
