import cv2
import numpy as np
import utile

#image selection and  setups
path = "1.png"
widthImg = 650
heightImg = 700

img = cv2.imread(path)

#preprocessing the img
img = cv2.resize(img,(widthImg,heightImg))
imgContours = img.copy()
imgBiggestContours = img.copy()
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
imgCanny = cv2.Canny(imgBlur,10,50)


#all countours find()
contours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours, contours, -1,(0,255,0),10)
#rectcountour find()
rectCon= utile.rectCountour(contours)
biggestContour = utile.getCornerPoints(rectCon[0])
# print(biggestContour.shape)
gradePoints = utile.getCornerPoints(rectCon[4])


if biggestContour.size != 0 and gradePoints.size != 0:
    cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,255,0),20)
    cv2.drawContours(imgBiggestContours,gradePoints,-1,(255,0,0),20)

imgBlank = np.zeros_like(img)
imageArray = ([img, imgGray,imgBlur,imgCanny],
              [imgContours, imgBiggestContours, imgBlank, imgBlank])
imgstacked = utile.stackImages(imageArray, 0.5)
 
cv2.imshow("stacked images", imgstacked)
cv2.waitKey(0)