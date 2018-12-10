import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from CRLibrary.physics import DifferentialDrive as ddrive
from CRLibrary.path import odometry as od
from CRLibrary.util import units
from CRLibrary.util import util

timer = wpilib.Timer()

MAXV = 10
MAXA = 15
MAXJ = 20

width = 33/12

def getLimits():
    global MAXV, MAXA, MAXJ
    return [MAXV, MAXA, MAXJ]

def makeTraj(name):
    if(name=="DriveStraight"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(12,0,0)
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

def getTraj(name):
    path = os.path.join(os.path.dirname(__file__),name)
    if(not os.path.exists(path)): os.makedirs(path)

    pickle_file1 = os.path.join(path,"Right.pickle")
    pickle_file2 = os.path.join(path,"Left.pickle")
    pickle_file3 = os.path.join(path,"Modifier.pickle")

    if wpilib.RobotBase.isSimulation():
        points = makeTraj(name)
        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
            dt=0.02, max_velocity=MAXV, max_acceleration=MAXA, max_jerk=MAXJ)

        modifier = pf.modifiers.TankModifier(trajectory).modify(14/12)
        left = modifier.getLeftTrajectory()
        right = modifier.getRightTrajectory()

        with open(pickle_file1, 'wb') as fp: pickle.dump(left, fp)
        with open(pickle_file2,'wb') as fp: pickle.dump(right,fp)
        with open(pickle_file3,'wb') as fp: pickle.dump(modifier,fp)
        return [left,right,modifier]
    else:
        with open(pickle_file1, 'rb') as fp: left = pickle.load(fp)
        with open(pickle_file2,'rb') as fp: right = pickle.load(fp)
        with open(pickle_file3,'rb') as fp: modifier = pickle.load(fp)
        return [left,right,modifier]

def showPath(left,right,modifier):
    if wpilib.RobotBase.isSimulation():
        from pyfrc.sim import get_user_renderer
        renderer = get_user_renderer()
        if renderer:
            renderer.draw_pathfinder_trajectory(left, color='#0000ff', offset=(-width/2,0))
            renderer.draw_pathfinder_trajectory(modifier.source, color='#00ff00', show_dt=1.0, dt_offset=0.0)
            renderer.draw_pathfinder_trajectory(right, color='#0000ff', offset=(width/2,0))
