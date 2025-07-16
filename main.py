
import api 
import webview
from jinja2 import Environment, FileSystemLoader
import os 

env = Environment(loader=FileSystemLoader('templates'))

id = 47

with open("styles/styles.css") as f:
    css = f.read()
    f.close()

print(f"{css}")
template = env.get_template("index.jinja2")
html = template.render(title="MyApp",header="Welcome to A4 Page",interactive=True,custom_css=css)
print(html)
# with open("test.html",'w') as f:
#     f.writelines(html)
#     f.close()

webview.create_window("Preview",html=html)
webview.start()