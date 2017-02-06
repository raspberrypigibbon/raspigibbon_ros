#!/usr/bin/env python
# coding: utf-8

from raspigibbon_utils import RS30X
import rospy
from sensor_msgs.msg import JointState

class Slave:
    def __init__(self):
        self.rs = RS30X.RS304MD()
        self.sub = rospy.Subscriber("/raspigibbon/master_joint_state", JointState, self.joint_callback, queue_size=10)
        for i in range(1,6):
            self.rs.setTorque(i, True)
            rospy.sleep(0.01)
        rospy.loginfo("servo initialized")

    def joint_callback(self, msg):
        for i in range(1, 6):
            self.rs.setAngle(i, msg.position[i-1])
        rospy.sleep(0.01)

if __name__ == "__main__":
    try:
        while not rospy.is_shutdown():
            rospy.init_node("slave_joint_state")
            slave = Slave()
            rospy.spin()
    except rospy.ROSInterruptException:
        pass

