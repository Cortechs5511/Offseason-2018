import wpilib
from wpilib.command.subsystem import Subsystem
import ctre
import wpilib
import wpilib.buttons
from wpilib.drive import DifferentialDrive
from commands.followjoystick import FollowJoystick

class Drive(Subsystem):
    '''
    This example subsystem controls a single Talon in PercentVBus mode.
    '''

    def __init__(self):
        '''Instantiates the motor object.'''

        super().__init__('Drive')

        self.DriveLeft1 = ctre.WPI_TalonSRX(10)
        self.DriveLeft2 = ctre.WPI_VictorSPX(11)
        self.DriveLeft3 = ctre.WPI_VictorSPX(12)
        self.DriveLeft2.set(ctre.WPI_VictorSPX.ControlMode.Follower, 10)
        self.DriveLeft3.set(ctre.WPI_VictorSPX.ControlMode.Follower, 10)

        self.DriveRight1 = ctre.WPI_TalonSRX(20)
        self.DriveRight2 = ctre.WPI_VictorSPX(21)
        self.DriveRight3 = ctre.WPI_VictorSPX(22)
        self.DriveRight2.set(ctre.WPI_VictorSPX.ControlMode.Follower, 20)
        self.DriveRight3.set(ctre.WPI_VictorSPX.ControlMode.Follower, 20)

        self.left = wpilib.SpeedControllerGroup(self.DriveLeft1)
        self.right = wpilib.SpeedControllerGroup(self.DriveRight1)

        self.drive = DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)


    def tankDrive(self, leftSpeed, rightSpeed,):
        self.drive.tankDrive(leftSpeed, rightSpeed)



    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
