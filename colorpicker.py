import cv2 as cv
import numpy as np


#---stacking image function
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


framewidth=240
frameheight=240
web=cv.VideoCapture(0)
web.set(3,framewidth)
web.set(4, frameheight)
web.set(10, 150)

def empty(a):
    pass

cv.namedWindow("hsv")
cv.resizeWindow("hsv", 240, 240)
cv.createTrackbar("hue min", "hsv", 0,179,empty)
cv.createTrackbar("hue max", "hsv", 179,179,empty)
cv.createTrackbar("sat min", "hsv", 0,255,empty)
cv.createTrackbar("sat max", "hsv", 255,255,empty)
cv.createTrackbar("val min", "hsv", 0,255,empty)
cv.createTrackbar("val max", "hsv", 255,255,empty)


while True:
    _,img=web.read()
    imghsv=cv.cvtColor(img, cv.COLOR_BGR2HSV)

    h_min=cv.getTrackbarPos("hue min", "hsv")
    h_max = cv.getTrackbarPos("hue max", "hsv")
    s_min = cv.getTrackbarPos("sat min", "hsv")
    s_max = cv.getTrackbarPos("sat max", "hsv")
    v_min = cv.getTrackbarPos("val min", "hsv")
    v_max=cv.getTrackbarPos("val max", "hsv")

    print(h_min)

    lower=np.array([h_min, s_min, v_min])
    upper=np.array([h_max, s_max, v_max])

    mask=cv.inRange(imghsv, lower, upper)
    result=cv.bitwise_and(img, img, mask=mask)

    mask=cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    hstack=np.hstack([img, mask, result])
    cv.imshow("stacking", hstack)

    if cv.waitKey(1) & 0xFF==ord('q'):
        break
