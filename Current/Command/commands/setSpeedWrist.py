import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setSpeedWrist(Command):

    def __init__(self):
        super().__init__('setSpeedWrist')
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist
        SmartDashboard.putData("setSpeedWrist", self)

    def execute(self):
        wristPos = self.Wrist.getAngle()
        Joystick = self.getRobot().xbox
        '''if Joystick.getXButton()==True and wristPos < 120: self.Wrist.setSpeed(0.4)
        elif Joystick.getBButton()==True and wristPos > -30: self.Wrist.setSpeed(0.4)
        else: self.Wrist.setSpeed(0)
        '''
        self.Wrist.setSpeed(Joystick.getY(2) * 1/5)

    def interrupted(self):
        self.Wrist.setSpeed(0)

    def end(self):
        self.Wrist.setSpeed(0)
