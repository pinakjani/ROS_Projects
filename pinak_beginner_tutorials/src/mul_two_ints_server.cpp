#include "ros/ros.h"
#include "pinak_beginner_tutorials/MulInts.h"

bool mul(pinak_beginner_tutorials::MulInts::Request  &req,pinak_beginner_tutorials::MulInts::Response &res)
{
    res.product = req.a*req.b;
    ROS_INFO("Inputs for Multiplication: x=%ld, y=%ld", (long int)req.a, (long int)req.b);
    ROS_INFO("Product of the Inputs: [%ld]", (long int)res.product);
    return true;
}
int main(int argc, char **argv)
{
    ros::init(argc,argv,"mul_two_ints_server");
    ros::NodeHandle n;
    ros::ServiceServer service = n.advertiseService("mul_two_ints",mul);
    ROS_INFO("Ready to Multiply.");
    ros::spin();
    return 0;
}