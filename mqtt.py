import paho.mqtt.client as mqtt
import uuid

# MQTT broker information
broker_address = "192.168.28.86"
broker_port = 1883
username = "admin"
password = "admin123"

# Generate a unique client ID using GUID
client_id = "mqtt-client-" + str(uuid.uuid4())

# Callback function when a message is received
def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " - " + str(msg.payload))

# Create an MQTT client instance
client = mqtt.Client(client_id)

# Set the callback function
client.on_message = on_message

# Set the username and password
client.username_pw_set(username, password)

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Subscribe to the topics
client.subscribe("alerts/#")
client.subscribe("fof/#")  # Subscribe to all subtopics under "fof"

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
