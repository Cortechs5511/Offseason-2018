import time
from networktables import NetworkTables

import logging

#logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

def init():
    sd.putNumber('dsTime',0)

def getTime():
    return sd.getNumber('dsTime',-1)

def setTime(new):
    sd.putNumber('dsTime', new)
