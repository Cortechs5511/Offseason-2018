
import wpilib
import ctre
import wpilib.drive

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.stick1 = wpilib.Joystick(0)
        self.stick2 = wpilib.Joystick(1)

        self.rightTop = ctre.WPI_VictorSPX(21)
        self.rightMiddle = ctre.WPI_TalonSRX(20)
        self.rightBottom = ctre.WPI_VictorSPX(22)
        self.drive_right = wpilib.drive.SpeedControllerGroup(rightTop, rightMiddle, rightBottom)

        self.leftTop = ctre.WPI_VictorSPX(11)
        self.leftMiddle = ctre.WPI_TalonSRX(10)
        self.leftBottom = ctre.WPI_VictorSPX(12)
        self.drive_left = wpilib.drive.SpeedControllerGroup(leftTop, leftMiddle, leftBottom)

        self.drive = wpilib.DifferentialDrive(self.drive_right, self.drive_left)


        def teleopPeriodic(self):
            self.drive.tankDrive(self.stick1.getY(), self.stick.getX())





if _name_ == '_main_':
    wpilib.run(MyRobot)
