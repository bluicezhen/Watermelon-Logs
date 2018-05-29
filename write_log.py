import json
from datetime import datetime


def write_log(app_logger, logs_dir, ch, method, properties, body):
    now = datetime.now()
    try:
        body_list = json.loads(body.decode("utf-8"))
        app_name = body_list[0]
        log_level = f"{ body_list[1] }".ljust(7)
        log_action = body_list[2]
        log_content = body_list[3]
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        log_file_name = _file_name(app_name, now)
        log_file = open(f"{ logs_dir }/{ log_file_name }", "at")
        log_file.write(f"{ now_str } - { log_level } - { log_action } - { log_content }\n")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except KeyError:
        app_logger.error("Log format illegal", body.decode("utf-8"))


def _file_name(app_name: str, time_now):
    year = time_now.year
    month = str(time_now.month).zfill(2)
    return f"{ app_name }-{ year }-{ month }.log"
