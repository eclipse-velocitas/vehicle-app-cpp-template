#!/bin/bash
# This file is maintained by velocitas CLI, do not modify manually. Change settings in .velocitas.json

sudo modprobe vcan
sudo ip link add name vcan0 type vcan
sudo ip link set dev vcan0 up
