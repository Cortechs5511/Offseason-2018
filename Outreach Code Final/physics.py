import math
#import numpy as np

from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

import sim.simComms as simComms

class PhysicsEngine(object):
    def __init__(self, controller):
        self.controller = controller
        self.position = 0

        self.DistPerPulseL = 4/12 * math.pi / 255
        self.DistPerPulseR = -4/12 * math.pi / 127

        # Change these parameters to fit your robot!
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_MINI_CIM,           # motor configuration
            140*units.lbs,                           # robot mass
            6,                                   # drivetrain gear ratio
            3,                                       # motors per side
            (33/12)*units.feet,        # robot wheelbase
            (40/12)*units.feet,     # robot width
            (35/12)*units.feet,    # robot length
            (4/12)*units.feet         # wheel diameter
        )

        self.distance = [0.0,0.0]

        self.controller.add_device_gyro_channel('navxmxp_spi_4_angle')

        self.deadZone=0#0.40

    def update_sim(self, hal_data, now, timeDiff):
        # Simulate the drivetrain
        left = hal_data['CAN'][10]['value']#*1.01
        right = hal_data['CAN'][20]['value']#*0.99

        if(abs(left)<self.deadZone): left = 0
        if(abs(right)<self.deadZone): right = 0

        x,y,angle = self.drivetrain.get_distance(-left, right, timeDiff)
        self.controller.distance_drive(x, y, angle)

        if(simComms.getEncoders()==True):
            self.distance = [0,0]
            simComms.resetEncodersSim()
        else:
            self.distance[0] += self.drivetrain.l_velocity*timeDiff
            self.distance[1] += self.drivetrain.r_velocity*timeDiff

        hal_data['encoder'][0]['count'] = int(self.distance[0]/self.DistPerPulseL)
        hal_data['encoder'][1]['count'] = int(self.distance[1]/self.DistPerPulseR)

        #lift = hal_data['CAN'][30]['value']
        #hal_data['encoder'][2]['count'] += int(lift*100)

        #wrist = hal_data['CAN'][40]['value']
        #hal_data['encoder'][3]['count'] += int(wrist*100)

        #intake = hal_data['CAN'][50]['value']
        #hal_data['encoder'][4]['count'] += int(intake*100)
