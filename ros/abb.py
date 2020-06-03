#!/usr/bin/env python

import pygame
import rospy
from sensor_msgs.msg import JointState

# Initialize joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialize ROS
rospy.init_node('abb')
pub = rospy.Publisher('abb_joint_states', JointState, queue_size=10)
rate = rospy.Rate(20) # hz

# Control loop
joint_1_position = 0.0
joint_2_position = 0.0
joint_3_position = 0.0
joint_4_position = 0.0

while not rospy.is_shutdown():

    # Get joystick values
    pygame.event.pump()
    joint_1_axis =  joystick.get_axis(0) # [-1, 1]
    joint_2_axis = -joystick.get_axis(1) # [-1, 1]
    joint_3_axis =  joystick.get_axis(2) # [-1, 1]
    joint_4_axis = -joystick.get_axis(3) # [-1, 1]

    # Prepare joint state message
    jointstates = JointState()
    jointstates.header.stamp = rospy.Time.now()
    jointstates.name = ['joint_1', 'joint_2', 'joint_3', 'joint_4']

    # Compute joint_1 position based on joystick
    joint_1_position = joint_1_position - 0.02 * joint_1_axis
    joint_1_position = min(max(joint_1_position, -2.97), 2.97)

    # Compute joint_2 position based on joystick
    joint_2_position = joint_2_position - 0.02 * joint_2_axis
    joint_2_position = min(max(joint_2_position, -1.13), 1.49)

    # Compute joint_3 position based on joystick
    joint_3_position = joint_3_position - 0.02 * joint_3_axis
    joint_3_position = min(max(joint_3_position, -3.14), 1.22)

    # Compute joint_4 position based on joystick
    joint_4_position = joint_4_position + 0.02 * joint_4_axis
    joint_4_position = min(max(joint_4_position, -5.24), 5.24)

    # Publish the joint states
    jointstates.position = [joint_1_position, joint_2_position, joint_3_position, joint_4_position]
    pub.publish(jointstates)

    # Control the loop rate
    rate.sleep()

# Cleanup
pygame.quit()
