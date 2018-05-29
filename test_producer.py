import pika
import json

if __name__ == "__main__":
    # APP_NAME, LOG_LEVEL, ACTION, CONTENT
    # body = ["TEST", "INFO", "Login", "Password error"]
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='logs')
    channel.basic_publish(exchange='', routing_key='logs', body=json.dumps(body, ensure_ascii=False))
    connection.close()
