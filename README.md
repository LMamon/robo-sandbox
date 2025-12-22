# robo-sandbox

**robo-sandbox** is a minimal robotics simulation sandbox that contains:
- Gazebo worlds and models
- ROS–Gazebo bridge and launch files

The repository is intentionally lightweight and assumes Gazebo, ROS 2, and PX4 (if used) are installed externally. Its purpose is to provide a clean place to iterate on simulation assets and integration logic without duplicating models or maintaining multiple branches.

---

## The problem addressesed

There is a practical incompatibility in the current Gazebo ecosystem particularly on macOS:

- **PX4 is only compatible with Gazebo Harmonic and newer**
- **Visualization tooling (ROS bridges, Foxglove, etc.) is unreliable or non-functional on Gazebo Harmonic**, because messages often do not propagate cleanly outside the `gz` transport layer
- **Older Gazebo versions (Ignition / Fortress)** work well for visualization, but **are incompatible with autopilot software**

This creates a split workflow:
- One setup that works for **visualization**
- Another setup that works for **autopilot simulation**
- The same worlds and models need to run in both

Maintaining separate model files or Git branches for this quickly becomes error-prone and hard to keep in sync.

---

## The solution used here

This repository keeps:
- **one set of worlds**
- **one set of models**
- **one ROS–Gazebo bridge configuration**

The only differences between visualization and autopilot workflows are handled by **version-specific Gazebo system plugins**, selected at runtime.

This is done by:
1. Using environment-variable substitution in SDF plugin declarations
2. Providing small `.zsh` files that export the correct plugin identifiers for the Gazebo version being used
3. Sourcing the appropriate file before launching the simulator

No files are duplicated, and no branches are required.

---

## Repository layout

```text
gazebo/
  ├─ worlds/
  └─ models/

rosgz/
  ├─ bridge.yaml
  ├─ rxsim_launch.py
  ├─ viz_mode.zsh
  └─ autopilot_mode.zsh
```

## Usage 
### Visualization mode (Ignition / Fortress)
Used when ROS visualization tools are the priority.
``` zsh
. rosgz/viz_mode.zsh
ign gazebo gazebo/worlds/<world>.sdf
```

### Autopilot
Used when running PX4 SITL.
```zsh
. rosgz/autopilot_mode.zsh
gz sim gazebo/worlds/<world>.sdf
```

the sourced .zsh file ensures the correct Gazebo system plugins are loaded for that version.
