# raspigibbon_ros

## About

ROS package suites of Raspberry Pi Gibbon Controller

## Requirements

requires the following to run controller on Raspberry Pi 3:

* Ubuntu
  * Ubuntu Xenial 16.04
    * Ubuntu MATE 16.04.1 recomended
* ROS
  * ROS Kinetic
* Device Driver
  * [raspigibbon_driver](https://github.com/Tiryoh/raspigibbon_driver)

## Installation

### Raspberry Pi on Raspberry Pi Gibbon

First, install the latest stable version of ROS Kinetic.

```
sudo apt install ros-kinetic-ros-base
```

Next, install the latest stable version of raspigibbon_driver.

```
cd ~/
git clone https://github.com/Tiryoh/raspigibbon_driver_installer.git
cd raspigibbon_driver_installer
sudo make install
```

Then, download this repository into `~/catkin_ws/src` and build it.

```
cd ~/catkin_ws/src
git clone https://github.com/raspberrypigibbon/raspigibbon_ros.git
cd ~/catkin_ws && catkin_make && source ~/catkin_ws/devel/setup.bash
```

### Ubuntu x64

First, install the latest stable version of ROS Kinetic.

```
sudo apt install ros-kinetic-desktop-full
```

Next, download this repository into `~/catkin_ws/src` and build it.

```
cd ~/catkin_ws/src
git clone https://github.com/raspberrypigibbon/raspigibbon_ros.git
cd ~/catkin_ws && catkin_make && source ~/catkin_ws/devel/setup.bash
```

## Usage

### Raspberry Pi on Raspberry Pi Gibbon

joint data publisher mode
```
roslaunch raspigibbon_bringup raspigibbon_joint_publisher.launch
```

joint data subscriber mode
```
roslaunch raspigibbon_bringup raspigibbon_joint_subscriber.launch
```

### Ubuntu x64

joint data publisher mode
```
roslaunch raspigibbon_description display_urdf.launch
roslaunch raspigibbon_bringup rviz_joint_publisher.launch
```

joint data subscriber mode
```
roslaunch raspigibbon_description display_urdf.launch
roslaunch raspigibbon_bringup rviz_joint_subscriber.launch
```


## License

This repository is licensed under the MIT license, see [LICENSE]( ./LICENSE ).

Unless attributed otherwise, everything is under the MIT license.

### Includings
* [Tiryoh/RS30X](https://github.com/Tiryoh/RS30X) - MIT license
  * futaba_serial_servo package
