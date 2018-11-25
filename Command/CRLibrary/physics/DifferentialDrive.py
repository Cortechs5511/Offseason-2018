#Dynamic model a differential drive robot
#Center of mass is coincident with center of rotation assumed

import CRLibrary
import CRLibrary.util.util as util
import CRLibrary.util.units as units
import CRLibrary.physics.DCMotorTransmission as DCMotorTransmission

class DifferentialDrive:
    #all units must be in SI!!

    #Equivalent mass when accelerating purely lienarly, in kg
    #equivalent in that it also absorbs effects of drivetrain inertia
    #measured by doing drivetrain acceleration characterization in a straight line
    __mass__ = 0

    #equivalent moment of inertia when accelerating purely angularly, in kg*m^2
    #this is equivalent in that it also absorbs the effects of drivetrain inertia
    #measure by doing drivetrain acceleration characterization while turning in place
    __moi__ = 0

    #drag torque proportional to angular velocity that resists turning, in N*m/rad/s
    #Emperical testing of drivebase shows that there was an unexplained loss of torque,
    #proportional to velocity, likely due to scrube of wheelsself.
    #Note this might not be purely linear
    __angularDrag__ = 0 #initially assume zero until further testing

    #measured by rolling the robot a known distance and counting encoder ticks
    __wheelRadius__ = 0 #in meters

    #Effective kinematic wheelbase radius. Might be larger than theoretical to compensate for skid steer
    #Measure by turning in place several times and figuring out what the equivalent wheelbase radius is
    __effWheelbaseRadius__ = 0 #in meters

    #Transmission for both sides of the drivebase
    __leftTransmission__ = None
    __rightTransmission__ = None

    def __init__(self,mass, moi, angularDrag, wheelRadius, effWheelbaseRadius, leftTransmission, rightTransmission):
        self.__mass__ = mass
        self.__moi__ =  moi
        self.__angularDrag__ = angularDrag #initially assume zero until further testing
        self.__wheelRadius__ = wheelRadius
        self.__effWheelbaseRadius__ = effWheelbaseRadius
        self.__leftTransmission__ = leftTransmission
        self.__rightTransmission__ = rightTransmission

    def mass(self): return self.__mass__
    def moi(self): return self.__moi__
    def angularDrag(self): return self.__angularDrag__
    def wheelRadius(self): return self.__wheelRadius__
    def effWheelbaseRadius(self): return self.__effWheelbaseRadius__
    def leftTransmission(self): return self.__leftTransmission__
    def rightTransmission(self): return self.__rightTransmission__

    #The following two functions can be solved either in velocity or acceleration, the math is the same
    def solveForwardKinematics(self, wheelMotion):
        chassisMotion = ChassisState()
        chassisMotion.linear = self.wheelRadius() * (wheelMotion.right+wheelMotion.left)/2
        chassisMotion.angular = self.wheelRadius() * (wheelMotion.right-wheelMotion.left)/(2*self.effWheelbaseRadius())
        return chassisMotion

    def solveInverseKinematics(self, chassisMotion):
        wheelMotion = WheelState()
        wheelMotion.left = (chassisMotion.linear-self.effWheelbaseRadius()*chassisMotion.angular)/self.wheelRadius()
        wheelMotion.right = (chassisMotion.linear+self.effWheelbaseRadius()*chassisMotion.angular)/self.wheelRadius()
        return wheelMotion

    def solveForwardDynamics_CS(self, chassisVelocity, voltage):
        dynamics = DriveDynamics()
        dynamics.wheelVelocity = self.solveInverseKinematics(chassisVelocity)
        dynamics.chassisVelocity = chassisVelocity
        if(util.epsilonEquals(dynamics.chassisVelocity.linear,0)): dynamics.curvature = 0
        else: dynamics.curvature = dynamics.chassisVelocity.angular/dynamics.chassisVelocity.linear
        dynamics.voltage = voltage
        self.solveForwardDynamics(dynamics)
        return dynamics

    def solveForwardDynamics_WS(self, wheelVelocity, voltage):
        dynamics = DriveDynamics()
        dynamics.wheelVelocity = wheelVelocity
        dynamics.chassisVelocity = self.solveForwardKinematics(wheelVelocity)
        if(util.epsilonEquals(dynamics.chassisVelocity.linear,0)): dynamics.curvature = 0
        else: dynamics.curvature = dynamics.chassisVelocity.angular/dynamics.chassisVelocity.linear
        dynamics.voltage = voltage
        self.solveForwardDynamics(dynamics)
        return dynamics

    def solveForwardDynamics(self, dynamics):
        leftStationary = util.epsilonEquals(dynamics.wheelVelocity.left,0) and abs(dynamics.voltage.left) < self.leftTransmission().frictionVoltage()
        rightStationary = util.epsilonEquals(dynamics.wheelVelocity.right,0) and abs(dynamics.voltage.right) < self.rightTransmission().frictionVoltage()

        if(leftStationary and rightStationary):
            dynamics.wheelTorque.left = 0
            dynamics.wheelTorque.right = 0
            dynamics.chassisAcceleration.linear = 0
            dynamics.chassisAcceleration.angular = 0
            dynamics.wheelAcceleration.left = 0
            dynamics.wheelAcceleration.right = 0
            dynamics.dcurvature = 0
            return

        dynamics.wheelTorque.left = self.leftTransmission().getTorqueForVoltage(dynamics.wheelVelocity.left, dynamics.voltage.left)
        dynamics.wheelTorque.right = self.rightTransmission().getTorqueForVoltage(dynamics.wheelVelocity.right, dynamics.voltage.right)

        #add forces and torques about the center of mass
        dynamics.chassisAcceleration.linear = (dynamics.wheelTorque.right + dynamics.wheelTorque.left) / (self.wheelRadius()*self.mass())

        #(Tr-Tl)/r_w*r_wb-drag*w=I*angular_accel
        dynamics.chassisAcceleration.angular = self.effWheelbaseRadius() * (dynamics.wheelTorque.right-dynamics.wheelTorque.left)/(self.wheelRadius()*self.moi())-dynamics.chassisVelocity.angular*self.angularDrag()/self.moi()

        #solve for change in curvature from angular wheelAcceleration
        #total angular acceleration = linear acceleration * curvature + v^2 * dcurvature
        if(util.epsilonEquals(dynamics.chassisVelocity.linear,0)): dynamics.dcurvature = 0
        else: dynamics.dcurvature = (dynamics.chassisAcceleration.angular-dynamics.chassisAcceleration.linear*dynamics.curvature)/(dynamics.chassisVelocity.linear**2)

        dynamics.wheelAcceleration.left = dynamics.chassisAcceleration.linear - dynamics.chassisAcceleration.angular * self.effWheelbaseRadius()
        dynamics.wheelAcceleration.right = dynamics.chassisAcceleration.linear + dynamics.chassisAcceleration.angular * self.effWheelbaseRadius()

    def solveInverseDynamics_CS(self, chassisVelocity, chassisAcceleration):
        dynamics = DriveDynamics()
        dynamics.chassisVelocity = chassisVelocity
        if(util.epsilonEquals(dynamics.chassisVelocity.linear,0)): dynamics.curvature = 0
        else: dynamics.curvature = dynamics.chassisVelocity.angular/dynamics.chassisVelocity.linear
        dynamics.chassisAcceleration = chassisAcceleration
        if(util.epsilonEquals(dynamics.chassisVelocity.linear,0)): dynamics.dcurvature = 0
        else: dynamics.dcurvature = (dynamics.chassisAcceleration.angular-dynamics.chassisAcceleration.linear*dynamics.curvature)/(dynamics.chassisVelocity.linear**2)
        dynamics.wheelVelocity = self.solveInverseKinematics(chassisVelocity)
        dynamics.wheelAcceleration = self.solveInverseKinematics(chassisAcceleration)
        self.solveInverseDynamics(dynamics)
        return dynamics

    def solveInverseDynamics_WS(self, wheelVelocity, wheelAcceleration):
        dynamics = DriveDynamics()
        dynamics.chassisVelocity = self.solveForwardKinematics(wheelVelocity)
        if(util.epsilonEquals(dynamics.chassisVelocity.linear,0)): dynamics.curvature = 0
        else: dynamics.curvature = dynamics.chassisVelocity.angular/dynamics.chassisVelocity.linear
        dynamics.chassisAcceleration = self.solveForwardKinematics(wheelAcceleration)
        if(util.epsilonEquals(dynamics.chassisVelocity.linear,0)): dynamics.dcurvature = 0
        else: dynamics.dcurvature = (dynamics.chassisAcceleration.angular-dynamics.chassisAcceleration.linear*dynamics.curvature)/(dynamics.chassisVelocity.linear**2)
        dynamics.wheelVelocity = wheelVelocity
        dynamics.wheelAcceleration = wheelAcceleration
        self.solveInverseDynamics(dynamics)
        return dynamics

    #assumptions about dynamics: velocities and accelerations provided, curvature and dcurvature computed
    def solveInverseDynamics(self, dynamics):
        #determine the necessary torques on the left and right wheels to produce the desired wheel accelerations
        dynamics.wheelTorque.left = self.wheelRadius()/2 * (dynamics.chassisAcceleration.linear*self.mass()-dynamics.chassisAcceleration.angular*self.moi()/self.effWheelbaseRadius()-dynamics.chassisVelocity.angular*self.angularDrag()/self.effWheelbaseRadius())
        dynamics.wheelTorque.right = self.wheelRadius()/2 * (dynamics.chassisAcceleration.linear*self.mass()+dynamics.chassisAcceleration.angular*self.moi()/self.effWheelbaseRadius()+dynamics.chassisVelocity.angular*self.angularDrag()/self.effWheelbaseRadius())

        dynamics.voltage.left = self.leftTransmission().getVoltageForTorque(dynamics.wheelVelocity.left, dynamics.wheelTorque.left)
        dynamics.voltage.right = self.leftTransmission().getVoltageForTorque(dynamics.wheelVelocity.right, dynamics.wheelTorque.right)

    def getMaxAbsVelocity(self, curvature, dcurvature, maxAbsVoltage):
        leftSpeedAtMaxVoltage = self.leftTransmission().freeSpeedAtV(maxAbsVoltage)
        rightSpeedAtMaxVoltage = self.rightTransmission().freeSpeedAtV(maxAbsVoltage)

        if(util.epsilonEquals(curvature, 0)): return self.wheelRadius()*min(leftSpeedAtMaxVoltage, rightSpeedAtMaxVoltage)
        if(abs(curvature)>1/util.kEpsilon):
            wheelSpeed = math.min(leftSpeedAtMaxVoltage, rightSpeedAtMaxVoltage)
            return util.sign(curvature) * self.wheelRadius() * wheelSpeed/self.effWheelbaseRadius()

        rightSpeedIfLeftMax = leftSpeedAtMaxVoltage * (self.effWheelbaseRadius()*curvature+1)/(1-self.effWheelbaseRadius()*curvature)
        if(abs(rightSpeedIfLeftMax)<=rightSpeedAtMaxVoltage+util.kEpsilon): return self.wheelRadius() * (leftSpeedAtMaxVoltage+rightSpeedIfLeftMax)/2
        leftSpeedIfRightMax = rightSpeedAtMaxVoltage * (1-self.effWheelbaseRadius()*curvature)/(1+self.effWheelbaseRadius()*curvature)
        return self.wheelRadius() * (rightSpeedAtMaxVoltage+leftSpeedIfRightMax)/2

