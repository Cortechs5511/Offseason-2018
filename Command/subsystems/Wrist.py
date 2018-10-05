import wpilib
import wpilib.buttons
from wpilib.command.subsystem import Subsystem

import ctre
from ctre import WPI_TalonSRX as Talon

import math

from commands.setFixedWrist import setFixedWrist
from commands.setPositionWrist import setPositionWrist

from wpilib import LiveWindow
from wpilib import SmartDashboard

class Wrist(Subsystem):

    posConv = 1/2222

    def __init__(self,Robot):
        super().__init__('Wrist')
        SmartDashboard.putNumber("WristPowerPercentage", 0.4)
        SmartDashboard.putNumber("WristGravity", -0.4)
        timeout = 0

        self.wrist = Talon(40)

        LiveWindow.addActuator("Wrist", "Motor", self.wrist)
        self.wrist.clearStickyFaults(timeout)
        self.wrist.configContinuousCurrentLimit(15,timeout)
        self.wrist.configPeakCurrentLimit(20,timeout)
        self.wrist.configPeakCurrentDuration(100, timeout)
        self.wrist.enableCurrentLimit(True)

        self.wrist.configVoltageCompSaturation(7,timeout) #Sets saturation value
        self.wrist.enableVoltageCompensation(True)
        #self.wrist.configOpenLoopRamp(3, timeout)

        self.wrist.configSelectedFeedbackSensor(0,0,timeout)
        self.wrist.configVelocityMeasurementPeriod(10,timeout) #Period in ms
        self.wrist.configVelocityMeasurementWindow(32,timeout) #averages 32 to get average

        self.wrist.setQuadraturePosition(0,timeout)

        [kP,kI,kD,kF] = [0.60, 0.00, 5.00, 0.00]

        self.wristController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        self.wristController.setInputRange(-30, 120) #input range in degrees
        self.wristController.setOutputRange(-0.8, 0.8) #output range in percent
        self.wristController.setAbsoluteTolerance(2.0) #tolerance in degrees
        self.wristController.setContinuous(False)

    def pidGet(self):
        return self.getAngle()

    def setPIDSourceType(self):
        return 0

    def getPIDSourceType(self):
        return 0

    def pidWrite(self, output):
        SmartDashboard.putNumber("WristError", self.wristController.getError())
        angle = self.getAngle()
        if output > 0 and angle > 0:
            output = min(output, 0.25) + math.cos(angle) * 0.25 * output
        elif output < 0 and angle > 0:
            output = -1
        elif output < 0 and angle < 0:
            output = max(output, -0.25)
        SmartDashboard.putNumber("WristPID_Out", output)
        self.__setSpeed__(output)

    def getAngle(self):
        #SmartDashboard.putNumber("WristGravity", math.radians(self.wrist.getSelectedSensorPosition(0)*self.posConv))
        #SmartDashboard.putNumber("WristAngle", self.wrist.getSelectedSensorPosition(0)*self.posConv)
        return math.radians(self.wrist.getSelectedSensorPosition(0)*self.posConv)

    def getRawPosition(self):
        return self.wrist.getSelectedSensorPosition(0)

    def getGravity(self):
        gravity = SmartDashboard.getNumber("WristGravity", -0.4) #Remain constant -2.4 V (take into account VoltageCompSaturation)
        return gravity

    def getTemp(self):
        return self.wrist.getTemperature()

    def getOutputCurrent(self):
        return self.wrist.getOutputCurrent()

    def setSpeed(self,speed):
        self.wristController.disable()
        self.__setSpeed__(speed)

    def __setSpeed__(self, speed):
        """ Moves wrist up if speed is negative. """
        powerpercentage = SmartDashboard.getNumber("WristPowerPercentage", 0.7)
        power = (powerpercentage * (speed)) + (self.getGravity()) *  (math.sin(self.getAngle()) * (1-powerpercentage))
        self.wrist.set(power)
        SmartDashboard.putNumber("WristPower",power)

    def setSpeedNoG(self,speed):
        self.wristController.disable()
        self.__setSpeedNoG__(speed)

    def __setSpeedNoG__(self, speed):
        self.wrist.set(speed)

    def setAngle(self, angle):
        self.wristController.setSetpoint(angle)
        self.wristController.enable()

    def zero(self):
        self.wrist.setQuadraturePosition(0,0)

    def initDefaultCommand(self):
        self.setDefaultCommand(setFixedWrist(0, timeout = 300))
