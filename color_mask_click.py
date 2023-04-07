import cv2
import numpy as np
import time
from picamera2 import Picamera2
dataWeight=.05
average=30
w=1280
h=720

def colorClick(event,xPos,yPos,f,p):
    global frame, LB, UB
    if event==1:
        mFrame = frame[yPos:yPos+1, xPos:xPos+1]
        mHSV=cv2.cvtColor(mFrame,cv2.COLOR_BGR2HSV)
        print (mHSV[0,0])
        (h,s,v)=mHSV[0,0]
        LB=np.array([np.clip(h-15,0,179),np.clip(s-100,0,255),np.clip(v-60,0,255)])
        UB=np.array([np.clip(h+15,0,179),np.clip(s+60,0,255),np.clip(v+60,0,255)])

picam=Picamera2()
picam.preview_configuration.main.size=(w,h)
picam.preview_configuration.main.format="RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()
tLast=time.time()-1

cv2.namedWindow('PiCam')
cv2.setMouseCallback('PiCam',colorClick)

LB=np.array([35,50,100])                       
UB=np.array([55,255,255])
while True:
    tDelta=time.time()-tLast
    fps=1/tDelta
    average=(dataWeight * fps)+((1 - dataWeight) * average)
    tLast=time.time()
    frame=picam.capture_array()
    cv2.putText(frame,str(int(average)).rjust(3)+str(' FPS'),(0,50),7,1,(255,0,0),3)
    
    
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cMask=cv2.inRange(frameHSV,LB,UB)
#     sMask=cv2.resize(cMask,(w//2,h//2))
#     cv2.imshow('mask',sMask)
    contours,junk=cv2.findContours(cMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
        #cv2.drawContours(frame,contours,0,(255,0,0),3)
        contour=contours[0]
        (x,y),radius = cv2.minEnclosingCircle(contour)
        centertc = (int(x),int(y))
        radius = int(radius)
        cv2.circle(frame,centertc,radius,(0,0,255),3) 
#     obj=cv2.bitwise_and(frame,frame,mask=cMask)
#     sobj=cv2.resize(obj,(w//2,h//2))
#     cv2.imshow('object',sobj)
    cv2.imshow("PiCam",frame)
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()
