#include "ros/ros.h"
#include "pinak_beginner_tutorials/AddTwoInts.h"
#include <cstdlib>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "add_two_ints_client");
 if (argc != 3)
  {
        ROS_INFO("Enter First Two and Last Two digits as arguments");
        return 1;
   }
 
   ros::NodeHandle n;
   ros::ServiceClient client = n.serviceClient<pinak_beginner_tutorials::AddTwoInts>("add_two_ints");
   pinak_beginner_tutorials::AddTwoInts srv;
   srv.request.a = atoll(argv[1]);
   srv.request.b = atoll(argv[2]);
   if (client.call(srv))
   {
     ROS_INFO("Sum of First and Last 2 digits of ID is: %ld", (long int)srv.response.sum);
   }
   else
   {
     ROS_ERROR("Failed to call service add_two_ints");
     return 1;
   }
 
   return 0;
   }