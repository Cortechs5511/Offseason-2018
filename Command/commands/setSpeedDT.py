import math

import wpilib
from wpilib.command import Command

class setSpeedDT(Command):

    def __init__(self, maxtime = 300):
        super().__init__('setSpeedDT')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.Joystick = self.getRobot().joystick0
        self.Joystick1 = self.getRobot().joystick1

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def execute(self):
        maxspeed = 0.90
        left = self.getRobot().joystick0.getY()
        right = self.getRobot().joystick1.getY()
        self.DT.tankDrive(-left * maxspeed ,-right * maxspeed)

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def interrupted(self):
        self.DT.tankDrive(0,0)

    def end(self):
        self.DT.tankDrive(0,0)
