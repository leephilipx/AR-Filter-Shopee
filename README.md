# Shopee - Try-it-on!
*Team McScipy (H3)*

By leveraging artificial intelligence to perform a) face detection and then b) key point localization, we can pinpoint the location of key features on the user’s face, such as eyes, nose and lips. 
Using Shopee’s live API, we can obtain images of accessories like spectacles, masks and hats

We can then attach the images to the correct positions on the user’s face, allowing for the virtual try-it-on experience.

<br>

## Mobile Application Description and Demo

### App Screens
<div style="text-align: center"><table><tr>
  <td style="text-align: center">
    <img src="https://github.com/ShopeeUltraHackathon2021/GroupH3/blob/master/shopping-app/assets/images/demo.gif" width="200"/></a>
</td>
</tr></table></div>
     
### Feature
The camera will send the live stream data to firebase ML vision API to do face detection and will return the data such as bounding box info. 
From the item image, we can do a background removal to clean up the image and show the item in the camera view. It will track the user’s face and move along with the user's movement and will also auto resize to fit the user's face. 

In this way, users can have the virtual experience of trying items on which used to be exclusive in physical shops. And during the covid situation, some of the stores restrict customers to try on items in the fear of spearing the virus via samples. This feature can allow users to try on things they like without worrying about potential risks that may exist in offline stores. 

### Technologies
The app is written in flutter so we can use one single code base to do development in both android and iOS. For the face detection, we are using firebase ml vision api.

### Credits
The code was adapted from, with heavy modifications: https://github.com/Boghdady/flutter-firebase-shopping-app & https://github.com/giandifra/Flutter-Smile-Face-Detection

<br>

## Python AR Filter
The more reliable face detection and AR filter is implemented in Python. The item image is retrieved from the cover url and the image is cropped while the background is removed.  
<ol type="a"><li>The boundary box encapsulating the face is detected by the Haar feature-based cascade classifier for frontal face. The facial region is then cropped and resized to 96x96 px for the prediction of keypoints by the CNN model. These keypoints will be used as reference to overlap the item on top.</li>
<li>The item is added on top according to the category it is assigned to. (eg. eyewear will use eye keypoints)</li></ol>

### Instructions to Try-it-on!
- Turn on the webcam.
- Run ```python shades.py``` as starting point.
- Use pre-trained ```my_model.h5``` as the model for facial points detection.
- Dependencies: ```Tensorflow 1.x```, ```Keras 2.3.1```, ```opencv-python```, ```NumPy```

### Demo
<img src="python_AR_CNN/Python-AR-CNN Demo.gif"/>

### Installation
    conda create -n face python=3.7 -y
    conda activate face

    # current CNN training code only works with tensorflow 1.x
    pip install tensorflow=1.14
    # latest keras version compatible with tensorflow 1.x
    pip install keras=2.3.1
    pip install opencv-python

### Training the model from scratch
1. Download the training data  _'training.zip'_ file from [here](https://www.kaggle.com/c/facial-keypoints-detection/data) and extract it into the _'data'_ folder.
2. Run ``` python model_builder.py ```

### Credits
The code was adapted from, with heavy modifications: https://github.com/acl21/Selfie_Filters_OpenCV
