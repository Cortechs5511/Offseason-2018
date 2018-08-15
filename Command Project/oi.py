from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton

from commands.crash import Crash


def getJoystick(num):
    '''
    Assign commands to button actions, and publish your joysticks so you
    can read values from them later.
    '''

    joystick = Joystick(0)
    joystick1 = Joystick(1)

    if num == 0:
        return joystick
    else:
        return joystick1
