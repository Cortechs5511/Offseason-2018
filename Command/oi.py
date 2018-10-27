import wpilib

from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton
from wpilib.buttons import Button
from wpilib.buttons import Trigger

from wpilib import XboxController as Xbox

from commands.setFixedWrist import setFixedWrist
from commands.setFixedLift import setFixedLift
from commands.setFixedIntake import setFixedIntake

from commands.setPositionWrist import setPositionWrist
from commands.setPositionLift import setPositionLift

from commands.setSpeedLift import setSpeedLift
from commands.setSpeedWrist import setSpeedWrist

import commands.Sequences as seq

from commands.Sequences import SwitchPosition
from commands.Sequences import SwitchShoot
from commands.Sequences import IntakePosition
from commands.Sequences import ProtectPosition
from commands.Sequences import ExchangePosition
from commands.Sequences import ExchangeShoot

from commands.crash import Crash

class axisButton(Trigger):

    def __init__(self, f, num, Threshold):
        self.f = f
        self.num = num
        self.Threshold = Threshold

    def get(self):
        return abs(self.f(self.num)) > self.Threshold


def getJoystick(num):
    '''
    Assign commands to button actions, and publish your joysticks so you
    can read values from them later.
    '''

    joystick0 = Joystick(0)
    joystick1 = Joystick(1)
    xbox = Xbox(2)

    if num == 0: return joystick0
    elif num == 1: return joystick1
    else: return xbox

def commands():
    joystick0 = getJoystick(0)
    joystick1 = getJoystick(1)
    xbox = getJoystick(2)

    button01 = JoystickButton(joystick0, 1)
    button01.whenPressed(ExchangeShoot(timeout=300))
    button02 = JoystickButton(joystick0, 2)
    button02.whenPressed(IntakePosition(timeout=300))
    button03 = JoystickButton(joystick0, 3)
    button03.whenPressed(ExchangePosition(timeout=300))
    button04 = JoystickButton(joystick0, 4)
    button04.whenPressed(ExchangePosition(timeout=300))

    button11 = JoystickButton(joystick1, 1)
    button11.whenPressed(SwitchShoot(timeout=300))
    button12 = JoystickButton(joystick1, 2)
    button12.whenPressed(SwitchPosition(timeout=300))
    button13 = JoystickButton(joystick1, 3)
    button13.whenPressed(ProtectPosition(timeout=300))
    button14 = JoystickButton(joystick1, 4)
    button14.whenPressed(ProtectPosition(timeout=300))

    x = JoystickButton(xbox, 1)
    x.whenPressed(setPositionWrist(-20, timeout=300))
    b = JoystickButton(xbox, 2)
    b.whenPressed(setPositionWrist(50, timeout=300))
    y = JoystickButton(xbox, 3)
    y.whenPressed(setPositionWrist(105, timeout=300))

    '''
    axis0 = axisButton(xbox.getY, 0, 0.1)
    axis0.whileActive(setFixedLift(xbox.getY(0)))
    axis1 = axisButton(xbox.getX, 1, 0.1)
    axis1.whileActive(setFixedWrist(xbox.getX(1)))
    trigger0 = axisButton(xbox.getTriggerAxis, 0, 0.1)
    trigger0.whileActive(setFixedIntake(xbox.getTriggerAxis(0)))
    trigger1 = axisButton(xbox.getTriggerAxis, 1, 0.1)
    trigger1.whileActive(setFixedIntake(-xbox.getTriggerAxis(1)))
'''

    axis0 = axisButton(xbox.getY, 0, 0.1)
    axis0.whileActive(setSpeedLift(timeout=300))
    axis1 = axisButton(xbox.getX, 1, 0.1)
    axis1.whileActive(setSpeedWrist(timeout=300))
    trigger0 = axisButton(xbox.getTriggerAxis, 0, 0.1)
    trigger0.whileActive(setFixedIntake(0.7, timeout=300))
    trigger1 = axisButton(xbox.getTriggerAxis, 1, 0.1)
    trigger1.whileActive(setFixedIntake(-0.7, timeout=300))
