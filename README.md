# 🌍 Urban Pulse - Real-time Air Quality Monitor

Sistema di monitoraggio della qualità dell'aria basato su microservizi.

## 🛠️ Architettura
- **Producer (Python)**: Recupera dati da OpenWeather API.
- **Message Broker (RabbitMQ)**: Gestisce lo streaming dei dati.
- **Consumer (Python)**: Elabora e salva i dati.
- **Time-Series DB (InfluxDB)**: Archiviazione ottimizzata.
- **Dashboard (Grafana)**: Visualizzazione geografica real-time.

## 🚀 Come avviarlo
1. Avvia i servizi con Docker: `docker-compose up -d`
2. Installa le dipendenze: `pip install -r requirements.txt`
3. Crea un file `.env` con la tua API Key.
4. Avvia il consumer: `python consumer_urban.py`
5. Avvia il producer: `python producer_urban.py`