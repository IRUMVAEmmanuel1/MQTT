"""Subscribe to messages on topic"""
 
 
import paho.mqtt.client as mqtt 

# MQTT settings 
broker_url = "localhost"
broker_port = 18083
username = "Irumva"
password = "GishushuAuca@2025"
topic = "auca_class"
client_id = "my_mqtt_client" 

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to broker")
        # Subscribe to the topic once connected
        client.subscribe(topic, qos=2)
    else:
        print(f"Failed to connect, return code {rc}\n")

# Callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")

# Create a new instance of the MQTT client with a specific client ID
client = mqtt.Client(client_id, clean_session=True)
client.on_connect = on_connect  # attach the connection callback function to the client
client.on_message = on_message  # attach the message callback function to the client

client.username_pw_set(username, password)  # set username and password
client.connect(broker_url, broker_port, 60)  # connect to the broker

# Start the network loop in a separate thread
client.loop_forever()
