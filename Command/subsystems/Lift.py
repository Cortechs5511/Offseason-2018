import wpilib
import wpilib.buttons
from wpilib.command.subsystem import Subsystem

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor
from commands.setSpeedLift import setSpeedLift
from commands.setFixedLift import setFixedLift
from commands.setPositionLift import setPositionLift

from wpilib import SmartDashboard

import math

class Lift(Subsystem):

    posConv = 1/183 #convert from encoder count to inches

    def __init__(self, Robot):
        super().__init__('Lift')

        self.LiftEncoder = wpilib.Encoder(4,5)
        self.LiftEncoder.setSamplesToAverage(10)
        self.LiftEncoder.reset()

        self.Robot = Robot

        timeout = 0

        Talon0 = Talon(30)
        Talon1 = Talon(31)

        Talon1.follow(Talon0)

        for motor in [Talon0,Talon1]:
            motor.clearStickyFaults(timeout) #Clears sticky faults

            motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
            motor.configPeakCurrentLimit(30,timeout) #20 Amps during Peak Duration
            motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(12,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages
            motor.configOpenLoopRamp(0.2,timeout) #number of seconds from 0 to 1

        Talon0.configSelectedFeedbackSensor(0,0,timeout)
        Talon0.configVelocityMeasurementPeriod(10,timeout) #Period in ms
        Talon0.configVelocityMeasurementWindow(32,timeout) #averages 32 to get average

        self.lift = Talon0

        [kP,kI,kD,kF] = [0.275 , 0.000, 1, 0.00] # These PID parameters are used on a real robot

        self.liftController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        self.liftController.setInputRange(0, 30) #input range in inches
        self.liftController.setOutputRange(-0.8, 0.8) #output range in percent
        self.liftController.setAbsoluteTolerance(0.5) #tolerance in inches
        self.liftController.setContinuous(False)

    def pidWrite(self, output):
        self.__setSpeed__(output)

    def pidGet(self):
       pos =  self.getHeight()
       return pos

    def setPIDSourceType(self):
        return 0

    def getPIDSourceType(self):
        return 0

    def getHeight(self):
        pos = self.LiftEncoder.get()*self.posConv
        return pos

    def getGravity(self):
        return 0.14

    def getTemp(self):
        return self.lift.getTemperature()

    def getOutputCurrent(self):
        return self.lift.getOutputCurrent()*2

    def setSpeed(self, speed):
        self.liftController.disable()
        self.__setSpeed__(speed)

    def __setSpeed__(self, speed):
        maxSpeed = 0.7
        #if (speed > 0 and self.Robot.wrist.getAngle() < 0): self.lift.set(self.getGravity())
        #else: self.lift.set(maxSpeed*speed + self.getGravity())
        self.lift.set(maxSpeed*speed+self.getGravity())

    def setHeight(self, height):
        self.liftController.enable()
        self.liftController.setSetpoint(height)

    def zero(self):
        self.lift.setQuadraturePosition(0,0)

    def initDefaultCommand(self):
        self.setDefaultCommand(setSpeedLift(300))

    def UpdateDashboard(self):
        SmartDashboard.putData("Lift_PID", self.liftController)
        SmartDashboard.putNumber("Lift_Height", self.getHeight())
        SmartDashboard.putNumber("Lift_Power", self.lift.get())
        SmartDashboard.putNumber("Lift_Amps", self.getOutputCurrent())
