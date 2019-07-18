#!/usr/bin/env python

## Simple myo demo that listens to std_msgs/UInt8 poses published 
## to the 'myo_gest' topic and drives turtlesim

import rospy, math
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist, Vector3
from ros_myo.msg import EmgArray
from sensor_msgs.msg import Imu

if __name__ == '__main__':

    rospy.init_node('turtlebot3_myo', anonymous=True)
    
    # Publish to the turtlesim movement topic
    tsPub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

    def strength(emgArr1):
	emgArr=emgArr1.data
	# Define proportional control constant:
	K = 0.005
        speed = 0.01
	# Get the average muscle activation of the left, right, and all sides
	aveRight=(emgArr[0]+emgArr[1]+emgArr[2]+emgArr[3])/4
	aveLeft=(emgArr[4]+emgArr[5]+emgArr[6]+emgArr[7])/4
	ave=(aveLeft+aveRight)/2
        #rospy.loginfo("total : %f" , ave)
        #rospy.loginfo("Right : %f",aveRight)
        #rospy.loginfo("left : %f",aveLeft)
	# If all muscles activated, drive forward exponentially
	#rospy.loginfo("left : %f > %f",aveLeft,aveRight) 
        
	# If only left muscles activated, rotate proportionally
        #rospy.loginfo("%f",0.1*math.exp(1))
        #i = 0
        #right = True
        #temp_r = emgArr[2]
        #for i in range(8):
        #    if temp_r < 200 or emgArr[2] < emgArr[i] and i != 2 and i != 1 :
        #       right = False
        #i = 0
        #left = True
        #temp_r = emgArr[6]
        #for i in range(8):
        #    if temp_r < 150 or emgArr[6] < emgArr[i] and i < 5 :
        #       left = False
        #rospy.loginfo(ave) 
        if emgArr[7]-emgArr[1] > 100 :
            rospy.loginfo("left")
            tsPub.publish(Twist(Vector3(0,0,0),Vector3(0,0,K*ave)))
        elif emgArr[1]-emgArr[6] > 200  :
            rospy.loginfo("right")
            tsPub.publish(Twist(Vector3(0,0,0),Vector3(0,0,-K*ave)))
        elif ave > 200 :
            rospy.loginfo("forward")
            tsPub.publish(Twist(Vector3(0.1*math.exp(K*ave),0,0),Vector3(0,0,0)))
        else :
            rospy.loginfo("stop")
            tsPub.publish(Twist(Vector3(0,0,0),Vector3(0,0,0)))
        
        #elif emgArr[1] > 250 and emgArr[2] > 250 and emgArr[7] < 300 and emgArr[4] <300:
	#    tsPub.publish(Twist(Vector3(0,0,0),Vector3(0,0,-K*ave)))
        #    rospy.loginfo("right")
	#if aveLeft > aveRight and ave > 115 and ave < 300:
	#    tsPub.publish(Twist(Vector3(0,0,0),Vector3(0,0,K*ave)))
	# If only right muscles activated, rotate proportionally
	#elif aveRight > aveLeft and ave > 135 and ave < 300:
	#    tsPub.publish(Twist(Vector3(0,0,0),Vector3(0,0,-K*ave)))
        #elif ave > 200:
	#    tsPub.publish(Twist(Vector3(0.1*math.exp(K*ave),0,0),Vector3(0,0,0)))	
	# If not very activated, don't move (high-pass filter)    
	#else: 
	#    tsPub.publish(Twist(Vector3(0,0,0),Vector3(0,0,0)))


    #def imu_func(imu):
    #    if imu.orientation.y > -0.7 :
    #        tsPub.publish(Twist(Vector3(0,0,0),Vector3(0,0,0)))

   # rospy.Subscriber("myo_imu", Imu, imu_func)
    rospy.Subscriber("myo_emg", EmgArray, strength)
    

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
