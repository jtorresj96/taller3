#import requests

#def fetch_data_from_api():
#    api_url = f'http://10.43.101.149/data?group_number=4'
#    try:
#        response = requests.get(api_url)
#        response.raise_for_status()  # Esto lanzará un error si el código de estado no es 200
#        data = response.json()
        # Aquí debes decidir qué hacer con los datos: guardarlos en un archivo, en una base de datos, etc.
#        print("Datos recibidos:", data)
#    except Exception as e:
#        print(f"Error al obtener datos de la API: {e}")

import requests

def fetch_data_from_api():
    api_url = 'http://10.43.101.149/data?group_number=4'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        # Aquí puedes procesar los datos como desees
        print("Datos recibidos:", data)
    else:
        print("Error al obtener datos de la API:", response.status_code)

# Ejemplo de uso: Solicitar datos del lote número 1
fetch_data_from_api()
