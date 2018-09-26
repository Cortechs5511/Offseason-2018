from wpilib.command import CommandGroup

from commands.setPositionWrist import setPositionWrist
from commands.setPositionLift import setPositionLift

from commands.setFixedLift import setFixedLift
from commands.setFixedIntake import setFixedIntake
from commands.setFixedIntake import setFixedIntake

from wpilib import SmartDashboard

def IntakePosition():
    cg = CommandGroup("IntakePositon")
    cg.addParallel(setPositionLift(0))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(-0.6))
    return cg

def Level2IntakePosition():
    cg = CommandGroup("Level2IntakePositon")
    cg.addParallel(setPositionLift(10))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(-0.6))
    return cg

def Level3IntakePosition():
    cg = CommandGroup("Level3IntakePositon")
    cg.addParallel(setPositionLift(20))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(-0.6))
    return cg

def SwitchPosition():
    cg = CommandGroup("SwitchPositon")
    cg.addParallel(setPositionLift(25))
    cg.addParallel(setPositionWrist(90))
    cg.addParallel(setFixedIntake(-0.3))
    return cg

def SwitchPosition2():
    cg = CommandGroup("SwitchPositon")
    cg.addParallel(setPositionLift(0))
    cg.addParallel(setPositionWrist(30))
    cg.addParallel(setFixedIntake(-0.3))
    return cg

def SwitchShoot():
    cg = CommandGroup("SwitchShoot")
    cg.addParallel(setPositionLift(25))
    cg.addParallel(setPositionWrist(90))
    cg.addParallel(setFixedIntake(0.6))
    return cg

def SwitchShoot2():
    cg = CommandGroup("SwitchShoot")
    cg.addParallel(setPositionLift(0))
    cg.addParallel(setPositionWrist(25))
    cg.addParallel(setFixedIntake(0.8))
    return cg

def ExchangeShoot():
    cg = CommandGroup("ExchangeShoot")
    cg.addParallel(setPositionLift(0))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(0.8))
    return cg

def ExchangePosition():
    cg = CommandGroup("ExchangePositon")
    cg.addParallel(setPositionLift(0))
    cg.addParallel(setPositionWrist(110))
    cg.addParallel(setFixedIntake(-0.3))
    return cg

def ProtectPosition():
    cg = CommandGroup("ProtectPosition")
    cg.addParallel(setFixedLift(-0.1))

    cg.addParallel(setPositionWrist(-20))
    cg.addParallel(setFixedIntake(-0.3))
    return cg

def UpdateDashboard():
    SmartDashboard.putData("IntakePosition", IntakePosition())
    SmartDashboard.putData("Level2IntakePosition",Level2IntakePosition())
    SmartDashboard.putData("Level3IntakePosition",Level3IntakePosition())
    SmartDashboard.putData("SwitchPositon",SwitchPosition())
    SmartDashboard.putData("SwitchShoot",SwitchShoot())
    SmartDashboard.putData("ExchangePositon",ExchangePosition())
    SmartDashboard.putData("ExchangeShoot",ExchangeShoot())
    SmartDashboard.putData("ProtectPosition",ProtectPosition())
