import pika
import json

if __name__ == "__main__":
    # APP_NAME, LOG_LEVEL, ACTION, CONTENT
    body = ["TEST", "INFO", "Login", "Password error1121212"]
    connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672"))
    channel = connection.channel()
    channel.queue_declare(queue='logs')
    channel.basic_publish(exchange='', routing_key='logs', body=json.dumps(body, ensure_ascii=False))
    connection.close()
