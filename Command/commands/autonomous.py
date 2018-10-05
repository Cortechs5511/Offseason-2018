from wpilib.command.commandgroup import CommandGroup

from wpilib.command.waitcommand import WaitCommand

from commands.DriveStraightDistance import DriveStraightDistance
from commands.DriveStraightTime import DriveStraightTime
from commands.TurnAngle import TurnAngle

import commands.Sequences as seq

from commands.setFixedDT import setFixedDT

from commands.Sequences import SwitchPosition
from commands.Sequences import SwitchShoot
from commands.Sequences import IntakePosition
from commands.Sequences import ProtectPosition
from commands.Sequences import ExchangePosition
from commands.Sequences import ExchangeShoot
from commands.setFixedWrist import setFixedWrist
from commands.setPositionWrist import setPositionWrist

class LeftSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__('LeftSwitchSide')
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addParallel(SwitchPosition())
        self.addSequential(DriveStraightDistance((154/12.0), timeout=5))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAngle(90, timeout=4))
        self.addSequential(DriveStraightDistance(20/12.0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class RightSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__('RightSwitchSide')
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addParallel(SwitchPosition())
        self.addSequential(DriveStraightDistance((154/12.0), timeout=5))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAngle(-90, timeout=4))
        self.addSequential(DriveStraightDistance(20/12.0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__('DriveStraight')
        self.addSequential(DriveStraightDistance(154/12.0, timeout=5))
        self.addParallel(ProtectPosition())

class LeftSwitchMiddle2Cube(CommandGroup):
    def __init__(self):
        super().__init__('LeftSwitchMiddle2Cube')
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightDistance(9.5/12.0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(-60, timeout=1))
        self.addSequential(DriveStraightDistance(125/12.0, timeout=3))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addSequential(DriveStraightDistance(36/12.0, timeout=1))
        self.addSequential(SwitchShoot(timeout=1))
        self.addSequential(DriveStraightDistance(-30/12, timeout=1))
        self.addSequential(TurnAngle(45, timeout=1))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightDistance(30/12, timeout=1))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightDistance(-30/12, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightDistance(30/12, timeout=1))
        self.addSequential(SwitchShoot(timeout=1))

class LeftSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__('LeftSwitchMiddle')
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightDistance(9.5/12.0, timeout=1))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAngle(-60, timeout=2))
        self.addSequential(DriveStraightDistance(125/12.0, timeout=5))
        self.addSequential(TurnAngle(0, timeout=2))
        self.addSequential(DriveStraightDistance(36/12.0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class RightSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__('RightSwitchMiddle')
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=2))
        self.addSequential(DriveStraightDistance(112/12.0, timeout=4))
        self.addParallel(SwitchPosition())
        self.addSequential(SwitchShoot(timeout=1))

class RightSwitchMiddle2Cube(CommandGroup):
    def __init__(self):
        super().__init__('RightSwitchMiddle2Cube')
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightDistance(112/12.0, timeout=2))
        self.addParallel(SwitchPosition(timeout=2))
        self.addSequential(SwitchShoot(timeout=1))
        self.addSequential(DriveStraightDistance(-30/12, timeout=1))
        self.addSequential(TurnAngle(-45, timeout=1))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightDistance(30/12, timeout=1))
        self.addParallel(IntakePosition (timeout=1))
        self.addSequential(DriveStraightDistance(-30/12, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightDistance(30/12, timeout=1))
        self.addSequential(SwitchShoot(timeout=1))
