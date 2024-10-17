from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
    image: bytes  # Image sent from the Flutter app (base64 encoded)