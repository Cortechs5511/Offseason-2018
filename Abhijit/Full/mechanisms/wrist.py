import wpilib
import math
import numpy as np

from wpilib.command.subsystem import Subsystem

import helper.helper as helper
import sim.simComms as simComms

from ctre import WPI_TalonSRX as Talon

class wrist(Subsystem):

    def __init__(self):
        timeout = 0 #Give max ms to do command

        self.motor = Talon(40)

        self.motor.clearStickyFaults(timeout) #Clears sticky faults
        self.motor.configContinuousCurrentLimit(15,timeout) #15 Amps per motor
        self.motor.configPeakCurrentLimit(20,timeout) #20 Amps during Peak Duration
        self.motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
        self.motor.enableCurrentLimit(True)

        self.motor.enableVoltageCompensation(True) #Compensates for lower voltages
        self.motor.configOpenLoopRamp(1,timeout) #3 seconds from 0 to 1

        self.motor.setQuadraturePosition(0,timeout)

        if(wpilib.RobotBase.isSimulation()): self.encoder = wpilib.Encoder(6,7)

    def getOut(self):
        return self.motor.get()

    def setOut(self,percent):
        self.motor.set(percent)

    def getPos(self):
        return self.motor.getQuadraturePosition()

    def getVel(self):
        return self.motor.getQuadratureVelocity()

    def getTemp(self):
        return self.getTemperature()

    def stop(self):
        self.setOut(0)
