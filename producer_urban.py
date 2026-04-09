import requests
import pika
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = {
    "Milano": {"lat": 45.4642, "lon": 9.1900},
    "Parigi": {"lat": 48.8566, "lon": 2.3522},
    "Londra": {"lat": 51.5074, "lon": -0.1278},
    "Pechino": {"lat": 39.9042, "lon": 116.4074}
}

def get_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            # QUESTO TI DIRÀ COSA NON VA
            print(f"❌ Errore API per {lat},{lon}: Stato {r.status_code} - {r.text}")
            return None
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
        return None

print("🚀 Urban Pulse Producer avviato.")

while True:
    try:
        # Apriamo la connessione solo quando serve
        credentials = pika.PlainCredentials('user', 'password')
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='urban_air_quality')

        for city, coords in CITIES.items():
            data = get_air_quality(coords['lat'], coords['lon'])
            if data:
                payload = {
                    "city": city, "lat": coords['lat'], "lon": coords['lon'],
                    "aqi": data['list'][0]['main']['aqi'],
                    "components": data['list'][0]['components']
                }
                channel.basic_publish(exchange='', routing_key='urban_air_quality', body=json.dumps(payload))
                print(f"✅ Inviato: {city}")
        
        # Chiudiamo la connessione prima dell'attesa lunga
        connection.close()
        print("--- Ciclo completato. In attesa di 10 minuti... ---")
        time.sleep(600)

    except Exception as e:
        print(f"❌ Errore: {e}. Riprovo tra 30 secondi...")
        time.sleep(30)