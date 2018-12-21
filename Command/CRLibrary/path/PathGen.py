import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from CRLibrary.physics import DifferentialDrive as ddrive
from CRLibrary.path import odometry as od
from CRLibrary.util import units
from CRLibrary.util import util

from path import PathList

MAXV = 5
MAXA = 10
MAXJ = 10

def getLimits():
    global MAXV, MAXA, MAXJ
    return [MAXV, MAXA, MAXJ]

def getTraj(name, model):
    path = os.path.join(os.path.join(os.path.abspath(os.path.join(os.path.abspath(
    os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), os.pardir)), os.pardir)),"path"),name)
    if(not os.path.exists(path)): os.makedirs(path)

    pickle_file1 = os.path.join(path,"Right.pickle")
    pickle_file2 = os.path.join(path,"Left.pickle")
    pickle_file3 = os.path.join(path,"Modifier.pickle")

    if wpilib.RobotBase.isSimulation():
        points = PathList.makeTraj(name)
        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
        dt=.0333, max_velocity=MAXV, max_acceleration=MAXA, max_jerk=MAXJ)

        modifier = pf.modifiers.TankModifier(trajectory).modify(units.metersToFeet(model.effWheelbaseRadius()))
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
            renderer.draw_pathfinder_trajectory(left, color='#0000ff', offset=(-1.5,0)) #half width in feet
            renderer.draw_pathfinder_trajectory(modifier.source, color='#00ff00', show_dt=1.0, dt_offset=0.0)
            renderer.draw_pathfinder_trajectory(right, color='#0000ff', offset=(1.5,0)) #half width in feet
