#!/usr/bin/env python
# coding: utf-8

import rospy
from sensor_msgs.msg import JointState
from futaba_serial_servo import RS30X


class Master:
    def __init__(self):
        self.rs = RS30X.RS304MD()
        self.pub = rospy.Publisher("master_joint_state", JointState, queue_size=10)
        self.r = rospy.Rate(30)
        for i in range(1,6):
            self.rs.setTorque(i, False)
            rospy.sleep(0.01)
        rospy.loginfo("servo initialized")

    def run(self):
        while not rospy.is_shutdown():
            js = JointState()
            js.name=["joint{}".format(i) for i in range(1,6)]
            js.position = [max(-150,min(150,self.rs.readAngle(i))) for i in range(1,6)]
            self.pub.publish(js)
            self.r.sleep()

if __name__ == "__main__":
    rospy.init_node("master_joint_state")
    master = Master()
    master.run()
