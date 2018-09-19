import wpilib
import wpilib.buttons
from wpilib.command.subsystem import Subsystem

import ctre
from ctre import WPI_TalonSRX as Talon

import math

from commands.setFixedWrist import setFixedWrist
from commands.setPositionWrist import setPositionWrist

from wpilib import LiveWindow
from wpilib import SmartDashboard

class Wrist(Subsystem):

    posConv = 1/2222

    def __init__(self,Robot):
        super().__init__('Wrist')
        SmartDashboard.putNumber("WristPowerPercentage", 0.4)
        SmartDashboard.putNumber("WristGravity", -0.4)
        timeout = 0

        self.wrist = Talon(40)

        LiveWindow.addActuator("Wrist", "Motor", self.wrist)
        self.wrist.clearStickyFaults(timeout)
        self.wrist.configContinuousCurrentLimit(15,timeout)
        self.wrist.configPeakCurrentLimit(20,timeout)
        self.wrist.configPeakCurrentDuration(100, timeout)
        self.wrist.enableCurrentLimit(True)

        self.wrist.configVoltageCompSaturation(6,timeout) #Sets saturation value
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
        gravity = SmartDashboard.getNumber("WristGravity", -0.4) #Remain constant -2.4 V (take into account VoltageCompSaturation)
        return gravity

    def getTemp(self):
        return self.wrist.getTemperature()

    def getOutputCurrent(self):
        return self.wrist.getOutputCurrent()

    def setSpeed(self, speed):
        """ Moves wrist up if speed is negative. """
        powerpercentage = SmartDashboard.getNumber("WristPowerPercentage", 0.4)
        power = (powerpercentage * (speed)) + (self.getGravity()) *  (math.sin(self.getAngle()) * (1-powerpercentage))
        self.wrist.set(power)
        SmartDashboard.putNumber("WristPower",power)

    def setSpeed2(self, speed):
        power = speed + self.getGravity() * math.sin(self.getAngle())

    def zero(self):
        self.lift.setQuadraturePosition(0)

    def initDefaultCommand(self):
        self.setDefaultCommand(setFixedWrist(0,))
        SmartDashboard.putData("WristCommand", self)
