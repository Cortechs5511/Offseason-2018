import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setSpeedDT(Command):

    def __init__(self):
        super().__init__('setSpeedDT')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        SmartDashboard.putData("setSpeedDT", self)

    def execute(self):
        left = self.getRobot().joystick0.getY()
        right = self.getRobot().joystick1.getY()
        self.DT.tankDrive(left,right)

    def interrupted(self):
        self.DT.tankDrive(0,0)

    def end(self):
        self.DT.tankDrive(0,0)
