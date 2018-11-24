#Dynamic model a differential drive robot
#Center of mass is coincident with center of rotation assumed

from ..Util import util

class DifferentialDrive:
    #all units must be in SI!!

    #Equivalent mass when accelerating purely lienarly, in kg
    #equivalent in that it also absorbs effects of drivetrain inertia
    #measured by doing drivetrain acceleration characterization in a straight line
    __mass__

    #equivalent moment of inertia when accelerating purely angularly, in kg*m^2
    #this is equivalent in that it also absorbs the effects of drivetrain inertia
    #measure by doing drivetrain acceleration characterization while turning in place
    __moi__

    #drag torque proportional to angular velocity that resists turning, in N*m/rad/s
    #Emperical testing of drivebase shows that there was an unexplained loss of torque,
    #proportional to velocity, likely due to scrube of wheelsself.
    #Note this might not be purely linear
    __angularDrag__

    #measured by rolling the robot a known distance and counting encoder ticks
    __wheelRadius__ #in meters

    #Effective kinematic wheelbase radius. Might be larger than theoretical to compensate for skid steer
    #Measure by turning in place several times and figuring out what the equivalent wheelbase radius is
    __effWheelbaseRadius__ #in meters

    #Transmission for both sides of the drivebase
    __leftTransmission__
    __rightTransmission__

    def __init__(mass, moi, angularDrag, wheelRadius, effWheelbaseRadius, leftTransmission, rightTransmission):
        __mass__ = mass
        __moi__ =  moi
        __angularDrag__ = angularDrag
        __wheelRadius__ wheelRadius
        __effWheelbaseRadius__ = effWheelbaseRadius
        __leftTransmission__ = leftTransmission
        __rightTransmission__ = rightTransmission

    def mass():
        return __mass__

    def moi():
        return __moi__

    def wheelRadius():
        return __wheelRadius__

    def effWheelbaseRadius():
        return __effWheelbaseRadius__

    def leftTransmission():
        return __leftTransmission__

    def rightTransmission():
        return __rightTransmission__

    #The following two functions can be solved either in velocity or acceleration, the math is the same
    def solveForwardKinematics(wheelMotion):
        chassisMotion = ChassisState()
        chassisMotion.linear = wheelRadius() * (wheelMotion.right+wheelMotion.left)/2
        chassisMotion.angular = wheelRadius() * (wheelMotion.right-wheelMotion.left)/(2*effWheelbaseRadius())
        return chassisMotion

    def solveInverseKinematics(chassisMotion):
        wheelMotion = WheelState()
        wheelMotion.left = (chassisMotion.linear-effWheelbaseRadius()*chassisMotion.angular)/wheelRadius()
        wheelMotion.right = (chassisMotion.linear+effWheelbaseRadius()*chassisMotion.angular)/wheelRadius()
        return wheelMotion

    def solveForwardDynamics_CS(chassisVelocity, voltage):
        dyanmics = DriveDynamics()
        dynamics.wheelVelocity = solveInverseKinematics(chassisVelocity)
        dynamics.chassisVelocity = chassisVelocity
        dynamics.curvature = dynamics.chassisVelocity.angular/dynamics.chassisVelocity.linear
        if(math.isnan(dynamics.curvature)): dynamics.curvature = 0
        dynamics.voltage = voltage
        solveForwardDynamics(dynamics)
        return dynamics

    def solveForwardDynamics_WS(wheelVelocity, voltage):
        dynamics = DriveDynamics()
        dynamics.wheelVelocity = wheelVelocity
        dynamics.chassisVelocity = solveForwardKinematics(wheelVelocity)
        dynamics.curvature = dynamics.chassisVelocity.angular/dynamics.chassisVelocity.linear
        if(math.isnan(dynamics.curvature)): dynamics.curvature = 0
        dynamics.voltage = voltage
        solveForwardDynamics(dynamics)
        return dynamics

    def solveForwardDynamics(dynamics):
        leftStationary = util.epsilonEquals(dynamics.wheelVelocity.left,0) and abs(dynamics.voltage.left) < leftTransmission().frictionVoltage()
        rightStationary = util.epsilonEquals(dynamics.wheelVelocity.right,0) and abs(dynamics.voltage.right) < rightTransmission().frictionVoltage()

        if(leftStationary and rightStationary):
            dynamics.wheelTorque.left = 0
            dynamics.wheelTorque.right = 0
            dynamics.chassisAcceleration.linear = 0
            dynamics.chassisAcceleration.angular = 0
            dynamics.wheelAcceleration.left = 0
            dynamics.wheelAcceleration.right = 0
            dynamics.dcurvature = 0
            return

        dynamics.wheelTorque.left = leftTransmission.getTorqueForVoltage(dynamics.wheelVelocity.left, dynamics.voltage.left)
        dynamics.wheelTorque.right = rightTransmission.getTorqueForVoltage(dynamics.wheelVelocity.right, dynamics.voltage.right)

        #add forces and torques about the center of mass
        dynamics.chassisAcceleration.linear = (dynamics.wheelTorque.right + dynamics.wheelTorque.left) / (wheelRadius()*mass())

        #(Tr-Tl)/r_w*r_wb-drag*w=I*angular_accel
        dynamics.chassisAcceleration.angular = effWheelbaseRadius() * (dynamics.wheelTorque.right-dynamics.wheelTorque.left)/(wheelRadius()*moi())-dynamics.chassisVelocity.angular*angularDrag()/moi()

        #solve for change in curvature from angular wheelAcceleration
        #total angular acceleration = linear acceleration * curvature + v^2 * dcurvature
        dynamics.dcurvature = (dynamics.chassisAcceleration.angular-dynamics.chassisAcceleration.linear*dynamics.curvature)/(dynamics.chassisVelocity.linear**2)
        if(isnan(dynamics.dcurvature)): dynamics.dcurvature = 0

        dynamics.wheelAcceleration.left = dynamics.chassisAcceleration.linear - dynamics.chassisAcceleration.angular * effWheelbaseRadius()
        dynamics.wheelAcceleration.right = dynamics.chassisAcceleration.linear + dynamics.chassisAcceleration.angular * effWheelbaseRadius()

    def solveInverseDynamics_CS(chassisVelocity, chassisState):
        dynamics = DriveDynamics()
        dynamics.chassisVelocity = chassisVelocity
        dynamics.curvature = dynamics.chassisVelocity.angular/dynamics.chassisVelocity.linear
        if(isnan(dynamics.curvature)): dynamics.curvature = 0
        dynamics.chassisAcceleration = chassisAcceleration
        dynamics.dcurvature = (dynamics.chassisAcceleration.angular-dynamics.chassisAcceleration.linear*dynamics.curvature)/(dynamics.chassisVelocity.linear**2)
        if(isnan(dynamics.dcurvature)): dynamics.dcurvature = 0
        dynamics.wheelVelocity = solveInverseKinematics(chassisVelocity)
        dynamics.wheelAcceleration = solveInverseKinematics(chassisAcceleration)
        solveInverseDynamics(dynamics)
        return dynamics

    def solveInverseDynamics_WS(wheelVelocity, wheelState):
        dynamics = DriveDynamics()
        dynamics.chassisVelocity = solveForwardKinematics(wheelVelocity)
        dynamics.curvature = dynamics.chassisVelocity.angular/dynamics.chassisVelocity.linear
        if(isnan(dynamics.curvature)): dynamics.curvature = 0
        dynamics.chassisAcceleration = solveForwardKinematics(wheelAcceleration)
        dynamics.dcurvature = (dynamics.chassisAcceleration.angular-dynamics.chassisAcceleration.linear*dynamics.curvature)/(dynamics.chassisVelocity.linear**2)
        if(isnan(dynamics.dcurvature)): dynamics.dcurvature = 0
        dynamics.wheelVelocity = wheelVelocity
        dynamics.wheelAcceleration = wheelAcceleration
        solveInverseDynamics(dynamics)
        return dynamics

    #assumptions about dynamics: velocities and accelerations provided, curvature and dcurvature computed
    def solveInverseDynamics(dynamics):
        #determine the necessary torques on the left and right wheels to produce the desired wheel accelerations
        dynamics.wheelTorque.left = wheelRadius()/2 * (dynamics.chassisAcceleration.linear*mass()-dynamics.chassisAcceleration.angular*moi()/effWheelbaseRadius()-dynamics.chassisVelocity.angular*angularDrag()/effWheelbaseRadius())
        dynamics.wheelTorque.right = wheelRadius()/2 * (dynamics.chassisAcceleration.linear*mass()+dynamics.chassisAcceleration.angular*moi()/effWheelbaseRadius())+dynamics.chassisVelocity.angular*angularDrag()/effWheelbaseRadius())

        dynamics.voltage.left = leftTransmission.getVoltageForTorque(dynamics.wheelVelocity.left, dynamics.wheelTorque.left)
        dynamics.voltage.right = leftTransmission.getVoltageForTorque(dynamics.wheelVelocity.right, dynamics.wheelTorque.right)

    def getMaxAbsVelocity(curvature, dcurvature, maxAbsVoltage):
        leftSpeedAtMaxVoltage = leftTransmission.freeSpeedAtV(maxAbsVoltage)
        rightSpeedAtMaxVoltage = rightTransmission.freeSpeedAtV(maxAbsVoltage)

        if(util.epsilonEquals(curvature, 0)): return wheelRadius()*min(leftSpeedAtMaxVoltage, rightSpeedAtMaxVoltage)
        if(isnan(curvature)):
            wheelSpeed = math.min(leftSpeedAtMaxVoltage, rightSpeedAtMaxVoltage)
            return util.sign(curvature) * wheelRadius() * wheelSpeed/effWheelbaseRadius()

        rightSpeedIfLeftMax = leftSpeedAtMaxVoltage * (effWheelbaseRadius()*curvature+1)/(1-effWheelbaseRadius()*curvature)
        if(abs(rightSpeedIfLeftMax)<=rightSpeedAtMaxVoltage+util.kEpsilon):
            return wheelRadius() * (leftSpeedAtMaxVoltage+rightSpeedIfLeftMax)/2
        leftSpeedIfRightMax = rightSpeedAtMaxVoltage * (1-effWheelbaseRadius()*curvature)/(1+effWheelbaseRadius()*curvature)
        return wheelRadius() * (rightSpeedAtMaxVoltage+leftSpeedIfRightMax)/2

    #can refer to velocity or acceleration depending on context
    class ChassisState:
        linear
        angular

        def __init__(linearIn, angularIn):
            linear = linearIn
            angular = angularIn

        def __init__():
            linear = 0
            angular = 0

    class WheelState:
        left
        right

        def __init__(leftIn, rightIn):
            left = leftIn
            right = rightIn

        def __init__():
            left = 0
            right = 0

        def get(getLeft):
            return getLeft? left : right

        def set(setLeft, val):
            if(setLeft): left = val
            else: right = val

    class DriveDynamics:
        curvature = 0.0 #1/m
        dcurvature = 0.0 #1/m^2
        chassisVelocity = ChassisState() #m/s
        chassisAcceleration = ChassisState() #m/s^2
        wheelVelocity = WheelState() #rad/s
        wheelAcceleration = WheelState() #rad/s^2
        voltage = WheelState() #V
        wheelTorque = WheelState() #N m
