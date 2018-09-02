import wpilib
import wpilib.buttons
from wpilib.command.subsystem import Subsystem

import ctre
from ctre import WPI_TalonSRX as Talon

from commands.followjoystick import FollowJoystick

class Wrist(Subsystem):
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

    def setSpeed(self, speed):
        self.wrist.set(speed)

    def getPos(self):
        return self.wrist.getQuadraturePosition()

    def getOutputCurrent(self):
        return self.wrist.getOutputCurrent()

    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
