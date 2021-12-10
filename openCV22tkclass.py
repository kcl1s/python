import cv2
print(cv2.__version__)
import numpy as np
import cvhelpers as cvHelp
from tkinter import *

width=640
height=480
cB = (0,0,0)
cW = (255,255,255)
npframe = np.zeros([height,width,3],dtype=np.uint8)
npframe[:,:]=cB

root = Tk()
myHands= cvHelp.mpHandArray()
myPose= cvHelp.mpPoseArray()
myFace= cvHelp.mpFaceBbox()
myMesh= cvHelp.mpMeshArray()
trackC= cvHelp.cvColorTracker()
fps= cvHelp.TrackFPS(.05)
gui= cvHelp.cvGUI(root,width,height)
gui.camStart()

def myloop():
    ignore,  frame = gui.cam.read()
    npframe[:,:]=cW
    if gui.bFace.get():
        faceBboxes=myFace.getFaceBB(frame,False)    #returns ((TLx,TLy),(width,height) for each face
        #print (faceBboxes)
        for facebb in faceBboxes:
            centerbb=(int(facebb[0][0]+facebb[1][0]/2),int(facebb[0][1]+facebb[1][1]/3))
            axisbb=(int(facebb[1][0]/2),int(facebb[1][1]*.625))
            cv2.ellipse(frame,centerbb,axisbb,0,0,360,(255,0,0),2)
    if gui.bPose.get():
        poseArray=myPose.getPose(frame,True)  #returns list of 33 x,y tuples  True shows wireframe
        #print (poseArray)
    if gui.bHands.get():            
        handArray,handLR=myHands.getLM(frame,True)  #returns 21 x,y tuples and Left,Right for each hand
        #print (handArray,handLR)
    if gui.trackColor.get():
        contours=trackC.doColorTrack(frame)
        if contours != None:
            for contour in contours:
                area=cv2.contourArea(contour)
                if area>100:
                    (x,y),radius = cv2.minEnclosingCircle(contour)
                    center = (int(x),int(y))
                    radius = int(radius)
                    cv2.circle(frame,center,radius,(0,255,0),2)
    if gui.bMesh.get():
        meshArray=myMesh.getMesh(frame,False)
        for mesh in meshArray:
            i=0
            for meshLMs in mesh:
                i +=100
                cv2.circle(frame,meshLMs,2,(255,0,0),1)
                cv2.circle(npframe,meshLMs,2,((i*3)%255,(i*7)%255,(i*13)%255),-1)
                
    cv2.putText(frame,str(int(fps.getFPS())).rjust(3)+str(' FPS'),(0,50),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),3)
    gui.displayImg(frame)
    gui.displayNP(npframe)
    root.after(10, myloop) 

myloop()
root.mainloop()
