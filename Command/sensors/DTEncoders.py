import math
#import numpy as np

import wpilib

import sim.simComms as simComms

class DTEncoders():

    def __init__(self):
        #Encoder PID Constants
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [2.00, 0.00, 0.00, 0.00] # These PID parameters are used in simulation
        else: [kP,kI,kD,kF] = [0.03, 0.00, 0.00, 0.00] # These PID parameters are used on a real robot
        kTolerance = .1 #feet

        self.leftEncoder = wpilib.Encoder(0,1)
        self.leftEncoder.setDistancePerPulse(4/12 * math.pi / 255)
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = wpilib.Encoder(2,3)
        self.rightEncoder.setDistancePerPulse(-4/12 * math.pi / 127)
        self.rightEncoder.setSamplesToAverage(10)


        PIDController =  wpilib.PIDController(kP, kI, kD, kF, self, output=self)
        PIDController.setOutputRange(-1.0, 1.0)
        PIDController.setAbsoluteTolerance(kTolerance)
        self.PIDController = PIDController
        self.PIDController.disable()

    def get(self):
        return [self.leftEncoder.get(),self.rightEncoder.get()]

    def getDistance(self):
        return [self.leftEncoder.getDistance(),self.rightEncoder.getDistance()]

    def getAvgDistance(self):
        return self.getDistance()[1]

    '''
    def getAvgVelocity(self):
        #feet per second
        return (self.leftEncoder.getRate() + self.rightEncoder.getRate())/ 2

    def getAvgAbsVelocity(self):
        #feet per second
        return (abs(self.leftEncoder.getRate()) + abs(self.rightEncoder.getRate()))/ 2
    '''

    def getAvgVelocity(self):
        #feet per second
        return self.rightEncoder.getRate()

    def getAvgAbsVelocity(self):
        #feet per second
        return self.rightEncoder.getRate()

    def updateDiff(self):
        self.diff = self.leftEncoder.getDistance()-self.rightEncoder.getDistance()

    def reset(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        simComms.resetEncoders()

    def enablePID(self):
        self.PIDController.enable()

    def disablePID(self):
        self.PIDController.disable()

    def setPID(self, setpoint):
        self.PIDController.setSetpoint(setpoint)

    def getPID(self):
        return self.PIDController.get()

    def pidGet(self):
        self.updateDiff()
        return self.diff

    def getPIDSourceType(self):
        self.updateDiff()
        return self.diff

    def pidWrite(self, output):
        pass
