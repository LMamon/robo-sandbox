# RXSIM

ROS 2 + PX4 autonomous drone simulation stack featuring Visual SLAM, 3D reconstruction, custom PX4 flight control, and real-time computer vision integration using Gazebo Harmonic and Jetson hardware.

## Overview

This project is an autonomous flight simulation and perception stack designed for experimentation with computer vision-based navigation, mapping, and remote sensing workflows in Arctic and GPS-limited environments.

The project integrates ROS 2, PX4, Gazebo Harmonic, Visual SLAM, and real-time 3D reconstruction into a unified simulation and control pipeline running on Jetson hardware.

The primary motivation behind the project is exploring how autonomous aerial systems can operate in remote environments where traditional infrastructure and positioning systems may be unreliable, unavailable, or operationally constrained. Arctic and remote sensing operations in Alaska present unique challenges involving terrain and micro climate conditions impacting ground station communications. With increasingly large operational areas, vision-driven autonomy is going to become essential.

This project focuses on building and validating the software, perception, and control pipeline required before transitioning toward real-world deployment and field experimentation.

The system currently supports:

* Visual SLAM-based localization
* Real-time 3D reconstruction and mapping
* Autonomous and custom PX4 flight modes
* QGroundControl mission planning and telemetry
* ROS 2 distributed communication
* Object detection integration
* Dockerized deployment environment

The project was developed and tested on a Jetson Orin Nano (8GB) running Ubuntu 22.04.

---

## Demo

[![vSLAM Autonomous Flight and 3D Mapping with PX4](https://img.youtube.com/vi/QUmoEZDUgAk/maxresdefault.jpg)](https://youtu.be/QUmoEZDUgAk?si=NtXnyQXWs3vzVq5n)

The demo includes:
- Autonomous flight mission
- Visual SLAM tracking
- Point cloud generation
- 3D voxel reconstruction
- PX4 + Gazebo + ROS 2 integration
- QGroundControl telemetry and control

---

## Core runtime flow:

1. Gazebo Harmonic simulates the environment and onboard sensors
2. ROS 2 transports camera, IMU, and state data
3. PX4 SITL handles flight control and vehicle dynamics
4. Visual SLAM estimates vehicle position in GPS-denied environments
5. Reconstruction pipelines generate spatial maps and voxel representations
6. QGroundControl provides operator control and mission interaction

---

## Features

### Isaac ROS cuVSLAM
- Stereo camera pipeline
- GPS-denied localization
- ROS 2 integrated odometry

### Isaac ROS nvBlox
- Point cloud generation
- Voxel-based mapping
- Real-time scene reconstruction

### PX4 Integration
- PX4 SITL integration
- Offboard/autonomous control
- QGroundControl compatibility for remote operation and control

### Object Detection
- Real-time inference pipeline support
- ROS 2 perception node integration
- Bounding box visualization support

### Distributed Simulation
- ROS 2 distributed node architecture
- Gazebo Harmonic transport integration
- Multi-process autonomy stack orchestration

---

## Technologies Used

### Core Frameworks
- ROS 2 Humble
- PX4 Autopilot
- Gazebo Harmonic
- QGroundControl
- Docker

### Perception / Mapping
- Visual SLAM
- NVBlox
- OpenCV
- Foxglove Studio

### Communication / Middleware
- Micro XRCE-DDS
- FastDDS
- ros_gz_bridge

### Hardware
- Jetson Orin Nano
- Ubuntu 22.04

---

## Requirements

### Host Requirements
- Ubuntu 22.04
- Docker
- NVIDIA Jetson Orin Nano
- QGroundControl installed on host system
- PX4-Autopilot installed on host system

### Recommended
- CUDA-capable Jetson device
- 8GB+ storage available for ROS/Gazebo builds

---

## Installation

### 1. Clone Repository

    git clone https://github.com/LMamon/rxsim/tree/main cd sim

### 2. Install PX4 Separately

PX4 is not bundled with this repository.

you can install and build PX4 externally by following their guide [[Building PX4 Software](https://docs.px4.io/main/en/dev_setup/building_px4)]

---

## Docker Setup

Build the container:

    docker build -t rxsim -f docker/Dockerfile .

Run the container:

    docker run -it --network host --privileged -v ~/PX4-Autopilot:/root/PX4-Autopilot rxsim

---

## Launching Environment

Inside the container:

    source rxsim_env.zsh

Launch Gazebo:

    runsim

Launch PX4 SITL:

    runsitl

Launch autopilot / ROS stack:

    launch_autopilot

---

## Related Packages / Dependencies

- [[PX4 Development](https://docs.px4.io/main/en/development/development)]
- [[ROS 2 Humble Link](https://docs.ros.org/en/humble/Installation.html)]
- [[Gazebo Harmonic Link](https://gazebosim.org/docs/harmonic/getstarted/)]
- [[QGroundControl Link](https://qgroundcontrol.com/)]
- [[Micro XRCE-DDS Link](https://docs.px4.io/main/en/middleware/uxrce_dds#micro-xrce-dds-agent-installation)]
- [[NVBlox Link](https://nvidia-isaac-ros.github.io/v/release-3.2/repositories_and_packages/isaac_ros_nvblox/index.html)]
- [[Visual SLAM Package Link](https://nvidia-isaac-ros.github.io/v/release-3.2/repositories_and_packages/isaac_ros_visual_slam/index.html)]
- [[Foxglove Studio Link](https://docs.foxglove.dev/docs)]

---

## Current Status

Release Version: v1.0

The project currently demonstrates:
- Autonomous simulated flight
- Visual SLAM localization
- Real-time reconstruction
- PX4 integration
- ROS 2 distributed autonomy workflows

under construction:
- CUDA based perception pipelines
- Path planning
- Semantic mapping
- Multi-agent coordination and RL

---

## License

Apache-2.0