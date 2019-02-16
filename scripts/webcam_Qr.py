from __future__ import print_function
import numpy as np
import cv2
from sys import argv
import zbar
import os
import sys

cap = cv2.VideoCapture(0)



# Find barcodes and QR codes
def decode(im):
	
	# Create zbar scanner
	scanner = zbar.ImageScanner()
	
	# Configure scanner
	scanner.parse_config('enable')	

	# Convert image to grayscale
	#imGray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

	imGray = im

	# Find height and width
	height, width = imGray.shape

	# Get raw image bytes
	raw = imGray.tobytes()

	# Wrap image data in a zbar image
	decodedObjects = zbar.Image(width, height, 'Y800', raw)

	# Scan the image for barcodes and QRCodes
	scanner.scan(decodedObjects)

	# Print results 
	for decodedObject in decodedObjects:
		print('Type : ', decodedObject.type); 
		print('Data :', decodedObject.data,'\n'); 
		print("something done");
	# Return decoded object
	return decodedObjects
		
# Display barcode and QR code location	
def display(im, decodedObjects):

	# Loop over all decoded objects
	for decodedObject in decodedObjects: 
		points = decodedObject.location
    
    # If the points do not form a quad, find convex hull
		if len(points) > 4 : 
			hull = cv2.convexHull(np.array([point for point in points]))
			hull = map(tuple, np.squeeze(hull))
		else : 
			hull = points;
    
    # Number of points in the convex hull
		n = len(hull)

    # Draw the convext hull
		for j in xrange(0,n):
			cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

	# Display results 
	cv2.imshow("Results", im);
	cv2.waitKey(0);


# Main 
#cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #gray=cv2.imread(frame,cv2.IMREAD_GRAYSCALE)	
    # Display the resulting frame
    cv2.imshow('frame',im)
    decodedObjects = decode(im)
    #print("init done")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

	# When everything done, release the capture
#display(im, decodedObjects)
cap.release()
cv2.destroyAllWindows()
