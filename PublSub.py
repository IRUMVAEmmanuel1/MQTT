"""
Combined MQTT Publisher and Subscriber script.
Run both functionalities in parallel using threading.
"""
  
import paho.mqtt.client as mqtt
import threading
import time

# MQTT settings
broker_url = "localhost"
broker_port = 1883  # Standard MQTT port, not dashboard port
username = "Irumva"
password = "GishushuAuca@2025"
topic = "auca_class"
publisher_client_id = "my_mqtt_client_publisher"
subscriber_client_id = "my_mqtt_client_subscriber"

# Callback when the client receives a CONNACK response from the server
def on_connect_publisher(client, userdata, flags, rc):
    if rc == 0:
        print("[Publisher] Connected successfully to broker")
    else:
        print(f"[Publisher] Failed to connect, return code {rc}")

# Callback when the subscriber client connects
def on_connect_subscriber(client, userdata, flags, rc):
    if rc == 0:
        print("[Subscriber] Connected successfully to broker")
        # Subscribe to the topic once connected
        client.subscribe(topic, qos=2)
        print(f"[Subscriber] Subscribed to {topic}")
    else:
        print(f"[Subscriber] Failed to connect, return code {rc}")

# Callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"[Subscriber] Message received on topic {msg.topic}: {msg.payload.decode()}")

def publisher_thread():
    """Function that runs the publisher in a separate thread"""
    # Create publisher client
    publisher = mqtt.Client(publisher_client_id, clean_session=True)
    publisher.on_connect = on_connect_publisher
    publisher.username_pw_set(username, password)
    
    # Connect to broker
    try:
        publisher.connect(broker_url, broker_port, 60)
    except Exception as e:
        print(f"[Publisher] Connection error: {e}")
        return
    
    # Start the network loop in a separate thread
    publisher.loop_start()
    
    try:
        while True:
            message = input("Enter message to publish or type 'exit' to quit: ")
            if message.lower() == 'exit':
                break
            publisher.publish(topic, message, qos=2)
            print(f"[Publisher] Published: {message}")
    except KeyboardInterrupt:
        print("[Publisher] Interrupted by user")
    finally:
        # Clean up
        publisher.loop_stop()
        publisher.disconnect()
        print("[Publisher] Disconnected")

def subscriber_thread():
    """Function that runs the subscriber in a separate thread"""
    # Create subscriber client
    subscriber = mqtt.Client(subscriber_client_id, clean_session=True)
    subscriber.on_connect = on_connect_subscriber
    subscriber.on_message = on_message
    subscriber.username_pw_set(username, password)
    
    # Connect to broker
    try:
        subscriber.connect(broker_url, broker_port, 60)
    except Exception as e:
        print(f"[Subscriber] Connection error: {e}")
        return
    
    # Start the network loop
    subscriber.loop_forever()

def main():
    # Create threads
    sub_thread = threading.Thread(target=subscriber_thread)
    pub_thread = threading.Thread(target=publisher_thread)
    
    # Set as daemon so they exit when the main program exits
    sub_thread.daemon = True
    
    # Start threads
    sub_thread.start()
    print("Subscriber thread started")
    
    # Short delay to allow subscriber to connect first
    time.sleep(1)
    
    pub_thread.start()
    print("Publisher thread started")
    
    # Wait for publisher thread to finish (when user types 'exit')
    pub_thread.join()
    
    print("Exiting program")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user")
        print("Exiting...")
