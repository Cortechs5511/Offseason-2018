import math

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.command.subsystem import Subsystem

from commands.setSpeedDT import setSpeedDT
from commands.setFixedDT import setFixedDT

import sensors.navx as navx
import sensors.DTEncoders as encoders

from wpilib import SmartDashboard

class Drive(Subsystem):

    dbLimit = 0.1
    k = -1
    maxSpeed = 0.7

    DistPerPulseL = 4/12 * math.pi / 127
    DistPerPulseR = 4/12 * math.pi / 255

    def __init__(self, Robot):
        super().__init__('Drive')
        SmartDashboard.putNumber("RightGain", 0.9)
        timeout = 0
        TalonLeft = Talon(10)
        TalonRight = Talon(20)
        TalonLeft.setSafetyEnabled(False)
        TalonRight.setSafetyEnabled(False)

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
                motor.setSafetyEnabled(False)
                motor.setInverted(True)

        for motor in [TalonLeft,TalonRight]:
            motor.setInverted(True)
            motor.setSafetyEnabled(False)
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

        self.navx = navx.NavX()
        self.encoders = encoders.DTEncoders()

        self.navx.disablePID()
        self.encoders.disablePID()

        self.TolDist = 0.2 #feet
        [kP,kI,kD,kF] = [0.07, 0.0, 0.20, 0.00]
        distController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        distController.setInputRange(0,  50) #feet
        distController.setOutputRange(-0.55, 0.55)
        distController.setAbsoluteTolerance(self.TolDist)
        distController.setContinuous(False)
        self.distController = distController
        self.distController.disable()

    def pidWrite(self, output):
        nominal = 0.2
        if output < nominal and output > 0: output = nominal
        elif output > -nominal and output < 0: output = -nominal
        self.__tankDrive__(output,output)

    def getPIDSourceType(self):
        return self.getAvgDistance()

    def pidGet(self):
        return self.getAvgDistance()

    def tankDrive(self,left,right):
        self.distController.disable()
        self.__tankDrive__(left,right)

    def __tankDrive__(self,left,right):
        RightGain = 0.9
        self.left.set(left)
        self.right.set(right* RightGain)

    def setDistance(self,distance):
        self.distController.setSetpoint(distance)
        self.distController.enable()

    def getOutputCurrent(self):
        return (self.right.getOutputCurrent()+self.left.getOutputCurrent())*3

    def getDistance(self):
        return self.encoders.getDistance()

    def getAvgDistance(self):
        return self.encoders.getAvgDistance()

    def getAngle(self):
        return self.navx.getAngle()

    def initDefaultCommand(self):
        self.setDefaultCommand(setSpeedDT())

    def UpdateDashboard(self):
        SmartDashboard.putData("DT_DrivePID", self.encoders.PIDController)
        SmartDashboard.putNumber("DT_AverageDistance", self.getAvgDistance())
        SmartDashboard.putNumber("DT_PowerLeft", self.left.get())
        SmartDashboard.putNumber("DT_PowerRight", self.right.get())
        SmartDashboard.putNumber("DT_EncoderCountsLeft", self.encoders.getDistance()[0])
        SmartDashboard.putNumber("DT_EncoderCountsRight", self.encoders.getDistance()[1])
        SmartDashboard.putNumber("DT_Angle", self.getAngle())
