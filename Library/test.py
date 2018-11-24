import util
import DCMotorTransmission
import DifferentialDrive

transmission = DCMotorTransmission.DCMotorTransmission(1, 1, 0)
drive = DifferentialDrive.DifferentialDrive(100, 10, 1, 0.05, 0.5, transmission, transmission)
