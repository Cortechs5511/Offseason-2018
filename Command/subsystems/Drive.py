import math

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from navx import AHRS as navx

import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem

from commands.diffDrive import diffDrive
from commands.setSpeedDT import setSpeedDT
from commands.setFixedDT import setFixedDT

from sim import simComms

from CRLibrary.physics import DCMotorTransmission as DCMotor
from CRLibrary.physics import DifferentialDrive as dDrive
from CRLibrary.path import odometry as od
from CRLibrary.path import Path
from CRLibrary.util import units as units

class Drive(Subsystem):

    mode = ""

    distPID = 0
    anglePID = 0

    prevDist = [0,0]

    maxSpeed = 1

    model = None

    navxVal = 0
    leftVal = 0
    rightVal = 0

    leftConv = 4/12 * math.pi / 255
    rightConv = -4/12 * math.pi / 127

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
        self.leftEncoder.setDistancePerPulse(self.leftConv)
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = wpilib.Encoder(2,3)
        self.rightEncoder.setDistancePerPulse(self.rightConv)
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
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.020,0.00,0.00,0.00]
        angleController = wpilib.PIDController(kP, kI, kD, kF, source=self.__getAngle__, output=self.__setAngle__)
        angleController.setInputRange(-180,  180) #degrees
        angleController.setOutputRange(-0.9, 0.9)
        angleController.setAbsoluteTolerance(self.TolAngle)
        angleController.setContinuous(True)
        self.angleController = angleController
        self.angleController.disable()

        self.od = od.Odometer()

        transmission = DCMotor.DCMotorTransmission(8.3, 2.22, 1.10) #8.02, 2.22, 1.10
        self.model = dDrive.DifferentialDrive(64, 10, 0, units.inchesToMeters(2.0), units.inchesToMeters(14), transmission, transmission)
        self.maxVel = self.maxSpeed*self.model.getMaxAbsVelocity(0, 0, 12)
        #print("Max Velocity: "+ str(self.maxVel))

        self.Path = Path.Path(self, self.model, self.od, self.getDistance)

    def __getDistance__(self):
        return self.getAvgDistance()

    def __setDistance__(self,output):
        self.distPID = output

    def __getAngle__(self):
        return self.getAngle()

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
        elif(mode=="Path"):
            self.distController.disable()
            self.angleController.disable()
            self.Path.initPath(name)
        elif(mode=="DiffDrive"):
            self.distController.disable()
            self.angleController.disable()
        elif(mode=="Direct"):
            self.distController.disable()
            self.angleController.disable()
        self.mode = mode

    def setDistance(self, distance):
        self.setMode("Distance",distance=distance)

    def setAngle(self, angle):
        self.setMode("Angle",angle=angle)

    def setCombined(self, distance, angle):
        self.setMode("Combined",distance=distance,angle=angle)

    def setPath(self, name, follower):
        self.Path.setFollower(follower)
        self.setMode("Path", name=name)

    def setDiffDrive(self):
        self.setMode("DiffDrive")

    def setDirect(self):
        self.setMode("Direct")

    def sign(self,num):
        if(num>0): return 1
        if(num==0): return 0
        return -1

    def tankDrive(self,left=0,right=0):
        self.updateSensors()
        if(self.mode=="Distance"):
            [left,right] = [self.distPID,self.distPID]
        elif(self.mode=="Angle"):
            [left,right] = [self.anglePID,-self.anglePID]
        elif(self.mode=="Combined"):
            [left,right] = [self.distPID+self.anglePID,self.distPID-self.anglePID]
        elif(self.mode=="Path"):
            [left, right] = self. Path.followPath()
        elif(self.mode=="DiffDrive"):
            wheelVelocity = dDrive.WheelState(left*self.maxVel/self.model.wheelRadius(), right*self.maxVel/self.model.wheelRadius())
            wheelAcceleration = dDrive.WheelState(0, 0) #Add better math here later
            voltage = self.model.solveInverseDynamics_WS(wheelVelocity, wheelAcceleration).getVoltage()
            [left, right] = [voltage[0]/12, voltage[1]/12]
        elif(self.mode=="Direct"):
            [left, right] = [left, right] #Add advanced logic here
        else:
            [left, right] = [0,0]

        left = min(abs(left),self.maxSpeed)*self.sign(left)
        right = min(abs(right),self.maxSpeed)*self.sign(right)

        self.__tankDrive__(left,right)

    def __tankDrive__(self,left,right):
        self.left.set(left)
        self.right.set(right)

        self.updateOdometry(left, right)

    def updateOdometry(self, left, right):
        vel = self.getVelocity()
        self.od.update(vel[0],vel[1],self.getAngle())
        self.prevDist = self.getDistance()

    def getOutputCurrent(self):
        return (self.right.getOutputCurrent()+self.left.getOutputCurrent())*3

    def updateSensors(self):
        self.leftVal = self.leftEncoder.get()
        self.rightVal = self.rightEncoder.get()
        self.navxVal = self.navx.getYaw()
        #self.navxVal = 0

    def getAngle(self):
        return self.navxVal

    def getRaw(self):
        return [self.leftVal, self.rightVal]

    def getDistance(self):
        return [self.leftVal*self.leftConv, self.rightVal*self.rightConv]

    def getAvgDistance(self):
        return (self.getDistance()[0]+self.getDistance()[1])/2

    def getVelocity(self):
        velocity = [30*(self.getDistance()[0]-self.prevDist[0]),30*(self.getDistance()[1]-self.prevDist[1])]
        self.prevDist = self.getDistance()
        return velocity

    '''
    def getVelocity(self):
        return [self.leftEncoder.getRate(), self.rightEncoder.getRate()] #Test if this works at meeting, does not work in sim
    '''

    def getAvgVelocity(self):
        return (self.getVelocity()[0]+self.getVelocity()[1])/2

    def getAvgAbsVelocity(self):
        return (abs(self.getVelocity()[0])+abs(self.getVelocity()[1]))/2

    def zeroEncoders(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        simComms.resetEncoders()

    def zeroNavx(self):
        self.navx.zeroYaw()
        #pass

    def zero(self):
        self.zeroEncoders()
        self.zeroNavx()

    def initDefaultCommand(self):
        self.setDefaultCommand(diffDrive(timeout = 300))
        #self.setDefaultCommand(setSpeedDT(timeout = 300))
        #pass

    def UpdateDashboard(self):
        #SmartDashboard.putData("DT_DistPID", self.distController)
        #SmartDashboard.putData("DT_AnglePID", self.angleController)

        SmartDashboard.putNumber("DT_DistanceAvg", self.getAvgDistance())
        #SmartDashboard.putNumber("DT_DistanceLeft", self.getDistance()[0])
        #SmartDashboard.putNumber("DT_DistanceRight", self.getDistance()[1])
        #SmartDashboard.putNumber("DT_Angle", self.getAngle())

        #SmartDashboard.putNumber("DT_PowerLeft", self.left.get())
        #SmartDashboard.putNumber("DT_PowerRight", self.right.get())

        #SmartDashboard.putNumber("DT_VelocityLeft", self.getVelocity()[0])
        #SmartDashboard.putNumber("DT_VelocityRight", self.getVelocity()[1])

        #SmartDashboard.putNumber("DT_CounLeft", self.getRaw()[0])
        #SmartDashboard.putNumber("DT_CountRight", self.getRaw()[1])

        #SmartDashboard.putNumber("DriveAmps",self.getOutputCurrent())
