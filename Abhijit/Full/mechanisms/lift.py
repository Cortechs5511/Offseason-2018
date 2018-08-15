import wpilib
import math
#import numpy as np

from wpilib.command.subsystem import Subsystem

import helper.helper as helper
import sim.simComms as simComms

from ctre import WPI_TalonSRX as Talon

class lift(Subsystem):

    def __init__(self):
        timeout = 0 #Give max ms to do command

        motors = [Talon(30), Talon(31)]

        for motor in motors:
            motor.clearStickyFaults(timeout) #Clears sticky faults
            motor.configContinuousCurrentLimit(15,timeout) #15 Amps per motor
            motor.configPeakCurrentLimit(20,timeout) #20 Amps during Peak Duration
            motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
            motor.enableCurrentLimit(True)

            motor.enableVoltageCompensation(True) #Compensates for lower voltages
            motor.configOpenLoopRamp(3,timeout) #3 seconds from 0 to 1

        motors[1].set(Talon.ControlMode.Follower,30)
        self.motor = motors[0]

        motor.setQuadraturePosition(0,timeout)

        if(wpilib.RobotBase.isSimulation()): self.encoder = wpilib.Encoder(4,5)

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
