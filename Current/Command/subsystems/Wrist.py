import wpilib
import wpilib.buttons
from wpilib.command.subsystem import Subsystem

import ctre
from ctre import WPI_TalonSRX as Talon

import math

from commands.setSpeedWrist import setSpeedWrist
from commands.setPositionWrist import setPositionWrist


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

        self.wrist.setQuadraturePosition(0,timeout)

    def getAngle(self):
        return math.radians(self.wrist.getSelectedSensorPosition(0)*self.posConv)

    def getRawPosition(self):
        return self.wrist.getSelectedSensorPosition(0)

    def getGravity(self):
        gravity = -0.2
        return gravity

    def getTemp(self):
        return self.wrist.getTemperature()

    def getOutputCurrent(self):
        return self.wrist.getOutputCurrent()

    def setSpeed(self, speed):
        """ Moves wrist up if speed is negative. """
        power = speed + (self.getGravity()) *  math.sin(self.getAngle())
        self.wrist.set(power)
        self.smartDashboard.putNumber("WristPower",power)

    def initDefaultCommand(self):
        self.setDefaultCommand(setPositionWrist())
