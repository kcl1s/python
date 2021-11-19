# Original code by YouTube user Big Bogey Face -Thanks
# adapted by Keith Lohmeyer
import cv2
import mediapipe as mp
import numpy as np
print(cv2.__version__)
width=1280
height=720
csx=int(width*.12)
csy=int(height*.12)
cex=int(width*.9)
cey=int(height*.98)
Cbrush=10
Rbrush=0
font = cv2.FONT_HERSHEY_SIMPLEX
LdataWeight=.2
davg=0
dbool=0
RdataWeight=.4
brushAvgX=0
brushAvgY=0
brushPosX=0
brushPosY=0
Dcolors=[(0,0,255),(255,0,255),(0,100,255),(5,85,160),(0,255,255),(0,255,150),
            (0,255,0),(255,0,0),(255,255,0),(255,255,255),(0,0,0)]
brushStatus=['Brush Up','Brush Down']
baseR=int(width*.004)
# Generate Class:
class mpArray:
    def __init__(self):
        self.Hands=mp.solutions.hands.Hands(False,2,.5,.5)
        self.Draw=mp.solutions.drawing_utils

    def getLM(self,img,doDraw):
        frame=img
        h,w,c=frame.shape
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.Hands.process(frameRGB)
        myHands=[]
        handsType=[]
        if results.multi_hand_landmarks != None:
            for hand in results.multi_handedness:
                handsType.append(hand.classification[0].label)
            for HLMs in results.multi_hand_landmarks:
                myHand=[]
                if doDraw==True:
                    self.Draw.draw_landmarks(frame,HLMs,mp.solutions.hands.HAND_CONNECTIONS)
                for LM in HLMs.landmark:
                    myHand.append((int(LM.x*w),int(LM.y*h)))
                myHands.append(myHand)              
        return myHands,handsType 

myLM= mpArray()
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cv2.namedWindow('my cam')
canvas=np.zeros([height,width,3],dtype=np.uint8)
while True:
    myHands=[]
    ignore,  frame = cam.read()
    frame=cv2.flip(frame,1)
    cleanFrame=frame
    handArray,handLR=myLM.getLM(cleanFrame,False)
    if not handArray:
        dbool=0         #no drawing without hands
    for lmks,hRL in zip(handArray,handLR):
        if hRL=='Left':
            # Check if Left Hand is Open or Closed:
            if (lmks[4][0]>lmks[3][0] and lmks[8][1]<lmks[6][1] and lmks[12][1]<lmks[10][1] and
                    lmks[16][1]<lmks[14][1] and lmks[20][1]<lmks[18][1]):
                drw=1
            else:
                drw=0
            davg=(LdataWeight * drw)+((1 - LdataWeight) * davg) #apply weighted average
            dbool=round(davg)                                   #Round to 0 or 1 at breakpoint .5                                  
        if hRL=='Right':
            brushAvgX=(RdataWeight * lmks[8][0])+((1 - RdataWeight) * brushAvgX)    #apply weighted averages penPosX
            brushPosX=int(brushAvgX)
            brushAvgY=(RdataWeight * lmks[8][1])+((1 - RdataWeight) * brushAvgY)    #apply weighted averages penPosY
            brushPosY=int(brushAvgY)
            if dbool:
                if (csx+baseR*Rbrush < brushPosX < cex-baseR*Rbrush and         # if on canvas/radius compensated
                        csy+baseR*Rbrush < brushPosY < cey-baseR*Rbrush): 
                    cv2.circle(canvas,(brushPosX,brushPosY),baseR*Rbrush,Dcolors[Cbrush],-1)
            else:
                if brushPosX > int(width*.93):                          #pick brush size
                    if int(height*.1) < brushPosY < int(height*.7):
                        Rbrush=int(brushPosY/height/.1)
                if brushPosY < int(height*.1):                          #pick brush color
                    if 0 < brushPosX < int(width*.88):
                        Cbrush=int((brushPosX/width/.08))
    cv2.rectangle(frame,(csx,csy),(cex,cey),(255,0,255),2)                                  #display canvas  
    for i in range (0,6,1):                                                                 #brush sizes
        j=int((height*.15)+(height*.1*i))
        cv2.circle(frame,(int(width*.965),j),baseR*(i+1),(255,255,255),-1)
        cv2.circle(frame,(int(width*.965),j),baseR*(i+1),(0,0,0),1)
    for i in range (0,6,1):                                                                 #Brush size rectangles
        j=int((height*.1)+(height*.1*i))
        cv2.rectangle(frame,(int(width*.93),j),(width,int(j+height*.1)),(255,255,255),2)
    for i in range (0,11,1):                                                                #Color picker rectangles
        cv2.rectangle(frame,(int(width*.08*i),0),(int(width*.08*(i+1)),int(height*.1)),Dcolors[i],-1)
        cv2.rectangle(frame,(int(width*.08*i),0),(int(width*.08*(i+1)),int(height*.1)),(255,255,255),2)
    cv2.putText(frame,'Rubber',(int(width*.81),int(height*.06)),font,height*.001,(255,255,255),2)
    cv2.putText(frame,brushStatus[dbool],(int(width*.01),int(height*.6)),font,height*.001,(255,255,255),2)
    Final_Display=cv2.addWeighted(frame,.9,canvas,1,0)                                      #combine frame & canvas
    cv2.circle(Final_Display,(brushPosX,brushPosY),baseR*Rbrush,Dcolors[Cbrush],-1)       #display brush last
    cv2.circle(Final_Display,(brushPosX,brushPosY),baseR*Rbrush,(255,255,255),2)
    cv2.resizeWindow('my cam',width,height)
    cv2.moveWindow('my cam',0,0)
    cv2.imshow('my cam', Final_Display)
    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey == ord('q'):
        break
    elif pressedKey == ord('c'):    #clear drawing
        canvas=np.zeros([height,width,3],dtype=np.uint8)
        Cbrush=10
cam.release()