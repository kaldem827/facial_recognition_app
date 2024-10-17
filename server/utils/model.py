import keras
import os
from server.utils.layers import L1Dist
import tensorflow as tf


def load_model(file_path):
    return keras.api.models.load_model(file_path,
                               custom_objects={'L1Dist': L1Dist, 'BinaryCrossentropy': keras.api.losses.BinaryCrossentropy})


current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the model file relative to this script's location
model_path = os.path.join(current_dir, "../../siamesemodel.keras")

# Load the model
model = load_model(model_path)