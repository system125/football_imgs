from typing import List
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import api
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time 
import model
from bs4 import BeautifulSoup
import svg_tools
import cache_request

def sleep_after_call(sleep_time:float=1.0):
    def sleepy_call_decor(func,sleep_time:float=1.0):
        """
        Calls the function and 
        then sleeps for 2 secon
        """

        def wrapper(*args,**kwargs):
            """
            Wrapper functions:
            """
            res = func(*args,**kwargs)

            time.sleep(sleep_time)

            return res
        return wrapper
    return sleepy_call_decor


@sleep_after_call()
def get_team_svg(team:str)->str | None:
    """
    Gets in team svg string and 
    returns the link to that svg resources
    """

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    options.add_experimental_option('excludeSwitches',["enable-logging"])
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver,10) #type: ignore

    driver.get(f"https://worldvectorlogo.com/search/{team}")

    
    time.sleep(2)
    html = driver.page_source

    img = driver.find_element('css selector','.logo__img')
    src = img.get_attribute('src')

    return src


def load_svg(team:model.Teams,league:str)->str | None:


    # soup = BeautifulSoup(response,"html.parser") #type: ignore

    # svg =  str(soup.find("svg"))
    # svg = svg_tools._ensure_svg_dimensions(svg_content=svg,width=210,height=210)
    
    direc = os.path.join("assets",league,"orig")
    os.makedirs(direc,exist_ok=True)
    file_name = f"{team.short_name}.svg"
    file = os.path.join(direc,file_name)

    if not os.path.exists(file):
        team_link = get_team_svg(f"{team.name} FC")
        response = requests.get(team_link).content #type: ignore
        with open(file,'wb') as f:
            f.write(response)

    return file

def gen_team_outline(team:model.Teams,league:str,refresh = False)-> str | None:
    direc = os.path.join("assets",league,"outline")
    os.makedirs(direc,exist_ok=True)
    file_name = f"{team.short_name}.svg"
    file = os.path.join(direc,file_name)
    
    if not os.path.exists(file) or refresh:
        logo_url = load_svg(team=team,league=league)
        with open(team.logo_url,'r') as f:
            svg = f.read()
        
        outline = svg_tools.extract_outline_svg(svg)

        with open(file,'w') as f:
            f.write(outline)
    return file

def map_teams_srcs(teams:List[model.Teams],league:str)->List[model.Teams]: # type: ignore
    for team in teams:
        file_path = load_svg(team,league=league)
        team.logo_url = file_path if file_path else ""
    return teams

def map_team_outlines(teams:List[model.Teams],league:str,refresh:bool=False)->List[model.Teams]:
    for team in teams:
        file_path = gen_team_outline(team=team,league=league,refresh=refresh)

        team.logo_url = file_path if file_path else ""
    return teams




if __name__=="__main__":



    import api 

    id = 47
    league_data = api.get_league_info(id = id )
    teams = api.get_teams_for_league(id = id)
    teams = map_teams_srcs(teams,league_data.name)
    teams_outline = map_team_outlines(teams,league_data.name) # type: ignore







