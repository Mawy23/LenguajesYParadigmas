import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.parse import urlparse, urljoin
import re

# Función para buscar una palabra en una página
def buscar_palabra(url, palabra):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    texto = soup.get_text()
    return texto.lower().count(palabra.lower())

# URL de la página principal de Marca
url = "https://www.marca.com/"

# Realizar la solicitud HTTP GET a la página principal
response = requests.get(url)

# Parsear el contenido HTML usando BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Encontrar todos los enlaces (href) en la página principal
enlaces = soup.find_all("a")

# Palabra a buscar en los enlaces
palabra_buscar = "profesional"

# Contador de enlaces procesados
contador = 0

# Diccionario para almacenar la frecuencia de la palabra en cada enlace
frecuencia_por_enlace = {}

# Recorrer cada enlace y buscar la palabra en ellos
for enlace in enlaces:
    href = enlace.get("href")
    if href is not None and contador < 10:  # Limitar a 10 enlaces como máximo
        # Construir la URL completa
        enlace_completo = urljoin(url, href)
        
        # Realizar la búsqueda de la palabra en el enlace
        frecuencia = buscar_palabra(enlace_completo, palabra_buscar)
        print(f"Se encontró la palabra '{palabra_buscar}', ({frecuencia} veces) en el enlace:\n{enlace_completo}\n\n")
        frecuencia_por_enlace[enlace_completo] = frecuencia

        contador += 1


# Crear un gráfico de barras de frecuencia de la palabra en cada enlace
enlaces = list(frecuencia_por_enlace.keys())
frecuencias = list(frecuencia_por_enlace.values())

plt.bar(enlaces, frecuencias)
plt.xlabel('Enlaces')
plt.ylabel(f'Frecuencia de "{palabra_buscar}"')
plt.title(f'Frecuencia de "{palabra_buscar}" en Enlaces')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
