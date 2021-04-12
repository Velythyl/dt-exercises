#!/bin/bash

source /environment.sh
source /code/solution/devel/setup.bash

# initialize launch file
dt-launchfile-init

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------

# NOTE: Use the variable DT_REPO_PATH to know the absolute path to your code
# NOTE: Use `dt-exec COMMAND` to run the main process (blocking process)

# launching app

python3 /code/solution.py &> /dev/null &
dt-exec roslaunch --wait car_interface all.launch veh:=$VEHICLE_NAME &
dt-exec roslaunch wheels_calibration wheels_calibration_node.launch veh:=$VEHICLE_NAME

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# wait for app to end
dt-launchfile-join
