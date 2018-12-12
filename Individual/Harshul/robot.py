import ctre
import wpilib

class MyRobot(wpilib.TimedRobot):

  def robotInit(self):
      #initialize motors
      #(left)
      self.DriveLeft1 = ctre.WPI_TalonSRX(10)
      self.DriveLeft2 = ctre.WPI_VictorSPX(11)
      self.DriveLeft3 = ctre.WPI_VictorSPX(12)
      self.DriveLeft2.follow(self.DriveLeft1)
      self.DriveLeft3.follow(self.DriveLeft1)
      #(right)
      self.DriveRight1 = ctre.WPI_TalonSRX(20)
      self.DriveRight2 = ctre.WPI_VictorSPX(21)
      self.DriveRight3 = ctre.WPI_VictorSPX(22)
      self.DriveRight2.follow(self.DriveRight1)
      self.DriveRight3.follow(self.DriveRight1)


      #intakes
      self.intake = ctre.WPI_TalonSRX(50)
      self.intake = ctre.WPI_TalonSRX(51)

      # IDK
      self.LeftEncoder = wpilib.Encoder(0, 1)
      self.RightEncoder = wpilib.Encoder(2, 3)
      #controller
      self.Controller = wpilib.XboxController(0)

  def teleopPeriod(self):
      maxSpeed = .85
      #right joystick
      if self.Controller.getY(1) > 0.25:
          # move left forward
          self.DriveLeft1.set(set.Controller.getY(1)*maxSpeed)
      elif self.Controller.getY(0) > 0.25:
          #move right forward
          self.DriveRight1.set(set.Controller.getY(0)*maxSpeed)
      if self.Controller.getXButton() == True:
          self.intake.set(1)
      elif self.Controller.getAButton() == True:
          self.intake.set(1)

if __name__ == '__main__':
    wpilib.run(MyRobot)
