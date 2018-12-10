import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from CRLibrary.physics import DifferentialDrive as ddrive
from CRLibrary.util import units
from CRLibrary.util import util

import odometry as od

from path import paths

time = 0
maxTime = 0

navx = 0

prevV = 0
prevW = 0

leftVFinal = 0
rightVFinal = 0

leftVTemp = 0
rightVTemp = 0

DT = None

finished = False

'''Gains'''
kV = [0.4, 0.0, 0.1, 0.0]
kA = [0.03, 0.0, 0.0, 0.0]
kB = 1.5
kZeta = 0.4

TolVel = 0.2
TolAngle = 3

def enablePID():
    global leftController, rightController, angleController

    leftController.enable()
    rightController.enable()
    angleController.enable()

    leftController.setSetpoint(0)
    rightController.setSetpoint(0)
    angleController.setSetpoint(0)

def disablePID():
    global leftController, rightController, angleController

    leftController.disable()
    rightController.disable()
    angleController.disable()

def initPath(drivetrain, name):
    global DT, left, right, time, maxTime

    DT = drivetrain
    finished = False

    [left,right,modifier] = paths.getTraj(name)
    paths.showPath(left,right,modifier)

    time = 0
    maxTime = len(left)

    enablePID()

def followPath(DT):
    global left, right, time, maxTime, prevV, prevW, leftVTemp, rightVTemp
    global leftVFinal, rightVFinal, leftController, rightController, finished
    global kB, kZeta

    if(time>=maxTime):
        leftController.disable()
        rightController.disable()
        finished = True
        return [0,0]

    leftSeg = left[time]
    rightSeg = right[time]
    time += 1

    xd = units.feetToMeters((leftSeg.x+rightSeg.x)/2)
    yd = units.feetToMeters((leftSeg.y+rightSeg.y)/2)
    thetad = (leftSeg.heading+rightSeg.heading)/2

    leftVeld = units.feetToMeters(leftSeg.velocity)
    rightVeld = units.feetToMeters(rightSeg.velocity)

    leftAcceld = units.feetToMeters(leftSeg.acceleration)
    rightAcceld = units.feetToMeters(rightSeg.acceleration)

    vd = (rightVeld + leftVeld)/2
    wd = (rightVeld - leftVeld)/(2*DT.model.effWheelbaseRadius())

    ad = (rightAcceld + leftAcceld)/2
    alphad = (rightAcceld - leftAcceld)/(2*DT.model.effWheelbaseRadius())

    [x, y, theta, rightVel, leftVel] = od.getSI()
    [y, theta] = [-y, -theta]

    v = vd * math.cos(thetad-theta) + k(vd,wd,kB,kZeta) * ((xd-x) * math.cos(theta) + (yd-y) * math.sin(theta))
    w = wd + kB * vd * sinc(util.angleDiffRad(thetad,theta)) * ((yd-y) * math.cos(theta) - (xd-x) * math.sin(theta)) + k(vd,wd,kB,kZeta) * util.angleDiffRad(thetad,theta)

    leftOut = v - DT.model.effWheelbaseRadius()*w #for velocity PID process variable
    rightOut = v + DT.model.effWheelbaseRadius()*w

    a = 50*(v-prevV) #50 iterations per second
    alpha = 50*(w-prevW)

    prevV = v #for next acceleration calculations
    prevW = w

    chassisVel = ddrive.ChassisState(v,w)
    chassisAccel = ddrive.ChassisState(a,alpha)

    voltage = DT.model.solveInverseDynamics_CS(chassisVel, chassisAccel).getVoltage()
    [leftV, rightV] = [voltage[0]/12, voltage[1]/12]

    leftVTemp = leftV #feed forward for PID
    rightVTemp = rightV

    leftController.setSetpoint(units.metersToFeet(leftOut))
    rightController.setSetpoint(units.metersToFeet(rightOut))
    angleController.setSetpoint(util.boundDeg(units.radiansToDegrees(-thetad)))

    return [leftVFinal+navx, rightVFinal-navx]

def k(vd, wd, b, zeta):
    return 2 * zeta * math.sqrt(wd**2+b*vd**2)

def sinc(theta):
    if(theta==0): return 1
    return math.sin(theta)/theta

'''PID Controllers Below'''

def getLeftVelocity(): return od.get()[3] #feet/second

def setLeftVelocity(output):
    global leftVTemp, leftVFinal
    leftVFinal = output + leftVTemp

MaxV = paths.getLimits()[0]
leftController = wpilib.PIDController(kV[0], kV[1], kV[2], kV[3], source=getLeftVelocity, output=setLeftVelocity)
leftController.setInputRange(-MaxV-3, MaxV+3) #feet/second
leftController.setOutputRange(-1, 1) #percent
leftController.setAbsoluteTolerance(TolVel)
leftController.setContinuous(False)
leftController.disable()

def getRightVelocity():
    return od.get()[4] #feet/second

def setRightVelocity(output):
    global rightVTemp, rightVFinal
    rightVFinal = output + rightVTemp

#TolVel, gains same as for left controller so unchanged
rightController = wpilib.PIDController(kV[0], kV[1], kV[2], kV[3], source=getRightVelocity, output=setRightVelocity)
rightController.setInputRange(-MaxV-3, MaxV+3) #feet/second
rightController.setOutputRange(-1, 1) #percent
rightController.setAbsoluteTolerance(TolVel)
rightController.setContinuous(False)
rightController.disable()

def getAngle():
    global DT
    return util.boundDeg(DT.getAngle())

def setAngle(output):
    global navx
    navx = output

angleController = wpilib.PIDController(kA[0], kA[1], kA[2], kA[3], source=getAngle, output=setAngle)
angleController.setInputRange(-180,  180) #degrees
angleController.setOutputRange(-0.9, 0.9)
angleController.setAbsoluteTolerance(TolAngle)
angleController.setContinuous(True)
angleController.disable()

def isFinished():
    global finished
    return finished
