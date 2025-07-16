
from dotenv import load_dotenv
import os 

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
API_URL = os.getenv("API_URL")

Auth_headers = {
    "x-rapidapi-key":API_KEY,
    "x-rapidapi-host":API_HOST
}


print(f"{API_KEY}")