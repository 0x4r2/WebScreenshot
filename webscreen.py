#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import json
import subprocess as sp
import pandas as pd
import requests
from datetime import datetime
import warnings

## nivel de alertas
warnings.filterwarnings("ignore")

# Variables personalizadas
URL = ""   #Edit This
WINDOW_SIZE = "1920,1080"
#CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'  # Ajusta la ruta del controlador de Chrome según tu sistema
## descargar version actualizada del driver http://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y/%m/%d at %H:%M:%S")

# Configuración de directorios
localpath = sp.getoutput('pwd')
output_dir = "WebScreen/"
os.makedirs(output_dir, exist_ok=True)
img_dir = os.path.join(localpath, output_dir, "img")
os.makedirs(img_dir, exist_ok=True)


# Configuración de opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')

# Inicializar el controlador de Chrome
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# Obtener información de la página web
titulo = driver.title
current_url = driver.current_url
driver.save_screenshot("WebScreen/img/web.png")
driver.close()

# Realizar una solicitud web para obtener información adicional
res = requests.get(current_url,verify=False)
status = res.status_code
headers = res.headers
code = res.text
formatted_headers = "<br>".join([f"{key}: {value}" for key, value in headers.items()])


# Crear el formato HTML del informe
web_head = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
  <title>WebScreenshotReport</title></head><body><center><h2>Screenshots</h2>'''

web_foot = '</table></div><p>Powered by 4r2-webscreenshot-2023®</p</center></body></html>'

timestamp = f'<p>Report Generated on {formatted_datetime}</p>' 

tablas = f'''
<div style="width:90%;">
<table border="1" class="table table-bordered text-wrap">
<tr >
    <th class="w-25 table-dark">Web Request Info</th>
    <th class="w-75 table-dark">Web Screenshot</th>
</tr>
<tr>
    <td>
        <div style="display: inline-block; width: 300; word-wrap: break-word">
            <br><b>Titulo:</b> {titulo}
            <br><b>URL:</b><a href={current_url} target="_blank">{current_url} </a>
            <br><b>Status Code:</b> {status}
            <br>
            <br><b>Headers:</b>{formatted_headers}
            <br> 
            <br>
            <br><a href="web.txt" target="_blank">Source Code</a>
            <br>
        </div>
    </td>
    <td class="align-middle">
        <div id="screenshot"><a href="img/web.png" target="_blank">
        <img src="img/web.png" width="100%"></a></div>
    </td>
</tr>''' 

# Guardar el archivo HTML
datos = web_head + timestamp+ tablas + web_foot
with open(os.path.join(output_dir, "result.html"), 'w') as f:
    f.write(datos)
    f.close()

# Guardar sourcecode
with open(os.path.join(output_dir, "web.txt"), 'w') as f:
    f.write(code)
    f.close()

print("Escaneo y generación de informe completados. Los resultados se han guardado en el directorio 'WebScreen'.")
