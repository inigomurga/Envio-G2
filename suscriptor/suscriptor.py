import paho.mqtt.client as mqtt
import ssl
import sys

BROKER = "mosquitto_broker"
PORT = 8883

def on_message(client, userdata, msg):
    print(f"Recibido: {msg.payload.decode()} en el tema {msg.topic}")

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["salon", "cocina"]:
        print("Uso: python suscriptor.py <salon|cocina>")
        sys.exit(1)

    topic = f"casa/{sys.argv[1]}"  # casa/salon o casa/cocina

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.tls_set(
        ca_certs="certs/ca.crt",
        certfile="certs/client.crt",
        keyfile="certs/client.key",
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(topic)

    print(f"Suscrito a {topic}. Esperando mensajes...")
    client.loop_forever()

if __name__ == "__main__":
    main()
