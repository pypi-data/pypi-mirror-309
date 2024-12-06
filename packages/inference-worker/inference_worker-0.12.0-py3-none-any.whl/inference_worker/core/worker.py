import pika, json
from multiprocessing import Process
from .handler import InferenceHandler
from .input import Message
from .utils import get_env_variable
from dotenv import load_dotenv
import logging

load_dotenv(override=True)

logger = logging.getLogger(__name__)

host = get_env_variable('HOST')
modelTag = get_env_variable('MODEL_TAG')
virtualHost = get_env_variable('VIRTUAL_HOST')
username = get_env_variable('USERNAME')
password = get_env_variable('PASSWORD')

class Worker:
    def __init__(self):
        self.host = host
        self.vhost = virtualHost
        self.credentials = pika.PlainCredentials(
            username=username, 
            password=password)
        
        self.queueName = f'{modelTag}_worker_queue'
        self.exchange = f'{modelTag}.direct'
        self.routingKey = f'{modelTag}.request'
        self.channel = None
        self.connection = None
        self.handler = InferenceHandler()
    

    def connect(self):
        logger.info('Initializing connection...')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                virtual_host=self.vhost,
                credentials=self.credentials
            )
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
        self.channel.queue_declare(queue=self.queueName, durable=True)
        self.channel.queue_bind(
            exchange=self.exchange,
            routing_key=self.routingKey, 
            queue=self.queueName)
        logger.info('Successfully connected')

    def process_message(self, ch, method, properties, body):
        print(f"Received message: {body.decode()}")
        try:
            message = json.loads(body.decode())
            request = message.get('request')
            errorCallback = message.get('errorCallback')
            outputCallback = message.get('outputCallback')

            input = Message(
                request=request,
                errorCallback=errorCallback,
                outputCallback=outputCallback
            )

            process = Process(target=self.handler.handle, args=(input,))
            process.start()
            
            while process.is_alive():
                self.connection.process_data_events(time_limit=1)

            process.join()
        except Exception as e:
            print('Problem occurs')
            print(e)
        
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.connect()
        self.channel.basic_qos(prefetch_count=1)  # Process one message at a time
        self.channel.basic_consume(queue=self.queueName, on_message_callback=self.process_message)
        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self):
        logger.info('Closing connection...')
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info('Connection closed.')


if __name__ == "__main__":
    try:
        worker = Worker()
        
        worker.connect()
        worker.start_consuming()
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt, shutting down...")
    finally:
        worker.close()