#can refer to velocity or acceleration depending on context
class ChassisState:
    linear = 0
    angular = 0

    def __init__(self, linearIn=0, angularIn=0):
        self.linear = linearIn
        self.angular = angularIn

    def print(self, name = ""):
        print(name + " (" + str(self.linear)+","+str(self.angular)+")")

#can refer to many things (velocity, acceleration, torque, voltage, etc.) depending on context
class WheelState:
    left = 0
    right = 0

    def __init__(self, leftIn=0, rightIn=0):
        self.left = leftIn
        self.right = rightIn

    def get(getLeft):
        if(getLeft): return left
        else: return right

    def set(setLeft, val):
        if(setLeft): left = val
        else: right = val

    def print(self, name = ""):
        print(name + " (" + str(self.left)+","+str(self.right)+")")

class DriveDynamics:
    curvature = 0.0 #1/m
    dcurvature = 0.0 #1/m^2
    chassisVelocity = ChassisState() #m/s
    chassisAcceleration = ChassisState() #m/s^2
    wheelVelocity = WheelState() #rad/s
    wheelAcceleration = WheelState() #rad/s^2
    voltage = WheelState() #V
    wheelTorque = WheelState() #N m

    def print(self):
        print("Drive Dynamics")
        print("Curvature: " + str(self.curvature))
        print("DCurvature: " + str(self.dcurvature))
        self.chassisVelocity.print("ChassisVelocity")
        self.chassisAcceleration.print("ChassisAcceleration")
        self.wheelVelocity.print("WheelVelocity")
        self.wheelAcceleration.print("wheelAcceleration")
        self.voltage.print("Voltage")
        self.wheelTorque.print("Wheel Torque")
        print()

    def getVoltage(self):
        return [self.voltage.left, self.voltage.right]
