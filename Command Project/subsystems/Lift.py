import wpilib
from wpilib.command.subsystem import Subsystem
import ctre
import wpilib
import wpilib.buttons
from wpilib.drive import DifferentialDrive
from commands.followjoystick import FollowJoystick

class Lift(Subsystem):
    '''
    This example subsystem controls a single Talon in PercentVBus mode.
    '''

    def __init__(self):
        '''Instantiates the motor object.'''

        super().__init__('Lift')


        self.lift = ctre.WPI_TalonSRX(30)
        self.Lift2 = ctre.WPI_TalonSRX(31)
        self.Lift2.set(ctre.WPI_TalonSRX.ControlMode.Follower, 30)


    def setSpeed(self, speed):
        self.lift.set(speed)


    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
