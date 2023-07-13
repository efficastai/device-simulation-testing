import time
from random import randint

import paho.mqtt.client as mqtt

from secrets import secrets

devices = [
    {
        "name": "maquina_1",
        "token": secrets.get('maq_1'),
        "broker": secrets.get('broker'),
        "port": secrets.get('port')
    },
    {
        "name": "maquina_2",
        "token": secrets.get('maq_2'),
        "broker": secrets.get('broker'),
        "port": secrets.get('port')
    },
    {
        "name": "maquina_3",
        "token": secrets.get('maq_3'),
        "broker": secrets.get('broker'),
        "port": secrets.get('port')
    },
    # agregar más dispositivos según sea necesario
]


def on_connect(client, userdata, flags, rc):
    print("Connection OK" if rc == 0 else print("Connection FAIL"))


# LOG de conexion
def on_log(client, userdata, level, buf):
    print("Log: " + buf)


# Metodo para publicar mensajes
def on_publish(client, userdata, result):
    print("Data publicada a Thingsboard")


# Respuesta cuando recibimos un PUBLISH del servidor
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


clients = []
for device in devices:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_log = on_log
    client.on_publish = on_publish
    client.on_message = on_message
    client.username_pw_set(device["token"])
    client.connect(device["broker"], device["port"], keepalive=60)
    client.loop_start()
    clients.append(client)

# SENDING DATA TO DEVICE

while True:
    for client in clients:
        pya = randint(0, 1)
       # ppm = randint(0, 40)
        payload = "{"
        #payload += "\"PPM2\":" + str(ppm) + ","
        payload += "\"PYA1\":" + str(0)
        payload += "}"
        ret = client.publish("v1/devices/me/telemetry", payload)
        print(payload)
    time.sleep(10)
