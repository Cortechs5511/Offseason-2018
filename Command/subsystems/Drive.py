import math

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from navx import AHRS as navx

import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem

from commands.setSpeedDT import setSpeedDT
from commands.setFixedDT import setFixedDT

import pathfinder as pf
from path import path

from sim import simComms

class Drive(Subsystem):

    mode = ""
    distPID = 0
    anglePID = 0
    spline = None

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
        [kP,kI,kD,kF] = [0.07, 0.00, 0.20, 0.00]
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.40, 0.00, 1.50, 0.00]
        distController = wpilib.PIDController(kP, kI, kD, kF, source=self.__getDistance__, output=self.__setDistance__)
        distController.setInputRange(0, 50) #feet
        distController.setOutputRange(-0.9, 0.9)
        distController.setAbsoluteTolerance(self.TolDist)
        distController.setContinuous(False)
        self.distController = distController
        self.distController.disable()

        self.TolAngle = 3 #degrees
        [kP,kI,kD,kF] = [0.024, 0.00, 0.20, 0.00]
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.02,0.00,0.20,0.00]
        angleController = wpilib.PIDController(kP, kI, kD, kF, source=self.__getAngle__, output=self.__setAngle__)
        angleController.setInputRange(-180,  180) #degrees
        angleController.setOutputRange(-0.9, 0.9)
        angleController.setAbsoluteTolerance(self.TolAngle)
        angleController.setContinuous(True)
        self.angleController = angleController
        self.angleController.disable()

    def __getDistance__(self):
        return self.getAvgDistance()

    def __setDistance__(self,output):
        self.distPID = output

    def __getAngle__(self):
        return self.getAngle()

    def getVelocity(self):
        return self.rightEncoder.getRate()

    def __setAngle__(self,output):
        self.anglePID = output

    def setMode(self, mode, name=None, distance=0, angle=0):
        self.distPID = 0
        self.anglePID = 0
        if(mode=="Distance"):
            self.distController.setSetpoint(distance)
            self.angleController.disable()
            self.distController.enable()
        elif(mode=="Angle"):
            self.angleController.setSetpoint(angle)
            self.distController.disable()
            self.angleController.enable()
        elif(mode=="Combined"):
            self.distController.setSetpoint(distance)
            self.angleController.setSetpoint(angle)
            self.distController.enable()
            self.angleController.enable()
        elif(mode=="PathFinder"):
            self.spline = path.initPath(self, name)
            self.distController.disable()
            self.angleController.disable()
        elif(mode=="Direct"):
            self.distController.disable()
            self.angleController.disable()
        self.mode = mode

    def setDistance(self,distance):
        self.setMode("Distance",distance=distance)

    def setAngle(self,angle):
        self.setMode("Angle",angle=angle)

    def setCombined(self,distance,angle):
        self.setMode("Combined",distance=distance,angle=angle)

    def setPathFinder(self,name):
        self.setMode("PathFinder", name=name)

    def setDirect(self):
        self.setMode("Direct")

    def sign(self,num):
        if(num>0): return 1
        if(num==0): return 0
        return -1

    def tankDrive(self,left=0,right=0):
        if(self.mode=="Distance"):
            [left,right] = [self.distPID,self.distPID]
        if(self.mode=="Angle"):
            [left,right] = [self.anglePID,-self.anglePID]
        if(self.mode=="Combined"):
            [left,right] = [self.distPID+self.anglePID,self.distPID-self.anglePID]
        if(self.mode=="PathFinder"):
            '''
            angle = pf.r2d(self.spline[0].getHeading())
            if(angle>180): angle=360-angle
            else: angle=-angle

            self.angleController.setSetpoint(angle)
            '''
            [left,right] = path.followPath(self,self.spline[0],self.spline[1])
            left=right
            #[left,right] = [left+self.anglePID,right-self.anglePID]

        left = min(abs(left),1)*self.sign(left)
        right = min(abs(right),1)*self.sign(right)

        self.__tankDrive__(left,right)

    def __tankDrive__(self,left,right):
        RightGain = 0.9
        if wpilib.RobotBase.isSimulation(): RightGain = 1

        maxSpeed = 0.7

        self.left.set(maxSpeed * left)
        self.right.set(maxSpeed * right * RightGain)

    def getOutputCurrent(self):
        return (self.right.getOutputCurrent()+self.left.getOutputCurrent())*3

    def getRaw(self):
        return [self.leftEncoder.get(),self.rightEncoder.get()]

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
