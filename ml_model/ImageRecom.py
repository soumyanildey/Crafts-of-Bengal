import numpy as np
import pickle as pkl
import tensorflow as tf
from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input
from keras.preprocessing import image
from keras.layers import GlobalMaxPool2D
from sklearn.neighbors import NearestNeighbors
import os
from numpy.linalg import norm
from PIL import Image as PILImage, ImageTk
import cv2
from keras.models import load_model

file_path_features = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'Images_features.pkl')
file_path_filenames = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'filenames.pkl')
file_path_model = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'model.keras')

with open(file_path_features, 'rb') as file:
        image_features = pkl.load(file)
with open(file_path_filenames, 'rb') as file:
        filenames = pkl.load(file)


# image_features = pkl.load(open(file_path_features, 'rb'))
# filenames = pkl.load(open(file_path_filenames, 'rb'))
model = load_model(file_path_model)



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

def hybrid_recom(uploaded_file, top_k=5):
    import numpy as np
    import tensorflow as tf
    import faiss
    from PIL import Image
    from io import BytesIO
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Dense, Flatten, Concatenate, Lambda
    from transformers import ViTImageProcessor, TFViTModel

    # Load ViT and ResNet
    input_layer = Input(shape=(224, 224, 3))
    resnet_base = ResNet50(weights='imagenet', include_top=False, input_tensor=input_layer)
    resnet_out = Flatten()(resnet_base.output)

    vit_processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
    vit_model = TFViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

    def vit_embedding_fn(x):
        x = tf.cast(x, tf.uint8).numpy()
        pixel_values = vit_processor(images=x, return_tensors="tf")["pixel_values"]
        return vit_model(pixel_values).last_hidden_state[:, 0, :]

    vit_features = Lambda(vit_embedding_fn, output_shape=(768,))(input_layer)
    merged = Concatenate()([resnet_out, vit_features])
    fc = Dense(512, activation='relu')(merged)
    embedding_output = Dense(256, activation='linear', name='embedding')(fc)
    fusion_model = Model(inputs=input_layer, outputs=embedding_output)
    fusion_model.compile(optimizer='adam', loss='mse')

    # Load features and FAISS index
    image_features = np.load("image_features_fusion.npy")
    image_paths = np.load("image_paths.npy", allow_pickle=True)
    index = faiss.IndexFlatL2(image_features.shape[1])
    index.add(image_features)

    # Preprocess uploaded image
    img = Image.open(BytesIO(uploaded_file.read())).convert('RGB').resize((224, 224))
    img_array = np.expand_dims(np.array(img).astype(np.float32), axis=0)
    img_tensor = tf.convert_to_tensor(img_array)

    # Extract features
    features = fusion_model(img_tensor, training=False).numpy()

    # Search FAISS index
    _, indices = index.search(features, top_k)
    return [image_paths[i] for i in indices[0]]
