# Reto Envío Seguro

**Iñigo Murga, Mikel García y Jon Cañadas**

## Explicación

Este proyecto es un reto de envío de mensajes mediante MQTT de forma segura. Incluye dos formas: la primera forma es un script suscriptor.py para escuchar los mensajes y un script publicador.py para enviar los mensajes y la segunda forma es suscribirse y publicar el mensaje mediante comandos. Para la realización hemos seguido los siguientes pasos:

1. Diseño del docker-compose sin seguridad

Para el diseño del docker-compose hemos tenido en cuenta las características más importantes que hemos considerado. Incluyendo tres contenedores.

2. Diseño del archivo mosquitto.conf sin seguridad

Para el diseño del mosquitto.conf incluimos las características necesarias.

3. Comprobar el funcionamiento de los envios 

Tras construir y lanzar los contenedores, introducimos los comandos necesarios para asegurar el correcto funcionamiento de la comunicación.

4. Desarrollo de los scripts python 

Al saber que la comunicación es correcta, desarrollamos el código de los scripts para lograr la automatización de la suscripción y publicación de los mensajes.

5. Realizar todas las configuraciones para la seguridad

Una vez que el proyecto sin seguridad está completo, procedemos a configurar todos los archivos necesarios para obtener la seguridad, además de generar todos los certificados necesarios.  

## Instalación

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/inigomurga/Envio-G2.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd Envio-G2
    ```
3. Construir y lanza los contenedores Docker:
    ```bash
    docker-compose up -d
    ```

## Uso

1. Mensajes mediante scripts:

    Publicador:
    ```bash
    docker exec -it mqtt_publicador sh 
    ```
    ```python
    python publicador.py
    ```
    Suscriptor:
    ```bash
    docker exec -it mqtt_suscriptor sh
    ```
    ```python
    python suscriptor.py salon
    ```
    ```python
    python suscriptor.py cocina
    ```
    
2. Mensajes mediante comandos:
    ```bash
    mosquitto_sub -h mosquitto_broker -p 8883 --cafile /mosquitto/config/certs/ca.crt \ --cert /mosquitto/config/certs/client.crt --key /mosquitto/config/certs/client.key \ -t casa/salon -d  
    ```

    ```bash
    mosquitto_pub -h mosquitto_broker -p 8883 --cafile /mosquitto/config/certs/ca.crt \ --cert /mosquitto/config/certs/client.crt --key /mosquitto/config/certs/client.key \ -t casa/salon -m "Temperatura salón: 25°C" -d
    ```
    
## Configuración de Docker Compose

Aquí está la configuración de Docker Compose:

```yaml
services:
  mosquitto_broker:
    image: eclipse-mosquitto:latest # Imagen de mosquitto como broker 
    container_name: mosquitto_broker # Nombre del contenedor
    restart: always # Política de reinicio
    ports: # Mapeo de puertos
      - "1883:1883" # Puertos específicos, el primero es en referencia al puerto local y el segundo al del contenedor de Docker 
      - "8883:8883"
    volumes: # Volumen para la persistencia de datos
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
      - ./mosquitto/certs:/mosquitto/certs
    networks: # Definición de red personalizada para que los contenedores puedan utilizar
      - mqtt_network

  publicador:
    build: ./publicador #Definición de como se construye la imagen
    container_name: mqtt_publicador # Nombre del contenedor
    depends_on: # El servicio va a depender del contenedor que se especifique
      - mosquitto_broker # Contenedor del que depende
    networks:
      - mqtt_network
    volumes: # Volumen para la persistencia de datos
      - ./mosquitto/config/certs:/app/certs

  suscriptor:
    build: ./suscriptor #Definición de como se construye la imagen
    container_name: mqtt_suscriptor # Nombre del contenedor
    depends_on: # El servicio va a depender del contenedor que se especifique
      - mosquitto_broker # Contenedor del que depende
    networks: # Definición de red personalizada para que los contenedores puedan utilizar
      - mqtt_network
    volumes: # Volumen para la persistencia de datos
      - ./mosquitto/config/certs:/app/certs

networks: # Definición de red personalizada para que los contenedores puedan utilizar
  mqtt_network:
    driver: bridge #Tipo de red que se utiliza, comentando que los contenedores estan en el mismo host

```

## Posibles vías de mejora

Para mejorar el reto hemos pensado en el desarrollo de una página web en la que se ejecute de forma más visual el proyecto. Sin embargo, no hemos llegado a conseguir desarrollarlo.

## Problemas / Retos encontrados

Al principio del reto, tenemos un planteamiento erróneo de la ejecución del proyecto los que nos resultó un una mayor demora de tiempo en la realización.

A su vez, a la hora de desarrollar la seguridad con certificados hemos tenido múltiples problemas tanto de configuración como de permisos lo que nos ha desesperado, pero finalmente se ha logrado.

## Alternativas posibles

Implementar una seguridad de forma diferente, como la introducción de credenciales en los clientes para diferenciarlos en la verificación de los mensajes.

Usar una base de datos externa para el almacenamiento de datos.
