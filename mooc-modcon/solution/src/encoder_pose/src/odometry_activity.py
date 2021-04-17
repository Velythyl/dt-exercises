#!/usr/bin/env python
# coding: utf-8

# In[1]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your odometry function! 

# DO NOT CHANGE THE NAME OF THIS FUNCTION OR THINGS WILL BREAK

def DeltaPhi(encoder_msg, prev_ticks):
    """
        Args:
            encoder_msg: ROS encoder message (ENUM)
            prev_ticks: Previous tick count from the encoders (int)
        Return:
            rotation_wheel: Rotation of the wheel in radians (double)
            ticks: current number of ticks (int)
    """
    ticks = encoder_msg.data

    delta_ticks = ticks-prev_ticks
    
    # for debugging
    print(f"        DELTA TICKS  {encoder_msg.header.frame_id}")
    print(delta_ticks)

    N_tot = encoder_msg.resolution #total number of ticks per wheel revolution

    alpha = 2*np.pi/N_tot # rotation per tick in radians 

    delta_phi = alpha*delta_ticks # in radians
    
    return delta_phi, ticks


# In[1]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your odometry function! 

import numpy as np 

# DO NOT CHANGE THE NAME OF THIS FUNCTION OR THINGS WILL BREAK

def poseEstimation( R, # radius of wheel (assumed identical) - this is fixed in simulation, and will be imported from your saved calibration for the physical robot
                    baseline_wheel2wheel, # distance from wheel to wheel; 2L of the theory
                    x_prev, # previous x estimate - assume given
                    y_prev, # previous y estimate - assume given
                    theta_prev, # previous orientation estimate - assume given
                    delta_phi_left, # left wheel rotation (rad)
                    delta_phi_right): # right wheel rotation (rad)
    
    """
        Calculate the current Duckiebot pose using dead reckoning approach.

        Returns x,y,theta current estimates:
            x_curr, y_curr, theta_curr (:double: values)
    """
    
    r = 0 #-0.10630302732213565 # keep 0 in simulation, change on the real robot 
    
    R_left = R * (1-r)
    R_right = R * (1+r)
    
    d_left = R_left * delta_phi_left 
    d_right = R_right * delta_phi_right
    
    d_A = (d_left + d_right)/2
    
    Dtheta = (d_right - d_left)/baseline_wheel2wheel
    Dx = d_A * np.cos(theta_prev)
    Dy = d_A * np.sin(theta_prev)
    
    x_curr = x_prev + Dx
    y_curr = y_prev + Dy
    theta_curr = theta_prev + Dtheta
    
    #x_curr = x_prev + R*(delta_phi_left+delta_phi_right)*np.cos(theta_prev)/2
    #y_curr = y_prev + R*(delta_phi_left+delta_phi_right)*np.sin(theta_prev)/2
    #theta_curr = theta_prev + R*(delta_phi_right-delta_phi_left)/baseline_wheel2wheel

    return x_curr, y_curr, theta_curr

