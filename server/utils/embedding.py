from server.utils.model import load_model, model
from server.utils.preprocess import preprocess
import numpy as np

def generate_embedding(image_bytes):
    # Preprocess the image (implement this function according to your model's needs)
    image = preprocess(image_bytes)

    # Load the pre-trained Siamese model


    # Generate the embedding using the model
    embedding = model.predict(np.expand_dims(image, axis=0))  # Add batch dimension

    return embedding