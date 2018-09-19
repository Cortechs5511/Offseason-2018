import wpilib
import math
#import numpy as np

import pickle
import os.path
import pathfinder as pf

desiredHeading=0
timer = wpilib.Timer()

init = False
leftFollower = None
rightFollower = None

width = 33/12

auto = "Left" #Options are Left, Middle, Right
gameData = "RRR" #Options are LLL, LRL, RRR, RLR

def getName(num):
    if(num==0):
        return "DriveStraight"
    elif(num==1):
        return "LeftSwitch"
    elif(num==2):
        return "RightScale"
    elif(num==3):
        return "LeftScale"
    elif(num==4):
        return "RightOppositeScale"
    elif(num==5):
        return "LeftOppositeScale"

def getNum(name):
    for i in range(0,100):
        if(getName(i)==name): return i

def makeTraj(num):
    if(num==0): #Drive Straight
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(9,0,0)
        ]
    if(num==1): #Left Switch
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(9,10,0),
        ]
    if(num==2): #Right Scale
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(24,2,math.radians(30))
        ]
    if(num==3): #Left Scale
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(24,-2,math.radians(-30))
        ]
    if(num==4): #Start Right, Opposite Scale
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(19,3,math.radians(55)),
            pf.Waypoint(19,16,math.radians(90)),
            pf.Waypoint(23,19,math.radians(-30))
        ]
    if(num==5): #Start Left, Opposite Scale
        points = [
            pf.Waypoint(0,0,0),
            pf.Waypoint(19,-3,math.radians(-55)),
            pf.Waypoint(19,-16,math.radians(-90)),
            pf.Waypoint(23,-19,math.radians(30))
        ]
    return points

def calcNum():
    if(auto=="Left"):
        if(gameData[1]=='L'): return getNum("LeftScale")
        else: return getNum("LeftOppositeScale")
    elif(auto=="Middle"):
        if(gameData[0]=='L'): return getNum("LeftSwitch")
        else: return getNum("DriveStraight")
    elif(auto=="Right"):
        if(gameData[1]=='L'): return getNum("RightOppositeScale")
        else: return getNum("RightScale")

    return num

def getTraj(num):
    name = getName(num)
    path = os.path.join(os.path.dirname(__file__),name)
    if(not os.path.exists(path)): os.makedirs(path)

    pickle_file1 = os.path.join(path,"Right.pickle")
    pickle_file2 = os.path.join(path,"Left.pickle")
    pickle_file3 = os.path.join(path,"Modifier.pickle")

    if wpilib.RobotBase.isSimulation():
        points = makeTraj(num)
        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
            dt=0.02, max_velocity=8.0, max_acceleration=6.0, max_jerk=120.0)

        modifier = pf.modifiers.TankModifier(trajectory).modify(self.width/2.4)
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
    # This code renders the followed path on the field in simulation (requires pyfrc 2018.2.0+)
    if wpilib.RobotBase.isSimulation():
        from pyfrc.sim import get_user_renderer
        renderer = get_user_renderer()
        if renderer:
            renderer.draw_pathfinder_trajectory(left, color='#0000ff', offset=(-self.width/2,0))
            renderer.draw_pathfinder_trajectory(modifier.source, color='#00ff00', show_dt=1.0, dt_offset=0.0)
            renderer.draw_pathfinder_trajectory(right, color='#0000ff', offset=(self.width/2,0))

def initPath(drivetrain):
    global init

    num = calcNum()
    [left,right,modifier] = getTraj(num)

    gains = [25,0,2,1/8,1/6] #P,I,D,1/V,1/A

    leftFollower = pf.followers.EncoderFollower(left)
    leftFollower.configureEncoder(drivetrain.encoders.get()[0], 127, 4/12) #Pulse Initial, pulsePerRev, WheelDiam
    leftFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    rightFollower = pf.followers.EncoderFollower(right)
    rightFollower.configureEncoder(drivetrain.encoders.get()[1], 255, 4/12) #Pulse Initial, pulsePerRev, WheelDiam
    rightFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    drivetrain.enablePIDs()

    showPath(left,right,modifier)

    timer.reset()
    timer.start()

    init = True

    return [leftFollower,rightFollower]

def followPath(drivetrain, leftFollower, rightFollower):
    global desiredHeading
    if(timer.get()>0.25 and not leftFollower.isFinished()):
        l = leftFollower.calculate(drivetrain.encoders.get()[0])
        r = rightFollower.calculate(drivetrain.encoders.get()[1])
        desiredHeading = pf.r2d(leftFollower.getHeading()) #degrees
        #drivetrain.navx.setPID(desiredHeading)
        #turn = drivetrain.navx.getPID()
        drivetrain.tank(l+turn,r-turn)
    else: drivetrain.stop()

def pathFinder(drivetrain):
    global leftFollower
    global rightFollower

    if(init==False and len(self.gameData)>0 and len(self.auto)>0): [leftFollower, rightFollower] = initPath(drivetrain)
    if(init==True): followPath(drivetrain,leftFollower,rightFollower)
