import math
import wpilib
from wpilib.command import Command
from sensors.DTEncoders import DTEncoders
#from sensors.navx import NavX

class DriveStraightDistancePID(Command):

    def __init__(self, distance = 10):
        super().__init__('DriveStraightDistancePID')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.setpoint = distance

        self.DT.encoders.enablePID()
        #self.DT.navx.enablePID()

        self.TolDist = 0.5 #feet
        self.finished = False

        [kP,kI,kD,kF] = [0.32, 0.00, 3.50, 0.00] #Tuned for simulation
        distController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)

        distController.setInputRange(0,  50) #feet
        distController.setOutputRange(-0.8, 0.8)
        distController.setAbsoluteTolerance(self.TolDist)
        distController.setContinuous(False)
        self.distController = distController

        self.setPID(distance)
        self.distController.disable()

    def execute(self):
        self.distController.enable()

        speed = self.getPID()
        #err = (self.DT.encoders.getPID()+self.DT.navx.getPID())/2
        err = self.DT.encoders.getPID()

        self.DT.tankDrive(speed+err, speed-err)

        if abs(self.setpoint-self.DT.getAvgDistance()) < self.TolDist and speed < 0.1:  self.finished = True
        else: self.finished = False

    def isFinished(self):
        return self.finished

    def interrupted(self):
        self.DT.tankDrive(0,0)
        self.DT.encoders.disablePID()
        #self.DT.navx.disablePID()
        self.disablePID()

    def end(self):
        self.DT.tankDrive(0,0)
        self.DT.encoders.disablePID()
        #self.DT.navx.disablePID()
        self.disablePID()

    def enablePID(self):
        self.distController.enable()

    def disablePID(self):
        self.distController.disable()

    def setPID(self, setpoint):
        self.distController.setSetpoint(setpoint)

    def getPID(self):
        return self.distController.get()

    def pidGet(self):
        return self.DT.getAvgDistance()

    def getPIDSourceType(self):
        return self.DT.getAvgDistance()

    def pidWrite(self, output):
        pass
