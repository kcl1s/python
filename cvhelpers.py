import mediapipe as mp
import cv2
import time
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np

class mpMeshArray:
    def __init__(self):
        self.Mesh=mp.solutions.face_mesh.FaceMesh(False,3,.5,.5)
        self.Draw=mp.solutions.drawing_utils

    def getMesh(self,frame,doDraw):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        h,w,c=frame.shape
        results=self.Mesh.process(frameRGB)
        myMeshs=[]
        if results.multi_face_landmarks != None:
            for faceMesh in results.multi_face_landmarks:
                myMesh=[]
                if doDraw==True:
                    self.Draw.draw_landmarks(frame,faceMesh,mp.solutions.face_mesh.FACE_CONNECTIONS)
                for LM in faceMesh.landmark:
                    myMesh.append((int(LM.x*w),int(LM.y*h)))
                myMeshs.append(myMesh)
        return myMeshs

    def npFrame(self,frame,meshs):
        cB = (0,0,0)
        h,w,c=frame.shape
        npframe = np.zeros([h,w,3],dtype=np.uint8)
        npframe[:,:]=cB
        for mesh in meshs:
            for meshLMs in mesh:
                cv2.circle(npframe,meshLMs,2,(255,0,0),1)
        

class mpFaceBbox:
    def __init__(self):
        self.Face=mp.solutions.face_detection.FaceDetection()
        self.Draw=mp.solutions.drawing_utils

    def getFaceBB(self,frame,doDraw):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        h,w,c=frame.shape
        results=self.Face.process(frameRGB)
        myFaceBBs=[]
        if results.detections != None:
            for face in results.detections:
                if doDraw==True:
                    self.Draw.draw_detection(frame,face)
                bBox=face.location_data.relative_bounding_box
                TLbb=(int(bBox.xmin*w),int(bBox.ymin*h))
                WHbb=(int(bBox.width*w),int(bBox.height*h))
                myFaceBBs.append((TLbb,WHbb))
        return myFaceBBs    #returns ((TLx,TLy),(width,height) for each face
                            #https://google.github.io/mediapipe/solutions/face_detection.html

class mpPoseArray:
    def __init__(self):
        self.Pose=mp.solutions.pose.Pose()
        self.Draw=mp.solutions.drawing_utils

    def getPose(self,frame,doDraw):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        h,w,c=frame.shape
        results=self.Pose.process(frameRGB)
        myPose=[]
        if results.pose_landmarks:
            for plm in results.pose_landmarks.landmark:
                myPose.append((int(plm.x*w),int(plm.y*h)))
            if doDraw==True:
                self.Draw.draw_landmarks(frame,results.pose_landmarks,mp.solutions.pose.POSE_CONNECTIONS)
        return myPose   #returns list of 33 x,y tuples for 1 body
                        #https://google.github.io/mediapipe/solutions/pose.html

class mpHandArray:
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
        return myHands,handsType    #returns 21 x,y tuples and Left,Right for each hand
                                    #https://google.github.io/mediapipe/solutions/hands.html

