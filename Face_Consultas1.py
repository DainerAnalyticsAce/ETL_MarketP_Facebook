import time
import pandas as pd
from bs4 import BeautifulSoup as bs
import random
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import requests
import csv
import re


# 1. Importar las librerías
# Ya importadas en el entorno Python

opciones = Options()
#Enviar argumento
# 1 para aceptar ; 2 para bloquear
opciones.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications" : 2
})


driver = webdriver.Chrome(options=opciones)  # 4. Inicializar el driver de Selenium
#Vamos abrir primera pestaña
driver.get("https://www.google.com/")
time.sleep(3)

#Agregamos la ruta del webdriver - ABRIR SEGUNDA PESTAÑA
driver.execute_script("window.open('about:blank','secondtab');")
driver.switch_to.window("secondtab")
driver.get("https://www.facebook.com/")
driver.implicitly_wait(10)
time.sleep(5)

#Moverse a la primera pestaña que es google
driver.switch_to.window(driver.window_handles[0])
driver.refresh()
time.sleep(5)

#Moverse a la segunda pestaña que es facebook
driver.switch_to.window(driver.window_handles[1])
driver.refresh()
time.sleep(3)

#Vamos abrir el navegador en grande
driver.maximize_window()


#Creamos la variable para llamar a la ruta del NAME
usuario = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'email')))
for i in "Correo de Facebook Escrito":
	usuario.send_keys(i)
	time.sleep(1+random.random())


##PARA INGRESAR LA CLAVE
clave = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'pass')))
for i in "Clave de Facebook Escrito":
	clave.send_keys(i)
	time.sleep(1+random.random())

time.sleep(2) #Le damos dos segundos antes de iniciar sesión
clave.send_keys(Keys.ENTER) #Presionar enter desde el campo contraseña
time.sleep(5)


#######PASO 2####################

time.sleep(3)
driver.get("https://www.facebook.com/")

time.sleep(3)
#######PASO 3####################

#IRNOS A MARKEPLACE
Ciudad = "bucaramanga"
driver.get("https://www.facebook.com/marketplace/"+Ciudad)
time.sleep(3)

################################################################
#Vamos a consultar lo que deseamos buscar
# Ingresamos a Markeplace
# Encontrar el campo de búsqueda
campo_busqueda = driver.find_element(By.XPATH, '//input[@aria-label="Search Marketplace"]')
# Texto a buscar
texto_busqueda = "Plataformas Streaming"

# Iterar sobre cada letra del texto
for letra in texto_busqueda:
    # Ingresar la letra en el campo de búsqueda
    campo_busqueda.send_keys(letra)
    # Esperar un tiempo aleatorio entre 1 y 2 segundos
    time.sleep(1 + random.random())

# Presionar Enter para realizar la búsqueda
campo_busqueda.send_keys(Keys.ENTER)
time.sleep(3)



#Vamos a tomar todo el Html que este#
html = driver.page_source
#print html para saber que tenemos todo
#Organizamos todo lo extraido para tener la información
soup = bs(html, 'lxml')

#print(soup)
#time.sleep(3)
#####################################################################
# Lista para almacenar los enlaces href
enlaces_href = []

divs_x3ct3a4 = soup.find_all('div', class_='xkrivgy x1gryazu x1n2onr6')


# Iterar sobre los divs encontrados
for div in divs_x3ct3a4:
    # Encontrar todas las etiquetas <a> dentro de cada div
    enlaces = div.find_all('a')
    
    # Obtener los enlaces href, limpiarlos y almacenarlos
    for enlace in enlaces:
        href = enlace.get('href')
        # Realizar la limpieza de datos para conservar solo la parte del enlace deseada
        enlace_limpio = re.search(r'\/marketplace\/item\/\d+', href)
        if enlace_limpio:
            enlace_completo = "https://www.facebook.com/" + enlace_limpio.group()
            enlaces_href.append(enlace_completo)


