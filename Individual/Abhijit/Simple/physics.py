import math
import numpy as np

from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

import sim.simComms as simComms
import helper.helper as helper

class PhysicsEngine(object):
    def __init__(self, controller):
        self.controller = controller
        self.position = 0

        # Change these parameters to fit your robot!
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_MINI_CIM,           # motor configuration
            140*units.lbs,                           # robot mass
            6,                                   # drivetrain gear ratio
            3,                                       # motors per side
            (helper.getWidth())*units.feet,        # robot wheelbase
            helper.getWidthBumpers()*units.feet,     # robot width
            helper.getLengthBumpers()*units.feet,    # robot length
            helper.getWheelDiam()*units.feet         # wheel diameter
        )

        self.distance = [0,0]

        self.controller.add_device_gyro_channel('navxmxp_spi_4_angle')

        self.deadZone=0.4

    def update_sim(self, hal_data, now, timeDiff):
        # Simulate the drivetrain
        left = hal_data['CAN'][10]['value']
        right = hal_data['CAN'][20]['value']

        if(abs(left)<self.deadZone): left = 0
        if(abs(right)<self.deadZone): right = 0

        x,y,angle = self.drivetrain.get_distance(-left, right, timeDiff)
        self.controller.distance_drive(x, y, angle)

        self.distance[0] += self.drivetrain.l_velocity*timeDiff
        self.distance[1] += self.drivetrain.r_velocity*timeDiff

        hal_data['encoder'][0]['count'] = int(self.distance[0]/helper.getDistPerPulse())
        hal_data['encoder'][1]['count'] = int(self.distance[1]/helper.getDistPerPulse())
