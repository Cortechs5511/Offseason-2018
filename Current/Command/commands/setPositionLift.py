from wpilib.command import Command
import math
from networktables import NetworkTables

class setLiftSpeed(Command):

    def __init__(self):
        super().__init__('Follow Joystick')
        self.smartDashboard = NetworkTables.getTable("SmartDashboard")
        self.requires(self.getRobot().lift)

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

    def initiate(self, lift_pos):
        self.liftTarget = lift_pos
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.025, 0.002, 0.20, 0.00] # These PID parameters are used in simulation
        else: [kP,kI,kD,kF] = [0.03, 0.00, 0.00, 0.00] # These PID parameters are used on a real robot
        kToleranceInches = 5.0

        liftController = wpilib.PIDController(kP, kI, kD, kF, self.getRobot().lift, output=self)
        liftController.setInputRange(20, 50)
        liftController.setOutputRange(-0.8, 0.8)
        liftController.setAbsoluteTolerance(kToleranceInches)
        liftController.setContinuous(True)
        self.liftController = liftController
        self.enablePID()
        self.setPID(setpoint)

    def execute(self):
        Lift = self.getRobot().lift
        lift_pos = Lift.getHeight()
        gravity_lift = self.getLiftGravity()
        initial = self.getPID()
        Lift.setSpeed(initial + gravity_lift)

    def interrupted(self):
        self.disablePID()

    def end(self):
        self.disablePID()
