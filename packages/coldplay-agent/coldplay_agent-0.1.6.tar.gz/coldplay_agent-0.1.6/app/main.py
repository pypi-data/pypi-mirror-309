# app/main.py

import argparse
from app.queues.queue_consumer import RabbitMQConsumer
from app.service.curl_service import CurlService
from app.service.message_service import MessageService
import configparser
import os

def message_callback(ch, method, properties, body):
    """
    RabbitMQ 消费消息的回调函数
    """
    print(f"Received message: {body}")
    success = MessageService.process_message(body)
    if success:
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 处理成功后确认消息
    else:
        print("Message processing failed, not acknowledging.")

def start_consumer(queue_name):
    """
    启动 RabbitMQ 消费者
    """
    consumer = RabbitMQConsumer(queue_name=queue_name, callback=message_callback)
    consumer.connect()
    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()

def main():
    
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(description="RabbitMQ Consumer")
    parser.add_argument("--queue", type=str, required=True, help="The name of the RabbitMQ queue")
    args = parser.parse_args()

    #回传创建队列数据
    CurlService.add_user_queue(args.queue)
    # 启动消费者，传递队列名称
    start_consumer(queue_name=args.queue)
    print(f"Running with queue: {args.queue}")

if __name__ == "__main__":
    main()