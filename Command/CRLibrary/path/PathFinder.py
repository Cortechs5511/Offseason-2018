import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from CRLibrary.path import PathGen

from wpilib import SmartDashboard

class PathFinder():

    def __init__(self, DT, model, odometer, getDistances):

        '''Variables'''
        self.DT = DT
        self.model = model
        self.getDistances = getDistances
        self.od = odometer
        self.leftFollower = None
        self.rightFollower = None
        self.PID = 0

        '''Gains'''
        kA = [0.000, 0.00, 0.00, 0.00] #angle
        #gains[4] = Voltage per Velocity (feet per second)
        self.gains = [0.005, 0, 0.35, 0.74/12, 0] #distance
        TolAngle = 3 #degrees

        '''PID Controllers'''
        self.angleController = wpilib.PIDController(kA[0], kA[1], kA[2], kA[3], source=self.od.getAngle, output=self.setAngle)
        self.angleController.setInputRange(-180,  180) #degrees
        self.angleController.setOutputRange(-0.9, 0.9)
        self.angleController.setAbsoluteTolerance(TolAngle)
        self.angleController.setContinuous(True)
        self.angleController.disable()

    def setAngle(self, output): self.PID = output

    def enablePID(self):
        self.angleController.enable()
        self.angleController.setSetpoint(0)

    def disablePID(self): self.angleController.disable()

    def initPath(self, name):
        self.time = 0
        [left,right,modifier] = PathGen.getTraj(name, self.model)
        PathGen.showPath(left,right,modifier)

        self.leftFollower = pf.followers.EncoderFollower(left)
        self.leftFollower.configureEncoder(int(self.getDistances()[0]*1000), 1000, 1/math.pi) #Pulse Initial, pulsePerRev, WheelDiam
        self.leftFollower.configurePIDVA(self.gains[0],self.gains[1],self.gains[2],self.gains[3],self.gains[4])

        self.rightFollower = pf.followers.EncoderFollower(right)
        self.rightFollower.configureEncoder(int(self.getDistances()[0]*1000), 1000, 1/math.pi) #Pulse Initial, pulsePerRev, WheelDiam
        self.rightFollower.configurePIDVA(self.gains[0],self.gains[1],self.gains[2],self.gains[3],self.gains[4])

        self.enablePID()

    def followPath(self):
        self.time += 1
        SmartDashboard.putNumber("TimePath:", self.time)
        angle = pf.r2d(self.leftFollower.getHeading())
        angle = 360-angle if angle>180 else -angle
        self.angleController.setSetpoint(angle)

        if(not self.leftFollower.isFinished()):
            out = [self.leftFollower.calculate(int(self.getDistances()[0]*1000))+self.PID, self.rightFollower.calculate(int(self.getDistances()[1]*1000))-self.PID]
            return [out[0]+1.1/12, out[1]+1.1/12]
        else: return [0,0]

    def isFinished(self):  return self.leftFollower.isFinished()
