import math
import wpilib
from wpilib import SmartDashboard
from wpilib.command import Command
from sensors.DTEncoders import DTEncoders
from sensors.navx import NavX

class TurnAnglePID(Command):

    def __init__(self, angle = 0, DEBUG=False, maxtime=300):
        super().__init__('TurnAnglePID')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.maxtime = maxtime
        self.timer = self.getRobot().timer

        self.setpoint = angle

        self.TolAngle = 3
        #[kP,kI,kD,kF] = [0.012, 0.00, 0.04, 0.00] #Tuned for simulation
        [kP,kI,kD,kF] = [0.018,0,0.2,0]
        angleController = wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        angleController.setInputRange(-180,  180) #degrees
        angleController.setOutputRange(-0.8, 0.8)
        angleController.setAbsoluteTolerance(self.TolAngle)
        angleController.setContinuous(True)
        self.angleController = angleController
        self.setPID(self.setpoint)
        self.angleController.disable()

        if(DEBUG): SmartDashboard.putData("NavXPID",self.angleController)

    def execute(self):
        self.enablePID()

        SmartDashboard.putNumber("DT_Angle",self.DT.getAngle())

    def isFinished(self):
        if abs(self.setpoint-self.DT.getAngle()) < self.TolAngle and self.DT.encoders.getAvgAbsVelocity() < .2 or self.timer.get() > self.maxtime:  return True
        else: return False

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
        nominal = 0.27
        if output < nominal and output > 0:
            output = nominal
        elif output > -nominal and output < 0:
            output = -nominal

        self.DT.tankDrive(output,-output)
