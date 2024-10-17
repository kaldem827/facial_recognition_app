import mysql.connector
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException

from server.config.db import get_connection, fetch_all_embeddings, fetch_user_by_id
from server.utils.embedding import generate_embedding

# Initialize FastAPI app
fetch_info_router = FastAPI().router


# Function to preprocess the image (you should implement this)
def preprocess(image_bytes):
    # Example: Load the image, resize, normalize, etc.
    return image_bytes  # Placeholder - implement preprocessing here


@fetch_info_router.post("/fetch-info/")
async def fetch_info(file: UploadFile = File(...)):
    """
    API endpoint to fetch user info by scanning a face image.
    The image will be compared with stored embeddings, and if matched, user information will be returned.
    """
    try:
        # Create database connection
        connection = get_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Failed to connect to the database")

        # Read the uploaded image
        image_bytes = await file.read()

        # Generate embedding for the uploaded image
        input_embedding = generate_embedding(image_bytes)

        # Fetch all stored embeddings from the database
        all_embeddings = fetch_all_embeddings(connection)
        if not all_embeddings:
            raise HTTPException(status_code=404, detail="No embeddings found")

        # Find the closest match based on embedding comparison
        min_distance = float('inf')
        matched_user_id = None

        for user_id, stored_embedding in all_embeddings:
            stored_embedding = np.frombuffer(stored_embedding)  # Convert from binary
            distance = np.linalg.norm(input_embedding - stored_embedding)

            if distance < min_distance:
                min_distance = distance
                matched_user_id = user_id

        # Define a matching threshold (tweak this based on your testing)
        threshold = 0.5

        # Check if the match is valid based on the threshold
        if min_distance < threshold:
            # Fetch user information
            user_info = fetch_user_by_id(connection, matched_user_id)
            if not user_info:
                raise HTTPException(status_code=404, detail="User not found")

            return {
                "status": "User found",
                "user_info": {
                    "id": user_info[0],
                    "name": user_info[1],
                    "email": user_info[2],
                    "age": user_info[3]
                }
            }
        else:
            raise HTTPException(status_code=404, detail="No matching user found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")