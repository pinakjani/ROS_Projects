#!/usr/bin/env python
import rospy
import sys
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
# bridge = CvBridge()
# cv_image = bridge.imgmsg_to_cv2(img_msg,desired_encoding='passthrough')

def mask_centre(img,mask):

    length = img.shape[0]
    height = img.shape[1]
    count = 0
    sumx = 0
    sumy = 0
    for i in range(1,height):
        for j in range(1,length):
            if mask[i,j] > 0:
                sumx += j
                sumy += i
                count += 1
    valx = sumx//(count) 
    valy = sumy//(count)
    # print(valx,valy)
    cv2.circle(img,(valx,valy),2,(255,255,255),-1)
    # cv2.imshow("win3",img)
    # cv2.waitKey(0)
    return img,(valx,valy)

def Imageops(img):
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        green_lower = np.array([58,10,95])
        green_upper = np.array([78,255,200])
        purple_lower = np.array([138,20,85])
        purple_upper = np.array([158,255,170])
        red_lower = np.array([118,20,95])
        red_upper = np.array([128,255,200])
        blue_lower = np.array([0,50,45])
        blue_upper = np.array([10,255,250])
        blue1_lower = np.array([175,50,45])
        blue1_upper = np.array([180,255,250])
        blue_mask1 = cv2.inRange(hsv, blue_lower, blue_upper)
        blue_mask2 = cv2.inRange(hsv, blue1_lower, blue1_upper)
        blue_mask = blue_mask1+blue_mask2
        blue_res = cv2.bitwise_and(img,img, mask= blue_mask)
        blue_res,blue_cen = mask_centre(blue_res,blue_mask)
        purp_mask = cv2.inRange(hsv, purple_lower, purple_upper)
        purp_res = cv2.bitwise_and(img,img, mask= purp_mask)
        purp_res,purp_cen = mask_centre(purp_res,purp_mask)
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        green_res = cv2.bitwise_and(img,img, mask= green_mask)
        green_res,green_cen = mask_centre(green_res,green_mask)
        red_mask = cv2.inRange(hsv, red_lower, red_upper)
        red_res = cv2.bitwise_and(img,img, mask= red_mask)
        red_res,red_cen = mask_centre(red_res,red_mask)
        print("The centre for Red Circle is at: ",red_cen)
        print("The centre for Purple Circle is at: ",purp_cen)
        print("The centre for Green Circle is at: ",green_cen)
        print("The centre for Blue Circle is at: ",blue_cen)
        cv2.imshow("win",np.concatenate((blue_res, purp_res), axis=1))
        cv2.waitKey(0)
        cv2.imshow("win1",np.concatenate((green_res, red_res), axis=1))
        cv2.waitKey(0)
        
def canny(img):      
      
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5,5), cv2.BORDER_DEFAULT)
    edges = cv2.Canny(image=img_blur, threshold1=20, threshold2=80)
    cv2.imshow("Canny",edges)
    cv2.waitKey(0)

def corner(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dest = cv2.cornerHarris(img_gray, 2, 7, 0.04)
    dest = cv2.dilate(dest, None)
    img[dest > 0.01 * dest.max()]=[0, 0, 255]
    cv2.imshow("Harris corner",img)
    cv2.waitKey(0)

def hough_circles(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    circles = cv2.HoughCircles(img_gray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=33,minRadius=0,maxRadius=0)

    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        print("Centre of the Hough circles is:",i[0],i[1])
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('detected circles',img)
    cv2.waitKey(0)


class image_converter:


    def __init__(self):
 
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/pinak_robot/camera1/image_raw",Image,self.callback)
    
    

    
    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        img = cv_image.copy()
        cv2.imwrite("/home/pinak/catkin_ws/src/urdf_basic/src/pinak_robot_img.jpg",img)
        print("Received an image! Please wait! Implementing Image Processing.")
        rospy.sleep(1)
        Imageops(img)
        # rospy.sleep(1)
        canny(img)
        corner(img)
        hough_circles(img)
        # cv2.imshow("Image window", img)
        # cv2.waitKey(0)
        
    
        
def main(args):

    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
   
if __name__ == '__main__':
    main(sys.argv)