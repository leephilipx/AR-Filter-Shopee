from my_CNN_model import *
import cv2
import numpy as np
from utils_shopee import *

# Define some parameters
image_file_path = 'test_shopee/shopee-image.png'
filter_no = 0

# Download image from Shopee API and load it
item, cat_no, total_filters = load_img(image_file_path, filter_no)  # {Hat, Eyewear, Mask}
item_shape = item.shape

''' ----------------------------------------- '''

# Load the model built in the previous step
my_model = load_my_CNN_model('my_model')

# Face cascade to detect faces
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

# Load the video
camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 720) 
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

# Keep looping
while True:
            
    # Grab the current paintWindow
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    frame2 = np.copy(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces, if error then terminate
    try:
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(90, 90), flags=cv2.CASCADE_SCALE_IMAGE)
    except Exception as e:
        camera.release()
        cv2.destroyAllWindows()
        print(f'\n{str(e)}')
        break

    for (x, y, w, h) in faces:
        
        '''Relative to boundary box, model uses 96x96 px'''
        
        # Grab the face
        gray_face = gray[y:y+h, x:x+w]
        color_face = frame[y:y+h, x:x+w]
    
        # Normalize to match the input format of the model - Range of pixel to [0, 1]
        gray_normalized = gray_face / 255.0
    
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
    
        # Pair them together (relating to boundary box)
        points = []
        for i, co in enumerate(keypoints[0][0::2]):
            points.append((co, keypoints[0][1::2][i]))
        
        '''Absolute position in webcam'''
        
        # Convert to keypoints to absolute positions
        absl = np.array(points)
        absl[:,0] = absl[:,0]*w/96.0 + x
        absl[:,1] = absl[:,1]*h/96.0 + y
        
        '''
        [0-3 left_eye_center, right_eye_center, left_eye_inner_corner, left_eye_outer_corner,
        [4-7] right_eye_inner_corner, right_eye_outer_corner, left_eyebrow_inner_end, left_eyebrow_outer_end,
        [8-11] right_eyebrow_inner_end, right_eyebrow_outer_end, nose_tip, mouth_left_corner,
        [12-14] mouth_right_corner, mouth_center_top_lip, mouth_center_bottom_lip
        '''

        if (cat_no == 0):  # Hat
            avg_eyebrow_y = (absl[6,1]+absl[8,1])/2                             # height of inner eyebrow
            item_width = int((absl[7,0]-absl[9,0])*1.6)                         # left & right outer eyebrow
            item_height = int(item_shape[0]/item_shape[1]*item_width)           # height/width*item_width
            item_center_x = int((absl[7,0]+absl[9,0])/2)                        # left & right outer eyebrow
            item_center_y = int(avg_eyebrow_y-(absl[10,1]-avg_eyebrow_y)*1.5)   # inner eyebrow - n*dist(nose & inner eyebrow)
        
        elif (cat_no == 1):  # Eyewear
            avg_eyebrow_y = (absl[6,1]+absl[8,1])/2                             # height of inner eyebrow
            item_width = int((absl[7,0]-absl[9,0])*1.2)                         # left & right outer eyebrow
            item_height = int((absl[10,1]-avg_eyebrow_y)/1.1)                   # nose & inner eyebrow
            item_center_x = int((absl[7,0]+absl[9,0])/2)                        # left & right outer eyebrow
            item_center_y = int((absl[10,1]+avg_eyebrow_y)/2)                   # nose & inner eyebrow

        elif (cat_no == 2):  # Mask
            item_width = int((absl[11,0]-absl[12,0])*3)                         # left & right mouth
            item_height = int((absl[14,1]-absl[10,1])*2)                        # nose & lower lip
            item_center_x = int((absl[12,0]+absl[11,0])/2)                      # left & right mouth
            item_center_y = int((absl[10,1]+absl[13,1]+2*absl[14,1])/4)         # nose, upper & 2*lower lip
            
        
        '''
        item_pos_x = range(item_center_x-int(item_width/2), item_center_x+np.ceil(item_width/2).astype(int))
        item_pos_y = range(item_center_y-int(item_height/2), item_center_y+np.ceil(item_height/2).astype(int))
        print(item_width, len(item_pos_x), ' ', item_height, len(item_pos_y), '  End:', item_center_y+np.ceil(item_height/2).astype(int))
        '''
        
        # Resize item
        item_resized = cv2.resize(item, (item_width, item_height), interpolation = cv2.INTER_CUBIC)
        transparent_region = item_resized[:,:,:3] != 0
        
        '''When item goes out of webcam region'''
        
        try:
            # Set item in position
            frame[item_center_y-int(item_height/2):item_center_y+np.ceil(item_height/2).astype(int), item_center_x-int(item_width/2):item_center_x+np.ceil(item_width/2).astype(int), :][transparent_region] = item_resized[:,:,:3][transparent_region]
            
            
            # Add KEYPOINTS to the frame2
            for keypoint in points:
                cv2.circle(face_resized_color2, keypoint, 1, (0,255,0), 1)
            frame2[y:y+h, x:x+w] = cv2.resize(face_resized_color2, original_shape, interpolation = cv2.INTER_CUBIC)
            
            # Add Boundary box containing face to frame 2
            cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        except Exception as e:
            print('>> ERR: Item out of webcam')
            pass
        

    # Show the frame and the frame2
    cv2.imshow("Selfie Filters", frame)
    cv2.imshow("Facial Keypoints", frame2)
    
    # Asynchronous keybinds
    if cv2.waitKey(1) & 0xFF == ord("w"):  # Change filter
        filter_no += 1
        filter_no %= total_filters
        item, cat_no, total_filters = load_img(image_file_path, filter_no)
        item_shape = item.shape
    elif cv2.waitKey(1) & 0xFF == ord("q"):    # KILL
        break
    elif cv2.waitKey(1) & 0xFF == ord("e"):  # Reload URLs
        item, cat_no, total_filters = load_img(image_file_path, filter_no)
        item_shape = item.shape

# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
print('>> Session end')