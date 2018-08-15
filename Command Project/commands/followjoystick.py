from wpilib.command import Command
from wpilib.drive import DifferentialDrive

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

        if self.getRobot().joystick.getRawButton(1) == True:
            self.getRobot().wrist.setSpeed(-0.3)
        elif self.getRobot().joystick.getRawButton(2) == True:
            self.getRobot().wrist.setSpeed(0.3)
        else:
            self.getRobot().wrist.setSpeed(0)

        if self.getRobot().joystick.getRawButton(3) == True:
            self.getRobot().intake.setSpeed(0.7)
        elif self.getRobot().joystick.getRawButton(4) == True:
            self.getRobot().intake.setSpeed(-0.7)
        else:
            self.getRobot().intake.setSpeed(0)

        self.getRobot().drive.tankDrive(self.getRobot().joystick.getY(), self.getRobot().joystick.getX())

