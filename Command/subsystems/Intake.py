import wpilib
import wpilib.buttons
from wpilib.command.subsystem import Subsystem

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from commands.setFixedIntake import setFixedIntake

from wpilib import SmartDashboard

class Intake(Subsystem):

    def __init__(self, Robot):
        super().__init__('Intake')

        timeout = 0

        TalonLeft = Talon(50)
        TalonRight = Talon(51)

        TalonRight.follow(TalonLeft)

        for motor in [TalonLeft,TalonRight]:
            motor.clearStickyFaults(timeout) #Clears sticky faults

            motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
            motor.configPeakCurrentLimit(30,timeout) #20 Amps during Peak Duration
            motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(12,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages
            #motor.configOpenLoopRamp(0.2,timeout) #number of seconds from 0 to 1

        self.intake = TalonLeft

    def setSpeed(self, speed):
        self.intake.set(speed)

    def getOutputCurrent(self):
        return self.intake.getOutputCurrent()*2

    def initDefaultCommand(self):
        self.setDefaultCommand(setFixedIntake(speed = 0, timeout = 300))

    def UpdateDashboard(self):
        #SmartDashboard.putNumber("Intake_Power", self.intake.get())
        #SmartDashboard.putNumber("Intake_Amps", self.getOutputCurrent())
        pass
