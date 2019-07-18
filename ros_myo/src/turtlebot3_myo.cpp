#include <ros/ros.h>
#include <sensor_msgs/Imu.h>
#include <string>
#include <geometry_msgs/Twist.h>//Vector3
//#include <geometry_msgs/Vector.h>
#include <ros_myo/EmgArray.h>
#include <ros_myo/MyoArm.h>


geometry_msgs::Twist move;
float speed = 0;
float ang = 0;
void imuMsgCallback(const sensor_msgs::Imu::ConstPtr &msg)
{
  if(msg->linear_acceleration.y < -0.7){
     ROS_INFO("Right");
     geometry_msgs::Twist move_temp;
     move_temp.angular.z = -ang;
     move = move_temp;
  }

  else if (msg->linear_acceleration.y > 0.7){
     ROS_INFO("Left");
     geometry_msgs::Twist move_temp;
     move_temp.angular.z = ang;
     move = move_temp;
  }
  else if (msg->linear_acceleration.x < 0.7){
     ROS_INFO("Stop");
     geometry_msgs::Twist move_temp;
     move = move_temp;
  }
  else if (msg->linear_acceleration.x > -0.5 && msg->linear_acceleration.x < 0.5){
     ROS_INFO("Forward");
     geometry_msgs::Twist move_temp;
     move_temp.linear.x = speed;
     move = move_temp;
  }
  else if (msg->linear_acceleration.x > -0.7){
     ROS_INFO("Backward");
     geometry_msgs::Twist move_temp;
   /*  
     if(msg->linear_acceleration.z > 0.19 )
        move_temp.angular.z = -ang;
     else if (msg->linear_acceleration.z < -0.19 )
        move_temp.angular.z = ang;
     else*/ 
        move_temp.linear.x = -speed;

     move = move_temp;
  }
}

void emgArrayMsgCallback(const ros_myo::EmgArray::ConstPtr &msg)
{   
    float total = msg->data[0]+msg->data[1]+msg->data[2]+msg->data[3]+msg->data[4]+msg->data[5]+msg->data[6]+msg->data[7] ;
    speed = 0.005 * 0.271828 *(total/8);
    ang = 0.005 * (total/8);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "turtlebot3_myo");
  ros::NodeHandle nh;
  ros::Publisher pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 10);
  ros::Subscriber imu = nh.subscribe("myo_imu", 10, imuMsgCallback);
  ros::Subscriber emg = nh.subscribe("myo_emg", 10, emgArrayMsgCallback);
  ros::Rate loop_rate(10);

  while (ros::ok())
  {
    ROS_INFO("%f",speed);
    pub.publish(move);
    ros::spinOnce();
    loop_rate.sleep();
  }
  ros::spin();
  return 0;
}
