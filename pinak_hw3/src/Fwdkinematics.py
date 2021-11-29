#!/usr/bin/env python
import rospy
import math
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Pose
from pinak_hw3.msg import qvals

def fwd_kinematics(data):
    print("Recieved following values in degrees:",data.q1,data.q2,data.q3)
    q1 = data.q1*math.pi/180
    q2 = data.q2*math.pi/180
    q3 = data.q3*math.pi/180
    a1 = np.array([[math.cos(q1),0, -math.sin(q1),0],[math.sin(q1),0,math.cos(q1),0],[0,-1,0,1],[0,0,0,1]])
    a2 = np.array([[math.cos(q2), -math.sin(q2),0,math.cos(q2)],[math.sin(q2),math.cos(q2),0,math.sin(q2)],[0,0,1,0],[0,0,0,1]])
    a3 = np.array([[math.cos(q3), -math.sin(q3),0,math.cos(q3)],[math.sin(q3),math.cos(q3),0,math.sin(q3)],[0,0,1,0],[0,0,0,1]])
    temp = np.matmul(a1,a2)
    T = np.matmul(temp,a3)
    print("T is:",T)
    print("The end effector pose is:",T[0:-1,[-1]])
    
    # print(a1,a2,a3)
def inv_kinematics(data):
    print("Recieved following values for Pose:",data.position.x,data.orientation)
    Xc = data.position.x
    Yc = data.position.y
    Zc = data.position.z
    q1 = math.atan2(Yc,Xc)
    s = Zc-1
    d = (Xc**2+Yc**2+s**2-2)/2
    q3 = math.atan2(math.sqrt(1-d**2),d)
    q2 = math.atan2(s-math.sin(q3),(Xc**2+Yc**2))
    

    print("q1:",q1*180/math.pi,q2*180/math.pi,q3*180/math.pi)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('fwdkinematics_node', anonymous=True)

    rospy.Subscriber('qvalues', qvals, fwd_kinematics)
    rospy.Subscriber('Pose',Pose, inv_kinematics)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()