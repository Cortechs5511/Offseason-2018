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

def initPath(drivetrain):
    [left,right,modifier] = getTraj()
    gains = [2,0,1,1/helper.getMaxV(),0]

    leftFollower = pf.followers.EncoderFollower(left)
    leftFollower.configureEncoder(drivetrain.getEncoders()[0], helper.getPulsesPerRev(), helper.getWheelDiam())
    leftFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    rightFollower = pf.followers.EncoderFollower(right)
    rightFollower.configureEncoder(drivetrain.getEncoders()[1], helper.getPulsesPerRev(), helper.getWheelDiam())
    rightFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    drivetrain.enableNavXPID()
    showPath(left,right,modifier)
    return [leftFollower,rightFollower]

def followPath(drivetrain, leftFollower, rightFollower):
    l = leftFollower.calculate(drivetrain.getEncoders()[0])
    r = rightFollower.calculate(drivetrain.getEncoders()[1])

    desiredHeading = pf.r2d(leftFollower.getHeading()) #degrees
    drivetrain.setNavXPID(desiredHeading)
    turn = drivetrain.getNavXPIDOut()
    [l,r] = [l+turn,r-turn]
    drivetrain.tank(-l,r)
