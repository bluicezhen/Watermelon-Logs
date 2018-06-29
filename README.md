# Watermelon Logs

> A lightweight log record application.

## 1. Installation:

This application depend on `Python 3.6+` and `RabbitMQ 3.7+`. It's support file/MongoDB to storage data and depend on `MongoDB3.6+`

Install Python depend library:

```bash
pip install -r pip install -r requirements.txt
```
or 

```bash
pipenv install
```

## 2. Use:

```bash
python main.py
```

Options:

 - --rmq-host TEXT        Host bind of RabbitMQ.
 - --rmq-port TEXT        Port bind of RabbitMQ.
 - --rmq-queue TEXT       Queue name of RabbitMQ.
 - --rmq-username TEXT    Username of RabbitMQ.
 - --rmq-password TEXT    Password of RabbitMQ.
 - --mongo                Use MongoDB or not
 - --mongo-username TEXT  Username of MongoDB
 - --mongo-password TEXT  Password of MongoDB
 - --mongo-host TEXT      Host bind of MongoDB
 - --mongo-port TEXT      Port bind of MongoDB
 - --mongo-db TEXT        Database name of MongoDB
 - --logs-dir TEXT        Director for storage logs file.
 - --help                 Show this message and exit.

## 3. Example:

- **Use file storage**:
    
    ```bash
    python main.py --logs-dir /logs \
    --rmq-host localhost \
    --rmq-port 5672 \
    --rmq-queue queue \
    --rmq-username guest \
    --rmq-password 123456 \
    ```
    
- **Use MongoDB storage**:
    
    ```bash
    python main.py --mongo \
    --rmq-host localhost \
    --rmq-port 5672 \
    --rmq-queue queue \
    --rmq-username guest \
    --rmq-password 123456 \
    --mongo-username guest \
    --mongo-password 123456 \
    --mongo-port 27017 \
    --mongo-host localhost \
    --mongo-db logs
    ```
- **Docker for file storage**:
    
    > This application save logs file to `/app/tmp` in Docker.
    
    ```bash
    docker run -d --name wlogs -v /logs:/app/tmp --net=host bluicezhen/watermelon-logs:1.1.0 \
    --rmq-host localhost \
    --rmq-port 5672 \
    --rmq-queue queue \
    --rmq-username guest \
    --rmq-password 123456 \
    ```
- **Docker for MongoDB storage**:
    
    ```bash
    docker run -d --name wlogs --net=host bluicezhen/watermelon-logs:1.1.0 \
    --rmq-host localhost \
    --rmq-port 5672 \
    --rmq-queue queue \
    --rmq-username guest \
    --rmq-password 123456 \
    --mongo \
    --mongo-username guest \
    --mongo-password 123456 \
    --mongo-port 27017 \
    --mongo-host localhost \
    --mongo-db logs
    ```
    
## 4. Client Example:

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

