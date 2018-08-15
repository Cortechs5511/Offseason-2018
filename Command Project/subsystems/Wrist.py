import wpilib
from wpilib.command.subsystem import Subsystem
import ctre
import wpilib
import wpilib.buttons
from wpilib.drive import DifferentialDrive
from commands.followjoystick import FollowJoystick

class Wrist(Subsystem):
    '''
    This example subsystem controls a single Talon in PercentVBus mode.
    '''

    def __init__(self):
        '''Instantiates the motor object.'''

        super().__init__('Wrist')

        self.wrist = ctre.WPI_TalonSRX(40)


    def setSpeed(self, speed):
        self.wrist.set(speed)


    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
