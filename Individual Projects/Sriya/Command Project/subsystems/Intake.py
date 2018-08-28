import wpilib
from wpilib.command.subsystem import Subsystem
import ctre
import wpilib
import wpilib.buttons
from wpilib.drive import DifferentialDrive
from commands.followjoystick import FollowJoystick

class Intake(Subsystem):
    '''
    This example subsystem controls a single Talon in PercentVBus mode.
    '''

    def __init__(self):
        '''Instantiates the motor object.'''

        super().__init__('Intake')

        self.intake = ctre.WPI_TalonSRX(50)
        self.intake2 = ctre.WPI_TalonSRX(51)
        self.intake2.set(ctre.WPI_TalonSRX.ControlMode.Follower, 50)


    def setSpeed(self, speed):
        self.intake.set(speed)


    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
