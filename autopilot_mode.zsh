#!/usr/bin/env zsh

##################################################
# RXSIM Environment Bootstrap
# ROS 2 + PX4 + Gazebo Harmonic + Isaac ROS
##################################################

############################
# Resolve Project Root
############################

SCRIPT_DIR="$(cd "$(dirname "${(%):-%N}")" && pwd)"
export RXSIM_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -f "/opt/ros/humble/setup.zsh" ]; then
    source /opt/ros/humble/setup.zsh
else
    echo "[RXSIM] ROS 2 Humble not found"
    return 1
fi

############################
# Workspace Paths
############################

export ROSGZ_WS="$RXSIM_ROOT/rosgz"
export PX4_ROS_UXRCE_DDS_WS="$RXSIM_ROOT/px4_ros_uxrce_dds_ws"
export ISAAC_ROS_WS="$ROSGZ_WS"

############################
# ROS 2 Settings
############################

export ROS_DOMAIN_ID=2
export ROS_LOCALHOST_ONLY=0
export ROS_USE_SIM_TIME=true
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

############################
# Gazebo Harmonic
############################

export GZ_VERSION=harmonic
export GZ_PARTITION=px4

export GZ_SIM_RESOURCE_PATH="$RXSIM_ROOT/Gazebo/models:$RXSIM_ROOT/Gazebo/worlds"

export GZ_NETWORK_ROLE=primary
export GZ_NETWORK_SECONDARIES=1

# Distributed networking
export GZ_IP=127.0.0.1
export GZ_RELAY=127.0.0.1

############################
# Gazebo Plugins
############################

export COAST_WATER_SHADER_PLUGIN=gz-sim-shader-param-system
export COAST_WATER_SHADER_NAME=gz::sim::systems::ShaderParam

export NAVSAT_PLUGIN=gz-sim-navsat-system
export NAVSAT_NAME=gz::sim::systems::NavSat

############################
# PX4 SITL
############################

export PX4_SYS_AUTOSTART=4006
export PX4_SYS_AUTOCONFIG=1
export PX4_GZ_STANDALONE=1

export PX4_GZ_WORLD=rxsim1
export PX4_GZ_MODEL_NAME=px4vision

############################
# Source Built Workspaces
############################

if [ -f "$PX4_ROS_UXRCE_DDS_WS/install/setup.zsh" ]; then
    source "$PX4_ROS_UXRCE_DDS_WS/install/setup.zsh"
else
    echo "[RXSIM] px4_ros_uxrce_dds_ws not built"
fi

if [ -f "$ROSGZ_WS/install/setup.zsh" ]; then
    source "$ROSGZ_WS/install/setup.zsh"
else
    echo "[RXSIM] rosgz workspace not built"
fi

############################
# Helper Functions
############################

function rxsim_root() {
    cd "$RXSIM_ROOT"
}

function rosgz_root() {
    cd "$ROSGZ_WS"
}

function px4_root() {
    cd "$RXSIM_ROOT/PX4-Autopilot"
}

############################
# Launch Functions
############################

function runsim() {
    gz sim -s -r -v 1 rxsim1.sdf
}

function rung() {
    gz sim -g -v 1
}

function runsitl() {
    cd "$RXSIM_ROOT/PX4-Autopilot" || return
    ./build/px4_sitl_default/bin/px4
}

function launch_autopilot() {
    ros2 launch rxsim autopilot.launch.py
}

function launch_vslam() {
    ros2 launch rxsim cu_vslam.launch.py
}

function launch_nvblox() {
    ros2 launch rxsim nvblox.launch.py
}

############################
# Status
############################

echo ""
echo "========================================"
echo " RXSIM Environment Loaded"
echo "========================================"
echo "Root:        $RXSIM_ROOT"
echo "ROS Domain:  $ROS_DOMAIN_ID"
echo "Gazebo:      Harmonic"
echo "PX4 World:   $PX4_GZ_WORLD"
echo "PX4 Model:   $PX4_GZ_MODEL_NAME"
echo "========================================"
echo ""
echo "Available commands:"
echo "  runsim"
echo "  runsitl"
echo "  launch_autopilot"
echo "  launch_vslam"
echo "  launch_nvblox" 
echo ""