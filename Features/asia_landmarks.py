import numpy as np
import pandas as pd
import PIL
import tensorflow as tf
import tensorflow_hub as hub
from geopy.geocoders import Nominatim


model_url = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_asia_V1/1'
labels = 'on_device_vision_classifier_landmarks_classifier_asia_V1_1\landmarks_classifier_asia_V1_label_map.csv'
img_shape = (321,321)
classifier = tf.keras.Sequential([hub.KerasLayer(model_url,input_shape=img_shape+(3,),output_key="predictions:logits")])
df = pd.read_csv(labels)
labels = dict(zip(df.id,df.name))

def Get_Addres(location):
    geolocator = Nominatim(user_agent="Your_Name")
    location = geolocator.geocode(location)
    return [(location.address),(location.latitude),(location.longitude)]
    

def landmark_detection(image_path):
  img = PIL.Image.open(image_path)
  img = img.resize(img_shape)
  img = np.array(img)/255.0
  img = img[np.newaxis]
  result = classifier.predict(img)
  return (labels[np.argmax(result)])
  
def landmark_detection_with_address(image):
    try:
      landmark = landmark_detection(image)
      address = Get_Addres(landmark)
      return {
              'landmark': landmark,
              'address': address }
    except Exception as e:
      print("Exception: " + str(e))
      
      





# Output
# India Gate, Rajpath, Pandara Park, Chanakya Puri Tehsil, New Delhi, Delhi, 020626, India
# (28.612925150000002, 77.22954465819639)