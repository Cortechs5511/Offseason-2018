import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setPositionWrist(Command):

    def __init__(self, setpoint = 0, Debug = False, maxtime = 300):
        super().__init__('setPositionWrist')
        self.setpoint = setpoint
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist

        [kP,kI,kD,kF] = [0.60, 0.00, 5.00, 0.00]

        self.wristController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        self.wristController.setInputRange(-30, 120) #input range in degrees
        self.wristController.setOutputRange(-0.8, 0.8) #output range in percent
        self.wristController.setAbsoluteTolerance(2.0) #tolerance in degrees
        self.wristController.setContinuous(False)

        if Debug == True:
            SmartDashboard.putData("WristPID", self.wristController)
            SmartDashboard.putData("setPositionWrist", self)

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

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
        SmartDashboard.putNumber("WristError", self.wristController.getError())
        angle = self.Wrist.getAngle()
        if output > 0 and angle > 0:
            output = min(output, 0.25) + math.cos(angle) * 0.25 * output
        elif output < 0 and angle > 0:
            output = -1
        elif output < 0 and angle < 0:
            output = max(output, -0.25)
        SmartDashboard.putNumber("WristPID_Out", output)
        self.Wrist.setSpeed(output)


    def initialize(self):
        self.enablePID()
        self.setPID()

    def execute(self):
        pass

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def interrupted(self):
        self.disablePID()
        self.Wrist.setSpeed(0)

    def end(self):
        self.disablePID()
        self.Wrist.setSpeed(0)
