from motor.motor_asyncio import AsyncIOMotorClient
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()
certificate_path = os.getenv("CERTIFICATE_PATH", "../app/certificate.pem")

MONGO_URI = "mongodb+srv://cryptosystem.q66ty3n.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=Cryptosystem"
CLIENT_DATABASE = "client"
APPLICATION_DATABASE = "application"
client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsCertificateKeyFile=certificate_path  
)

client_db = client[CLIENT_DATABASE]
application_db = client[APPLICATION_DATABASE]