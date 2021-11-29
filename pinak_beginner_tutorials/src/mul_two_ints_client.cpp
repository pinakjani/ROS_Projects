#include "ros/ros.h"
#include "pinak_beginner_tutorials/MulInts.h"
#include <cstdlib>

int main(int argc,char **argv)
{
    ros::init(argc,argv,"mul_two_ints_client");
    if(argc !=3 )
    {
        ROS_INFO("Enter Two Numbers for Multiplication:");
        return 1;
    }

    ros::NodeHandle n;
    ros::ServiceClient client = n.serviceClient<pinak_beginner_tutorials::MulInts>("mul_two_ints");
    pinak_beginner_tutorials::MulInts srv;
    srv.request.a = atoll(argv[1]);
    srv.request.b = atoll(argv[2]);
    if (client.call(srv))
    {
        ROS_INFO("Product of two Numbers is:%ld",(long int)srv.response.product);
    }
    else{
        ROS_ERROR("Failed to call service mul_two_ints");
        return 1;
    }
    return 0;

}