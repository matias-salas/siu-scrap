#%%
import requests
from bs4 import BeautifulSoup
import json

url = "https://guarani.unsam.edu.ar/cyt_alumnos/acceso"

def get_links(url):
    response = requests.get(url)
    # Obtengo el html de la pagina
    soup = BeautifulSoup(response.text, 'html.parser')
    # Busco todos los tags <script>
    script_tags = soup.find_all('script')

    for script_tag in script_tags: # Recorro todos los tags <script>
        try:
            # Si el tag <script> tiene el atributo type="text/javascript" y comienza con "kernel.renderer.on_arrival"
            if script_tag['type'] == 'text/javascript' and script_tag.string.startswith('kernel.renderer.on_arrival'):
                # Obtengo el contenido del tag <script>
                if "cartelera" in script_tag.string: # Si el contenido del tag <script> contiene la palabra "cartelera" (que es lo que busco)
                    # Como se que dentro de ese tag <script> esta el contenido que quiero, lo parseo como json
                    load = json.loads(script_tag.string[script_tag.string.find("(")+1:script_tag.string.rfind(")")])
                    # Obtengo el valor de la clave "content"
                    content = load['content']
                    # Parseo el contenido como html, ya que es un html
                    content_soup = BeautifulSoup(content, 'html.parser')
                    # Busco todos los tags <a>
                    a_tags = content_soup.find_all('a')
                    # Imprimo los href de los tags <a>
                    return a_tags # Devuelvo los tags <a>
        except:
            pass

links = get_links(url)
for link in links:
    print(link['href'])

