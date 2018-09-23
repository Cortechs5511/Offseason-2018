import math
import wpilib
from wpilib.command import Command
from sensors.DTEncoders import DTEncoders
#from sensors.navx import NavX

class TurnAnglePID(Command):

    def __init__(self, angle = 0):
        super().__init__('TurnAnglePID')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.setpoint = angle

        self.TolAngle = 3
        [kP,kI,kD,kF] = [0.015, 0.0001, 0.20, 0.00] #Tuned for simulation
        angleController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        angleController.setInputRange(-180,  180) #degrees
        angleController.setOutputRange(-0.8, 0.8)
        angleController.setAbsoluteTolerance(self.TolAngle)
        angleController.setContinuous(True)
        self.angleController = angleController
        self.setPID(self.setpoint)
        self.angleController.disable()

        self.finished = False

    def execute(self):
        self.enablePID()
        self.speed = self.getPID()
        self.DT.tankDrive(self.speed,-self.speed)

        if abs(self.setpoint-self.DT.getAngle()) < self.TolAngle and abs(self.speed) < 0.1:  self.finished = True
        else: self.finished = False

    def isFinished(self):
        return self.finished

    def interrupted(self):
        self.DT.tankDrive(0,0)
        self.disablePID()

    def end(self):
        self.DT.tankDrive(0,0)
        self.disablePID()

    def enablePID(self):
        self.angleController.enable()

    def disablePID(self):
        self.angleController.disable()

    def setPID(self, setpoint):
        self.angleController.setSetpoint(setpoint)

    def getPID(self):
        return self.angleController.get()

    def pidGet(self):
        return self.DT.getAngle()

    def getPIDSourceType(self):
        return self.DT.getAngle()

    def pidWrite(self, output):
        pass
