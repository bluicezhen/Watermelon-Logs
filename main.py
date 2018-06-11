import click
import functools
import logging
import pika
from logger import get_logger as get_app_logger
from pymongo import MongoClient
from write_log_file import write_log_file
from write_log_db import write_log_db


@click.command()
@click.option("--rmq-host", default="localhost", help="Host bind of RabbitMQ.")
@click.option("--rmq-port", default="5672", help="Port bind of RabbitMQ.")
@click.option("--rmq-queue", default="logs", help="Queue name of RabbitMQ.")
@click.option("--rmq-username", default="guest", help="Username of RabbitMQ.")
@click.option("--rmq-password", default="guest", help="Password name of RabbitMQ.")
@click.option("--logs-dir", default="./tmp", help="Director for storage logs file.")
@click.option("--debug", default="false")
def main(rmq_host: str, rmq_port: str, rmq_queue: str, rmq_username: str, rmq_password: str, logs_dir: str, debug: str):
    storage = "mongo"
    try:
        port = int(rmq_port)

        if debug == "false":
            app_logger = get_app_logger()
        else:
            app_logger = get_app_logger(logging.INFO, stream_out=False, file_path=f"{ logs_dir }/logs.log")

        connect_url = f"amqp://{ rmq_username }:{ rmq_password }@{ rmq_host }:{ port }"
        connection = pika.BlockingConnection(pika.URLParameters(connect_url))
        channel = connection.channel()
        channel.queue_declare(queue=rmq_queue)

        if storage == "file":
            channel.basic_consume(functools.partial(write_log_file, app_logger, logs_dir), queue=rmq_queue)
        elif storage == "mongo":
            mongo_client = MongoClient('mongodb://localhost:27017/')
            mongo_db = mongo_client["logs"]
            channel.basic_consume(functools.partial(write_log_db, app_logger, mongo_db), queue=rmq_queue)

        channel.start_consuming()
    except ValueError:
        print("Illegal Port")


if __name__ == "__main__":
    main()
