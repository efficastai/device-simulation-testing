import paho.mqtt.client as mqtt
from random import randint
from secrets import secrets
import time

# ACCESO A DISPOSITIVO EN THINGSBOARD
DEVICE = secrets.get('device_token')
broker = secrets.get('broker')
port = secrets.get('port')


# Respuesta cuando el cliente recibe Connect Acknowledgement (CONNACK MSG)
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


maquina_1 = mqtt.Client()
maquina_1.on_connect = on_connect
maquina_1.on_log = on_log
maquina_1.on_publish = on_publish
maquina_1.on_message = on_message
maquina_1.username_pw_set(DEVICE)
maquina_1.connect(broker, port, keepalive=60)
maquina_1.loop_start()  # Sin esto no se ejecutan las funciones callback

# SENDING DATA TO DEVICE

while True:
    pya_val = 1  # randint(0, 1)
    ppm_val = randint(1, 100)
    payload = "{"
    payload += "\"ppm\":" + str(pya_val) + ","
    payload += "\"pya\":" + str(ppm_val)
    payload += "}"
    ret = maquina_1.publish("v1/devices/me/telemetry", payload)
    print(payload)
    time.sleep(5)
