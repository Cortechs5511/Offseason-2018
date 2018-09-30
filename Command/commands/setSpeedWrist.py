import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setSpeedWrist(Command):

    def __init__(self, maxtime = 300):
        super().__init__('setSpeedWrist')
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist
        SmartDashboard.putNumber("WristJoystickSpeed", 0.3)

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def execute(self):
        wristPos = self.Wrist.getAngle()
        Joystick = self.getRobot().xbox
        speed = SmartDashboard.getNumber("WristJoystickSpeed", 0.3)
        self.Wrist.setSpeed(Joystick.getX(1))

        #self.Wrist.setSpeed(Joystick.getY(2) * 1/5)

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def interrupted(self):
        self.Wrist.setSpeed(0)

    def end(self):
        self.Wrist.setSpeed(0)
