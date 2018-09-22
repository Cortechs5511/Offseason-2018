from wpilib.command.commandgroup import CommandGroup

from wpilib.command.waitcommand import WaitCommand

from commands.DriveStraightDistance import DriveStraightDistance
from commands.DriveStraightTime import DriveStraightTime
from commands.TurnAngle import TurnAngle

from commands.DriveStraightDistancePID import DriveStraightDistancePID
from commands.DriveStraightTimePID import DriveStraightTimePID
from commands.TurnAnglePID import TurnAnglePID

class AutonomousProgram(CommandGroup):
    '''
    A simple program that spins the motor for two seconds, pauses for a second,
    and then spins it in the opposite direction for two seconds.
    '''

    def __init__(self):
        super().__init__('Autonomous Program')
