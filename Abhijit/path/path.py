import wpilib
import math
import numpy as np

import pickle
import os.path
import pathfinder as pf

import helper.helper as helper

def getTraj():
    pickle_file1 = os.path.join(os.path.dirname(__file__), 'right.pickle')
    pickle_file2 = os.path.join(os.path.dirname(__file__), 'left.pickle')
    pickle_file3 = os.path.join(os.path.dirname(__file__), 'modifier.pickle')

    if wpilib.RobotBase.isSimulation():
        points = [
            pf.Waypoint(0, 0, 0),
            pf.Waypoint(11, 6, 0),
            ]

        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
            dt=helper.getPeriod(),max_velocity=helper.getMaxV(),max_acceleration=helper.getMaxA(),max_jerk=120.0)

        modifier = pf.modifiers.TankModifier(trajectory).modify(helper.getWidth())

        # Do something with the new Trajectories...
        left = modifier.getLeftTrajectory()
        right = modifier.getRightTrajectory()

        with open(pickle_file1, 'wb') as fp:
            pickle.dump(left, fp)
        with open(pickle_file2,'wb') as fp:
            pickle.dump(right,fp)
        with open(pickle_file3,'wb') as fp:
            pickle.dump(modifier,fp)
        return [left,right,modifier]
    else:
        with open(pickle_file1, 'rb') as fp:
            left = pickle.load(fp)
        with open(pickle_file2,'rb') as fp:
            right = pickle.load(fp)
        with open(pickle_file3,'rb') as fp:
            modifier = pickle.load(fp)
        return [left,right,modifier]

def showPath(left,right,modifier):
    # This code renders the followed path on the field in simulation (requires pyfrc 2018.2.0+)
    if wpilib.RobotBase.isSimulation():
        from pyfrc.sim import get_user_renderer
        renderer = get_user_renderer()
        if renderer:
            renderer.draw_pathfinder_trajectory(left, color='#0000ff', offset=(-1,0))
            renderer.draw_pathfinder_trajectory(modifier.source, color='#00ff00', show_dt=1.0, dt_offset=0.0)
            renderer.draw_pathfinder_trajectory(right, color='#0000ff', offset=(1,0))
