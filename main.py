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
@click.option("--logs-dir", default="./tmp", help="Director for storage logs file.")
@click.option("--debug", default="false")
def main(rmq_host, rmq_port, rmq_queue, logs_dir, debug):
    try:
        port = int(rmq_port)

        if debug == "false":
            app_logger = get_app_logger()
        else:
            app_logger = get_app_logger(logging.INFO, stream_out=False, file_path=f"{ logs_dir }/logs.log")

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_host, port=port))
        channel = connection.channel()
        channel.queue_declare(queue=rmq_queue)
        channel.basic_consume(functools.partial(write_log, app_logger, logs_dir),
                              queue=rmq_queue,
                              arguments={"aaa": 111})
        channel.start_consuming()
    except ValueError:
        print("Illegal Port")


if __name__ == "__main__":
    main()
