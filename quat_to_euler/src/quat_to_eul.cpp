#include "ros/ros.h"
#include "geometry_msgs/Quaternion.h"

// Creating a local variable of type Quaternion
geometry_msgs::Quaternion quat;

// Callback Function to calculate and display the Euler
void SubCallback(const geometry_msgs::Quaternion::ConstPtr & msg)
{
  // Assigning values from the topic to a local variable 
  quat.x = msg->w;
  quat.y = msg->x;
  quat.z= msg->y;
  quat.w = msg->w;
  
 
 
// To calculate the Euler angles from quaternions by applying formula
  float temp = 2*((quat.y*quat.w)-(quat.x*quat.z));
  float phi = atan2(2*((quat.x*quat.y)+(quat.z*quat.w)),((quat.x*quat.x)-(quat.y*quat.y)-(quat.z*quat.z)+(quat.w*quat.w)));
  float theta  = atan2(-1*temp,sqrt(1-(temp*temp)));
  float psi = atan2(2*((quat.x*quat.w)+(quat.y*quat.z)),((quat.x*quat.x)+(quat.y*quat.y)-(quat.z*quat.z)-(quat.w*quat.w)));
  // To print values of Euler Angles
  ROS_INFO("PHI : [%f]", phi);
  ROS_INFO("ThETA : [%f]", theta);
  ROS_INFO("PSI : [%f]", psi);
}

// %EndTag(CALLBACK)%

int main(int argc, char **argv)
{
  /**
   * The ros::init() function needs to see argc and argv so that it can perform
   * any ROS arguments and name remapping that were provided at the command line.
   * For programmatic remappings you can use a different version of init() which takes
   * remappings directly, but for most command-line programs, passing argc and argv is
   * the easiest way to do it.  The third argument to init() is the name of the node.
   *
   * You must call one of the versions of ros::init() before using any other
   * part of the ROS system.
   */
  ros::init(argc, argv, "quat_to_eul");

  /**
   * NodeHandle is the main access point to communications with the ROS system.
   * The first NodeHandle constructed will fully initialize this node, and the last
   * NodeHandle destructed will close down the node.
   */
  ros::NodeHandle n;

  /**
   * The subscribe() call is how you tell ROS that you want to receive messages
   * on a given topic.  This invokes a call to the ROS
   * master node, which keeps a registry of who is publishing and who
   * is subscribing.  Messages are passed to a callback function, here
   * called chatterCallback.  subscribe() returns a Subscriber object that you
   * must hold on to until you want to unsubscribe.  When all copies of the Subscriber
   * object go out of scope, this callback will automatically be unsubscribed from
   * this topic.
   *
   * The second parameter to the subscribe() function is the size of the message
   * queue.  If messages are arriving faster than they are being processed, this
   * is the number of messages that will be buffered up before beginning to throw
   * away the oldest ones.
   */
// %Tag(SUBSCRIBER)%
  ros::Subscriber sub = n.subscribe("/geometry_msgs/Quaternion", 10, SubCallback);
// %EndTag(SUBSCRIBER)%

  /**
   * ros::spin() will enter a loop, pumping callbacks.  With this version, all
   * callbacks will be called from within this thread (the main one).  ros::spin()
   * will exit when Ctrl-C is pressed, or the node is shutdown by the master.
   */
// %Tag(SPIN)%
  ros::spin();
// %EndTag(SPIN)%

  return 0;
}