from my_CNN_model import *
import cv2
import sys
import numpy as np
import requests
from utils_shopee import *

# Load the model built in the previous step
my_model = load_my_CNN_model('my_model')

# Face cascade to detect faces
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

# Define the upper and lower boundaries for a color to be considered "Blue"
blueLower = np.array([100, 60, 60])
blueUpper = np.array([140, 255, 255])

# Define a 5x5 kernel for erosion and dilation
kernel = np.ones((5, 5), np.uint8)

image_file_path = 'test_shopee/shopee-image.png'
item_cat = 1  # {Eyewear, Mask}

# Define filters
filters = [image_file_path, 'images/sunglasses.png', 'images/sunglasses_2.png', 'images/sunglasses_3.jpg', 'images/sunglasses_4.png', 'images/sunglasses_5.jpg', 'images/sunglasses_6.png']
filterIndex = 0

# Custom function SHOPEE
load_img(image_file_path)
        
# Load the video
camera = cv2.VideoCapture(0)

# Keep looping
while True:
            
    # Grab the current paintWindow
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    frame2 = np.copy(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    try:
        # faces = face_cascade.detectMultiScale(gray, 1.25, 6)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(90, 90), flags=cv2.CASCADE_SCALE_IMAGE)
    except Exception as e:
        camera.release()
        cv2.destroyAllWindows()
        print(f'\n{str(e)}')
        break

    # # Add the 'Next Filter' button to the frame
    # frame = cv2.rectangle(frame, (500,10), (620,65), (235,50,50), -1)
    # cv2.putText(frame, "NEXT FILTER", (512, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    # # Determine which pixels fall within the blue boundaries and then blur the binary image
    # blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    # blueMask = cv2.erode(blueMask, kernel, iterations=2)
    # blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    # blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    # # Find contours (bottle cap in my case) in the image
    # (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
    #  	cv2.CHAIN_APPROX_SIMPLE)
    # center = None

    # # Check to see if any contours were found
    # if len(cnts) > 0:
    #  	# Sort the contours and find the largest one -- we
    #  	# will assume this contour correspondes to the area of the bottle cap
    #     cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
    #     # Get the radius of the enclosing circle around the found contour
    #     ((x, y), radius) = cv2.minEnclosingCircle(cnt)
    #     # Draw the circle around the contour
    #     cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    #     # Get the moments to calculate the center of the contour (in this case Circle)
    #     M = cv2.moments(cnt)
    #     center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

    #     if center[1] <= 65:
    #         if 500 <= center[0] <= 620: # Next Filter
    #             filterIndex += 1
    #             filterIndex %= 6
    #             continue
        
    #if (len(faces)>=1): x, y, w, h = faces[0]
    for (x, y, w, h) in faces:
        
        # Boundary box containing face
        cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Grab the face
        gray_face = gray[y:y+h, x:x+w]
        color_face = frame[y:y+h, x:x+w]
    
        # Normalize to match the input format of the model - Range of pixel to [0, 1]
        gray_normalized = gray_face / 255
    
        # Resize it to 96x96 to match the input format of the model
        original_shape = gray_face.shape # A Copy for future reference
        face_resized = cv2.resize(gray_normalized, (96, 96), interpolation = cv2.INTER_AREA)
        face_resized_copy = face_resized.copy()
        face_resized = face_resized.reshape(1, 96, 96, 1)
    
        # Predicting the keypoints using the model
        keypoints = my_model.predict(face_resized)
    
        # De-Normalize the keypoints values
        keypoints = keypoints * 48 + 48
    
        # Map the Keypoints back to the original image
        face_resized_color = cv2.resize(color_face, (96, 96), interpolation = cv2.INTER_AREA)
        face_resized_color2 = np.copy(face_resized_color)
    
        # Pair them together
        points = []
        for i, co in enumerate(keypoints[0][0::2]):
            points.append((co, keypoints[0][1::2][i]))
        
        # Add FILTER to the frame
        item = cv2.imread(filters[filterIndex], cv2.IMREAD_UNCHANGED)
        
        if item_cat == 0:  # Eyewear
            item_width = int((points[7][0]-points[9][0])*1.1)
            item_height = int((points[10][1]-points[8][1])/1.1)
            item_resized = cv2.resize(item, (item_width, item_height), interpolation = cv2.INTER_CUBIC)
            transparent_region = item_resized[:,:,:3] != 0
            item_center_x = int((points[11][0]+points[12][0])/2)
            item_center_x = int((points[13][1]+points[14][1])/2)

        elif item_cat == 1:  # Mask
            item_width = int((points[7][0]-points[9][0])*1.3)
            item_height = int((points[14][1]-points[10][1])*1.4)
            item_resized = cv2.resize(item, (item_width, item_height), interpolation = cv2.INTER_CUBIC)
            transparent_region = item_resized[:,:,:3] != 0
            item_center_x = int((points[11][0]+points[12][0])/2)
            item_center_y = int(points[13][1])
        
        # Resize the face_resized_color image back to its original shape
        face_resized_color[item_center_y-int(item_height/2):item_center_y+np.ceil(item_height/2).astype(int), item_center_x-int(item_width/2):item_center_x+np.ceil(item_width/2).astype(int), :][transparent_region] = item_resized[:,:,:3][transparent_region]
        frame[y:y+h, x:x+w] = cv2.resize(face_resized_color, original_shape, interpolation = cv2.INTER_CUBIC)
    
        # Add KEYPOINTS to the frame2
        for keypoint in points:
            cv2.circle(face_resized_color2, keypoint, 1, (0,255,0), 1)
    
        frame2[y:y+h, x:x+w] = cv2.resize(face_resized_color2, original_shape, interpolation = cv2.INTER_CUBIC)

    # Show the frame and the frame2
    cv2.imshow("Selfie Filters", frame)
    cv2.imshow("Facial Keypoints", frame2)
    
    
    # If the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    elif cv2.waitKey(1) & 0xFF == ord("z"):
        filterIndex += 1
        filterIndex %= 7
    elif cv2.waitKey(1) & 0xFF == ord("a"):
        print('Change category or load new image')
    #     load_img(image_file_path)
    
    
    

# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
print('>> Session end')