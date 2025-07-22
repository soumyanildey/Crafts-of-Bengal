import numpy as np
import pickle as pkl
import tensorflow as tf
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPool2D
from sklearn.neighbors import NearestNeighbors
import os
from numpy.linalg import norm
from PIL import Image as PILImage, ImageTk
import cv2
from keras.models import load_model

file_path_features = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'Images_features.pkl')
file_path_filenames = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'filenames.pkl')

with open(file_path_features, 'rb') as file:
        image_features = pkl.load(file)
with open(file_path_filenames, 'rb') as file:
        filenames = pkl.load(file)
# image_features = pkl.load(open(file_path_features, 'rb'))
# filenames = pkl.load(open(file_path_filenames, 'rb'))
model = load_model(r'C:\Users\soumy\Desktop\e_commerce\e_commerce\ml_model\model.keras')



n_neighbors = min(5, len(image_features))
neighbors = NearestNeighbors(
    n_neighbors=n_neighbors, algorithm='brute', metric='euclidean')
neighbors.fit(image_features)

def extract_features(image_path,model):
  img=image.load_img(image_path,target_size=(299,299))
  img_array=image.img_to_array(img)
  expanded_img_array=np.expand_dims(img_array,axis=0)
  img_preprocess=preprocess_input(expanded_img_array)
  result=model.predict(img_preprocess).flatten()
  normalized_result=result/norm(result)
  return normalized_result

def get_image_recommendations(image_path, model, neighbors, filenames):
    # Extract features from the input image
    input_image = extract_features(image_path, model)
    distance, indices = neighbors.kneighbors([input_image])

    # Get the filenames of the recommended images
    recommended_filenames = [filenames[idx] for idx in indices[0]]

    return recommended_filenames

def get_recommendations(image_path):
    recommended_images = get_image_recommendations(image_path, model, neighbors, filenames)
    return recommended_images