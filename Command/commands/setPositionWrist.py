import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setPositionWrist(Command):

    def __init__(self, setpoint = 0, Debug = False, maxtime = 300):
        super().__init__('setPositionWrist')
        self.setpoint = setpoint
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist

        if Debug == True:
            SmartDashboard.putData("setPositionWrist", self)

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def execute(self):
        if(self.setpoint == 90 and self.Wrist.getAngle() > (math.pi / 4)):
            self.Wrist.setSpeedNoG(0)
        else:
            self.Wrist.setAngle(self.setpoint)

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def interrupted(self):
        self.Wrist.setSpeed(0)

    def end(self):
        self.Wrist.setSpeed(0)
