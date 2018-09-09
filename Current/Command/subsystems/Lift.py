import wpilib
import wpilib.buttons
from wpilib.command.subsystem import Subsystem
from networktables import NetworkTables

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from commands.setSpeedLift import setSpeedLift

class Lift(Subsystem):

    posConv = 1/2380 #convert from encoder count to inches

    def __init__(self):
        super().__init__('Lift')

        self.smartDashboard = NetworkTables.getTable("SmartDashboard")

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

    def getLiftGravity(self):
        return self.smartDashboard.getNumber("liftGravity", 0.0)
        #return 0.17

    def getHeight(self):
        pos = self.lift.getSelectedSensorPosition(0)*self.posConv
        self.smartDashboard.putNumber("liftHeight",pos)
        return pos

    def getTemp(self):
        return self.lift.getTemperature()

    def getOutputCurrent(self):
        return self.lift.getOutputCurrent()*2

    def setSpeed(self, speed):
        self.lift.set(speed+self.getLiftGravity())

    def initDefaultCommand(self):
        self.setDefaultCommand(setSpeedLift())
