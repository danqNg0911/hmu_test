import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000
)

db = client[DB_NAME]

async def connect_to_database():
    try:
        await client.admin.command('ping')
        print(f"Connected to MongoDB database: {DB_NAME}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

async def close_database_connection():
    client.close()
    print("Closed the MongoDB database connection")