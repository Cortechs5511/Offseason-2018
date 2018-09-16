import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setPositionLift(Command):

    def __init__(self, setpoint = 0, Debug = False):
        super().__init__('setPositionLift')
        self.setpoint = setpoint
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift

        [kP,kI,kD,kF] = [0.20 , 0.20, 0.00, 0.00] # These PID parameters are used on a real robot

        self.liftController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        self.liftController.setInputRange(0, 30) #input range in inches
        self.liftController.setOutputRange(-0.8, 0.8) #output range in percent
        self.liftController.setAbsoluteTolerance(0.5) #tolerance in inches
        self.liftController.setContinuous(False)

        if Debug:
            SmartDashboard.putData("LiftPID", self.liftController)

    def setPIDSourceType(self):
        return 0

    def getPIDSourceType(self):
        return 0

    def pidGet(self):
        return self.Lift.getHeight()

    def enablePID(self):
        self.liftController.enable()

    def disablePID(self):
        self.liftController.disable()

    def pidGet(self):
       pos =  self.Lift.getHeight()
       SmartDashboard.putNumber("LiftPIDget", pos)
       return pos

    def setPID(self, setpoint):
        self.liftController.setSetpoint(setpoint)

    def pidWrite(self, output):
        SmartDashboard.putNumber("LiftPID_Out", output)
        SmartDashboard.putNumber("LiftError", self.liftController.getError())
        self.Lift.setSpeed(output)

    def initialize(self):
        self.enablePID()
        self.setPID(self.setpoint)

    def interrupted(self):
        self.disablePID()
        self.Lift.setSpeed(0)

    def end(self):
        self.disablePID()
        self.Lift.setSpeed(0)
