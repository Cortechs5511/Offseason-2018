import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from CRLibrary.physics import DifferentialDrive as ddrive
from CRLibrary.util import units
import odometry as od

timer = wpilib.Timer()

MAXV = 10
MAXA = 15
MAXJ = 20

width = 33/12

gains = [1,0,1,1/MAXV,0]

left = None
right = None
time = 0
maxTime = 0

navx = 0

prevV = 0
prevW = 0

leftVFinal = 0
rightVFinal = 0

leftVTemp = 0
rightVTemp = 0

TolVel = 0.2 #feet/second

DT = None

[kP,kI,kD,kF] = [0.00, 0.00, 0.00, 0.00]
if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.40, 0.00, 0.10, 0.00]

def getLeftVelocity():
    return od.get()[3] #feet/second

def getRightVelocity():
    return od.get()[4] #feet/second

def makeTraj(name):
    print("Here")
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
    elif(name=="CrazyTest"):
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

def initPath(drivetrain, name):
    global DT, left, right, time, maxTime, leftController, rightController

    DT = drivetrain

    [left,right,modifier] = getTraj(name)

    leftFollower = pf.followers.EncoderFollower(left)
    leftFollower.configureEncoder(drivetrain.getRaw()[0], 255, 4/12) #Pulse Initial, pulsePerRev, WheelDiam
    leftFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    rightFollower = pf.followers.EncoderFollower(right)
    rightFollower.configureEncoder(-drivetrain.getRaw()[1], 127, 4/12) #Pulse Initial, pulsePerRev, WheelDiam
    rightFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

    showPath(left,right,modifier)

    time = 0
    maxTime = len(left)

    leftController.enable()
    rightController.enable()
    angleController.enable()

    leftController.setSetpoint(0)
    rightController.setSetpoint(0)
    angleController.setSetpoint(0)

    return [leftFollower,rightFollower]

def followPath(DT):
    global left, right, time, maxTime, prevV, prevW, leftVTemp, rightVTemp, leftVFinal, rightVFinal, leftController, rightController

    if(time>=maxTime):
        leftController.disable()
        rightController.disable()
        return [0,0]

    leftSeg = left[time]
    rightSeg = right[time]
    time += 1

    xd = units.feetToMeters((leftSeg.x+rightSeg.x)/2)
    yd = units.feetToMeters((leftSeg.y+rightSeg.y)/2) #unsure if needs to be negated
    thetad = (leftSeg.heading+rightSeg.heading)/2 #unsure if needs to be negated

    leftVeld = units.feetToMeters(leftSeg.velocity)
    rightVeld = units.feetToMeters(rightSeg.velocity)

    leftAcceld = units.feetToMeters(leftSeg.acceleration)
    rightAcceld = units.feetToMeters(rightSeg.acceleration)

    vd = (rightVeld + leftVeld)/2
    wd = (rightVeld - leftVeld)/(2*DT.model.effWheelbaseRadius()) #unsure if needs to be negated

    ad = (rightAcceld + leftAcceld)/2
    alphad = (rightAcceld - leftAcceld)/(2*DT.model.effWheelbaseRadius())

    [x, y, theta, rightVel, leftVel] = od.getSI()
    [y, theta] = [-y, -theta]

    b = 1.5 #needs to be tuned
    zeta = 0.4 #needs to be tuned
    v = vd * math.cos(thetad-theta) + k(vd,wd,b,zeta) * ((xd-x) * math.cos(theta) + (yd-y) * math.sin(theta))
    w = wd + b * vd * sinc(angleDiffRad(thetad,theta)) * ((yd-y) * math.cos(theta) - (xd-x) * math.sin(theta)) + k(vd,wd,b,zeta) * angleDiffRad(thetad,theta) #unsure if needs to be negated

    leftOut = v - DT.model.effWheelbaseRadius()*w
    rightOut = v + DT.model.effWheelbaseRadius()*w

    a = 50*(v-prevV)
    alpha = 50*(w-prevW)

    prevV = v
    prevW = w

    chassisVel = ddrive.ChassisState(v,w)
    chassisAccel = ddrive.ChassisState(a,alpha)

    voltage = DT.model.solveInverseDynamics_CS(chassisVel, chassisAccel).getVoltage()
    [leftV, rightV] = [voltage[0]/12, voltage[1]/12]

    leftVTemp = leftV
    rightVTemp = rightV

    leftController.setSetpoint(units.metersToFeet(leftOut))
    rightController.setSetpoint(units.metersToFeet(rightOut))
    angleController.setSetpoint(boundDeg(units.radiansToDegrees(-thetad)))
    #return [leftVFinal+navx, rightVFinal-navx] #with b=0, zeta=0, should function like untuned pathfinder, ie inaccurate
    return [leftVFinal, rightVFinal]

def k(vd, wd, b, zeta):
    return 2 * zeta * math.sqrt(wd**2+b*vd**2)

def sinc(theta):
    if(theta==0): return 1
    return math.sin(theta)/boundRad(theta)

def setLeftVelocity(output):
    global leftVTemp, leftVFinal
    ff = leftVTemp
    leftVFinal = output + ff

def setRightVelocity(output):
    global rightVTemp, rightVFinal
    ff = rightVTemp
    rightVFinal = output + ff


leftController = wpilib.PIDController(kP, kI, kD, kF, source=getLeftVelocity, output=setLeftVelocity)
leftController.setInputRange(-MAXV-3, MAXV+3) #feet/second
leftController.setOutputRange(-1, 1) #percent
leftController.setAbsoluteTolerance(TolVel)
leftController.setContinuous(False)
leftController.disable()

rightController = wpilib.PIDController(kP, kI, kD, kF, source=getRightVelocity, output=setRightVelocity)
rightController.setInputRange(-MAXV-3, MAXV+3) #feet/second
rightController.setOutputRange(-1, 1) #percent
rightController.setAbsoluteTolerance(TolVel)
rightController.setContinuous(False)
rightController.disable()

def getAngle():
    global DT
    return boundDeg(DT.getAngle())

def setAngle(output):
    global navx
    navx = output

TolAngle = 3 #degrees
[kP,kI,kD,kF] = [0.024, 0.00, 0.20, 0.00]
if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.025,0.00,0.00,0.00]
angleController = wpilib.PIDController(kP, kI, kD, kF, source=getAngle, output=setAngle)
angleController.setInputRange(-180,  180) #degrees
angleController.setOutputRange(-0.9, 0.9)
angleController.setAbsoluteTolerance(TolAngle)
angleController.setContinuous(True)
angleController.disable()

def angleDiffDeg(a, b):
    diff = boundDeg(a)-boundDeg(b)
    diffMinus = diff - 360
    diffPlus = diff + 360
    if(abs(diffMinus)<abs(diff)): return diffMinus
    if(abs(diffPlus)<abs(diff)): return diffPlus
    return diff

def angleDiffRad(a,b):
    diff = boundRad(a)-boundRad(b)
    diffMinus = diff - 2*math.pi
    diffPlus = diff + 2*math.pi
    if(abs(diffMinus)<abs(diff)): return diffMinus
    if(abs(diffPlus)<abs(diff)): return diffPlus
    return diff

def boundDeg(angle):
    if(angle<-180): return boundDeg(angle+360)
    if(angle>180): return boundDeg(angle-360)
    return angle

def boundRad(angle):
    if(angle<-math.pi): return boundRad(angle+2*math.pi)
    if(angle>math.pi): return boundRad(angle-2*math.pi)
    return angle
