#!/usr/bin/env python3

import wpilib
import math
import numpy as np

#Robot Dimensions
bumpers = 3.5/12 #feet
width = 33/12 #excluding bumpers
length = 28/12 #excluding bumpers

widthBumpers = width + 2*bumpers
lengthBumpers = length + 2*bumpers

def getBumpers():
    global bumpers
    return bumpers

def getWidth():
    global width
    return width

def getLength():
    global length
    return length

def getWidthBumpers():
    global widthBumpers
    return widthBumpers

def getLengthBumpers():
    global lengthBumpers
    return lengthBumpers

#Period
period = 0.02 #20 milliseconds
freq = 50 #50 runs per second

def getPeriod():
    global period
    return period

def getFreq():
    global freq
    return freq

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
maxV = 8 # ft/s
maxA = 6

def getMaxV():
    global maxV
    return maxV

def getMaxA():
    global maxA
    return maxA


#AUTONOMOUS CONSTANTS
auto = ""
gameData = ""

def getAuto():
    global auto
    return auto

def setAuto(input):
    global auto
    auto = input

def getGameData():
    global gameData
    return gameData

def setGameData(input):
    global gameData
    gameData = input


def sign(num):
    if(num<0): return -1
    elif(num>0): return 1
    return 0
