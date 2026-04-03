# robo-sandbox

**robo-sandbox** is a minimal robotics simulation sandbox that contains:
- Gazebo worlds and models
- ROS 2 - Gazebo bridge and launch system
- Real time vision inference
- Mono VIO pipeline integrated with PX4 SITL

The system is designed to support remote sensing and autonomy in GNSS-degraded environments, with a focus on onboard visual perception and edge deployment.

The repository is intentionally lightweight and assumes Gazebo (harmonic), ROS 2 (humble), and PX4(v1.16) are installed on host system. The system is designed as a mondular autonomy pipeline not just a simulator, assets have been modified for stable builds on both macOS and ubuntu 22.04.



---
## Launch

Everything runs through a single launch file

```zsh
cd rosgz
colcon build --packages-select <packages>
. install/setup.zsh
```

### Autopilot mode (full system)
```zsh 
ros2 launch rxsim system.launch.py mode:=autopilot
```

### Visualization mode (no PX4)
```zsh
ros2 launch rxsim system.launch.py mode:=viz
```
---

## Platforms

- Jetson Orin Nano SDK is the primary deployment platform + target
- macOS supported for visualization and development

## Repository layout

```text
gazebo/
  ├─ worlds/
  ├─ models/
  └─ labels.txt

rosgz/
  ├─ * open_vins/
  ├─ perception/
  ├─ * px4_msgs/
  ├─ * ros_gz/
  ├─ rxsim/
  ├─ vio/
  └─ * vision_opencv
```
px4_ros_uxrce_dds_ws and PX4-Autopilot not shown

TODO: docker container

TODO: demo recording


\* external packages