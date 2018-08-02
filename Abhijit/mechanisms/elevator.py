import wpilib
import math
import numpy as np

from wpilib.command.subsystem import Subsystem

import helper.helper as helper
import sim.simComms as simComms

from ctre import WPI_TalonSRX as Talon

class Elevator(Subsystem):

    def __init__(self):
        timeout = 10 #Give 10 ms to do command

        motors = [Talon(30), Talon(31)]
        
        for motor in motors:
            motor.clearStickyFaults(timeout) #Clears sticky faults
            motor.configContinuousCurrentLimit(15,timeout) #15 Amps per motor
            motor.configPeakCurrentLimit(20,timeout) #20 Amps during Peak Duration
            motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
            motor.enableCurrentLimit(True)

            motor.enableVoltageCompensation(True) #Compensates for lower voltages

            motor.configNeutralDeadband(0.05,timeout) #5% deadband

            motor.configOpenLoopRamp(3,timeout) #3 seconds from 0 to 1

            motor.configPeakOutputForward(0.9,timeout) #Max forward speed of 0.9
            motor.configPeakOutputReverse(-0.5,timeout) #Max backward speed of -0.5

        motors[1].set(Talon.ControlMode.Follower,30)
        self.motor = motors[0]

        motor.setQuadraturePosition(0,timeout)

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
