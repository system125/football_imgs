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
from svgpathtools import Path
import xml.etree.ElementTree as ET
from svgoutline import svg_to_outlines
from bs4 import BeautifulSoup
from svgpathtools import svg2paths
from io import StringIO
import math
import re
import svg_tools

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

def load_svg(src:str)->str | None:
    response = requests.get(src).text

    soup = BeautifulSoup(response,"html.parser") #type: ignore

    return str(soup.find("svg"))


if __name__=="__main__":

    team_svg = get_team_svg("chelsea")
    print(f"svg site: {team_svg}")

    response_svg = load_svg(team_svg) #type: ignore

    with open("assets/original.svg",'w') as f:
        f.write(response_svg) #type: ignore
    
    outlines = svg_tools.extract_outline_svg(response_svg) #type: ignore
    print(outlines)
    with open("assets/outlines.svg",'w') as f:
        f.write(outlines)
    


