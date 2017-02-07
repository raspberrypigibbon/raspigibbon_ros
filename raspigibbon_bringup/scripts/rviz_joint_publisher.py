#!/usr/bin/env python
# coding: utf-8

import rospy
from sensor_msgs.msg import JointState

class Slave:
    def __init__(self):
        self.sub = rospy.Subscriber("/joint_states", JointState, self.joint_callback, queue_size=10)
        self.pub = rospy.Publisher("master_joint_state", JointState, queue_size=10)

    def joint_callback(self, msg):
        js = JointState();
        for i in range(1, 6):
            js.name.append("joint"+str(i))
            js.position.append(msg.position[i-1]*180.0/3.14159)
        self.pub.publish(js)
        rospy.sleep(0.01)

if __name__ == "__main__":
    try:
        while not rospy.is_shutdown():
            rospy.init_node("rviz_joint_state_publisher")
            slave = Slave()
            rospy.spin()
    except rospy.ROSIntteruptException:
        pass

