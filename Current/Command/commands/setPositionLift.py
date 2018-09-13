from wpilib.command import Command
import math
from networktables import NetworkTables
import wpilib
from wpilib import SmartDashboard

class setPositionLift(Command):

    def __init__(self, setpoint):
        super().__init__('setLiftSpeed')

        self.setpoint = setpoint

        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.025, 0.002, 0.20, 0.00] # These PID parameters are used in simulation
        else: [kP,kI,kD,kF] = [0.03, 0.00, 0.00, 0.00] # These PID parameters are used on a real robot

        self.liftController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        self.liftController.setInputRange(20, 50) #input range in inches
        self.liftController.setOutputRange(-0.8, 0.8) #output range in percent
        self.liftController.setAbsoluteTolerance(5.0) #tolerance in inches
        self.liftController.setContinuous(True)

        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift


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
