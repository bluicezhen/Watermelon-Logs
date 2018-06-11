import json
from datetime import datetime
from pymongo.collection import Collection
from pymongo.database import Database


def write_log_db(app_logger, db: Database, ch, method, properties, body):
    try:
        body_list = json.loads(body.decode("utf-8"))
        document = {
            "log_level": f"{ body_list[1] }".ljust(7),
            "log_action": body_list[2],
            "log_content": body_list[3],
            "time": datetime.utcnow()
        }
        collection: Collection = db[body_list[0]]
        collection.insert_one(document)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except KeyError:
        app_logger.error("Log format illegal", body.decode("utf-8"))
