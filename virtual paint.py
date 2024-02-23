import cv2 as cv
import numpy as np

framewidth, frameheight=680, 400
web=cv.VideoCapture(0)
web.set(3, framewidth)
web.set(4, frameheight)
web.set(10, 150)

#----orange purple green
mycolors=[[5,107,0,19,255,255],
          [133,56,0,159,156,255],
          [57,76,0,100,255,255]]


mycolorvalues=[[51,153,255],[255,0,255],[0,255,0]]


mypoints=[]
def findcolor(img, mycolors, mycolorvalues):
    imghsv= cv.cvtColor(img, cv.COLOR_BGR2HSV)
    count=0
    newpoints=[]
    for color in mycolors:
        lower= np.array(color[0:3])
        upper=np.array(color[3:6])
        mask=cv.inRange(imghsv, lower, upper)
        x,y=getcontours(mask)
        cv.circle(imgresult,(x,y),5,(mycolorvalues[count]),cv.FILLED)
        #cv.imshow(str(color[0]), mask)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count+=1

    return  newpoints
def getcontours(img):
    contours, hierarchy =cv.findContours(img, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for c in contours:
        area=cv.contourArea(c)
        if area>500:
            #cv.drawContours(imgresult, c, -1,(255,0,0),3)
            peri=cv.arcLength(c,True)
            approx=cv.approxPolyDP(c,0.02*peri,True)
            x,y,w,h=cv.boundingRect(approx)
    return x+w//2,y


def draw(mypoints, mycolorvalues):
    for point in mypoints:
        cv.circle(imgresult, (point[0], point[1]), 5, mycolorvalues[point[2]], cv.FILLED)


while True:
    success, img=web.read()
    imgresult = img.copy()
    newpoints=findcolor(img, mycolors, mycolorvalues)
    if len(newpoints)!=0:
        for n in newpoints:
            mypoints.append(n)
    if len(mypoints)!=0:
        draw(mypoints, mycolorvalues)
    cv.imshow("webcam", imgresult)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break


