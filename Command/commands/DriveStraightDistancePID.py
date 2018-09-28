import math
import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard
from sensors.DTEncoders import DTEncoders
#from sensors.navx import NavX

class DriveStraightDistancePID(Command):

    def __init__(self, distance = 10, Debug = False, maxtime=300):
        super().__init__('DriveStraightDistancePID')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.maxtime = maxtime
        self.timer = self.getRobot().timer

        self.setpoint = distance

        #self.DT.encoders.enablePID()
        #self.DT.navx.enablePID()

        self.TolDist = 0.2 #feet
        self.finished = False

        [kP,kI,kD,kF] = [0.07, 0.0, 0.20, 0.00]
        distController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        distController.setInputRange(0,  50) #feet
        distController.setOutputRange(-0.55, 0.55)
        distController.setAbsoluteTolerance(self.TolDist)
        distController.setContinuous(False)
        self.distController = distController
        self.distController.disable()

        if Debug == True: SmartDashboard.putData("Distance_PID",self.distController)

    def initialize(self):
        setpoint = self.setpoint + self.pidGet()
        self.setPID(setpoint)
        self.distController.enable()

    def execute(self):
        pass

        '''
        speed = self.getPID()
        #err = (self.DT.encoders.getPID()+self.DT.navx.getPID())/2
        err = self.DT.encoders.getPID()

        self.DT.tankDrive(speed+err, speed-err)
        '''

    def isFinished(self):
        rate = abs(self.DT.encoders.getAvgVelocity())
        minrate = 0.25
        if self.distController.onTarget() and rate < minrate or self.timer.get() > self.maxtime: return True
        else: return False

        '''
        if abs(self.setpoint-self.DT.getAvgDistance()) < self.TolDist and speed < 0.1:  self.finished = True
        else: self.finished = False
        return self.finished
        '''

    def interrupted(self):
        self.DT.tankDrive(0,0)
        #self.DT.encoders.disablePID()
        #self.DT.navx.disablePID()
        self.disablePID()

    def end(self):
        self.DT.tankDrive(0,0)
        #self.DT.encoders.disablePID()
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
        nominal = 0.2
        if output < nominal and output > 0: output = nominal
        elif output > -nominal and output < 0: output = -nominal

        self.DT.tankDrive(output,output)
