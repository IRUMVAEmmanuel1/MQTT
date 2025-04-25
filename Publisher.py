"""Publish terminal messages to topic"""

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
    else:
        print(f"Failed to connect, return code {rc}\n")
        # If the client fails to connect then we should stop the loop
        client.loop_stop()

# Create a new instance of the MQTT client with a specific client ID
client = mqtt.Client(client_id, clean_session=True)
client.on_connect = on_connect  # attach the callback function to the client
client.username_pw_set(username, password)  # set username and password

client.connect(broker_url, broker_port, 60)  # connect to the broker

# Start the network loop in a separate thread
client.loop_start()

try:
    while True:
        message = input("Enter message to publish or type 'exit' to quit: ")
        if message.lower() == 'exit':
            break
        client.publish(topic, message, qos=2)
except KeyboardInterrupt:
    print("Program interrupted by user, exiting...")

# Stop the network loop and disconnect
client.loop_stop()
client.disconnect()