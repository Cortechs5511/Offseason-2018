import math
import wpilib
import oi

from wpilib import SmartDashboard
import wpilib.buttons

from wpilib.command import Command
from commandbased import CommandBasedRobot

from commands.setPositionWrist import setPositionWrist
from commands.setPositionLift import setPositionLift

from commands.setFixedDT import setFixedDT
from commands.setFixedIntake import setFixedIntake
from commands.setFixedLift import setFixedLift
from commands.setFixedWrist import setFixedWrist

from commands.setSpeedDT import setSpeedDT
from commands.setSpeedLift import setSpeedLift
from commands.setSpeedWrist import setSpeedWrist

from commands.DriveStraightTime import DriveStraightTime
from commands.DriveStraightDistance import DriveStraightDistance
from commands.DriveStraightCombined import DriveStraightCombined
from commands.DrivePath import DrivePath
from commands.TurnAngle import TurnAngle

from commands.getLimelightData import getLimelightData

from commands.Zero import Zero

from commands import Sequences

from commands import autonomous

from subsystems import Wrist, Intake, Lift, Drive

import pathfinder as pf
from CRLibrary.path.Path import Path as path
from CRLibrary.path.odometry import Odometer as od

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from networktables import NetworkTables

class Limelight:
    def __init__(self):
        self.table = NetworkTables.getTable("limelight")
        self.table.putNumber('ledMode',1)
        print ('it ran')

    def ReadLimelightData(self):
        self.ty = self.table.getNumber('ty',None)
        self.ta = self.table.getNumber('ta',None)
        self.ts = self.table.getNumber('ts',None)
        self.tx = self.table.getNumber('ts',None)
        return [self.tx,self.ty,self.ta,self.ts]

    def getTx(self):
        self.table.putNumber('ledMode',1)
        if self.InformationAvailable() == False:
            return 0
        else:
            return self.table.getNumber('tx',None)
    def getTy(self):
        if self.InformationAvailable() == False:
            return 0
        else:
            return self.table.getNumber('ty',None)
    def getTa(self):
        if self.InformationAvailable() == False:
            return 0
        else:
            return self.table.getNumber('ta',None)
    def getTs(self):
        if self.InformationAvailable() == False:
            return 0
        else:
            return self.table.getNumber('ts',None)

    def getDistance(self):
        abox = 143
        ta = self.getTa()
        d = math.sqrt((abox)/(4*math.tan(0.471)*math.tan(0.3576)*ta))
        return d

    def UpdateDashboard(self):
        self.ty = self.table.getNumber('ty',None)
        self.ta = self.table.getNumber('ta',None)
        self.ts = self.table.getNumber('ts',None)
        self.tx = self.table.getNumber('ts',None)

    def InformationAvailable(self):
        return self.table.getNumber('tv',None) == 1
