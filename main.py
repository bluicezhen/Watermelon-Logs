import click
import functools
import logging
import pika
from logger import get_logger as get_app_logger
from write_log import write_log


@click.command()
@click.option("--rmq-host", default="localhost", help="Host bind of RabbitMQ.")
@click.option("--rmq-port", default="5672", help="Port bind of RabbitMQ.")
@click.option("--rmq-queue", default="logs", help="Queue name of RabbitMQ.")
@click.option("--rmq-username", default="guest", help="Username of RabbitMQ.")
@click.option("--rmq-password", default="guest", help="Password name of RabbitMQ.")
@click.option("--logs-dir", default="./tmp", help="Director for storage logs file.")
@click.option("--debug", default="false")
def main(rmq_host, rmq_port, rmq_queue, rmq_username, rmq_password, logs_dir, debug):
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
        channel.basic_consume(functools.partial(write_log, app_logger, logs_dir),
                              queue=rmq_queue)
        channel.start_consuming()
    except ValueError:
        print("Illegal Port")


if __name__ == "__main__":
    main()
