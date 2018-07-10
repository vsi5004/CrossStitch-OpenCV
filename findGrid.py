import cv2
import numpy as np

GREEN = (0, 255, 0)
RED = (0, 0, 255)

def scaleImage(expectedWidth, image):
	ratio = expectedWidth / image.shape[1]
	dim = (expectedWidth, int(image.shape[0] * ratio))
	return cv2.resize(image, dim, interpolation = cv2.INTER_AREA);

def drawLines(lines, img, color):
	for line in lines:
		x1, y1, x2, y2 = line[0]
		cv2.line(img, (x1, y1), (x2, y2), color, 1)
	return img;

def updateImage():
	imgOvrl = imgOrig.copy()
	imgOvrl = drawLines(hLines, imgOvrl, GREEN)
	imgOvrl = drawLines(vLines, imgOvrl, RED)
	imgOvrl = scaleImage(900, imgOvrl)	
	cv2.imshow("Image", imgOvrl)
	return;

def updateHorzLines(hVal):	
	global hLines
	hLines = cv2.HoughLinesP(imgFlt, 1, np.pi/2, hVal, minLineLength=1500, maxLineGap=100)
	updateImage()
	return;

def updateVertLines(vVal):
	global vLines
	vLines = cv2.HoughLinesP(imgFlt, 1, np.pi, vVal, minLineLength=1500, maxLineGap=100)
	updateImage()
	return;

imgOrig = cv2.imread("grid.jpg")
imgFlt = cv2.cvtColor(imgOrig, cv2.COLOR_BGR2GRAY)
imgFlt = cv2.bilateralFilter(imgFlt,4,15,15)
imgFlt = cv2.adaptiveThreshold(imgFlt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,5)
imgFlt = cv2.bitwise_not(imgFlt)

cv2.namedWindow('Image')
cv2.createTrackbar('Horizontal Lines','Image',1500,1800,updateHorzLines)
cv2.createTrackbar('Vertical Lines','Image',1500,1800,updateVertLines)

hVal = cv2.getTrackbarPos('Horizontal Lines','Image')
vVal = cv2.getTrackbarPos('Vertical Lines','Image')
hLines = cv2.HoughLinesP(imgFlt, 1, np.pi/2, hVal, minLineLength=1500, maxLineGap=100)
vLines = cv2.HoughLinesP(imgFlt, 1, np.pi, vVal, minLineLength=1500, maxLineGap=100)
updateImage()

cv2.waitKey(0)
cv2.destroyAllWindows()
