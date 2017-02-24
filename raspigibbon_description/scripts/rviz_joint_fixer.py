#!/usr/bin/env python
# coding: utf-8

import rospy
from sensor_msgs.msg import JointState

class Dummy:
    def __init__(self):
        self.sub = rospy.Subscriber(rospy.get_namespace()+"joint_states", JointState, self.joint_callback, queue_size=10)
        self.pub = rospy.Publisher(rospy.get_namespace()+"joint_states_source", JointState, queue_size=10)
        self.r = rospy.Rate(50)

    def joint_callback(self, msg):
        js = JointState();
        if len(msg.position) > 0:
            js.name.append("joint6")
            js.position.append(-msg.position[4])
            self.pub.publish(js)
        self.r.sleep()

if __name__ == "__main__":
    try:
        while not rospy.is_shutdown():
            rospy.init_node("rviz_slave_joint_state")
            dummy = Dummy()
            rospy.spin()
    except rospy.ROSIntteruptException:
        pass

