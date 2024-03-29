import paho.mqtt.client as mqtt
import subprocess

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("protosystemdemo/doorbell/ring")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	if msg.payload == "1":
		filenamering1 = r'./doorbell-1.wav'
		subprocess.Popen([ "/usr/bin/aplay", '-q', filenamering1 ] )
	if msg.payload == "2":
		filenamering2 = r'./doorbell-2.wav'
		subprocess.Popen([ "/usr/bin/aplay", '-q', filenamering2 ] )
	

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()