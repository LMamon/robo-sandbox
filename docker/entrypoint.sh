#!/bin/bash

source /opt/ros/humble/setup.bash

if [ -f "/root/rxsim/rosgz/install/setup.bash" ]; then
    source /root/rxsim/rosgz/install/setup.bash
fi

exec "$@"