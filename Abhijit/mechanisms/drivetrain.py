#!/usr/bin/env python3

import wpilib
import math
import numpy as np

from wpilib.command.subsystem import Subsystem
from wpilib.drive import DifferentialDrive

import helper.helper as helper
import sim.simComms as simComms

import sensors.navx as navx
import sensors.DTEncoders as encoders

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

class Drivetrain(Subsystem):

    dbLimit = 0.1
    maxSpeed = 0.85
    k = -2

    def __init__(self):
        [TalonLeft,VictorLeft1,VictorLeft2] = [Talon(10), Victor(11), Victor(12)]
        VictorLeft1.set(Victor.ControlMode.Follower,10)
        VictorLeft2.set(Victor.ControlMode.Follower,10)

        [TalonRight, VictorRight1, VictorRight2] = [Talon(20), Victor(21), Victor(22)]
        VictorRight1.set(Victor.ControlMode.Follower,20)
        VictorRight2.set(Victor.ControlMode.Follower,20)

        self.left = TalonLeft
        self.right = TalonRight

        self.navx = navx.NavX()
        self.encoders = encoders.DTEncoders()

        self.navx.disablePID()
        self.encoders.disablePID()

    def simpleInit(self):
        self.simpleDrive = DifferentialDrive(self.left,self.right)

    def setParams(dbLimit,k,maxSpeed):
        self.dbLimit = dbLimit
        self.maxSpeed = maxSpeed
        self.k = k

    def tank(self,left,right):
        self.navx.disablePID()
        self.encoders.disablePID()

        if(abs(left)<self.dbLimit):left = 0
        else: left = abs(left)/left*(math.e**(self.k*abs(left))-1) / (math.exp(self.k)-1)

        if(abs(right)<self.dbLimit): right = 0
        else: right = abs(right)/right*(math.e**(self.k*abs(right))-1) / (math.exp(self.k)-1)

        left *= self.maxSpeed
        right *= self.maxSpeed

        self.left.set(left)
        self.right.set(right)

    def tankAuto(self,left,right):
        self.navx.disablePID()
        self.encoders.disablePID()

        self.left.set(left)
        self.right.set(right)

    def arcade(self,throttle,turn):
        self.navx.disablePID()
        self.encoders.disablePID()

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
        self.navx.disablePID()
        self.encoders.disablePID()
        self.simpleDrive.tankDrive(left,right)

    def simpleArcade(self,left,right):
        self.navx.disablePID()
        self.encoders.disablePID()
        self.simpleDrive.arcadeDrive(left,right)

    def driveStraight(self,power):
        self.encoders.enablePID()
        self.encoders.setPID(0)
        adjust = self.encoders.getPID()
        [left,right] = [power+adjust,power-adjust]
        self.left.set(left)
        self.right.set(right)

    def driveStraightAdvanced(self,power):
        self.encoders.enablePID()
        self.encoders.setPID(0)
        self.navx.enablePID()
        self.navx.setPID(0)
        adjust = (self.encoders.getPID() + self.navx.getPID())/2
        self.left.set(power+adjust)
        self.right.set(power-adjust)

    def turnToAngle(self,setpoint):
        self.navx.enablePID()
        self.navx.setPID(setpoint)
        turn = self.navx.getPID()
        self.left.set(turn)
        self.right.set(-turn)

    def initGetWheelbase(self):
        self.total = 0
        self.prevAngle = 0
        self.currAngle = 0
        self.print = False

    def getWheelbase(self,speed,spins):
        if(self.total<spins):
            self.tankAuto(speed,-speed)
            self.currAngle = self.navx.getAngle()
            if(self.currAngle<self.prevAngle): self.total+=1
            self.prevAngle = self.currAngle
        elif(self.print==False):
            self.distance = (abs(self.encoders.getDistance()[0])+abs(self.encoders.getDistance()[1]))/2/spins/math.pi*12
            print(self.distance)
            self.print=True
        else: self.stop()

    def stop(self):
        self.left.set(0)
        self.right.set(0)
        self.navx.disablePID()
        self.encoders.disablePID()
