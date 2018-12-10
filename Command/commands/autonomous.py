from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from wpilib import SmartDashboard

from commands.DriveStraightCombined import DriveStraightCombined
from commands.DriveStraightDistance import DriveStraightDistance
from commands.DriveStraightTime import DriveStraightTime
from commands.DrivePathFinder import DrivePathFinder
from commands.TurnAngle import TurnAngle

from commands.setFixedDT import setFixedDT

import commands.Sequences as seq
from commands.Sequences import SwitchPosition
from commands.Sequences import SwitchShoot
from commands.Sequences import IntakePosition
from commands.Sequences import ProtectPosition
from commands.Sequences import ExchangePosition
from commands.Sequences import ExchangeShoot
from commands.setFixedWrist import setFixedWrist
from commands.setPositionWrist import setPositionWrist

#PATHFINDER AUTOS

class LeftSwitchMiddlePF(CommandGroup):
    def __init__(self):
        super().__init__("LeftSwitchMiddlePF")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addParallel(SwitchPosition(timeout=5))
        self.addSequential(DrivePathFinder(name="LeftSwitch", timeout=5))
        self.addSequential(SwitchShoot(timeout=1))
        '''
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=0, timeout=2))
        self.addSequential(TurnAngle(45, timeout=1))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=45, timeout=2))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=45, timeout=2))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))
        '''

class RightSwitchMiddlePF(CommandGroup):
    def __init__(self):
        super().__init__("RightSwitchMiddlePF")
        self.addSequential(DrivePathFinder(name="DriveStraight", timeout=15))

class LeftScalePF(CommandGroup):
    def __init__(self):
        super().__init__("LeftScalePF")
        self.addSequential(DrivePathFinder(name="LeftScale", timeout=15))

class RightScalePF(CommandGroup):
    def __init__(self):
        super().__init__("RightScalePF")
        self.addSequential(DrivePathFinder(name="RightScale", timeout=15))

class LeftOppositeScalePF(CommandGroup):
    def __init__(self):
        super().__init__("LeftOppositeScalePF")
        self.addSequential(DrivePathFinder(name="LeftOppositeScale", timeout=15))

class RightOppositeScalePF(CommandGroup):
    def __init__(self):
        super().__init__("RightOppositeScalePF")
        self.addSequential(DrivePathFinder(name="RightOppositeScale", timeout=15))

class CrazyTestPF(CommandGroup):
    def __init__(self):
        super().__init__("CrazyTestPF")
        self.addSequential(DrivePathFinder(name="CrazyTest", timeout=15))

#STANDARD AUTOS

class LeftSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__("LeftSwitchSide")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addParallel(SwitchPosition())
        self.addSequential(DriveStraightCombined(distance=154/12.0, angle=0, timeout=5))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAngle(90, timeout=4))
        self.addSequential(DriveStraightCombined(distance=20/12.0, angle=90, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class RightSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__("RightSwitchSide")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addParallel(SwitchPosition())
        self.addSequential(DriveStraightCombined(distance=154/12.0, angle=0, timeout=5))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAngle(-90, timeout=4))
        self.addSequential(DriveStraightCombined(distance=20/12.0, angle=-90, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__("DriveStraight")
        self.addSequential(DriveStraightCombined(distance=154/12.0, angle=0, timeout=5))
        self.addParallel(ProtectPosition(timeout = 5))

class LeftSwitchMiddle2Cube(CommandGroup):
    def __init__(self):
        super().__init__("LeftSwitchMiddle2Cube")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=9.5/12.0, angle=0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(-60, timeout=1))
        self.addSequential(DriveStraightCombined(distance=110/12.0, angle=-60, timeout=4))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addSequential(DriveStraightCombined(distance=36/12.0, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=0, timeout=2))
        self.addSequential(TurnAngle(45, timeout=1))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=45, timeout=2))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=45, timeout=2))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class LeftSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__("LeftSwitchMiddle")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=9.5/12.0, angle=0, timeout=1))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAngle(-60, timeout=2))
        self.addSequential(DriveStraightCombined(distance=125/12.0, angle=-60, timeout=5))
        self.addSequential(TurnAngle(0, timeout=2))
        self.addSequential(DriveStraightCombined(distance=36/12.0, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class RightSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__("RightSwitchMiddle")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=2))
        self.addSequential(DriveStraightCombined(distance=112/12.0, angle=0, timeout=4))
        self.addParallel(SwitchPosition())
        self.addSequential(SwitchShoot(timeout=1))

class RightSwitchMiddle2Cube(CommandGroup):
    def __init__(self):
        super().__init__("RightSwitchMiddle2Cube")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=112/12.0, angle=0, timeout=4))
        self.addParallel(SwitchPosition(timeout=2))
        self.addSequential(SwitchShoot(timeout=1))
        self.addParallel(DriveStraightTime(speed=0, timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=0, timeout=2))
        self.addSequential(DriveStraightTime(speed=0,timeout=1))
        self.addSequential(TurnAngle(-45, timeout=1))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=-45, timeout=2))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=-45, timeout=2))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=42/12, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

def UpdateDashboard():
    SmartDashboard.putData("LeftSwitchMiddlePF", LeftSwitchMiddlePF())
    SmartDashboard.putData("RightSwitchMiddlePF", RightSwitchMiddlePF())
    SmartDashboard.putData("LeftScalePF", LeftScalePF())
    SmartDashboard.putData("RightScalePF", RightScalePF())
    SmartDashboard.putData("LeftOppositeScalePF", LeftOppositeScalePF())
    SmartDashboard.putData("RightOppositeScalePF", RightOppositeScalePF())

    SmartDashboard.putData("LeftSwitchSide", LeftSwitchSide())
    SmartDashboard.putData("RightSwitchSide", RightSwitchSide())
    SmartDashboard.putData("DriveStraight", DriveStraight())
    SmartDashboard.putData("LeftSwitchMiddle", LeftSwitchMiddle())
    SmartDashboard.putData("RightSwitchMiddle", RightSwitchMiddle())
    SmartDashboard.putData("LeftSwitchMiddle2Cube", LeftSwitchMiddle2Cube())
    SmartDashboard.putData("RightSwitchMiddle2Cube", RightSwitchMiddle2Cube())
