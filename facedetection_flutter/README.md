# Flutter Face detection + add in mask

## App demo
<div style="text-align: center"><table><tr>
  <td style="text-align: center">
    <img src="https://github.com/ShopeeUltraHackathon2021/GroupH3/blob/master/shopping-app/assets/images/demo.gif" width="200"/></a>
</td>
</tr></table></div>

By leveraging artificial intelligence to perform a) face detection and then b) key point localization, we can pinpoint the location of key features on the user’s face, such as eyes, nose and lips. 
Using Shopee’s live API, we can obtain images of accessories like spectacles, masks and hats

We can then attach the images to the correct positions on the user’s face, allowing for the virtual try-it-on experience.

## Feature
The camera will send the live stream data to firebase ML vision API to do face detection and will return the data such as bounding box info. 
From the item image, we can do a background removal to clean up the image and show the item in the camera view. It will track the user’s face and move along with the user's movement and will also auto resize to fit the user's face. 

In this way, users can have the virtual experience of trying items on which used to be exclusive in physical shops. And during the covid situation, some of the stores restrict customers to try on items in the fear of spearing the virus via samples. This feature can allow users to try on things they like without worrying about potential risks that may exist in offline stores. 

## Technologies
The app is written in flutter so we can use one single code base to do development in both android and iOS. For the face detection, we are using firebase ml vision api.
  
Thanks to [Maurice Parrish](https://github.com/bparrishMines) for [mlkit_demo](https://github.com/bparrishMines/mlkit_demo).