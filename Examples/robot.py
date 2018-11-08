import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import ctre


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.Intake1 = ctre.WPI_TalonSRX(20)
        self.Intake2 = ctre.WPI_TalonSRX(51)
        self.Intake2.follow(self.Intake)

    def teleopInit(self):
        self.count = 0

    def teleopPeriodic(self):
        self.count += 1
        sd.putNumber("count", self.count)
        self.Intake1.set(-0.5)

if __name__ == '__main__':
    wpilib.run(MyRobot)
