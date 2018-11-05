import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class setPositionWrist(TimedCommand):

    def __init__(self, setpoint = 0, timeout = 300):
        super().__init__('setPositionWrist', timeoutInSeconds = timeout)
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist
        self.setpoint = setpoint

    def execute(self):
        if(self.setpoint >= 90 and self.Wrist.getAngle() > (math.pi / 4)): self.Wrist.setSpeedNoG(0)
        else: self.Wrist.setAngle(self.setpoint)

    def interrupted(self):
        self.end()

    def end(self):
        self.Wrist.setSpeed(0)
