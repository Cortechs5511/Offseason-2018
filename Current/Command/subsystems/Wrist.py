import wpilib
import wpilib.buttons
from wpilib.command.subsystem import Subsystem

import ctre
from ctre import WPI_TalonSRX as Talon

from commands.followjoystick import FollowJoystick

class Wrist(Subsystem):

    posConv = 1
    velConv = 1

    def __init__(self):
        super().__init__('Wrist')
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

    def setSpeed(self, speed):
        self.wrist.set(speed)

    def getData(self):
        pos = self.wrist.getSelectedSensorPosition(0)
        vel = self.wrist.getSelectedSensorVelocity(0)
        return [pos,vel]

    def getDataUnits(self):
        pos = self.getData()[0]*self.posConv
        vel = self.getData()[1]*self.velConv
        return [pos,vel]

    def getTemp(self):
        return self.wrist.getTemperature()

    def getOutputCurrent(self):
        return self.wrist.getOutputCurrent()

    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
