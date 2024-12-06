# app/queue_consumer.py

import pika
from app.config.config import RabbitMQConfig

class RabbitMQConsumer:
    def __init__(self, queue_name, callback):
        self.queue_name = queue_name
        self.callback = callback
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(RabbitMQConfig.USERNAME, RabbitMQConfig.USERPWD)
        
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RabbitMQConfig.HOST, port=RabbitMQConfig.PORT,  credentials=credentials)
        )
        self.channel = self.connection.channel()

        # 确保队列存在
        self.channel.queue_declare(queue=self.queue_name, durable=RabbitMQConfig.DURABLE)

    def start_consuming(self):
        # 消费者设置
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=False
        )
        print(f"[*] Waiting for messages in {self.queue_name}. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self):
        if self.connection:
            self.connection.close()