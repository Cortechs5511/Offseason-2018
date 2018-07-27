#!/usr/bin/env python3

import wpilib
import math
import numpy as np

from wpilib.command.subsystem import Subsystem
from wpilib.drive import DifferentialDrive
import helper.helper as helper
import sim.simComms as simComms

class Drivetrain(Subsystem):

    dbLimit = 0.1
    k = -2
    maxSpeed = 0.85

    encoderDists = [0,0]

    def __init__(self, motors, encoders,navx):
        self.left = motors[0]
        self.right = motors[1]
        self.leftEncoder = encoders[0]
        self.rightEncoder = encoders[1]
        self.navx = navx

    def simpleInit(self):
        self.simpleDrive = DifferentialDrive(self.left,self.right)

    def setParams(dbLimit,k,maxSpeed):
        self.dbLimit = dbLimit
        self.k = k
        self.maxSpeed = maxSpeed

    def tank(self,left,right):
        if(abs(left)<self.dbLimit):left = 0
        else: left = abs(left)/left*(math.e**(self.k*abs(left))-1) / (math.exp(self.k)-1)

        if(abs(right)<self.dbLimit): right = 0
        else: right = abs(right)/right*(math.e**(self.k*abs(right))-1) / (math.exp(self.k)-1)

        left *= self.maxSpeed
        right *= self.maxSpeed

        self.left.set(left)
        self.right.set(right)

        self.updateEncoders()

    def tankAuto(self,left,right):
        self.left.set(left)
        self.right.set(right)
        self.updateEncoders()

    def arcade(self,throttle,turn):
        left = 0
        right = 0

        if(abs(throttle)>self.dbLimit): throttle = np.sign(throttle)*(math.exp(self.k*abs(throttle))-1)/(math.exp(self.k)-1)
        else: throttle = 0

        if(abs(turn)>self.dbLimit): turn = np.sign(turn)*(math.exp(k*abs(turn))-1)/(math.exp(self.k)-1)
        else: turn = 0

        L0 = throttle + turn
        R0 = throttle - turn

        L1 = self.maxSpeed * L0/(max(abs(L0),abs(R0),1))
        R1 = self.maxSpeed * R0/(max(abs(L0),abs(R0),1))

        self.left.set(L1)
        self.right.set(R1)

        self.updateEncoders()

    def simpleTank(self,left,right):
        self.simpleDrive.tankDrive(left,right)
        self.updateEncoders()

    def simpleArcade(self,left,right):
        self.simpleDrive.arcadeDrive(left,right)
        self.updateEncoders()

    def updateEncoders(self):
        self.encoderDists = [self.leftEncoder.getDistance(),self.rightEncoder.getDistance()]

    def clearEncoders(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        simComms.resetEncoders()

    def printEncoders(self):
        print("Encoder Positions: " + "{0:.2f}".format(self.encoderDists[0])+"\t"+"{0:.2f}".format(self.encoderDists[1]))

    def stop(self):
        self.left.set(0)
        self.right.set(0)
