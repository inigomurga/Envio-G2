import paho.mqtt.client as mqtt
import ssl
import time
import random

BROKER = "mosquitto_broker"
PORT = 8883
TOPIC_SALON = "casa/salon"
TOPIC_COCINA = "casa/cocina"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.tls_set(
    ca_certs="certs/ca.crt",
    certfile="certs/client.crt",
    keyfile="certs/client.key",
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)
client.connect(BROKER, PORT, 60)

while True:
    temp_salon = round(random.uniform(18.0, 30.0), 2)
    temp_cocina = round(random.uniform(18.0, 30.0), 2)

    client.publish(TOPIC_SALON, f"Temperatura salón: {temp_salon}°C")
    print(f"Publicado en {TOPIC_SALON}: {temp_salon}°C")

    client.publish(TOPIC_COCINA, f"Temperatura cocina: {temp_cocina}°C")
    print(f"Publicado en {TOPIC_COCINA}: {temp_cocina}°C")

    time.sleep(5)
