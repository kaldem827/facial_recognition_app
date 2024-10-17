from fastapi import APIRouter, UploadFile, File, HTTPException

from server.config.db import create_connection, insert_user, insert_embedding
from server.models.user import User
from server.utils.embedding import generate_embedding

add_user_router = APIRouter()

@add_user_router.post("/add-user/")
async def add_user(user: User, file: UploadFile = File(...)):
    try:
        # Create database connection
        connection = create_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Failed to connect to the database")

        # Read the uploaded image
        image_bytes = await file.read()

        # Generate embedding from the uploaded image
        embedding = generate_embedding(image_bytes)

        # Insert user info into the 'users' table
        user_id = insert_user(connection, user.name, user.email, user.age)
        if not user_id:
            raise HTTPException(status_code=500, detail="Failed to add user to the database")

        # Insert the generated embedding into the 'embeddings' table
        success = insert_embedding(connection, user_id, embedding.tobytes())
        if not success:
            raise HTTPException(status_code=500, detail="Failed to add embedding to the database")

        return {"status": "User added successfully", "user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")