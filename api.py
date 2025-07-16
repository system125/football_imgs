
from dataclasses import dataclass
from dotenv import load_dotenv
import os 
import requests
from cache_request import cache_by_id
import model 

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
API_URL = os.getenv("API_URL")

Auth_headers = {
    "x-rapidapi-key":API_KEY,
    "x-rapidapi-host":API_HOST
}

@cache_by_id(model.LeagueInfo)
def get_league_info(id:int):
    """
    Loads league roster from api 
    and returns the roster
    """
    print("Made a request!")

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

        return  model.LeagueInfo(
            name=name,
            country=country,
            logo_url=logo
        )
        
@cache_by_id(model.Teams)      
def get_teams_for_league(id:int):
    print("Made a request!")
    querystring = {"leagueid":f"{id}"}

    response = requests.get(
        f"{API_URL}/football-get-list-all-team",
                headers=Auth_headers,
                params=querystring
    )

    if response.status_code != 200:
        raise Exception("Error! Loading stuff!")
    
    teams = response.json()["response"]["list"]
    team_return = []

    for team in teams:
        team_return.append(
            model.Teams(
                short_name=team["shortName"],
                name=team["name"],
                logo_url=team["logo"]
            )
        )
    return team_return

   
