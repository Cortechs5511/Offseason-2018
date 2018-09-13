from wpilib.command import CommandGroup

from commands.setSpeedWrist import setSpeedWrist
from commands.setPositionWrist import setPositionWrist
from commands.setSpeedLift import setSpeedLift
from commands.setPositionLift import setPositionLift
from commands.setSpeedIntake import setSpeedIntake
from commands.setFixedIntake import setFixedIntake

from wpilib import SmartDashboard

def IntakePosition():
    cg = CommandGroup("IntakePositon")
    cg.addParallel(setPositionLift(0))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(0.5))
    return cg

def Level2IntakePosition():
    cg = CommandGroup("Level2IntakePositon")
    cg.addParallel(setPositionLift(13))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(0.5))
    return cg

def Level3IntakePosition():
    cg = CommandGroup("Level3IntakePositon")
    cg.addParallel(setPositionLift(21))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(0.5))
    return cg

def SwitchPosition():
    cg = CommandGroup("IntakePositon")
    cg.addParallel(setPositionLift(25))
    cg.addParallel(setPositionWrist(90))
    cg.addParallel(setFixedIntake(0))
    return cg

def SwitchShoot():
    cg = CommandGroup("SwitchShoot")
    cg.addParallel(setPositionLift(25))
    cg.addParallel(setPositionWrist(90))
    cg.addParallel(setFixedIntake(-0.4))
    return cg

def ExchangePosition():
    cg = CommandGroup("ExchangePosition")
    cg.addParallel(setPositionLift(0))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(-0.5))
    return cg

def ExchangeShoot():
    cg = CommandGroup("ExchangeShoot")
    cg.addParallel(setPositionLift(0))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(-0.5))
    return cg

def ProtectPosition():
    cg = CommandGroup("ProtectPosition")
    cg.addParallel(setPositionLift(0))
    cg.addParallel(setPositionWrist(-100))
    cg.addParallel(setFixedIntake(0))


def UpdateDashboard():
    SmartDashboard.putData("Intake_Position", IntakePosition())
