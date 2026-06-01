FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

# Core Utilities
RUN apt-get update && apt-get install -y 
    curl 
    wget 
    git 
    vim 
    nano 
    tmux 
    gnupg2 
    lsb-release 
    software-properties-common 
    build-essential 
    cmake 
    python3-pip


# ROS 2 Humble

RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -

RUN echo "deb http://packages.ros.org/ros2/ubuntu jammy main" 
    > /etc/apt/sources.list.d/ros2.list

RUN apt-get update && apt-get install -y 
    ros-humble-desktop 
    python3-colcon-common-extensions 
    python3-rosdep

# Gazebo Harmonic
RUN curl -sSL https://packages.osrfoundation.org/gazebo.gpg | apt-key add -

RUN echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable jammy main" 
    > /etc/apt/sources.list.d/gazebo-stable.list

RUN apt-get update && apt-get install -y 
    gz-harmonic


RUN apt-get update && apt-get install -y 
    ros-humble-rviz2 
    ros-humble-xacro 
    ros-humble-tf2-tools 
    ros-humble-image-transport 
    ros-humble-cv-bridge 
    ros-humble-foxglove-bridge


# Workspace

WORKDIR /root/rxsim

COPY . /root/rxsim

# ROSDEP
RUN rosdep init || true
RUN rosdep update

# Build ROS Workspace

RUN source /opt/ros/humble/setup.bash && 
    cd /root/rxsim/rosgz && 
    rosdep install --from-paths src --ignore-src -r -y && 
    colcon build --symlink-install

# Entrypoint

COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["bash"]