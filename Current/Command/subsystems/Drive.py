import math
import numpy as np
from typing import Any
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

    dband = 0.1
    k = -1
    maxspeed = 0.7
    DistPerPulse = 4 * np.pi / 127

    def __init__(self, DistPerPulse=DistPerPulse):
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

        self.RightEncoder = wpilib.Encoder(2,3)

        self.RightEncoder.setDistancePerPulse(DistPerPulse)


    def setParams(self, dbLimit, k, maxSpeed):
        self.dbLimit = dbLimit
        self.maxSpeed = maxSpeed
        self.k = k

    def tankDrive(self,left,right):

        if(abs(left) < self.dband):left = 0
        else: left = abs(left)/left*(math.e**(self.k*abs(left))-1) / (math.exp(self.k)-1)

        if(abs(right) < self.dband):right = 0
        else: right = abs(right)/right*(math.e**(self.k*abs(right))-1) / (math.exp(self.k)-1)

        left *= self.maxspeed
        right *= self.maxspeed * -1

        self.drive.tankDrive(left, right)

    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
