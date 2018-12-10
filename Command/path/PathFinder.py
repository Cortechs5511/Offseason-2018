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

def enablePID():
    global angleController
    angleController.enable()
    angleController.setSetpoint(0)

def disablePID():
    global angleController
    angleController.disable()

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

    enablePID()

def followPath(DT):
    global globalLeft, globalRight, angleController, navx

    angle = pf.r2d(globalLeft.getHeading())
    angle = 360-angle if angle>180 else -angle
    angleController.setSetpoint(angle)

    if(not globalLeft.isFinished()):
        return [globalLeft.calculate(DT.getRaw()[0])+navx, globalRight.calculate(-DT.getRaw()[1])-navx]
    else: return [0,0]

def isFinished():
    global globalLeft
    return globalLeft.isFinished()

def getAngle():
    global DT
    return DT.getAngle()

def setAngle(output):
    global navx
    navx = output

navx = 0
TolAngle = 3 #degrees
[kP,kI,kD,kF] = [0.024, 0.00, 0.20, 0.00]
if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.020,0.00,0.00,0.00]
angleController = wpilib.PIDController(kP, kI, kD, kF, source=getAngle, output=setAngle)
angleController.setInputRange(-180,  180) #degrees
angleController.setOutputRange(-0.9, 0.9)
angleController.setAbsoluteTolerance(TolAngle)
angleController.setContinuous(True)
angleController.disable()
