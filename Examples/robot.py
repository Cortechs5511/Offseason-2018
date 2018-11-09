import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import ctre


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.Intake1 = ctre.WPI_TalonSRX(50)
        self.Intake2 = ctre.WPI_TalonSRX(51)
        self.Intake2.follow(self.Intake1)
        AxisPowers = wpilib.Joystick(2)

    def teleopInit(self):
        self.count = 0

    def teleopPeriodic(self):
        self.count += 1
        sd.putNumber("count", self.count)
        west = AxisPowers.getAxis(5)
        self.Intake1.set(west)

if __name__ == '__main__':
    wpilib.run(MyRobot)
