import util
import DCMotorTransmission
import DifferentialDrive

transmission = DCMotorTransmission.DCMotorTransmission(1, 1, 0)
drive = DifferentialDrive.DifferentialDrive(100, 10, 1, 0.05, 0.5, transmission, transmission)

#dynamics = DifferentialDrive.DriveDynamics()
chassisVelocity = DifferentialDrive.ChassisState(5, 4)
chassisAcceleration = DifferentialDrive.ChassisState(3, 2)

wheelVelocity = DifferentialDrive.WheelState(5, 4)
wheelAcceleration = DifferentialDrive.WheelState(3, 2)

voltage = DifferentialDrive.WheelState(10, 10)

drive.solveForwardDynamics_CS(chassisVelocity, voltage).print()
drive.solveForwardDynamics_WS(wheelVelocity, voltage).print()
drive.solveInverseDynamics_CS(chassisVelocity, chassisAcceleration).print()
drive.solveInverseDynamics_WS(wheelVelocity, wheelAcceleration).print()

print(drive.getMaxAbsVelocity(5, 4, 10))
