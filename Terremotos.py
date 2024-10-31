import tkinter as tk
import requests
from datetime import datetime

def fetch_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
    result_label.config(text="Cargando...")  # Mensaje de carga
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if response.content:
            data = response.json()
            
            if data.get('features'):
                events = data['features'][:5]  # Muestra los primeros 5 eventos
                result_text = ""
                for event in events:
                    properties = event['properties']
                    time = datetime.fromtimestamp(properties['time'] / 1000)  # Convertir tiempo de Unix a datetime
                    result_text += f"Magnitud: {properties['mag']}, Lugar: {properties['place']}, Fecha y Hora: {time}\n\n"
                
                result_label.config(text=result_text)
            else:
                result_label.config(text="No se encontraron eventos.")
        else:
            result_label.config(text="Respuesta vacía.")
    except requests.exceptions.ConnectionError:
        result_label.config(text="Error de conexión. Verifica tu Internet.")
    except requests.exceptions.Timeout:
        result_label.config(text="La solicitud ha caducado.")
    except requests.exceptions.JSONDecodeError:
        result_label.config(text="Error al decodificar la respuesta JSON.")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error: {e}")

def fetch_earthquake_data(start_date, end_date):
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('features'):
            result_text = ""
            events = data['features'][:5]  # Muestra hasta los primeros 5 eventos
            for event in events:
                properties = event['properties']
                time = datetime.fromtimestamp(properties['time'] / 1000)
                result_text += f"Magnitud: {properties['mag']}, Lugar: {properties['place']}, Fecha y Hora: {time}\n\n"
            
            earthquake_label.config(text=result_text)
        else:
            earthquake_label.config(text="No se encontraron eventos para los parámetros especificados.")
    except requests.exceptions.ConnectionError:
        earthquake_label.config(text="Error de conexión. Verifica tu Internet.")
    except requests.exceptions.Timeout:
        earthquake_label.config(text="La solicitud ha caducado.")
    except requests.exceptions.JSONDecodeError:
        earthquake_label.config(text="Error al decodificar la respuesta JSON.")
    except requests.exceptions.RequestException as e:
        earthquake_label.config(text=f"Error: {e}")

def fetch_event_count(min_magnitude):
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&minmagnitude={min_magnitude}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        count = data.get('count', 0)
        count_label.config(text=f"Total de eventos de terremotos con magnitud mínima {min_magnitude}: {count}")
    except requests.exceptions.ConnectionError:
        count_label.config(text="Error de conexión. Verifica tu Internet.")
    except requests.exceptions.Timeout:
        count_label.config(text="La solicitud ha caducado.")
    except requests.exceptions.JSONDecodeError:
        count_label.config(text="Error al decodificar la respuesta JSON.")
    except requests.exceptions.RequestException as e:
        count_label.config(text=f"Error: {e}")

def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Terremotos por Fechas")
    new_window.geometry("400x550")
    
    tk.Label(new_window, text="Fecha de Inicio (AAAA-MM-DD):").pack(pady=5)
    start_date_entry = tk.Entry(new_window)
    start_date_entry.pack(pady=5)

    tk.Label(new_window, text="Fecha de Fin (AAAA-MM-DD):").pack(pady=5)
    end_date_entry = tk.Entry(new_window)
    end_date_entry.pack(pady=5)

    global earthquake_label
    earthquake_label = tk.Label(new_window, text="Resultados aparecerán aquí", justify="left", wraplength=350)
    earthquake_label.pack(pady=10)

    search_button = tk.Button(new_window, text="Buscar Terremotos", command=lambda: fetch_earthquake_data(start_date_entry.get(), end_date_entry.get()))
    search_button.pack(pady=10)

def open_count_window():
    count_window = tk.Toplevel(root)
    count_window.title("Conteo de Terremotos por Magnitud")
    count_window.geometry("400x300")
    
    tk.Label(count_window, text="Magnitud Mínima:").pack(pady=10)
    min_magnitude_entry = tk.Entry(count_window)
    min_magnitude_entry.pack(pady=5)

    global count_label
    count_label = tk.Label(count_window, text="Resultados aparecerán aquí", justify="left", wraplength=350)
    count_label.pack(pady=20)

    search_button = tk.Button(count_window, text="Buscar Conteo de Terremotos", command=lambda: fetch_event_count(min_magnitude_entry.get()))
    search_button.pack(pady=10)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Aplicación de Terremotos")
root.geometry("400x600")
root.resizable(False, False)

# Título de la ventana principal
title_label = tk.Label(root, text="Terremotos", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Resultado de la búsqueda inicial
result_label = tk.Label(root, text="Resultados aparecerán aquí", justify="left", wraplength=350)
result_label.pack(pady=20)

# Botón para obtener datos de terremotos
fetch_button = tk.Button(root, text="Obtener Datos de Terremotos", command=fetch_data)
fetch_button.pack(side="bottom", pady=10)

# Botón para abrir la ventana secundaria de búsqueda
open_window_button = tk.Button(root, text="Abrir Ventana de Búsqueda de Terremotos", command=open_new_window)
open_window_button.pack(side="bottom", pady=10)

# Botón para abrir la ventana de conteo de terremotos
open_count_window_button = tk.Button(root, text="Abrir Ventana de Conteo de Terremotos", command=open_count_window)
open_count_window_button.pack(side="bottom", pady=10)

root.mainloop()
