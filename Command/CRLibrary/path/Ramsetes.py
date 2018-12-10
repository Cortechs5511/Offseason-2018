import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from CRLibrary.physics import DifferentialDrive as ddrive
from CRLibrary.util import units
from CRLibrary.util import util


from path import paths

class Ramsetes():

    def __init__(self, drivetrain, model, odometer):

        '''Variables'''
        self.DT = drivetrain
        self.model = model
        self.od = odometer

        self.time = 0
        self.maxTime = 0

        self.prev = [0, 0]
        self.PID = [0, 0, 0] #left, right, angle

        self.DT = None
        self.finished = False

        '''Gains'''
        kV = [0.40, 0.0, 0.1, 0.0]
        kA = [0.03, 0.0, 0.0, 0.0]

        self.kB = 1.5
        self.kZeta = 0.4

        TolVel = 0.2
        TolAngle = 3

        '''PID Controllers'''
        self.MaxV = paths.getLimits()[0]
        self.leftController = wpilib.PIDController(kV[0], kV[1], kV[2], kV[3], source=self.od.getLeftVelocity, output=self.setLeft)
        self.leftController.setInputRange(-self.MaxV-3, self.MaxV+3) #feet/second
        self.leftController.setOutputRange(-1, 1) #percent
        self.leftController.setAbsoluteTolerance(TolVel)
        self.leftController.setContinuous(False)
        self.leftController.disable()

        #TolVel, gains same as for left controller so unchanged
        self.rightController = wpilib.PIDController(kV[0], kV[1], kV[2], kV[3], source=self.od.getRightVelocity, output=self.setRight)
        self.rightController.setInputRange(-self.MaxV-3, self.MaxV+3) #feet/second
        self.rightController.setOutputRange(-1, 1) #percent
        self.rightController.setAbsoluteTolerance(TolVel)
        self.rightController.setContinuous(False)
        self.rightController.disable()

        self.angleController = wpilib.PIDController(kA[0], kA[1], kA[2], kA[3], source=self.od.getAngle, output=self.setAngle)
        self.angleController.setInputRange(-180,  180) #degrees
        self.angleController.setOutputRange(-0.9, 0.9)
        self.angleController.setAbsoluteTolerance(TolAngle)
        self.angleController.setContinuous(True)
        self.angleController.disable()

    def setLeft(self, output):
        self.PID[0] = output

    def setRight(self, output):
        self.PID[1] = output

    def setAngle(self, output):
        self.PID[2] = output

    def enablePID(self):
        self.leftController.enable()
        self.rightController.enable()
        self.angleController.enable()

        self.leftController.setSetpoint(0)
        self.rightController.setSetpoint(0)
        self.angleController.setSetpoint(0)

    def disablePID(self):
        self.leftController.disable()
        self.rightController.disable()
        self.angleController.disable()

    '''The Algorithm!'''

    def initPath(self, name):
        self.finished = False

        [self.left,self.right,modifier] = paths.getTraj(name)
        paths.showPath(self.left,self.right,modifier)

        self.time = 0
        self.maxTime = len(self.left)

        self.enablePID()

    def followPath(self):
        if(self.time>=self.maxTime): return [0,0]

        leftSeg = self.left[self.time]
        rightSeg = self.right[self.time]
        self.time += 1

        xd = units.feetToMeters((leftSeg.x+rightSeg.x)/2)
        yd = units.feetToMeters((leftSeg.y+rightSeg.y)/2)
        thetad = (leftSeg.heading+rightSeg.heading)/2

        leftVeld = units.feetToMeters(leftSeg.velocity)
        rightVeld = units.feetToMeters(rightSeg.velocity)

        leftAcceld = units.feetToMeters(leftSeg.acceleration)
        rightAcceld = units.feetToMeters(rightSeg.acceleration)

        vd = (rightVeld + leftVeld)/2
        wd = (rightVeld - leftVeld)/(2*self.model.effWheelbaseRadius())

        ad = (rightAcceld + leftAcceld)/2
        alphad = (rightAcceld - leftAcceld)/(2*self.model.effWheelbaseRadius())

        [x, y, theta, rightVel, leftVel] = self.od.getSI()
        [y, theta] = [-y, -theta]

        #The main calculations based on Ramsetes algorithm
        v = vd * math.cos(thetad-theta) + self.k(vd,wd,self.kB,self.kZeta) * ((xd-x) * math.cos(theta) + (yd-y) * math.sin(theta))
        w = wd + self.kB * vd * self.sinc(util.angleDiffRad(thetad,theta)) * ((yd-y) * math.cos(theta) - (xd-x) * math.sin(theta))
        + self.k(vd,wd,self.kB,self.kZeta) * util.angleDiffRad(thetad,theta)

        leftOut = v - self.model.effWheelbaseRadius()*w #for velocity PID process variable
        rightOut = v + self.model.effWheelbaseRadius()*w

        a = 50*(v-self.prev[0]) #50 iterations per second
        alpha = 50*(w-self.prev[1])

        self.prev = [v, w] #for next acceleration calculations

        chassisVel = ddrive.ChassisState(v,w)
        chassisAccel = ddrive.ChassisState(a,alpha)

        voltage = self.model.solveInverseDynamics_CS(chassisVel, chassisAccel).getVoltage()
        [leftV, rightV] = [voltage[0]/12, voltage[1]/12]

        self.leftController.setSetpoint(units.metersToFeet(leftOut))
        self.rightController.setSetpoint(units.metersToFeet(rightOut))
        self.angleController.setSetpoint(util.boundDeg(units.radiansToDegrees(-thetad)))

        return [leftV+self.PID[0]+self.PID[2], rightV+self.PID[1]-self.PID[2]]

    def k(self, vd, wd, b, zeta): return 2 * zeta * math.sqrt(wd**2+b*vd**2)

    def sinc(self, theta): return (1 if theta==0 else math.sin(theta)/theta)

    def isFinished(self): return self.time>self.maxTime
