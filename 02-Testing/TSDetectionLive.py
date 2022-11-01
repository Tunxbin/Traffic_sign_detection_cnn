import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

modelPath = 'C:/Users/win/Downloads/PBL4_Test/03-Training/Models'
model = keras.models.load_model(modelPath+'/TSModel')

def returnRedness(img):
	yuv=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
	y,u,v=cv2.split(yuv)
	return v

def threshold(img,T=150):
	_,img=cv2.threshold(img,T,255,cv2.THRESH_BINARY)
	return img 

def findContour(img):
	contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	return contours

def findBiggestContour(contours):
	m = 0
	c = [cv2.contourArea(i) for i in contours]
	return contours[c.index(max(c))]

def boundaryBox(img,contours):
	x,y,w,h=cv2.boundingRect(contours)
	img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	sign=img[y:(y+h) , x:(x+w)]
	return img,sign


#--------------------------------------------------------------------------

cap=cv2.VideoCapture(0)

while(True):
	_, frame = cap.read()
	redness = returnRedness(frame) 
	thresh = threshold(redness) 	
	try:
		contours = findContour(thresh)
		big = findBiggestContour(contours)
		if cv2.contourArea(big) > 3000:
			print(cv2.contourArea(big))
			img,sign = boundaryBox(frame,big)
			cv2.imshow('frame',img)
			cv2.imshow('sign',sign)
		else:
			cv2.imshow('frame',frame)
	except:
		cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()