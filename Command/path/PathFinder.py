import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from path import paths

gains = [1,0,1,1/paths.getLimits()[0],0]

DT = None
globalLeft = None
globalRight = None

def initPath(drivetrain, name):
    global DT, globalLeft, globalRight

    [left,right,modifier] = paths.getTraj(name)
    paths.showPath(left,right,modifier)

    leftFollower = pf.followers.EncoderFollower(left)
    leftFollower.configureEncoder(drivetrain.getRaw()[0], 255, 4/12) #Pulse Initial, pulsePerRev, WheelDiam
    leftFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    rightFollower = pf.followers.EncoderFollower(right)
    rightFollower.configureEncoder(-drivetrain.getRaw()[1], 127, 4/12) #Pulse Initial, pulsePerRev, WheelDiam
    rightFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    DT = drivetrain
    globalLeft = leftFollower
    globalRight = rightFollower

def followPath(DT):
    global globalLeft, globalRight

    angle = pf.r2d(globalLeft.getHeading())
    if(angle>180): angle=360-angle
    else: angle=-angle
    DT.angleController.setSetpoint(angle)
    update = DT.anglePID

    if(not globalLeft.isFinished()):
        return [globalLeft.calculate(DT.getRaw()[0])+update, globalRight.calculate(-DT.getRaw()[1])-update]
    else: return [0,0]

def isFinished():
    global globalLeft
    return globalLeft.isFinished()
