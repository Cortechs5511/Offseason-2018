from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton
import wpilib

from commands.crash import Crash


def getJoystick(num):
    '''
    Assign commands to button actions, and publish your joysticks so you
    can read values from them later.
    '''

    joystick0 = Joystick(0)
    joystick1 = Joystick(1)
    xbox = wpilib.XboxController(2)

    if num == 0:
        return joystick0
    elif num == 1:
        return joystick1
    else:
        return xbox
