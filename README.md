# Watermelon Logs

> A lightweight log record application.

## 1. Installation

This application depend on `Python 3.6+` and `RabbitMQ 3.7+`. 

Install Python depend library:

```bash
pip install -r pip install -r requirements.txt
```
or 

```bash
pipenv install
```

## 2. Use

```bash
python main.py
```

Options:

-  --rmq-host Host bind of RabbitMQ.
-  --rmq-port Port bind of RabbitMQ.
-  --rmq-queue Queue name of RabbitMQ.
-  --logs-dir Director for storage logs file.

Client Example:

```python
import pika
import json

if __name__ == "__main__":
    # APP_NAME, LOG_LEVEL, ACTION, CONTENT
    body = ["TEST", "INFO", "Login", "Password error"]
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='logs')
    channel.basic_publish(exchange='', routing_key='logs', body=json.dumps(body, ensure_ascii=False))
    connection.close()
```