#print(enlaces_href)
#####################################################################
# Lista para almacenar los precios
precios = []
divs_padre = soup.find_all('div', class_='xkrivgy x1gryazu x1n2onr6')

# Iterar sobre los divs de la clase padre
for div_padre in divs_padre:
    # Encontrar todos los elementos span con la clase x193iq5w dentro de la clase padre
    divs_precio = div_padre.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u')
    # Iterar sobre los divs de precios dentro de la clase padre
    for div in divs_precio:
        # Obtener el texto del precio y limpiarlo
        precio_texto = div.get_text(strip=True)
        # Limpiar el texto del precio eliminando el símbolo "$" y los espacios en blanco
        precio_limpio = re.sub(r'\$|\s', '', precio_texto)
        # Agregar el precio limpio a la lista de precios
        precios.append(precio_limpio)

#print(precios)
#####################################################################

# Lista para almacenar los textos
textos = []
divs_padre = soup.find_all('div', class_='xkrivgy x1gryazu x1n2onr6')

# Iterar sobre los divs de la clase padre
for div_padre in divs_padre:
    # Encontrar todos los elementos span con la clase específica dentro de la clase padre
    divs_texto = div_padre.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
    # Iterar sobre los divs de texto dentro de la clase padre
    for div_texto in divs_texto:
        # Obtener el texto del elemento span y agregarlo a la lista de textos
        texto = div_texto.get_text(strip=True)
        # Reemplazar caracteres con tilde por sus equivalentes sin tilde
        texto_sin_tilde = unidecode(texto)
        # Agregar el texto a la lista de textos
        textos.append(texto_sin_tilde)

#print(textos)
#####################################################################


# Lista para almacenar todas las ciudades
ciudades = []
divs_padre = soup.find_all('div', class_='xkrivgy x1gryazu x1n2onr6')

# Iterar sobre los divs de la clase padre
for div_padre in divs_padre:
    # Encontrar todos los elementos de ciudad dentro de cada div padre
    ciudades_div = div_padre.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')
    # Iterar sobre todas las ciudades encontradas en el div actual
    for ciudad in ciudades_div:
        # Obtener el texto de la ciudad, quitar las tildes y agregarlo a la lista de ciudades
        ciudad_texto = unidecode(ciudad.get_text(strip=True))
        ciudades.append(ciudad_texto)


#####################################################################

# Lista para almacenar las URLs de las imágenes
#imagenes = []
#divs_padre = soup.find_all('div', class_='xkrivgy x1gryazu x1n2onr6')

# Iterar sobre los divs de la clase padre
#for div_padre in divs_padre:
#    # Encontrar todas las etiquetas <img> dentro de la clase padre
#    imagenes_div = div_padre.find_all('img')
#    # Iterar sobre todas las imágenes encontradas en el div actual
#    for imagen in imagenes_div:
#        # Obtener la URL de la imagen y agregarla a la lista de imágenes
#        url_imagen = imagen.get('src')
#        if url_imagen:  # Verificar si la URL de la imagen no es nula
#            imagenes.append(url_imagen)

###################################################
###################################################


# Crear un diccionario con los datos y sus respectivos nombres de hoja
datos_por_hoja = {
    "Enlaces_Href": enlaces_href,
    "Precios": precios,
    "Textos": textos,
    "Ciudades": ciudades
    #"Imagenes": imagenes
}

# Crear un objeto ExcelWriter para escribir en un archivo CSV
with pd.ExcelWriter('datos_Marke_facebook.xlsx') as writer:
    # Iterar sobre cada par (nombre de hoja, datos) en el diccionario
    for nombre_hoja, datos in datos_por_hoja.items():
        # Convertir los datos en un DataFrame de pandas
        df = pd.DataFrame(datos, columns=[nombre_hoja])
        # Escribir el DataFrame en una hoja del archivo CSV
        df.to_excel(writer, index=False, sheet_name=nombre_hoja)