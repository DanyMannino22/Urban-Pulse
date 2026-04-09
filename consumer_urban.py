import pika
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Configurazione InfluxDB (Controlla che i dati siano uguali ai tuoi)
token = "my-super-secret-token"
org = "my-org"
bucket = "urban_air_data" # Crea questo bucket su InfluxDB prima di partire!
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"📥 Ricevuto dato per: {data['city']}")

    # Creiamo il punto per InfluxDB con coordinate GPS
    point = Point("air_quality") \
        .tag("city", data['city']) \
        .field("aqi", float(data['aqi'])) \
        .field("pm10", float(data['components']['pm10'])) \
        .field("co", float(data['components']['co'])) \
        .field("no2", float(data['components']['no2'])) \
        .field("latitude", data['lat']) \
        .field("longitude", data['lon'])

    write_api.write(bucket=bucket, org=org, record=point)
    print(f"✅ Archiviato {data['city']} su InfluxDB")

# Setup RabbitMQ
# Definiamo le credenziali
credentials = pika.PlainCredentials('user', 'password')

# Colleghiamoci usando quelle credenziali
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue='urban_air_quality')

channel.basic_consume(queue='urban_air_quality', on_message_callback=callback, auto_ack=True)

print('[*] In attesa di dati. Per uscire premi CTRL+C')
channel.start_consuming()