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

        self.wrist.clearStickyFaults(0)
        self.wrist.configContinuousCurrentLimit(15,0)
        self.wrist.configPeakCurrentLimit(20,0)
        self.wrist.configPeakCurrentDuration(100, 0)
        self.wrist.enableCurrentLimit(True)

        self.wrist.enableVoltageCompensation(True)
        self.wrist.configOpenLoopRamp(3, 0)

    def setSpeed(self, speed):
        self.wrist.set(speed)

    def getPos(self):
        return self.wrist.getQuadraturePosition()

    def getOutputCurrent(self):
        return self.wrist.getOutputCurrent()

    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