class cvColorTracker:
    firstClick=True
    newClick=False
    def __init__(self):
       self.mHSV=np.zeros([1,1,3],dtype=np.uint8)

    def doColorTrack(self,frame):
        if (cvColorTracker.newClick):
            mFrame = frame[cvGUI.imgClick[1]:cvGUI.imgClick[1]+1, 
                            cvGUI.imgClick[0]:cvGUI.imgClick[0]+1]
            self.mHSV=cv2.cvtColor(mFrame,cv2.COLOR_BGR2HSV)
            (h,s,v)=self.mHSV[0,0]
            self.Hmin=np.clip(h-15,0,179)
            self.Hmax=np.clip(h+15,0,179)
            self.Smin=np.clip(s-60,0,255)
            self.Smax=np.clip(s+60,0,255)
            self.Vmin=np.clip(v-60,0,255)
            self.Vmax=np.clip(v+60,0,255)
            cvColorTracker.newClick=False
            cvColorTracker.firstClick=False

        frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        if cvColorTracker.firstClick==False:    
            LB=np.array([self.Hmin,self.Smin,self.Vmin])                       
            UB=np.array([self.Hmax,self.Smax,self.Vmax])                      
            cMask=cv2.inRange(frameHSV,LB,UB)
            contours,junk=cv2.findContours(cMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            return contours
            
class TrackFPS:           #Weighted average (low pass) filter for frames per second
    def __init__(self,dataWeight):
        self.dw=dataWeight
        self.state=0
    
    def getFPS(self):
        if self.state==0:
            self.average=0
            self.tlast=time.time()
            self.state = 1
        elif self.state==1:
            self.tDelta=time.time()-self.tlast
            self.average=1/self.tDelta
            self.tlast=time.time()
            self.state = 2            
        else:
            self.tDelta=time.time()-self.tlast
            self.fps=1/self.tDelta
            self.average=(self.dw * self.fps)+((1 - self.dw) * self.average)
            self.tlast=time.time()
        return self.average

class cvGUI:                    #https://tkdocs.com/index.html
    imgClick=(0,0)

    def __init__(self,master,h,w):
        self.h=h
        self.w=w
        self.root=master
        # set up GUI       
        guiFrame = ttk.Frame(self.root, padding=10)
        guiFrame.grid()
        # set control frame above video
        controlFrame=ttk.Frame(guiFrame, padding=10)
        controlFrame.grid(column=0, row=0)
        # set controls
        self.bFace=BooleanVar()
        cb1=ttk.Checkbutton(controlFrame,text='Face Bbox',variable=self.bFace)
        cb1.grid(column=0, row=0, padx=10)
        self.bPose=BooleanVar()
        cb2=ttk.Checkbutton(controlFrame,text='Body Pose',variable=self.bPose)
        cb2.grid(column=1, row=0, padx=10)
        self.bHands=BooleanVar()
        cb3=ttk.Checkbutton(controlFrame,text='Hands',variable=self.bHands)
        cb3.grid(column=2, row=0, padx=10)
        self.trackColor=BooleanVar()
        cb4=ttk.Checkbutton(controlFrame,text='Track Color',variable=self.trackColor)
        cb4.grid(column=3, row=0, padx=10)
        self.bMesh=BooleanVar()
        cb3=ttk.Checkbutton(controlFrame,text='Mesh',variable=self.bMesh)
        cb3.grid(column=4, row=0, padx=10)
        
        buttonQuit=ttk.Button(controlFrame, text="Quit", command=self.quitGUI)
        buttonQuit.grid(column=5, row=0)
        self.root.bind('q', self.quitGUI)
        # set video frame below controls
        imageFrame=ttk.Frame(guiFrame)
        imageFrame.grid(column=0, row=1)
        self.camIMG = ttk.Label(imageFrame)
        self.camIMG.grid(row=0, column=0)
        self.camIMG.bind('<1>', self.IMGxy)
        self.npIMG = ttk.Label(imageFrame)
        self.npIMG.grid(row=0, column=1)

    def quitGUI(self,*args):
        self.cam.release()
        self.root.destroy()

    def IMGxy(self,e):     #update x,y if click in image
        cvGUI.imgClick=(e.x,e.y)
        cvColorTracker.newClick=True

    def camStart(self):
        self.cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.w)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,self.h)
        self.cam.set(cv2.CAP_PROP_FPS, 30)

    def displayImg(self,frame):
        frameRGBA = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(frameRGBA)
        imgtk = ImageTk.PhotoImage(image=img)
        self.camIMG.imgtk = imgtk
        self.camIMG.configure(image=imgtk)

    def displayNP(self,npframe):
        frameRGBA = cv2.cvtColor(npframe, cv2.COLOR_BGR2RGBA)
        npimg = Image.fromarray(frameRGBA)
        npimgtk = ImageTk.PhotoImage(image=npimg,width=self.w,height=self.h)
        self.npIMG.imgtk = npimgtk
        self.npIMG.configure(image=npimgtk)
