FROM python:3.9
WORKDIR /app
COPY suscriptor.py .
RUN pip install paho-mqtt
CMD ["python", "suscriptor.py", "salon"]
 
