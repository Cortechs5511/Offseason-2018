import wpilib
import math

import pickle
import os.path
import pathfinder as pf

timer = wpilib.Timer()

width = 33/12
gains = [0,0,0,1/20,0] #P,I,D,1/V,1/A #[25,0,2,1/4,1/6]

def makeTraj(name):
    if(name=="DriveStraight"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(12,0,0)
        ]
    if(name=="LeftSwitch"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(10,9,0),
        ]
    if(name=="RightScale"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(24,2,math.radians(30))
        ]
    if(name=="LeftScale"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(24,-2,math.radians(-30))
        ]
    if(name=="RightOppositeScale"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(19,3,math.radians(55)),
            pf.Waypoint(19,16,math.radians(90)),
            pf.Waypoint(23,19,math.radians(-30))
        ]
    if(name=="LeftOppositeScale"):
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(19,-3,math.radians(-55)),
            pf.Waypoint(19,-16,math.radians(-90)),
            pf.Waypoint(23,-19,math.radians(30))
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
            dt=0.02, max_velocity=20, max_acceleration=6.0, max_jerk=120.0)

        modifier = pf.modifiers.TankModifier(trajectory).modify(width/2.4)
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

def ftToM(ft):
    return ft*12*2.54/100

def mToFt(m):
    return m*100/2.54/12

def initPath(drivetrain, name):
    [left,right,modifier] = getTraj(name)

    leftFollower = pf.followers.EncoderFollower(left)
    leftFollower.configureEncoder(drivetrain.getRaw()[0], 255, 4/12) #Pulse Initial, pulsePerRev, WheelDiam
    leftFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    rightFollower = pf.followers.EncoderFollower(right)
    rightFollower.configureEncoder(-drivetrain.getRaw()[1], 127, 4/12) #Pulse Initial, pulsePerRev, WheelDiam
    rightFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    showPath(left,right,modifier)

    timer.reset()
    timer.start()

    return [leftFollower,rightFollower]

def followPath(drivetrain, leftFollower, rightFollower):
    if(not leftFollower.isFinished()):
        print(drivetrain.getDistance())
        return [leftFollower.calculate(drivetrain.getRaw()[0]), rightFollower.calculate(-drivetrain.getRaw()[1])]
    else: return [0,0]
