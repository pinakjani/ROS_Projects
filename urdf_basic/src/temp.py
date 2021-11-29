import cv2
import math
import numpy as np
img1  = cv2.imread("/home/pinak/catkin_ws/src/urdf_basic/src/pinak_robot_img.jpg")
img2  = cv2.imread("/home/pinak/catkin_ws/src/urdf_basic/src/pinak_robot_img2.jpg")

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
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # cv2.imshow("window",img_gray)
    # cv2.waitKey(0)  
    # img = cv2.medianBlur(img,5)
    # cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img_gray,cv2.HOUGH_GRADIENT,2,45,param1=40,param2=20,minRadius=0,maxRadius=15)

    circles = np.uint16(np.around(circles))
    features = []
    for i in circles[0,:]:
        # draw the outer circle
        print("Centre of the circle is:",i[0],i[1])
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        features.append((i[0],i[1]))

    cv2.line(img,features[0],features[1],(0,0,0),2)
    cv2.imshow('detected circles',img)
    cv2.waitKey(0)

# hough_circles(img)
# cv2.imshow("win1",img)
# cv2.waitKey(0)
def cent(img,mask):
    M = cv2.moments(mask)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(img,(cX,cY),2,(255,255,255),-1)
    return img,(cX,cY)


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

def features(img):    
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    green_lower = np.array([58,10,95])
    green_upper = np.array([78,255,200])
    purple_lower = np.array([138,20,85])
    purple_upper = np.array([158,255,170])
    red_lower = np.array([118,200,75])
    red_upper = np.array([128,255,200])
    blue_lower = np.array([0,50,45])
    blue_upper = np.array([10,255,250])
    blue1_lower = np.array([175,50,45])
    blue1_upper = np.array([180,255,250])
    blue_mask1 = cv2.inRange(hsv, blue_lower, blue_upper)
    blue_mask2 = cv2.inRange(hsv, blue1_lower, blue1_upper)
    blue_mask = blue_mask1+blue_mask2
    blue_res = cv2.bitwise_and(img,img, mask= blue_mask)
    blue_res,blue_cen = cent(img,blue_mask)
    purp_mask = cv2.inRange(hsv, purple_lower, purple_upper)
    purp_res = cv2.bitwise_and(img,img, mask= purp_mask)
    purp_res,purp_cen = cent(img,purp_mask)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    green_res = cv2.bitwise_and(img,img, mask= green_mask)
    green_res,green_cen = cent(img,green_mask)
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    red_res = cv2.bitwise_and(img,img, mask= red_mask)
    red_res,red_cen = cent(img,red_mask)
    print("The centre for Red Circle is at: ",red_cen)
    print("The centre for Purple Circle is at: ",purp_cen)
    print("The centre for Green Circle is at: ",green_cen)
    print("The centre for Blue Circle is at: ",blue_cen)
    # cv2.line(img,blue_cen,purp_cen,(0,0,0),2)
    # slope = math.atan2((blue_cen[1]-purp_cen[1]),(blue_cen[0]-purp_cen[0]))
    # print(slope*180/math.pi)
    return [blue_cen,purp_cen]
    cv2.imshow("win",img)
    cv2.waitKey(0)


f1 = features(img1)
f2 = features(img2)
slope1 = math.atan2((f1[0][1]-f2[0][1]),(f1[0][0]-f2[0][0]))
slope2 = math.atan2((f1[1][1]-f2[1][1]),(f1[1][0]-f2[1][0]))
print("Blue slope;",slope1*180/math.pi)
print("Purp slope;",slope2*180/math.pi)
cv2.line(img1,f1[0],f2[0],(0,0,0),2)
cv2.line(img1,f1[1],f2[1],(0,0,0),2)
cv2.imshow("image",img1)
cv2.waitKey(0)