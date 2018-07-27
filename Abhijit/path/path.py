import wpilib
import math
import numpy as np

import pickle
import os.path
import pathfinder as pf

# Pathfinder constants
MAX_VELOCITY = 10 # ft/s
MAX_ACCELERATION = 6

def getTraj():
    pickle_file1 = os.path.join(os.path.dirname(__file__), 'right.pickle')
    pickle_file2 = os.path.join(os.path.dirname(__file__), 'left.pickle')
    pickle_file3 = os.path.join(os.path.dirname(__file__), 'modifier')

    if wpilib.RobotBase.isSimulation():
        points = [
            pf.Waypoint(0, 0, 0),
            pf.Waypoint(9, 5, 0),
            ]

        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,dt=0.02,max_velocity=MAX_VELOCITY,max_acceleration=MAX_ACCELERATION,max_jerk=120.0)

        modifier = pf.modifiers.TankModifier(trajectory).modify(2.0)

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
