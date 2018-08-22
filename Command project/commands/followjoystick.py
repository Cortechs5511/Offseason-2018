from wpilib.command import Command
from wpilib.drive import DifferentialDrive
import math

class FollowJoystick(Command):
    '''
    This command will read the joystick's y axis and use that value to control
    the speed of the SingleMotor subsystem.
    '''


    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(self.getRobot().lift)
        self.requires(self.getRobot().wrist)
        self.requires(self.getRobot().intake)
        self.requires(self.getRobot().drive)


    def execute(self):
        self.getRobot().lift.setSpeed(self.getRobot().joystick.getZ())

        gravity = 0.2
        wspot = 22000

        LEFT = self.getRobot().joystick.getY()
        RIGHT = self.getRobot().joystick1.getY()

        if self.getRobot().wrist.getPos() > wspot:
            x = gravity
        elif self.getRobot().wrist.getPos() * -1 < wspot:
            x = gravity * -1
        else:
            x = 0

        if self.getRobot().joystick.getRawButton(1) == True:
            self.getRobot().wrist.setSpeed(-0.3 + x)
        elif self.getRobot().joystick.getRawButton(2) == True:
            self.getRobot().wrist.setSpeed(0.3 - x)
        else:
            self.getRobot().wrist.setSpeed(x)

        if self.getRobot().joystick.getRawButton(3) == True:
            self.getRobot().intake.setSpeed(0.7)
        elif self.getRobot().joystick.getRawButton(4) == True:
            self.getRobot().intake.setSpeed(-0.7)
        else:
            self.getRobot().intake.setSpeed(0)

        self.getRobot().drive.tankDrive(LEFT,RIGHT)

