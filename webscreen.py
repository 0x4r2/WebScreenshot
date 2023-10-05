#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os, re , sys ,json
import subprocess as sp
import pandas as pd
import requests
from datetime import datetime
import warnings
import argparse
import string
import random


def hide_warn():
    ## nivel de alertas
    warnings.filterwarnings("ignore")

def get_emails(webtext):
    patron = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    lista = re.findall(patron, webtext)
    emails = ''
    for email in lista:
        emails += email + '\n'
    return emails

def get_size(size_web):
    if size_web is None:
        return "1280,720"
    size_web = size_web.lower()
    if 'x' in size_web:
        return size_web.replace('x', ',')
    return  "1280,720"  #"1920,1080"

def get_screenshots(URL):
    # Inicializar el controlador de Chrome
    driver = webdriver.Chrome(service=service,options=chrome_options)
    
    ## Size Personalizado
    #altura_pagina = driver.execute_script("return document.body.scrollHeight")
    #driver.set_window_size(1080, altura_pagina)

    # Obtener información de la página web
    driver.get(URL)
    titulo = driver.title
    current_url = driver.current_url
    image_path=''.join(random.choice(chars) for _ in range(15))
    driver.save_screenshot(f"{output_dir}img/{image_path}.png")
    driver.close()

    # Realizar una solicitud GET para obtener información adicional
    res = requests.get(current_url,verify=False)
    status = res.status_code
    headers = res.headers
    code = res.text
    email_list = get_emails(code)
    formatted_headers = "<br>".join([f"{key}: {value}" for key, value in headers.items()])
    filas = f'''
    <tr>
        <td>
            <div style="display: inline-block; width: 300; word-wrap: break-word">
                <br><b>Titulo:</b> {titulo}
                <br><b>URL: </b><a href={current_url} target="_blank"> {current_url} </a>
                <br><b>Status Code:</b> {status}
                <br><b>Emails Found:</b> {email_list}
                <br>
                <br><b>Headers:</b>{formatted_headers}
                <br> 
                <br>
                <br><a href="{image_path}.txt" target="_blank">Source Code</a>
                <br>
            </div>
        </td>
        <td class="align-middle">
            <div id="screenshot"><a href="img/{image_path}.png" target="_blank">
            <img src="img/{image_path}.png" width="100%"></a></div>
        </td>
    </tr>''' 
    # Guardar sourcecode
    with open(os.path.join(output_dir, f"{image_path}.txt"), 'w') as f:
        f.write(code)
        f.close()

    return filas

def main():
    
    if isinstance(URL, str):
        filas = get_screenshots(URL)
        print(f"Procesando la url: {URL}")
    elif isinstance(URL, list):
        filas = ''
        for url in URL:
            data = get_screenshots(url)
            filas += data
            print(f"Procesando la url: {url}")

    tabla = f'''<div style="width:90%;"><table border="1" class="table table-bordered text-wrap"><tr><th class="w-25 table-dark">Web Request Info</th><th class="w-75 table-dark">Web Screenshot</th></tr>{filas}</table></div>'''


    # Guardar el archivo HTML
    datos = web_head + timestamp+ tabla + web_foot
    base_nombre = "result"
    count = 1
    while True:
        nombre_archivo = f"{base_nombre}{count}.html"
        ruta_archivo = os.path.join(output_dir, nombre_archivo)

        if not os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'w') as f:
                f.write(datos)
                f.close()
            break
        count += 1

    print(f"\nEscaneo y generación de informe completados. Los resultados se han guardado en el directorio: ./WebScreen/{nombre_archivo}")    
    sys.exit()

if __name__ == "__main__":

    print("WebScreenshotReport v1.1 - 0x4r2\n")
    parser = argparse.ArgumentParser(description="Screenshot de una URL o una lista de URLs")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--url", help="URL a procesar")
    group.add_argument("-f", "--file", help="Archivo que contiene una lista de URLs")
    parser.add_argument("-s", "--size", help="(opcional) Tamaño  para la captura de pantalla ejm: 1920x1080")
    args = parser.parse_args()

    if args.url:
        URL = args.url 
    elif args.file:
        try:
            with open(args.file, "r") as file:
                URL = file.read().splitlines()
        except FileNotFoundError:
            print("Error. El archivo no existe.")
            sys.exit()
    else:
        print("Debes proporcionar una URL con -u o una lista de URLs desde un archivo con -f.")
        sys.exit()

    
    # Variables personalizadas
    size_web = args.size if args.size else None
    WINDOW_SIZE = get_size(size_web)
    print(f"Resolución Seleccionada: {WINDOW_SIZE}")
    #CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'  # Ajusta la ruta del controlador de Chrome según tu sistema
    ## descargar version actualizada del driver http://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y/%m/%d at %H:%M:%S")
    chars=string.digits+string.ascii_lowercase
    hide_warn()

    # Configuración de directorios
    localpath = sp.getoutput('pwd')
    output_dir = "WebScreen/"
    os.makedirs(output_dir, exist_ok=True)
    img_dir = os.path.join(localpath, output_dir, "img")
    os.makedirs(img_dir, exist_ok=True)

    # Configuración de opciones de Chromium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-ssl-errors=true')
    chrome_options.add_argument('--ignore-certificate-errors')
    driver="/usr/local/bin/chromedriver"
    service = webdriver.ChromeService(executable_path=driver)


    # Crear el formato HTML del informe
    web_head = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous"><title>WebScreenshotReport</title></head><body><center><h2>Screenshots</h2>'''
    web_foot = '<p>Powered by 4r2-webscreenshot-2023®</p</center></body></html>'
    timestamp = f'<p>Report Generated on {formatted_datetime}</p>' 

    main()