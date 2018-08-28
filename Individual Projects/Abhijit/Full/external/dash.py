import time
from networktables import NetworkTables

import logging

#logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

def init():
    sd.putNumber("time",0)
    sd.putString("auto","Right")

def getTime():
    return sd.getNumber("time",-1)

def setTime(new):
    sd.putNumber("time", new)

def getAuto():
    return sd.getString("auto","")

def setAuto(new):
    sd.putNumber("auto", new)
