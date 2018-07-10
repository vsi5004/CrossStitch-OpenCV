import cv2
import numpy as np

def scaleImage(expectedWidth, image):
	ratio = expectedWidth / image.shape[1]
	dim = (expectedWidth, int(image.shape[0] * ratio))
 
	# perform the actual resizing of the image and show it
	return cv2.resize(image, dim, interpolation = cv2.INTER_AREA);

def autoCanny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged

if __name__ == '__main__' :

	# Read image
	im = cv2.imread("image.jpg")

	im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	#im_gray = autoCanny(im_gray)
	im_gray = scaleImage(1000, im_gray)

	# Select ROI
	showCrosshair = False
	fromCenter = False
	r = cv2.selectROI("Image", im_gray, fromCenter, showCrosshair)


	# Crop image
	imCrop = im_gray[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

	# Display cropped image
	cv2.imwrite('crop.jpg',imCrop)
	cv2.imshow("Image", imCrop)
	cv2.waitKey(0)
