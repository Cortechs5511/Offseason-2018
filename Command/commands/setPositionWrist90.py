import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setPositionWrist90(Command):

    def __init__(self, Debug = False, maxtime = 300):
        super().__init__('setPositionWrist90')
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist


        if Debug == True:
            SmartDashboard.putData("setPositionWrist90", self)

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def execute(self):
        angle = self.Wrist.getAngle()

        if angle > (math.pi / 4):
            self.Wrist.setSpeedNoG(0)
        else:
            self.Wrist.setSpeedNoG(0.55)

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def interrupted(self):
        self.Wrist.setSpeed(0)

    def end(self):
        self.Wrist.setSpeed(0)
