import cv2
thresh=200
img=cv2.imread('leaves.jpg')
imgBGRA = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
height,width,x=imgBGRA.shape
for h in range(height):
    for w in range(width):
        pData=imgBGRA[h][w]
        if pData[0] > thresh and pData[1] > thresh and pData[2] > thresh:
            pData[3]=0
            imgBGRA[h][w]=pData
cv2.imwrite('leavesCV2.png',imgBGRA)