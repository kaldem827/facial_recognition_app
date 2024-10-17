import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 5))  # Default pool size is 5

# Create a global connection pool using credentials from .env
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=DB_POOL_SIZE,  # Number of connections in the pool
    pool_reset_session=True,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    # auth_plugin='caching_sha2_password'
)

# Function to get a connection from the pool
def get_connection():
    try:
        connection = connection_pool.get_connection()
        return connection
    except Error as e:
        print(f"Error getting connection: {e}")
        return None

# Function to insert a new user into the 'users' table
def insert_user(connection, name, email, age):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, age))
        connection.commit()
        return cursor.lastrowid  # Return the user ID of the newly added user
    except Error as e:
        print(f"Error inserting user: {e}")
        return None

# Function to insert a user's face embedding into the 'embeddings' table
def insert_embedding(connection, user_id, embedding):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO embeddings (user_id, embedding) VALUES (%s, %s)"
        cursor.execute(query, (user_id, embedding))
        connection.commit()
        return True
    except Error as e:
        print(f"Error inserting embedding: {e}")
        return False

# Function to fetch all embeddings from the 'embeddings' table
def fetch_all_embeddings(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, embedding FROM embeddings")
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching embeddings: {e}")
        return []

# Function to fetch user information by user_id
def fetch_user_by_id(connection, user_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching user: {e}")
        return None
