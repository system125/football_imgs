from dataclasses import dataclass

@dataclass
class LeagueInfo:
    name:str
    country:str 
    logo_url:str

@dataclass
class Teams:
    short_name:str
    name:str 
    logo_url:str 