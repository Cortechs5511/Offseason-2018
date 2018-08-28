import math
#import numpy as np

import wpilib
from robotpy_ext.common_drivers import navx

import helper.helper as helper

class NavX():

    def __init__(self):
        self.navx = navx.AHRS.create_spi()

        #NavX PID Constants
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.025, 0.002, 0.20, 0.00] # These PID parameters are used in simulation
        else: [kP,kI,kD,kF] = [0.03, 0.00, 0.00, 0.00] # These PID parameters are used on a real robot
        kToleranceDegrees = 5.0

        turnController = wpilib.PIDController(kP, kI, kD, kF, self.navx, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(kToleranceDegrees)
        turnController.setContinuous(True)
        self.turnController = turnController
        self.turnController.disable()

    def enablePID(self):
        self.turnController.enable()

    def disablePID(self):
        self.turnController.disable()

    def setPID(self, setpoint):
        self.turnController.setSetpoint(setpoint)

    def getPID(self):
        return self.turnController.get()

    def getAngle(self):
        return self.navx.getYaw()

    def pidWrite(self, output):
        pass
