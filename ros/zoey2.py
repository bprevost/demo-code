#!/usr/bin/env python

import pygame
import rospy
from sensor_msgs.msg import JointState
from math import pi

# Initialize joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialize ROS
rospy.init_node('zoey')
pub = rospy.Publisher('zoey_joint_states', JointState, queue_size=10)
rate = rospy.Rate(10) # hz

# Control loop
neck_position = 0.0
head_position = 0.0
while not rospy.is_shutdown():

    # Get joystick values
    pygame.event.pump()
    neck_axis = joystick.get_axis(1) # [-1, 1]
    head_axis = joystick.get_axis(2) # [-1, 1]

    # Prepare joint state message
    jointstates = JointState()
    jointstates.header.stamp = rospy.Time.now()
    jointstates.name = ['neck_joint', 'head_swivel']

    # Compute neck position based on joystick
    neck_position = neck_position + 0.01 * (-neck_axis)
    neck_position = min(max(neck_position, 0), 1)

    # Compute head position based on joystick
    head_position = head_position + pi/20 * head_axis

    # Publish the joint states
    jointstates.position = [neck_position, head_position]
    pub.publish(jointstates)

    # Control the loop rate
    rate.sleep()

# Cleanup
pygame.quit()
