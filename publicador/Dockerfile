FROM python:3.9
WORKDIR /app
COPY publicador.py .
RUN pip install paho-mqtt
CMD ["python", "publicador.py"]
