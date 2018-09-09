import wpilib
import wpilib.buttons
from wpilib.command.subsystem import Subsystem

import ctre
from ctre import WPI_TalonSRX as Talon

import math

from commands.setSpeedWrist import setSpeedWrist

from networktables import NetworkTables

class Wrist(Subsystem):

    posConv = 1/2222

    def __init__(self):
        super().__init__('Wrist')

        self.smartDashboard = NetworkTables.getTable("SmartDashboard")

        timeout = 0

        self.wrist = Talon(40)

        self.wrist.clearStickyFaults(timeout)
        self.wrist.configContinuousCurrentLimit(15,timeout)
        self.wrist.configPeakCurrentLimit(20,timeout)
        self.wrist.configPeakCurrentDuration(100, timeout)
        self.wrist.enableCurrentLimit(True)

        self.wrist.configVoltageCompSaturation(12,timeout) #Sets saturation value
        self.wrist.enableVoltageCompensation(True)
        #self.wrist.configOpenLoopRamp(3, timeout)

        self.wrist.configSelectedFeedbackSensor(0,0,timeout)
        self.wrist.configVelocityMeasurementPeriod(10,timeout) #Period in ms
        self.wrist.configVelocityMeasurementWindow(32,timeout) #averages 32 to get average

    def getAngle(self):

        return pos


    def getGravity(self):
        gravity = 0.17
        if self.getAngle() < 0:
            return gravity * 1
        else:
            return gravity * -1


    def getTemp(self):
        return self.wrist.getTemperature()

    def getOutputCurrent(self):
        return self.wrist.getOutputCurrent()

    def setSpeed(self, speed):
        self.wrist.set(speed+self.getGravity())

    def initDefaultCommand(self):
        self.setDefaultCommand(setSpeedWrist())
