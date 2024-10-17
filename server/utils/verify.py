from server.utils.preprocess import preprocess
import os
import numpy as np


def verify(model, input_img_bytes, validation_img_bytes, detection_threshold=0.5, verification_threshold=0.7):
    # Preprocess both input and validation images
    input_img = preprocess(input_img_bytes)
    validation_img = preprocess(validation_img_bytes)

    # Predict the embeddings for both images using the Siamese network
    input_embedding = model.predict(np.expand_dims(input_img, axis=0))  # (1, 4096)
    validation_embedding = model.predict(np.expand_dims(validation_img, axis=0))  # (1, 4096)

    # Calculate L1 distance between the embeddings
    l1_distance = np.abs(input_embedding - validation_embedding)

    # Calculate the similarity (closer to zero means more similar)
    similarity = np.sum(l1_distance)

    # Apply detection and verification thresholds
    detection = similarity < detection_threshold  # If distance is below threshold, consider it a match
    verified = detection >= verification_threshold  # Proportion of positives for verification

    return similarity, verified