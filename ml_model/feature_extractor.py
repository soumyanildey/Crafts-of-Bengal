import tensorflow as tf
from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.layers import GlobalMaxPooling2D
import os


def load_feature_extractor_model():
    base_model = InceptionResNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(299, 299, 3)
    )
    base_model.trainable = False

    model = tf.keras.Sequential([
        base_model,
        GlobalMaxPooling2D()
    ])
    return model


if __name__ == "__main__":
    model = load_feature_extractor_model()

    # Save the model in .keras format in the same directory
    save_path = os.path.join(os.path.dirname(
        __file__), "model.keras")
    model.save(save_path)

    print(f"Model saved at: {save_path}")
