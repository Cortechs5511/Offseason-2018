import wpilib
from wpilib.command.subsystem import Subsystem
import ctre
import wpilib
import wpilib.buttons
from wpilib.drive import DifferentialDrive
from commands.followjoystick import FollowJoystick
from ctre import WPI_TalonSRX

class Lift(Subsystem):
    '''
    This example subsystem controls a single Talon in PercentVBus mode.
    '''

    def __init__(self):
        '''Instantiates the motor object.'''

        super().__init__('Lift')

        self.lift = ctre.WPI_TalonSRX(30)
        self.Lift2 = ctre.WPI_TalonSRX(31)
        self.Lift2.set(WPI_TalonSRX.ControlMode.Follower,30)

        motors = [WPI_TalonSRX(31)]

        for motor in motors:
            motor.clearStickyFaults(0)
            motor.configContinuousCurrentLimit(15,0)
            motor.configPeakCurrentLimit(20,0)
            motor.configPeakCurrentDuration(100, 0)
            motor.enableCurrentLimit(True)

            motor.enableVoltageCompensation(True)
            motor.configOpenLoopRamp(3, 0)

    def setSpeed(self, speed):
        self.lift.set(speed)


    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
