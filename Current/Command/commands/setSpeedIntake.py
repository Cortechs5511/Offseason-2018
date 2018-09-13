import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setSpeedIntake(Command):

    def __init__(self):
        super().__init__('SetSpeedIntake')
        self.requires(self.getRobot().intake)
        self.Intake = self.getRobot().intake
        SmartDashboard.putData("setSpeedIntake", self)

    def execute(self):
        Joystick = self.getRobot().xbox
        if Joystick.getTriggerAxis(0) == True: self.Intake.setSpeed(0.7)
        elif Joystick.getTriggerAxis(1) == True: self.Intake.setSpeed(-0.7)
        else: self.Intake.setSpeed(0)

    def interrupted(self):
        self.Intake.setSpeed(0)

    def end(self):
        self.Intake.setSpeed(0)
