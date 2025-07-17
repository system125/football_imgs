from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import api

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



team_name = "liverpool"
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver,10) # type: ignore
driver.get(f"https://worldvectorlogo.com/search/{team_name}")



html = driver.page_source
img = driver.find_element('css selector','.logo__img')
src = img.get_attribute('src')
print(src)

import requests 
import cv2 
import numpy as np
response = requests.get(src) #type: ignore
svg_content = response.content

with open("temp.svg",'wb') as f:
    f.write(svg_content)

from svgpathtools import svg2paths
paths, attributes = svg2paths('temp.svg')

import matplotlib.pyplot as plt
from svgpathtools import Path

for path in paths:
    for segment in path:
        # Sample points along the segment to plot the curve
        num_points = 100  # adjust for smoothness
        pts = [segment.point(t) for t in [i/num_points for i in range(num_points+1)]]
        xs = [pt.real for pt in pts]
        ys = [pt.imag for pt in pts]

        plt.plot(xs, ys, 'k-')

plt.gca().invert_yaxis()  # SVG y-axis is flipped compared to matplotlib
plt.axis('equal')
plt.show()



with open("test.html",'w',encoding="UTF-8") as f:
    f.writelines(html)
    f.close()
