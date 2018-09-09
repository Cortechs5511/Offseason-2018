from wpilib.command import Command
import math
from networktables import NetworkTables

class setPositionWrist(Command):

    def __init__(self):
        super().__init__('setWristSpeed')
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist

    def pidGet(self):
        return self.Wrist.getAngle()

    def enablePID(self):
        self.wristController.enable()

    def disablePID(self):
        self.wristController.disable()

    def getPID(self):
        return self.wristController.get()

    def setPID(self, setpoint):
        self.wristController.setSetpoint(setpoint)

    def pidWrite(self, output):
        pass

    def initiate(self, setpoint):
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.025, 0.002, 0.20, 0.00] # These PID parameters are used in simulation
        else: [kP,kI,kD,kF] = [0.03, 0.00, 0.00, 0.00] # These PID parameters are used on a real robot

        self.wristController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        self.wristController.setInputRange(-30, 120) #input range in degrees
        self.wristController.setOutputRange(-0.8, 0.8) #output range in percent
        self.wristController.setAbsoluteTolerance(5.0) #tolerance in degrees
        self.wristController.setContinuous(True)

        self.enablePID()
        self.setPID(setpoint)

    def execute(self):
        self.Wrist.setSpeed(self.getPID())

    def interrupted(self):
        self.disablePID()
        self.Wrist.setSpeed(0)

    def end(self):
        self.disablePID()
        self.Wrist.setSpeed(0)
