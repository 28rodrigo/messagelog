import paho.mqtt.client as mqtt
import uuid
import os
import datetime

# MQTT broker information
broker_address = os.environ.get('MQTT_ADDRESS')
broker_port = int(os.environ.get('MQTT_PORT'))
username = os.environ.get('MQTT_USERNAME')
password = os.environ.get('MQTT_PASSWORD')
topic = os.environ.get('MQTT_TOPIC')

# Generate a unique client ID using GUID
client_id = "mqtt-client-" + str(uuid.uuid4())

output_file = 'mqtt_received_messages.txt'
with open(output_file, 'a') as file:
        file.write(f'Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \n\n')
# Callback function when a message is received
def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " - " + str(msg.payload))
    with open(output_file, 'a') as file:
        file.write(f'Received message with topic key {msg.topic}: {msg.payload}\n')

# Create an MQTT client instance
client = mqtt.Client(client_id)

# Set the callback function
client.on_message = on_message

# Set the username and password
client.username_pw_set(username, password)

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Subscribe to the topics
client.subscribe(topic) # Subscribe to all subtopics under "fof"

# Start the MQTT loop to listen for messages
client.loop_start()

# Keep the script running until interrupted
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Disconnect the client
client.loop_stop()
client.disconnect()
