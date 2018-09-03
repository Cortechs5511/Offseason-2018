import math

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.command.subsystem import Subsystem

from commands.followjoystick import FollowJoystick

#import sensors.navx as navx
import sensors.DTEncoders as encoders

class Drive(Subsystem):

    dbLimit = 0.1
    k = -1
    maxSpeed = 0.7

    DistPerPulseL = 4/12 * math.pi / 127
    DistPerPulseR = 4/12 * math.pi / 255

    def __init__(self):
        super().__init__('Drive')

        timeout = 0

        TalonLeft = Talon(10)
        TalonRight = Talon(20)

        if not wpilib.RobotBase.isSimulation():
            VictorLeft1 = Victor(11)
            VictorLeft2 = Victor(12)
            VictorLeft1.follow(TalonLeft)
            VictorLeft2.follow(TalonLeft)

            VictorRight1 = Victor(21)
            VictorRight2 = Victor(22)
            VictorRight1.follow(TalonRight)
            VictorRight2.follow(TalonRight)

            for motor in [VictorLeft1,VictorLeft2,VictorRight1,VictorRight2]:
                motor.clearStickyFaults(timeout)

        for motor in [TalonLeft,TalonRight]:
            motor.clearStickyFaults(timeout) #Clears sticky faults

            motor.configContinuousCurrentLimit(15,timeout) #15 Amps per motor
            motor.configPeakCurrentLimit(20,timeout) #20 Amps during Peak Duration
            motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(12,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

            motor.configOpenLoopRamp(0.2,timeout) #number of seconds from 0 to 1


        self.left = TalonLeft
        self.right = TalonRight

        #self.navx = navx.NavX()
        self.encoders = encoders.DTEncoders()

        #self.navx.disablePID()
        self.encoders.disablePID()

    def tankDrive(self,left,right):
        if(abs(left) < self.dbLimit): left = 0
        else: left = self.maxSpeed*abs(left)/left*(math.exp(self.k*abs(left))-1) / (math.exp(self.k)-1)

        if(abs(right) < self.dbLimit): right = 0
        else: right = self.maxSpeed*abs(right)/right*(math.exp(self.k*abs(right))-1) / (math.exp(self.k)-1)

        self.left.set(left)
        self.right.set(right)

    def getOutputCurrent(self):
        return (self.right.getOutputCurrent()+self.left.getOutputCurrent())*3

    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
