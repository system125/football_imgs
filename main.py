
import api 
import webview
from jinja2 import Environment, FileSystemLoader
import os 
import api 
import get_svg
env = Environment(loader=FileSystemLoader('templates'))
import model

with open("styles/styles.css") as f:
    css = f.read()
    f.close()

print(f"{css}")

id = 47
league_data = api.get_league_info(id = id )
teams = api.get_teams_for_league(id = id)
template = env.get_template("index.jinja2")

teams = get_svg.map_team_outlines(teams,league_data.name)
html = template.render(
    title=league_data.name, #type: ignore
    header="Welcome to A4 Page",
    custom_css=css,
    league_img=league_data.logo_url, #type: ignore
    teams = teams #type: ignore

)

print(html)
with open("test.html",'w') as f:
    f.writelines(html)
    f.close()

webview.create_window("Preview",html=html)
webview.start()