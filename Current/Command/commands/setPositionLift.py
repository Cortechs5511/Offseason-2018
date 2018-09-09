from wpilib.command import Command
import math
from networktables import NetworkTables

class setPositionLift(Command):

    def __init__(self):
        super().__init__('setLiftSpeed')
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift

    def pidGet(self):
        return self.Lift.getHeight()

    def enablePID(self):
        self.liftController.enable()

    def disablePID(self):
        self.liftController.disable()

    def getPID(self):
        return self.liftController.get()

    def setPID(self, setpoint):
        self.liftController.setSetpoint(setpoint)

    def pidWrite(self, output):
        pass

    def initiate(self, setpoint):
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.025, 0.002, 0.20, 0.00] # These PID parameters are used in simulation
        else: [kP,kI,kD,kF] = [0.03, 0.00, 0.00, 0.00] # These PID parameters are used on a real robot

        self.liftController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        self.liftController.setInputRange(20, 50) #input range in inches
        self.liftController.setOutputRange(-0.8, 0.8) #output range in percent
        self.liftController.setAbsoluteTolerance(5.0) #tolerance in inches
        self.liftController.setContinuous(True)

        self.enablePID()
        self.setPID(setpoint)

    def execute(self):
        self.Lift.setSpeed(self.getPID())

    def interrupted(self):
        self.disablePID()
        self.Lift.setSpeed(0)

    def end(self):
        self.disablePID()
        self.Lift.setSpeed(0)
