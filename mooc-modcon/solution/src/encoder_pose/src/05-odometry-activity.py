#!/usr/bin/env python
# coding: utf-8

# In[1]:



import numpy as np # already imported above 

# DO NOT CHANGE THE NAME OF THIS FUNCTION
def poseEstimation( R,
                    baseline_wheel2wheel,
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
    theta_curr = theta_prev + R*(delta_phi_right-delta_phi_left)/baseline_wheel2wheel
    
    return x_curr, y_curr, theta_curr

