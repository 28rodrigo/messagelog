import pika
import datetime
import os 

# RabbitMQ connection parameters
rabbitmq_host = os.environ.get('RABBITMQ_HOST')
rabbitmq_port = int(os.environ.get('RABBITMQ_PORT'))
rabbitmq_username = os.environ.get('RABBITMQ_USERNAME')
rabbitmq_password = os.environ.get('RABBITMQ_PASSWORD')
rabbitmq_exchange = os.environ.get('RABBITMQ_EXCHANGE')
rabbitmq_routing_key = os.environ.get('RABBITMQ_ROUTING_KEY')
# File path to save the received messages
output_file = 'rabbit_received_messages.txt'
with open(output_file, 'a') as file:
        file.write(f'Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \n\n')
def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    routing_key = method.routing_key
    print(f'Received message with routing key {routing_key}: {message}')
    with open(output_file, 'a') as file:
        file.write(f'Received message with routing key {routing_key}: {message}\n')

# Connect to RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
channel = connection.channel()

# Declare the exchange
channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='topic')

# Declare a random queue
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind the queue to the exchange with the specified routing key
channel.queue_bind(exchange=rabbitmq_exchange, queue=queue_name, routing_key=rabbitmq_routing_key)

# Set up the callback function
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Listening to the RabbitMQ broker...')
channel.start_consuming()