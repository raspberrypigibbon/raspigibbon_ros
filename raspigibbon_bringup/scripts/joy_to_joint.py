#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time, math, rospy
from sensor_msgs.msg import Joy
from sensor_msgs.msg import JointState

l[5] = [0.1,0.1,0.1,0.1,0.1]

def callback(data):
    array = data.axes[:3] + data.axes[4:6]
    send.position = [i * 10 for i in array]

def IK(data):
    pass


if __name__ == "__main__":
    rospy.sleep(0.1)
    send = JointState()
    try:
        while not rospy.is_shutdown():
            sub = rospy.Subscriber('/joy', Joy, callback, queue_size=10)
            rospy.init_node('master_joint_state')
            pub = rospy.Publisher("master_joint_state", JointState, queue_size=10)
            if not rospy.is_shutdown():
                try:
                    js = JointState()
                    js.position = send.position
                    js.name=["joint{}".format(i) for i in range(1,6)]
                    # for i in range(1,6):
                        # js.name.append("joint"+str(i))
                        # js.position.append(res) 
                    pub.publish(js)
                    # print js
                    rospy.sleep(0.01)
                except:
                    rospy.logerr("Sending Data Failed")

    except rospy.ROSInterruptException:
        pass

