import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setPositionWrist(Command):

    def __init__(self, setpoint = 0):
        super().__init__('setPositionWrist')
        self.setpoint = setpoint
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist

        SmartDashboard.putNumber("kPWrist", 0.01 )

        [kP,kI,kD,kF] = [SmartDashboard.getNumber("kPWrist", 0.01), 0.00, 0.00, 0.00]

        self.wristController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        self.wristController.setInputRange(-30, 120) #input range in degrees
        self.wristController.setOutputRange(-0.8, 0.8) #output range in percent
        self.wristController.setAbsoluteTolerance(5.0) #tolerance in degrees
        self.wristController.setContinuous(False)

        SmartDashboard.putData("WristPID", self.wristController)
        SmartDashboard.putData("setPositionWrist", self)

    def pidGet(self):
        return self.Wrist.getAngle()

    def enablePID(self):
        self.wristController.enable()

    def disablePID(self):
        self.wristController.disable()

    def pidGet(self):
       pos =  math.degrees(self.Wrist.getAngle())
       SmartDashboard.putNumber("WristPIDget", pos)
       return pos

    def setPIDSourceType(self):
        return 0

    def getPIDSourceType(self):
        return 0

    def setPID(self):
        self.wristController.setSetpoint(self.setpoint)

    def pidWrite(self, output):
        SmartDashboard.putNumber("WristPID_Out", output)
        SmartDashboard.putNumber("WristError", self.wristController.getError())
        self.Wrist.setSpeed(output)

    def initialize(self):
        self.enablePID()
        self.setPID()

    def execute(self):
        pass

    def interrupted(self):
        self.disablePID()
        self.Wrist.setSpeed(0)

    def end(self):
        self.disablePID()
        self.Wrist.setSpeed(0)
