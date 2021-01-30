# McSpicy Notes
- Run ```shades.py``` as starting point
- Own files: ```utils_shopee.py```, ```test_shopee/```
- Use existing ```my_model.h5``` as the model for facial points detection
- Dependencies: ```Tensorflow 1.x```, ```Keras 2.3.1```, ```opencv-python```, ```Numpy```

# Installation
    conda create -n face python=3.7 -y
    conda activate face

    # current CNN training code only works with tensorflow 1.x
    pip install tensorflow=1.14
    # latest keras version compatible with tensorflow 1.x
    pip install keras=2.3.1
    pip install opencv-python

## Training the model from scratch
1. Download the training data  _'training.zip'_ file from [here](https://www.kaggle.com/c/facial-keypoints-detection/data) and extract it into the _'data'_ folder.

2. Run ``` python model_builder.py ```

## Running the try-it-on demo on laptop webcam
1. Run ``` python shades.py ```

### Credits
The code was adapted from, with heavy modifications: https://github.com/acl21/Selfie_Filters_OpenCV
