import math

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from navx import AHRS as navx

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.command.subsystem import Subsystem

from commands.setSpeedDT import setSpeedDT
from commands.setFixedDT import setFixedDT

from sim import simComms

from wpilib import SmartDashboard

class Drive(Subsystem):

    mode = ""

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

        self.navx = navx.create_spi()

        self.leftEncoder = wpilib.Encoder(0,1)
        self.leftEncoder.setDistancePerPulse(4/12 * math.pi / 255)
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = wpilib.Encoder(2,3)
        self.rightEncoder.setDistancePerPulse(-4/12 * math.pi / 127)
        self.rightEncoder.setSamplesToAverage(10)

        self.TolDist = 0.2 #feet
        [kP,kI,kD,kF] = [0.07, 0.0, 0.20, 0.00]
        distController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        distController.setInputRange(0,  50) #feet
        distController.setOutputRange(-0.55, 0.55)
        distController.setAbsoluteTolerance(self.TolDist)
        distController.setContinuous(False)
        self.distController = distController
        self.distController.disable()

        self.TolAngle = 3 #degrees
        [kP,kI,kD,kF] = [0.024,0,0.2,0]

        angleController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        angleController.setInputRange(-180,  180) #degrees
        angleController.setOutputRange(-0.8, 0.8)
        angleController.setAbsoluteTolerance(self.TolAngle)
        angleController.setContinuous(True)
        self.angleController = angleController
        self.angleController.disable()

    def pidWrite(self, output):
        if(self.mode == "Distance"):
            nominal = 0.2
            if output < nominal and output > 0: output = nominal
            elif output > -nominal and output < 0: output = -nominal
            self.__tankDrive__(output,output)
        elif(self.mode == "Angle"):
            nominal = 0#nominal = 0.27
            if output < nominal and output > 0: output = nominal
            elif output > -nominal and output < 0: output = -nominal
            self.__tankDrive__(output,-output)

    def getPIDSourceType(self):
        if(self.mode == "Distance"): return self.getAvgDistance()
        elif(self.mode == "Angle"): return self.getAngle()
        else: return 0

    def pidGet(self):
        if(self.mode == "Distance"): return self.getAvgDistance()
        elif(self.mode == "Angle"): return self.getAngle()
        else: return 0

    def tankDrive(self,left,right):
        self.distController.disable()
        self.angleController.disable()
        self.__tankDrive__(left,right)

    def __tankDrive__(self,left,right):
        RightGain = 0.9
        maxSpeed = 0.7
        self.left.set(maxSpeed * left)
        self.right.set(maxSpeed * right * RightGain)

    def setDistance(self,distance):
        self.distController.setSetpoint(distance)
        self.angleController.disable()
        self.distController.enable()
        self.mode = "Distance"

    def setAngle(self,angle):
        self.angleController.setSetpoint(angle)
        self.distController.disable()
        self.angleController.enable()
        self.mode = "Angle"

    def getOutputCurrent(self):
        return (self.right.getOutputCurrent()+self.left.getOutputCurrent())*3

    def getDistance(self):
        return [self.leftEncoder.getDistance(),self.rightEncoder.getDistance()]

    def getAvgDistance(self):
        return self.getDistance()[1] #One encoder broken

    def getAvgVelocity(self):
        return self.rightEncoder.getRate() #feet per second, one encoder broken

    def getAvgAbsVelocity(self):
        return abs(self.rightEncoder.getRate()) #feet per second, one encoder broken

    def zeroEncoders(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        simComms.resetEncoders()

    def zeroNavx(self):
        self.navx.zeroYaw()

    def zero(self):
        self.zeroEncoders()
        self.zeroNavx()

    def getAngle(self):
        return self.navx.getYaw()

    def initDefaultCommand(self):
        self.setDefaultCommand(setSpeedDT(timeout = 300))

    def UpdateDashboard(self):
        SmartDashboard.putData("DT_DistPID", self.distController)
        SmartDashboard.putData("DT_AnglePID", self.angleController)

        SmartDashboard.putNumber("DT_DistanceAvg", self.getAvgDistance())
        SmartDashboard.putNumber("DT_DistanceLeft", self.getDistance()[0])
        SmartDashboard.putNumber("DT_DistanceRight", self.getDistance()[1])
        SmartDashboard.putNumber("DT_Angle", self.getAngle())

        SmartDashboard.putNumber("DT_PowerLeft", self.left.get())
        SmartDashboard.putNumber("DT_PowerRight", self.right.get())

        SmartDashboard.putNumber("DriveAmps",self.getOutputCurrent())
