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

    #NavX PID Constants
    if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [1.50, 0.00, 0.10, 0.00] # These PID parameters are used in simulation
    else: [kP,kI,kD,kF] = [0.03, 0.00, 0.00, 0.00] # These PID parameters are used on a real robot
    kToleranceDegrees = 5.0

    def __init__(self, motors, encoders,navx):
        self.left = motors[0]
        self.right = motors[1]
        self.leftEncoder = encoders[0]
        self.rightEncoder = encoders[1]
        self.navx = navx

        turnController = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self.navx, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        turnController.setContinuous(True)
        self.turnController = turnController

        self.turn = 0
        self.turnController.disable()

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

    def tankAuto(self,left,right):
        self.left.set(left)
        self.right.set(right)


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


    def simpleTank(self,left,right):
        self.simpleDrive.tankDrive(left,right)

    def simpleArcade(self,left,right):
        self.simpleDrive.arcadeDrive(left,right)



    def getEncoders(self):
        return [self.leftEncoder.get(),self.rightEncoder.get()]

    def getEncoderDists(self):
        return [self.leftEncoder.getDistance(),self.rightEncoder.getDistance()]

    def clearEncoders(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        simComms.resetEncoders()

    def printEncoders(self):
        print("Encoder Positions: " + "{0:.2f}".format(self.encoderDists[0])+"\t"+"{0:.2f}".format(self.encoderDists[1]))



    def enableNavXPID(self):
        self.turnController.enable()

    def disableNavXPID(self):
        self.turnController.disable()

    def setNavXPID(self, setpoint):
        self.turnController.setSetpoint(setpoint)

    def getNavXPIDOut(self):
        return self.turn

    def getAngle(self):
        return self.navx.getYaw()

    def pidWrite(self, output):
        self.turn = output



    def stop(self):
        self.left.set(0)
        self.right.set(0)
