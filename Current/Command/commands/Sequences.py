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

def UpdateDashboard():
    SmartDashboard.putData("Intake_Position", IntakePosition())
