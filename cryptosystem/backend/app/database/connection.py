from motor.motor_asyncio import AsyncIOMotorClient
import urllib.parse
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
import os

load_dotenv()
username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

MONGO_URI = f"mongodb+srv://{username}:{password}@cryptosystem.q66ty3n.mongodb.net/?retryWrites=true&w=majority&appName=Cryptosystem"
CLIENT_DATABASE = "client"
APPLICATION_DATABASE = "application"
client = AsyncIOMotorClient(
    MONGO_URI,
    server_api=ServerApi('1'),
)

client_db = client[CLIENT_DATABASE]
application_db = client[APPLICATION_DATABASE]