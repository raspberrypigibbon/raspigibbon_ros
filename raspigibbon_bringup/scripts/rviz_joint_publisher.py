#!/usr/bin/env python
# coding: utf-8

import rospy
from sensor_msgs.msg import JointState

class RvizMaster:
    def __init__(self):
        self.sub = rospy.Subscriber("/raspigibbon_on_rviz/joint_states", JointState, self.joint_callback, queue_size=10)
        self.pub = rospy.Publisher("master_joint_state", JointState, queue_size=10)
        self.r = rospy.Rate(40)

    def joint_callback(self, msg):
        js = JointState();
        for i in range(1, 6):
            js.name.append("joint"+str(i))
            js.position.append(msg.position[i-1]*180.0/3.14159)
        self.pub.publish(js)
        self.r.sleep()

if __name__ == "__main__":
    try:
        while not rospy.is_shutdown():
            rospy.init_node("rviz_joint_state_publisher")
            rviz = RvizMaster()
            rospy.spin()
    except rospy.ROSIntteruptException:
        pass

