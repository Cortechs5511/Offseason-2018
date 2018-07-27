#!/usr/bin/env python3

import wpilib
import math
import numpy as np

#DT CONSTANTS
wheelDiam = 4/12 #feet
pulsesPerRev = 127
distPerPulse = wheelDiam * math.pi / pulsesPerRev

def getWheelDiam():
    global wheelDiam
    return wheelDiam

def getPulsesPerRev():
    global pulsesPerRev
    return pulsesPerRev

def getDistPerPulse():
    global distPerPulse
    return distPerPulse

#PATHFINDER CONSTANTS
maxV = 10 # ft/s
maxA = 6

def getMaxV():
    global maxV
    return maxV

def getMaxA():
    global maxA
    return maxA
