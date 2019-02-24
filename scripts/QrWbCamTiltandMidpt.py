
from __future__ import print_function
import numpy as np
import cv2
from sys import argv
import zbar
import os
import sys
import math 
from shapely.geometry import LineString

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
			cv2.line(im, hull[j], hull[ (j+1) % n], (0,0,255), 3)
			#print(j)
			#print(hull[j], hull[ (j+1) % n])
	# Display results
		x_0,y_0=hull[0]
		x_1,y_1=hull[1]
		x_2,y_2=hull[2]
		x_3,y_3,=hull[3]

		x_diff=x_0-x_3
		y_diff = y_0 - y_3


		line1=LineString([(x_0,y_0),(x_2,y_2)])
		line2=LineString([(x_1,y_1),(x_3,y_3)])

		cv2.line(im, hull[0], hull[ (2) % n], (0,0,255), 3)
		cv2.line(im, hull[1], hull[ (3) % n], (0,0,255), 3)
		#midpoint= find_intersection(hull[0], hull[ (2) % n],hull[1], hull[ (3) % n]) 
		midpoint = line1.intersection(line2)

		print("midpoint",midpoint)
		mid_x=int(midpoint.x)
		mid_y=int(midpoint.y)
		font = cv2.FONT_HERSHEY_SIMPLEX

		cv2.circle(im,(mid_x,mid_y), 8, (255,255,255), -1)
		cv2.putText(im,'midpoint',(mid_x,mid_y), font, 2,(255,255,255),2,cv2.LINE_AA)
			

		
		print("tilt angle= ",math.degrees(math.atan2(y_diff, x_diff)))
		print("something done");
	cv2.imshow("Results", im)

	#cv2.waitKey(0);


def find_intersection( p1, p2 , p3 ,p4 ) :
	s1 = p1
	e1 = p2

	s2 = p3
	e2 = p4

	a1 = (s1[1] - e1[1]) / (s1[0] - e1[0])
	b1 = s1[1] - (a1 * s1[0])

	a2 = (s2[1] - e2[1]) / (s2[0] - e2[0])
	b2 = s2[1] - (a2 * s2[0])

	if abs(a1 - a2) < sys.float_info.epsilon:
		return False

	x = (b2 - b1) / (a1 - a2)
	y = a1 * x + b1
	return (x, y)


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
    display(im, decodedObjects)
    #print("init done")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

	# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
