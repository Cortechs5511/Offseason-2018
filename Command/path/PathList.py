import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from CRLibrary.physics import DifferentialDrive as ddrive
from CRLibrary.path import odometry as od
from CRLibrary.util import units
from CRLibrary.util import util

def makeTraj(name):
    if(name=="DriveStraight"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(20,0,0)
        ]
    elif(name=="LeftSwitch"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(7,9,0),
            pf.Waypoint(10,9,0)
        ]
    elif(name=="RightScale"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(24,2,math.radians(30))
        ]
    elif(name=="LeftScale"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(24,-2,math.radians(-30))
        ]
    elif(name=="RightOppositeScale"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(19,3,math.radians(55)),
            pf.Waypoint(19,16,math.radians(90)),
            pf.Waypoint(23,19,math.radians(-30))
        ]
    elif(name=="LeftOppositeScale"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(19,-3,math.radians(-55)),
            pf.Waypoint(19,-16,math.radians(-90)),
            pf.Waypoint(23,-19,math.radians(30))
        ]
    elif(name=="Test"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(10,0,0),
            pf.Waypoint(20,10,math.radians(-90)),
            pf.Waypoint(10,20,math.radians(180)),
            pf.Waypoint(0,10,math.radians(90)),
            pf.Waypoint(10,0,0)
        ]
    return points
