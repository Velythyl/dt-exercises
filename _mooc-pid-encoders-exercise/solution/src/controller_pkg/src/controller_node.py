#!/usr/bin/env python3
import numpy as np
import rospy

from duckietown.dtros import DTROS, NodeType, TopicType
from duckietown_msgs.msg import WheelEncoderStamped, Twist2DStamped
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry

import PID_controller

import time


class EncoderPoseNode(DTROS):
    """
        Computes an estimate of the Duckiebot pose using the wheel encoders.
        Args:
            node_name (:obj:`str`): a unique, descriptive name for the ROS node
        Configuration:

        Publisher:
            ~encoder_localization (:obj:`PoseStamped`): The computed position
        Subscribers:
            ~/left_wheel_encoder_node/tick (:obj:`WheelEncoderStamped`):
                encoder ticks
            ~/right_wheel_encoder_node/tick (:obj:`WheelEncoderStamped`):
                encoder ticks
    """

    def __init__(self, node_name):

        # Initialize the DTROS parent class
        super(EncoderPoseNode, self).__init__(
            node_name=node_name,
            node_type=NodeType.LOCALIZATION
        )
        # get the name of the robot
        self.veh = rospy.get_namespace().strip("/")

        # Add the node parameters to the parameters dictionary
        self.delta_phi_left = 0
        self.left_tick_prev = ""

        self.delta_phi_right = 0
        self.right_tick_prev = ""

        self.x_prev = 0
        self.y_prev = 0
        self.theta_prev = 0

        self.x_curr = 0
        self.y_curr = 0
        self.theta_curr = 0

        self.prev_e = 0
        self.prev_int = 0
        self.time = 0
        self.v_0 = 0.2
        self.y_ref=-0.10

        # nominal R and L:
        self.R = rospy.get_param(f'/{self.veh}/kinematics_node/radius', 100)
        self.baseline = rospy.get_param(f'/{self.veh}/kinematics_node/baseline', 100)

        # Construct publishers
        self.db_estimated_pose = rospy.Publisher(
            f'/{self.veh}/encoder_localization',
            Odometry,
            queue_size=1,
            dt_topic_type=TopicType.LOCALIZATION
        )

        # Wheel encoders subscribers:
        left_encoder_topic = f'/{self.veh}/left_wheel_encoder_node/tick'
        self.enco_left = rospy.Subscriber(
            left_encoder_topic,
            WheelEncoderStamped,
            self.cbLeftEncoder,
            queue_size=1
        )

        right_encoder_topic = f'/{self.veh}/right_wheel_encoder_node/tick'
        self.enco_right = rospy.Subscriber(
            right_encoder_topic,
            WheelEncoderStamped,
            self.cbRightEncoder,
            queue_size=1
        )

        car_cmd_topic = f'/{self.veh}/joy_mapper_node/car_cmd'
        self.pub_car_cmd = rospy.Publisher(
            car_cmd_topic,
            Twist2DStamped,
            queue_size=1,
            dt_topic_type=TopicType.CONTROL
        )

        self.SIM_STARTED = False
        rospy.Timer(rospy.Duration(0.2), self.Controller)

        self.log("Initialized!")
    
    def poseEstimation(self, R,
                    baseline,
                    x_prev,
                    y_prev,
                    theta_prev,
                    delta_phi_left,
                    delta_phi_right):
        """
            Calculate the current Duckiebot pose using dead reckoning approach,
            based on the kinematic model.

            Returns:
                x_curr, y_curr, theta_curr (:double: values)
        """
        x_curr = x_prev + R*(delta_phi_left+delta_phi_right)*np.cos(theta_prev)/2
        y_curr = y_prev + R*(delta_phi_left+delta_phi_right)*np.sin(theta_prev)/2
        theta_curr = theta_prev + R*(delta_phi_right-delta_phi_left)/(baseline)

        #x_curr = y_curr = theta_curr=0

        return x_curr, y_curr, theta_curr
    
    
    
    def DeltaPhi(self, encoder_msg, prev_ticks):
        """
            Args:
                encoder_msg (ROS encoder message)
                prev_ticks (Current ticks)
            Return:
                rotation_wheel (double) Rotation of the wheel
                ticks (int) current number of ticks
        """
        #rotation_wheel = ticks = 0

        ticks = encoder_msg.data

        delta_ticks = ticks-prev_ticks

        N_tot = encoder_msg.resolution

        alpha = 2*np.pi/N_tot

        rotation_wheel = alpha*delta_ticks

        return rotation_wheel, ticks 

    def cbLeftEncoder(self, encoder_msg):
        """
            Wheel encoder callback, the rotation of the wheel.
            Args:
                encoder_msg (:obj:`WheelEncoderStamped`) encoder ROS message.
        """
        ticks = encoder_msg.data

        if self.left_tick_prev == "":
            self.left_tick_prev = ticks
            return

        self.delta_phi_left, self.left_tick_prev = self.DeltaPhi(
            encoder_msg, self.left_tick_prev)
        # compute the new pose
        self.posePublisher()
        self.SIM_STARTED = True

    def cbRightEncoder(self, encoder_msg):
        """
            Wheel encoder callback, the rotation of the wheel.
            Args:
                encoder_msg (:obj:`WheelEncoderStamped`) encoder ROS message.
        """
        ticks = encoder_msg.data

        if self.right_tick_prev == "":
            self.right_tick_prev = ticks
            return

        self.delta_phi_right, self.right_tick_prev = self.DeltaPhi(
            encoder_msg, self.right_tick_prev)
        # compute the new pose
        self.posePublisher()
        self.SIM_STARTED = True

    def posePublisher(self):
        """
            Publish the pose of the Duckiebot given by the kinematic model
                using the encoders.
            Publish:
                ~/encoder_localization (:obj:`PoseStamped`): Duckiebot pose.
        """
        self.x_curr, self.y_curr, self.theta_curr = self.poseEstimation(
            self.R, self.baseline,
            self.x_prev, self.y_prev, self.theta_prev,
            self.delta_phi_left, self.delta_phi_right)

        self.x_prev = self.x_curr
        self.y_prev = self.y_curr
        self.theta_prev = self.theta_curr

        odom = Odometry()
        odom.header.frame_id = "map"
        odom.header.stamp = rospy.Time.now()

        odom.pose.pose.position.x = self.x_curr
        odom.pose.pose.position.y = self.y_curr
        odom.pose.pose.position.z = 0

        odom.pose.pose.orientation.x = 0
        odom.pose.pose.orientation.y = 0
        odom.pose.pose.orientation.z = np.sin(self.theta_curr/2)
        odom.pose.pose.orientation.w = np.cos(self.theta_curr/2)

        self.db_estimated_pose.publish(odom)
        
    def Controller(self, event):
        """
        Calculate theta and perform the control actions given by the PID
        """
        if not self.SIM_STARTED:
            return

        delta_time = time.time()-self.time

        self.time = time.time()
        
        u, self.prev_e, self.prev_int = PID_controller.PIDController(
            self.v_0,
            self.y_ref,
            self.y_curr,
            self.prev_e,
            self.prev_int,
            delta_time
        )

        if u == []:
            return

        # self.setGain(u[1])
        self.publishCmd(u)
    #
    # Pose estimation is the function that is created by the user.
    #
    def publishCmd(self, u):
        """Publishes a car command message.

        Args:
            omega (:obj:`double`): omega for the control action.
        """       

        car_control_msg = Twist2DStamped()
        car_control_msg.header.stamp = rospy.Time.now()

        car_control_msg.v = u[0]  # v
        car_control_msg.omega = u[1]  # omega

        self.pub_car_cmd.publish(car_control_msg)

    def onShutdown(self):
        super(EncoderPoseNode, self).onShutdown()


if __name__ == "__main__":
    # Initialize the node
    encoder_pose_node = EncoderPoseNode(node_name='encoder_pose_node')
    # Keep it spinning
    rospy.spin()
