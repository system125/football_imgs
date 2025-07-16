
from dataclasses import dataclass
from dotenv import load_dotenv
import os 
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
API_URL = os.getenv("API_URL")

Auth_headers = {
    "x-rapidapi-key":API_KEY,
    "x-rapidapi-host":API_HOST
}



@dataclass
class LeagueInfo:
    name:str
    country:str 
    logo_url:str

def get_league_info(id:int):
    """
    Loads league roster from api 
    and returns the roster
    """

    querystring={"leagueid":f"{id}"}
    if API_URL:
        response = requests.get(
                        f"{API_URL}/football-get-league-detail",
                        headers=Auth_headers,
                        params=querystring
                        )
        logo_response = requests.get(
            f"{API_URL}/football-get-league-logo",
            headers=Auth_headers,
            params=querystring
        )
        if response.status_code != 200 or logo_response.status_code != 200:
            raise Exception("Error!! Loading league data!")
        league_data = response.json()["response"]["leagues"]

        name = league_data["name"]
        country = league_data["country"]
        logo = logo_response.json()['response']['url']

        return LeagueInfo(
            name=name,
            country=country,
            logo_url=logo
        )
        
        
        

        
