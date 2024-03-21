from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
CLIENT_DATABASE = "client"
APPLICATION_DATABASE = "application"

client = AsyncIOMotorClient(MONGO_URI)

client_db = client[CLIENT_DATABASE]
application_db = client[APPLICATION_DATABASE]